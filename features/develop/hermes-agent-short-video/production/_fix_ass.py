# -*- coding: utf-8 -*-
"""修复 ASS 文件：字号加大（48），去掉多余逗号"""
import re
from pathlib import Path

PROD = Path(r"D:\harnessworld\one-context\features\develop\hermes-agent-short-video\production")
SRT = PROD / "sub.srt"
OUT_ASS = PROD / "_sub.ass"

def to_ass_time(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    total = int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
    th = int(total // 3600)
    tm = int((total % 3600) // 60)
    ts = total % 60
    return f"{th}:{tm:02d}:{ts:05.2f}"

content = SRT.read_text(encoding="utf-8")

# 写入 ASS，FontSize=48（大字，适合手机），字号加大
ass_lines = [
    "[Script Info]\n",
    "Title: Hermes\n",
    "ScriptType: v4.00+\n",
    "PlayResX: 1920\n",
    "PlayResY: 1080\n\n",
    "[V4+ Styles]\n",
    "Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BorderStyle,Outline,Alignment,MarginV\n",
    # FontSize=48 加大，PrimaryColour=黄色&H00FFFF，Outline=2黑边，Alignment=2底部居中，MarginV=60距底
    "Style: Default,Arial,48,&H00FFFF,&H000000,1,3,2,60\n\n",
    "[Events]\n",
    "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n",
]

pat = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)", re.DOTALL)
for m in pat.finditer(content):
    start = to_ass_time(m.group(2))
    end = to_ass_time(m.group(3))
    text = m.group(4).strip().replace("\n", "\\N")
    # 正确格式: Layer,Start,End,Style,Name(空),MarginL,MarginR,MarginV,Effect(空),Text
    ass_lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")

OUT_ASS.write_text("".join(ass_lines), encoding="utf-8")
print(f"ASS written: {OUT_ASS.stat().st_size} bytes")
print("Sample lines:")
for line in ass_lines[-3:]:
    print(f"  {line.rstrip()}")
