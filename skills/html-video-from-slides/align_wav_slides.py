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
  {"slideDurationsSec": [float, ...], "method": "whisper_align|silence_split|equal_split",
   "warnings": [...], "subtitleGaps": [...], "vadFilterUsed": bool, ...}
  默认关闭 VAD；可用 --strict-subtitles 在存在超长无字幕区间时非零退出。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import replace


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
        idx = 0
        for seg in segments:
            text = (getattr(seg, "text", "") or "").strip()
            text = to_simp_zh(text, enabled=t2s)
            if not text:
                continue
            idx += 1
            start = _srt_time(float(seg.start))
            end = _srt_time(float(seg.end))
            f.write(f"{idx}\n{start} --> {end}\n{text}\n\n")


_SRT_TIME_RE = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})"
)


def _srt_ts_to_sec(h, m, s, ms) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_srt_times(srt_path: str) -> list[tuple[float, float]]:
    """Return list of (start_sec, end_sec) for each subtitle block."""
    if not os.path.isfile(srt_path):
        return []
    with open(srt_path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    blocks = re.split(r"\n\s*\n", content.strip())
    out: list[tuple[float, float]] = []
    for b in blocks:
        lines = [ln.strip() for ln in b.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        m = _SRT_TIME_RE.match(lines[1])
        if not m:
            continue
        t0 = _srt_ts_to_sec(*m.groups()[:4])
        t1 = _srt_ts_to_sec(*m.groups()[4:])
        out.append((t0, t1))
    return out


def find_subtitle_gaps(
    spans: list[tuple[float, float]],
    audio_end: float,
    *,
    threshold_sec: float,
) -> list[dict]:
    """
    找出 SRT 中超过 threshold_sec 的「无字幕」区间（含片头、条间、片尾）。
    """
    gaps: list[dict] = []
    if threshold_sec <= 0:
        return gaps
    if not spans:
        if audio_end > threshold_sec:
            gaps.append(
                {
                    "fromSec": 0.0,
                    "toSec": round(audio_end, 3),
                    "durationSec": round(audio_end, 3),
                    "kind": "no_subtitles_at_all",
                }
            )
        return gaps
    if spans[0][0] > threshold_sec:
        gaps.append(
            {
                "fromSec": 0.0,
                "toSec": round(spans[0][0], 3),
                "durationSec": round(spans[0][0], 3),
                "kind": "head",
            }
        )
    for i in range(len(spans) - 1):
        g = spans[i + 1][0] - spans[i][1]
        if g > threshold_sec:
            gaps.append(
                {
                    "fromSec": round(spans[i][1], 3),
                    "toSec": round(spans[i + 1][0], 3),
                    "durationSec": round(g, 3),
                    "kind": "between",
                }
            )
    tail = audio_end - spans[-1][1]
    if tail > threshold_sec:
        gaps.append(
            {
                "fromSec": round(spans[-1][1], 3),
                "toSec": round(audio_end, 3),
                "durationSec": round(tail, 3),
                "kind": "tail",
            }
        )
    return gaps


def extract_wav_segment(src: str, dst: str, t0: float, t1: float) -> None:
    """用 ffmpeg 切出 [t0, t1) 片段为 16k mono WAV（供二次 Whisper）。"""
    dur = max(t1 - t0, 0.05)
    r = subprocess.run(
        [
            ffmpeg_bin(),
            "-y",
            "-nostdin",
            "-ss",
            str(t0),
            "-i",
            src,
            "-t",
            str(dur),
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            dst,
        ],
        capture_output=True,
        text=True,
        timeout=600,
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr or r.stdout or "ffmpeg extract failed")


def offset_segment(seg, dt: float):
    """将片段与词级时间轴整体平移 dt 秒（叠回原 WAV 时间轴）。"""
    new_words = None
    if seg.words:
        new_words = [
            replace(w, start=float(w.start) + dt, end=float(w.end) + dt) for w in seg.words
        ]
    return replace(
        seg,
        start=float(seg.start) + dt,
        end=float(seg.end) + dt,
        words=new_words,
    )


def fill_segment_gaps(
    wav_path: str,
    seg_list: list,
    audio_end: float,
    model,
    transcribe_kw: dict,
    *,
    gap_threshold_sec: float,
    max_gap_sec: float,
) -> tuple[list, list[str]]:
    """
    对「整段转写后时间轴上仍超过 gap_threshold_sec 的无字幕区间」切 WAV 二次转写并合并。
    用于修复整段推理时仍漏掉的清晰人声（与 no_speech 阈值、30s chunk 等叠加问题无关时仍有效）。
    """
    warnings: list[str] = []
    spans: list[tuple[float, float]] = []
    for seg in seg_list:
        text = (getattr(seg, "text", "") or "").strip()
        if not text:
            continue
        spans.append((float(seg.start), float(seg.end)))
    spans.sort(key=lambda x: x[0])
    gaps = find_subtitle_gaps(spans, audio_end, threshold_sec=gap_threshold_sec)
    extra: list = []
    for g in gaps:
        dur = float(g["durationSec"])
        if dur > max_gap_sec:
            warnings.append(
                f"跳过缺口二次转写（{g['fromSec']:.1f}-{g['toSec']:.1f}，{dur:.1f}s > max {max_gap_sec}s）"
            )
            continue
        t0 = float(g["fromSec"])
        t1 = float(g["toSec"])
        fd, tmp_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        try:
            extract_wav_segment(wav_path, tmp_path, t0, t1)
        except Exception as e:
            warnings.append(f"缺口切分失败 {t0:.1f}-{t1:.1f}: {e}")
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            continue
        sub_kw = {**transcribe_kw}
        sub_kw["no_speech_threshold"] = None
        sub_kw["vad_filter"] = False
        try:
            gen, _ = model.transcribe(tmp_path, **sub_kw)
            n = 0
            for seg in gen:
                if not (getattr(seg, "text", "") or "").strip():
                    continue
                extra.append(offset_segment(seg, t0))
                n += 1
            if n:
                warnings.append(f"缺口二次转写 {t0:.1f}-{t1:.1f}s：补充 {n} 条片段")
            else:
                warnings.append(
                    f"缺口二次转写 {t0:.1f}-{t1:.1f}s：未产出文本（可能为静音/纯音乐）"
                )
        except Exception as e:
            warnings.append(f"缺口转写失败 {t0:.1f}-{t1:.1f}: {e}")
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    if not extra:
        return seg_list, warnings

    merged = list(seg_list) + extra
    merged.sort(key=lambda s: float(s.start))
    return merged, warnings


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
    ap.add_argument(
        "--vad-filter",
        action="store_true",
        help="启用 faster-whisper 内置 VAD（可能裁掉很轻的气口/片头口播；默认关闭以提高字幕完整率）",
    )
    ap.add_argument(
        "--max-subtitle-gap-sec",
        type=float,
        default=2.5,
        help="超过该秒数的无字幕区间会记入 subtitleGaps 并告警（默认 2.5）",
    )
    ap.add_argument(
        "--strict-subtitles",
        action="store_true",
        help="若存在超过阈值的字幕缺口则非零退出（不生成成片配置供后续步骤使用）",
    )
    ap.add_argument(
        "--no-speech-threshold",
        type=str,
        default="0.85",
        help=(
            "faster-whisper：仅当 no_speech_prob 大于该值时才跳过当前音频块（库默认 0.6 偏严，易漏清晰人声）。"
            "提高此值可减少漏检；字面量 none/null 表示关闭此项过滤。"
        ),
    )
    ap.add_argument(
        "--no-fill-srt-gaps",
        action="store_true",
        help="关闭：对超长无字幕区间切 WAV 二次转写并合并（默认开启）",
    )
    ap.add_argument(
        "--max-gap-fill-sec",
        type=float,
        default=180.0,
        help="超过该秒数的缺口不二次转写（默认 180）",
    )
    ap.add_argument(
        "--hotwords",
        default="",
        help="faster-whisper hotwords：空格分隔的提示词，利于专有名词（如 Claude、API）拼写",
    )
    args = ap.parse_args()
    gap_fill_warnings: list[str] = []
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
    nst_raw = (args.no_speech_threshold or "").strip().lower()
    if nst_raw in ("none", "null", ""):
        no_speech_threshold: float | None = None
    else:
        no_speech_threshold = float(nst_raw)

    transcribe_kw: dict = {
        "language": "zh",
        "word_timestamps": True,
        # 勿写「请使用简体中文转写…」长句，易被 Whisper 当幻听输出到字幕开头
        "initial_prompt": "中文播客，讨论企业与人工智能；专名保留常见英文拼写。",
        # 库默认 0.6：no_speech_prob > 阈值 则整段跳过，片头/垫乐旁白易被误杀成大段无字幕；skill 默认提高到 0.85
        "no_speech_threshold": no_speech_threshold,
    }
    # 默认关闭 VAD：开启时容易把轻声/片头当成非语音裁掉，导致 SRT 出现大段空白。
    if args.vad_filter:
        transcribe_kw["vad_filter"] = True
        transcribe_kw["vad_parameters"] = dict(min_silence_duration_ms=400)
    else:
        transcribe_kw["vad_filter"] = False

    hw = (args.hotwords or "").strip()
    if hw:
        transcribe_kw["hotwords"] = hw

    print(
        f"INFO: no_speech_threshold={no_speech_threshold} "
        f"（仅当 no_speech_prob 大于该值时跳过；None=关闭此项过滤）",
        flush=True,
    )
    if hw:
        print(f"INFO: hotwords={hw!r}", flush=True)

    segments_gen, info = model.transcribe(args.wav, **transcribe_kw)

    seg_list = list(segments_gen)
    audio_end = float(info.duration) if info.duration else 0.0

    if (
        args.srt_out
        and seg_list
        and not args.no_fill_srt_gaps
        and audio_end > 0
    ):
        seg_list, gap_fill_warnings = fill_segment_gaps(
            args.wav,
            seg_list,
            audio_end,
            model,
            transcribe_kw,
            gap_threshold_sec=args.max_subtitle_gap_sec,
            max_gap_sec=args.max_gap_fill_sec,
        )
        for w in gap_fill_warnings:
            print(f"INFO: {w}", flush=True)

    words = []
    for seg in seg_list:
        if seg.words:
            words.extend(seg.words)

    # 输出 SRT 字幕（如果请求）
    if args.srt_out and seg_list:
        write_srt(seg_list, args.srt_out, t2s=use_t2s)

    def finalize_out(out: dict) -> int:
        """写入 out.json；分析字幕缺口；strict 模式下有缺口则返回 4。"""
        out["audioDurationSec"] = round(audio_end, 3)
        out["vadFilterUsed"] = bool(args.vad_filter)
        out["whisperModel"] = args.model
        out["noSpeechThreshold"] = no_speech_threshold
        out["whisperHotwords"] = hw if hw else None
        out["srtGapFillUsed"] = bool(args.srt_out and not args.no_fill_srt_gaps)
        if gap_fill_warnings:
            out.setdefault("warnings", []).extend(gap_fill_warnings)
        if args.srt_out:
            out["srtFile"] = args.srt_out
        if args.srt_out and os.path.isfile(args.srt_out):
            spans = parse_srt_times(args.srt_out)
            gaps = find_subtitle_gaps(
                spans, audio_end, threshold_sec=args.max_subtitle_gap_sec
            )
            out["subtitleGaps"] = gaps
            out["subtitleGapThresholdSec"] = args.max_subtitle_gap_sec
            w = out.setdefault("warnings", [])
            for g in gaps:
                msg = (
                    f"字幕缺口约 {g['durationSec']:.1f}s（{g['fromSec']:.2f}–{g['toSec']:.2f}，{g['kind']}）"
                )
                w.append(msg)
                # 避免 Windows 默认控制台编码无法输出 U+26A0 等符号导致崩溃
                print(f"WARN: {msg}", flush=True)
        else:
            out["subtitleGaps"] = []
            out["subtitleGapThresholdSec"] = args.max_subtitle_gap_sec
            if args.srt_out and not os.path.isfile(args.srt_out):
                out.setdefault("warnings", []).append("未生成 SRT 文件（Whisper 无有效片段）")

        with open(args.out_json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

        if args.strict_subtitles and out.get("subtitleGaps"):
            print(
                "\nERROR: --strict-subtitles：存在超长无字幕区间。已写入 align JSON 供排查；已中止，未生成成片。\n"
                "   处理：补全 sub.srt、或提高 no_speech_threshold（noSpeechThreshold）、或改用更大 whisperModel、或确认未误开 --vad-filter。\n",
                file=sys.stderr,
                flush=True,
            )
            return 4
        return 0

    if not words or audio_end <= 0:
        durs, w = silence_split_durations(args.wav, len(slides), audio_end or 1.0)
        out = {
            "slideDurationsSec": durs,
            "method": "silence_split",
            "warnings": w + ["Whisper 未返回有效词，已降级"],
        }
        return finalize_out(out)

    big, times = build_char_timeline(words, t2s=use_t2s)
    if len(big) < 10:
        durs, w = silence_split_durations(args.wav, len(slides), audio_end)
        out = {
            "slideDurationsSec": durs,
            "method": "silence_split",
            "warnings": w + ["转写过短，已降级"],
        }
        return finalize_out(out)

    durs, warns = align_slides_to_timeline(slides, big, times, audio_end)
    method = "whisper_align"
    if any("未找到匹配" in x for x in warns) or any("均分" in x for x in warns):
        method = "whisper_align_partial"

    out = {
        "slideDurationsSec": durs,
        "method": method,
        "warnings": warns,
    }
    return finalize_out(out)


if __name__ == "__main__":
    sys.exit(main())
