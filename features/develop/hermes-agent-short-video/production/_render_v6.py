# -*- coding: utf-8 -*-
"""渲染 v6: 幻灯截图 + voiceover.wav + sub.srt → final_v6.mp4
两阶段：①逐片段合成 ②concat + 烧字幕
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PROD = Path(__file__).parent
SLIDES = sorted(PROD.glob("slide_v6_*.png"))
TIMES = json.loads((PROD / "slide_page_times_v6.json").read_text(encoding="utf-8"))
WAV = PROD / "voiceover.wav"
SRT = PROD / "sub.srt"
OUT = PROD / "final_v6.mp4"

W, H = 1920, 1080


def run(args: list, desc: str = ""):
    print(f"  [{desc}]")
    r = subprocess.run(args, cwd=PROD, capture_output=True)
    if r.returncode != 0:
        err = r.stderr.decode("utf-8", errors="replace")
        print(f"    ERROR:\n{err[-600:]}")
        sys.exit(1)
    return r


def main():
    n = len(SLIDES)
    assert n == len(TIMES), f"Slides {n} != Times {len(TIMES)}"
    print(f"Rendering {n} slides -> {OUT.name}")

    clip_files = []

    # ── Stage 1: 每个片段单独合成视频 ──
    for i in range(n):
        pt = TIMES[i]
        start, end = pt["start"], pt["end"]
        dur = end - start
        clip = PROD / f"clip_{i:02d}.mp4"
        clip_files.append(clip)

        if clip.exists():
            print(f"  [skip clip {i}] already exists")
            continue

        # 图片无限 loop → 时长 = dur
        run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", f"slide_v6_{i:02d}.png",
            "-i", str(WAV),
            "-ss", str(start), "-to", str(end),
            "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-r", "25", "-t", str(dur),
            "-pix_fmt", "yuv420p",
            "-shortest",
            clip
        ], f"clip {i:02d} ({start:.1f}s->{end:.1f}s, {dur:.1f}s)")

    # ── Stage 2: Concat ──
    concat_list = PROD / "clips.txt"
    concat_list.write_text(
        "\n".join(f"file 'clip_{i:02d}.mp4'" for i in range(n)),
        encoding="utf-8"
    )
    concat_raw = PROD / "concat_raw.mp4"
    run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", "clips.txt",
        "-c", "copy",
        concat_raw
    ], "concat clips")

    # ── Stage 3: 烧字幕 ──
    # 字幕样式：黄色大字（FontSize=48），适合手机竖屏观看
    tmp_ass = PROD / "_sub.ass"

    import re as _re
    def _to_ass(s):
        h, m, rest = s.split(":")
        sec, ms = rest.split(",")
        total = int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
        th = int(total // 3600)
        tm = int((total % 3600) // 60)
        ts = total % 60
        return f"{th}:{tm:02d}:{ts:05.2f}"

    content = SRT.read_text(encoding="utf-8")
    ass_lines = [
        "[Script Info]\nTitle: Hermes\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n\n",
        "[V4+ Styles]\n",
        "Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BorderStyle,Outline,Alignment,MarginV\n",
        "Style: Default,Arial,48,&H00FFFF,&H000000,1,3,2,60\n\n",
        "[Events]\nFormat: Layer,Start,End,Style,Text\n",
    ]
    pat = _re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)", _re.DOTALL)
    for m in pat.finditer(content):
        start = _to_ass(m.group(2))
        end = _to_ass(m.group(3))
        text = m.group(4).strip().replace("\n", "\\N")
        # 5字段格式: Layer,Start,End,Style,Text（与Format行一致，避免空字段导致显示0）
        ass_lines.append(f"Dialogue: 0,{start},{end},Default,{text}\n")

    tmp_ass.write_text("".join(ass_lines), encoding="utf-8")
    print(f"  [ASS] {tmp_ass} ({tmp_ass.stat().st_size} bytes)")

    # filter_complex: [0:v] + ass overlay
    fc = f"[0:v]ass={tmp_ass.name}[vout]"
    run([
        "ffmpeg", "-y",
        "-i", str(concat_raw),
        "-filter_complex", fc,
        "-map", "[vout]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        str(OUT)
    ], "burn ASS subtitles")

    # 清理临时文件
    for f in PROD.glob("clip_*.mp4"):
        f.unlink()
    concat_raw.unlink()
    concat_list.unlink()

    print(f"\nDone: {OUT}  ({OUT.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()