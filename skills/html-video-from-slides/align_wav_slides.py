#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从整段 WAV + 每页幻灯文案（与口播大致一致）自动推算 slideDurationsSec。
依赖: pip install faster-whisper huggingface_hub
  可选（推荐）: pip install opencc-python-reimplemented
  安装 OpenCC 后，写出 SRT 与对齐用词级时间轴前会做繁体→简体，并与幻灯 innerText 更好匹配。

用法:
  python align_wav_slides.py --wav path/to/audio.wav --slides-json path/to/slides.json --out-json path/to/out.json

slides.json: {"slides": ["第一页可见文案...", ...]}

输出 out.json:
  {"slideDurationsSec": [float, ...], "method": "whisper_align|silence_split|equal_split", "warnings": [...]}
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys


def ffmpeg_bin() -> str:
    return os.environ.get("FFMPEG_PATH") or os.environ.get("FFMPEG_BIN") or "ffmpeg"


# 对齐时剥离的标点（避免正则里混用引号导致 SyntaxError）
_NORM_DELETE = (
    "`'\"「」『』【】[]()（）,，.。·…:：;；!！?？"
    "\\/_—-+=|<>"
)


_t2s_converter = None  # False = 已探测失败；OpenCC 对象 = 可用


def _get_t2s():
    """繁体→简体（可选依赖 opencc-python-reimplemented）。"""
    global _t2s_converter
    if _t2s_converter is not None:
        return _t2s_converter if _t2s_converter is not False else None
    try:
        from opencc import OpenCC  # type: ignore

        _t2s_converter = OpenCC("t2s")
    except Exception:
        _t2s_converter = False
    return _t2s_converter if _t2s_converter is not False else None


def to_simp_zh(s: str, *, enabled: bool) -> str:
    if not enabled or not s:
        return s
    cc = _get_t2s()
    return cc.convert(s) if cc else s


def norm_chars(s: str) -> str:
    """去空白与常见标点，便于与 ASR 文本对齐（中英混合）。"""
    s = re.sub(r"[\s\u3000]+", "", s)
    s = s.translate(str.maketrans("", "", _NORM_DELETE))
    return s.lower()


def _srt_time(seconds: float) -> str:
    """Format seconds to SRT timestamp: 00:00:00,000"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(segments, output_path: str, *, t2s: bool) -> None:
    """Write Whisper segments to SRT file (with BOM for Windows)."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\ufeff")
        for i, seg in enumerate(segments, 1):
            text = (getattr(seg, "text", "") or "").strip()
            text = to_simp_zh(text, enabled=t2s)
            if not text:
                continue
            start = _srt_time(float(seg.start))
            end = _srt_time(float(seg.end))
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def build_char_timeline(
    words: list, *, t2s: bool
) -> tuple[str, list[tuple[float, float]]]:
    """words: faster_whisper Word with .word .start .end"""
    big = ""
    times: list[tuple[float, float]] = []
    for w in words:
        raw = getattr(w, "word", "") or ""
        raw = to_simp_zh(raw, enabled=t2s)
        ntxt = norm_chars(raw)
        if not ntxt:
            continue
        dur = max(float(w.end) - float(w.start), 1e-3)
        n = len(ntxt)
        for i, _ch in enumerate(ntxt):
            t0 = float(w.start) + dur * i / n
            t1 = float(w.start) + dur * (i + 1) / n
            big += _ch
            times.append((t0, t1))
    return big, times


