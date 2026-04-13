# -*- coding: utf-8 -*-
"""
Hermes Agent: parse SRT + manually assign 23 slides
→ wav-durations.json
"""
from __future__ import annotations
import pathlib, json, sys

PROD = pathlib.Path(r"D:\harnessworld\one-context\features\develop\hermes-agent-short-video\production")
SRT = PROD / "sub.srt"
OUT = PROD / "wav-durations.json"

# ── parse SRT ──────────────────────────────────────────────────────────────
def to_secs(h, m, s, ms):
    return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000.0

entries = []
raw = SRT.read_bytes().decode('utf-8', errors='replace').replace('\r\n', '\n')
lines = raw.split('\n')
i = 0
while i < len(lines):
    line = lines[i].strip()
    # find a line that looks like an index (all digits)
    if line.isdigit():
        idx = int(line)
        # next non-empty line should be timestamp
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i >= len(lines):
            break
        ts_line = lines[i].strip()
        m = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})', ts_line)
        if m:
            start = to_secs(m.group(1), m.group(2), m.group(3), m.group(4))
            end = to_secs(m.group(5), m.group(6), m.group(7), m.group(8))
            # collect content lines (skip empty, skip next index)
            i += 1
            content_lines = []
            while i < len(lines):
                nxt = lines[i].strip()
                if nxt == '':
                    i += 1
                    break
                if nxt.isdigit():
                    break
                content_lines.append(nxt)
                i += 1
            content = ' '.join(content_lines)
            entries.append({'idx': idx, 'start': start, 'end': end, 'text': content})
        else:
            i += 1
    else:
        i += 1

import re
print(f"Entries: {len(entries)}")
if entries:
    print(f"  first: [{entries[0]['start']:.3f}s] '{entries[0]['text'][:50]}'")
    print(f"  last:  [{entries[-1]['end']:.3f}s] '{entries[-1]['text'][:50]}'")
wav_total = entries[-1]['end'] if entries else 0.0
print(f"  WAV total: {wav_total:.2f}s")

# ── manual slide → SRT range mapping ────────────────────────────────────────
# Based on 口播文字稿.md timing (each slide ~20-30s)
# (slide_idx, start_s, end_s, description)
MANUAL_RANGES = [
    (0,  0.0,  18.0,  "封面 欢迎收听"),
    (1,  18.0, 36.0,  "Hello 大家好"),
    (2,  36.0, 60.0,  "开源 自动生成技能 悬念"),
    (3,  60.0, 90.0,  "OpenClaw 特别麻烦"),
    (4,  90.0, 114.0, "周报重来 头大"),
    (5,  114.0,150.0, "设计理念 PART01"),
    (6,  150.0,186.0, "OpenClaw 交通枢纽"),
    (7,  186.0,222.0, "Hermes 画风 自我进化"),
    (8,  222.0,258.0, "插件市场 markdown"),
    (9,  258.0,294.0, "自动归纳 技能 记忆分层"),
    (10, 294.0,330.0, "框架选择 权衡"),
    (11, 330.0,366.0, "个人用户 隐私 本地"),
    (12, 366.0,408.0, "PART02 自动生成技能 门槛"),
    (13, 408.0,450.0, "LLM 判断 模板"),
    (14, 450.0,486.0, "agentskills.io 标准"),
    (15, 486.0,534.0, "40% 提速 自我进化"),
    (16, 534.0,570.0, "PART03 前景 适合人群"),
    (17, 570.0,606.0, "创业 科研 学生"),
    (18, 606.0,636.0, "数字助理 全能管家"),
    (19, 636.0,672.0, "团队协作 客服运维"),
    (20, 672.0,714.0, "本地闭环 跨会话"),
    (21, 714.0,750.0, "工具 平台 MIT"),
    (22, 750.0,  wav_total, "感谢收听 拜拜"),
]

# override last to use actual wav total
MANUAL_RANGES[-1] = (22, 750.0, wav_total, "感谢收听 拜拜")

durations = [round(end - start, 2) for _, start, end, _ in MANUAL_RANGES]
total = sum(durations)
print(f"\nSlide durations (total={total:.2f}s vs WAV={wav_total:.2f}s):")
for idx, start, end, desc in MANUAL_RANGES:
    print(f"  slide {idx:2d}: {durations[idx]:.2f}s  [{start:.1f}-{end:.1f}s] {desc}")

# scale to match wav_total
if abs(total - wav_total) > 1.0:
    scale = wav_total / total
    durations = [round(d * scale, 2) for d in durations]
    total = sum(durations)
    print(f"\nScaled (x{scale:.4f}), total={total:.2f}s:")
    for i, d in enumerate(durations):
        print(f"  slide {i:2d}: {d:.2f}s")

result = {
    'slideDurationsSec': durations,
    'totalSec': round(total, 2),
    'note': 'Hermes Agent manual SRT→slide mapping, based on 口播文字稿'
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\nSaved: {OUT}")
