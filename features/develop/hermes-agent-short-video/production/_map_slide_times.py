# -*- coding: utf-8 -*-
"""从 SRT + slide 关键词自动推断 v6 的 slidePageTimesWav"""
from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

SRT = Path(__file__).parent / "sub.srt"


class Caption(NamedTuple):
    idx: int
    start_sec: float
    end_sec: float
    text: str


def parse_srt(path: Path) -> list[Caption]:
    content = path.read_text(encoding="utf-8")
    captions: list[Caption] = []
    pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)", re.DOTALL)
    for m in pattern.finditer(content):
        idx = int(m.group(1))
        start = parse_time(m.group(2))
        end = parse_time(m.group(3))
        text = m.group(4).strip().replace("\n", " ")
        captions.append(Caption(idx, start, end, text))
    return captions


def parse_time(s: str) -> float:
    h, mn, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(mn) * 60 + int(sec) + int(ms) / 1000


# v6 slide keywords → last caption text that belongs to this slide
# Key transition points in voiceover
V6_SLIDES = [
    # (slide_idx, keyword to find, description)
    (0,  "欢迎收听",       "封面 - 欢迎"),
    (1,  "Hello 大家",     "悬念 - Hermes是什么"),
    (2,  "OpenClaw的时候",  "痛点 - OpenClaw太麻烦"),
    (3,  "Hermes Agent",   "两个路数 - 核心对比"),
    (4,  "OpenClaw",       "技能管理对比"),
    (5,  "怎么选",         "怎么选"),
    (6,  "PART",           "PART 2 - 自动生成技能"),
    (7,  "门槛",           "触发门槛"),
    (8,  "复盘",           "复盘机制"),
    (9,  "保存成一个新的技能", "LLM分析"),
    (10, "agentskills",    "agentskills.io"),
    (11, "40%",            "实际收益"),
    (12, "前景",           "PART 3 - 前景场景"),
    (13, "个人用户",       "个人用户"),
    (14, "团队协作",       "团队协作"),
    (15, "本地闭环",       "核心优势"),
    (16, "几十种工具",     "工程力"),
    (17, "百闻不如一见",   "结尾"),
]


def find_caption_end(captions: list[Caption], keyword: str, after_sec: float = 0) -> float:
    """找包含 keyword 的 caption 的 end_sec"""
    for cap in captions:
        if cap.start_sec >= after_sec and keyword in cap.text:
            return cap.end_sec
    # fallback: try anywhere after after_sec
    for cap in captions:
        if keyword in cap.text:
            return cap.end_sec
    return after_sec + 20  # fallback


def main() -> None:
    captions = parse_srt(SRT)
    print(f"Loaded {len(captions)} captions")

    times = []
    last_end = 0.0

    for slide_idx, keyword, desc in V6_SLIDES:
        end = find_caption_end(captions, keyword, last_end)
        # ensure minimum duration 5s
        if end - last_end < 3:
            end = last_end + 10
        times.append({"slide": slide_idx, "start": round(last_end, 2), "end": round(end, 2), "desc": desc})
        print(f"  slide-{slide_idx:02d}: {round(last_end,2)}s → {round(end,2)}s  ({round(end-last_end,1)}s)  [{desc}]")
        last_end = end

    # fill remaining to last caption
    if captions:
        last_cap_end = captions[-1].end_sec
        if last_end < last_cap_end:
            times[-1] = {"slide": 17, "start": round(last_end, 2), "end": round(last_cap_end, 2), "desc": "结尾"}
            print(f"  Extended slide-17 end to {round(last_cap_end,2)}s")

    # Build slidePageTimesWav
    page_times = []
    for i, t in enumerate(times):
        if i < len(times) - 1:
            end = times[i + 1]["start"]
        else:
            end = t["end"]
        page_times.append({"start": t["start"], "end": round(end, 2)})

    print("\n=== slidePageTimesWav ===")
    for i, pt in enumerate(page_times):
        print(f"  {i}: start={pt['start']}, end={pt['end']}")

    # Save
    out = Path(__file__).parent / "slide_page_times_v6.json"
    import json
    out.write_text(json.dumps(page_times, indent=2), encoding="utf-8")
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