def align_slides_to_timeline(
    slide_texts: list[str], big: str, times: list[tuple[float, float]], audio_end: float
) -> tuple[list[float], list[str]]:
    """顺序匹配每页文案在转写中的结束时刻，再插值成连续分区，得到各页时长。"""
    warnings: list[str] = []
    n = len(slide_texts)
    # 每页「口播结束」的绝对时间（秒），None 表示未匹配
    end_t: list[float | None] = [None] * n
    cursor = 0

    for i, st in enumerate(slide_texts):
        sn = norm_chars(st)
        if not sn:
            warnings.append(f"第 {i + 1} 页 HTML 几乎无文字，将用插值补时长")
            continue

        idx = big.find(sn, cursor)
        matched_len = len(sn)
        if idx == -1:
            for L in range(len(sn), max(1, min(len(sn), 16)), -1):
                idx = big.find(sn[:L], cursor)
                if idx != -1:
                    matched_len = L
                    warnings.append(f"第 {i + 1} 页仅匹配前 {L} 字（ASR 可能与幻灯文案不完全一致）")
                    break
        if idx == -1:
            warnings.append(f"第 {i + 1} 页在转写中未找到匹配，将用插值")
            continue

        hi = idx + matched_len - 1
        if hi >= len(times):
            hi = len(times) - 1
        end_t[i] = times[hi][1]
        cursor = hi + 1

    # 分区边界 T[0]=0 … T[n]=audio_end；T[i+1] ≈ 第 i 页口播结束时刻
    known_any = any(t is not None for t in end_t)
    if not known_any:
        e = audio_end / max(n, 1)
        return [round(e, 4)] * n, warnings + ["全文无匹配，均分音频"]

    T: list[float | None] = [None] * (n + 1)
    T[0] = 0.0
    prev_b = 0.0
    for i in range(n):
        if end_t[i] is not None:
            t = min(float(end_t[i]), audio_end - 0.02)
            if t <= prev_b:
                t = prev_b + 0.05
            T[i + 1] = t
            prev_b = t
    T[n] = audio_end

    # 线性插值填满 T[1..n-1]
    for _ in range(n + 2):
        for i in range(1, n):
            if T[i] is not None:
                continue
            L, R = i - 1, i + 1
            while L > 0 and T[L] is None:
                L -= 1
            while R < n and T[R] is None:
                R += 1
            if T[L] is not None and T[R] is not None:
                T[i] = T[L] + (T[R] - T[L]) * (i - L) / (R - L)
        if all(T[i] is not None for i in range(n + 1)):
            break
    for i in range(1, n):
        if T[i] is None:
            T[i] = T[0] + (T[n] - T[0]) * i / n

    for i in range(n):
        if T[i + 1] < T[i]:
            T[i + 1] = T[i] + 0.1

    durations = [max(0.12, round(T[i + 1] - T[i], 4)) for i in range(n)]
    ssum = sum(durations)
    if abs(ssum - audio_end) > 0.05:
        scale = audio_end / ssum
        durations = [round(x * scale, 4) for x in durations]

    return durations, warnings


def silence_split_durations(wav_path: str, n_slides: int, total: float) -> tuple[list[float], list[str]]:
    """ffmpeg silencedetect 粗分；失败则均分。"""
    warnings = []
    try:
        r = subprocess.run(
            [
                ffmpeg_bin(),
                "-nostats",
                "-i",
                wav_path,
                "-af",
                "silencedetect=noise=-30dB:d=0.35",
                "-f",
                "null",
                "-",
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )
        txt = (r.stderr or "") + (r.stdout or "")
        starts = [float(m.group(1)) for m in re.finditer(r"silence_start: ([0-9.]+)", txt)]
        ends = [float(m.group(1)) for m in re.finditer(r"silence_end: ([0-9.]+)", txt)]
        if len(starts) < n_slides - 1:
            raise ValueError("静音点不足")
        mids = []
        for i in range(min(len(starts), len(ends))):
            mids.append((starts[i] + ends[i]) / 2)
        mids = sorted(mids)[: n_slides - 1]
        while len(mids) < n_slides - 1:
            mids.append(total * (len(mids) + 1) / n_slides)
        pts = [0.0] + mids + [total]
        durs = [round(pts[i + 1] - pts[i], 4) for i in range(n_slides)]
        warnings.append("使用静音检测切页（质量取决于页间是否有明显停顿）")
        return durs, warnings
    except Exception as e:
        warnings.append(f"静音切分失败 ({e})，改为均分")
        e = total / n_slides
        return [round(e, 4)] * n_slides, warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wav", required=True)
    ap.add_argument("--slides-json", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument(
        "--model",
        default="medium",
        help="faster-whisper 模型: tiny/base/small/medium/large-v3 等",
    )
    ap.add_argument(
        "--srt-out",
        default=None,
        help="输出 SRT 字幕文件路径（与转写同源）",
    )
    ap.add_argument(
        "--no-t2s",
        action="store_true",
        help="禁用繁体→简体（默认启用；需 pip install opencc-python-reimplemented）",
    )
    args = ap.parse_args()
    use_t2s = not args.no_t2s
    if use_t2s and _get_t2s() is None:
        print(
            "⚠️  未安装 OpenCC，SRT 可能混用繁体。建议: pip install opencc-python-reimplemented",
            flush=True,
        )

    with open(args.slides_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    slides = data.get("slides") or []
    if not slides:
        print("slides.json 缺少 slides 数组", file=sys.stderr)
        return 2

    try:
        from faster_whisper import WhisperModel
        import huggingface_hub
    except ImportError as e:
        print(
            f"缺少依赖: {e}。请执行: pip install faster-whisper huggingface_hub",
            file=sys.stderr,
        )
        return 3

    # 确保缓存完整，防止 bin 文件损坏导致崩溃
    os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
    os.environ["HF_HUB_DISABLE_XET"] = "1"
    model_id = f"Systran/faster-whisper-{args.model}"

    def load_model():
        return WhisperModel(args.model, device="cpu", compute_type="int8")

    try:
        model = load_model()
    except Exception as e:
        err_msg = str(e)
        # 检测模型加载失败（常见于 bin 文件损坏或缺失）
        if "model.bin" in err_msg or "Unable to open file" in err_msg or "not found" in err_msg.lower():
            print(f"⚠️  模型缓存损坏或缺失 ({e})，正在从 hf-mirror.com 重新下载...", flush=True)
            try:
                # 清理损坏的缓存
                cached = huggingface_hub.snapshot_download(model_id, local_files_only=False)
                print(f"✅ 模型已缓存至: {cached}", flush=True)
            except Exception as dl_err:
                print(f"⚠️  重新下载失败: {dl_err}，尝试强制清理后重试...", flush=True)
                cache_base = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub", f"models--{model_id.replace('/','--')}")
                if os.path.exists(cache_base):
                    shutil.rmtree(cache_base)
                huggingface_hub.snapshot_download(model_id, local_files_only=False)
            model = load_model()
        else:
            raise
    segments_gen, info = model.transcribe(
        args.wav,
        language="zh",
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=300),
        initial_prompt="请使用简体中文转写中文内容，专有名词保持常用英文拼写。",
    )

    seg_list = list(segments_gen)

    words = []
    for seg in seg_list:
        if seg.words:
            words.extend(seg.words)

    # 输出 SRT 字幕（如果请求）
    if args.srt_out and seg_list:
        write_srt(seg_list, args.srt_out, t2s=use_t2s)

    audio_end = float(info.duration) if info.duration else 0.0
    if not words or audio_end <= 0:
        durs, w = silence_split_durations(args.wav, len(slides), audio_end or 1.0)
        out = {
            "slideDurationsSec": durs,
            "method": "silence_split",
            "warnings": w + ["Whisper 未返回有效词，已降级"],
        }
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        return 0

    big, times = build_char_timeline(words, t2s=use_t2s)
    if len(big) < 10:
        durs, w = silence_split_durations(args.wav, len(slides), audio_end)
        out = {
            "slideDurationsSec": durs,
            "method": "silence_split",
            "warnings": w + ["转写过短，已降级"],
        }
        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        return 0

    durs, warns = align_slides_to_timeline(slides, big, times, audio_end)
    method = "whisper_align"
    if any("未找到匹配" in x for x in warns) or any("均分" in x for x in warns):
        method = "whisper_align_partial"

    out = {
        "slideDurationsSec": durs,
        "method": method,
        "warnings": warns,
        "audioDurationSec": round(audio_end, 3),
    }
    if args.srt_out:
        out["srtFile"] = args.srt_out
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
