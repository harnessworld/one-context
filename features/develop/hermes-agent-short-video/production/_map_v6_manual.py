# -*- coding: utf-8 -*-
"""
从原始 23-slidedurations.json 反推 v6 18 页时间轴
原始每段时长不变，只是合并相邻的 segment
原始 23 段：
  0-2: 封面/开场/悬念(0-24.16s)
  3-5: 痛点(24.16-51.76s)  
  6-12: 设计理念+对比(51.76-198.64s) ← v6 slide 3-5
  13-16: 自动生成技能(198.64-314.88s) ← v6 slide 7-9
  17-18: agentskills(314.88-360.72s) ← v6 slide 10
  19-20: 收益(360.72-399.16s) ← v6 slide 11
  21-22: 前景(399.16-438.10s) ← v6 slide 12-13
  23-25: 团队(438.10-492.86s) ← v6 slide 14-15
  26-27: 优势+工程(492.86-534.26s) ← v6 slide 16-17
  28-29: 结尾(534.26-546.6s) ← v6 slide 18

v6 18 页：
  0: 封面(0-6.92s) ← orig 0
  1: 悬念 Hermes是什么(6.92-14.14s) ← orig 1-2
  2: 痛点 OpenClaw太麻烦(14.14-27.72s) ← orig 3-5
  3: 两个路数(27.72-39.12s) ← orig 6-7
  4: 技能管理对比(39.12-43.84s) ← orig 8-9
  5: 怎么选(43.84-55.24s) ← orig 10-12
  6: PART 2(55.24-66.64s) ← orig 13 (PART标签)
  7: 门槛(66.64-108.9s) ← orig 13-14 (阈值5+/15次)
  8: 复盘+LLM(108.9-135.5s) ← orig 15-16 (复盘/LLM)
  9: agentskills.io(135.5-162.1s) ← orig 17-18
  10: 实际收益(162.1-188.12s) ← orig 19-20
  11: PART 3(188.12-199.56s) ← orig 21 (PART标签)
  12: 前景场景(199.56-235.44s) ← orig 21-22 (前景+团队)
  13: 个人用户(235.44-263.88s) ← orig 23-25
  14: 团队协作(263.88-326.32s) ← orig 26-27
  15: 核心优势(326.32-344.24s) ← orig 28
  16: 工程力(344.24-382.38s) ← orig 29
  17: 结尾(382.38-546.6s) ← orig 30-31

手动调参
"""
import json
from pathlib import Path

orig_durations = [6.92,7.22,10.02,13.58,4.72,11.4,15.26,28.5,26.6,24.98,28.5,26.02,42.9,43.28,46.64,38.44,17.92,39.1,3.34,34.96,24.96,29.6,21.74]

# 原始各 slide 在 orig_durations 中的 index 范围
# 根据 23-slide HTML 的实际内容段落
orig_slide_segments = [
    (0,),           # 0 封面
    (1,2),          # 1 开场+悬念
    (3,4,5),        # 2 痛点
    (6,7),          # 3 两个路数
    (8,9),          # 4 技能管理
    (10,11,12),     # 5 怎么选
    (13,),          # 6 PART 2
    (13,14),        # 7 门槛 (13=开场+阈值, 14=复盘+LLM)
    (14,15),        # 8 复盘机制+LLM分析
    (16,17,18),     # 9 agentskills
    (19,20),        # 10 收益
    (21,),          # 11 PART 3
    (21,22),        # 12 前景+团队开场
    (22,23,24),     # 13 个人用户
    (24,25,26),     # 14 团队协作+管家
    (27,),          # 15 核心优势
    (28,),          # 16 工程力
    (29,30,31),     # 17 结尾
]

def cumsum(lst):
    out = [0]
    for x in lst:
        out.append(out[-1] + x)
    return out

orig_cum = cumsum(orig_durations)

page_times = []
for i, seg in enumerate(orig_slide_segments):
    start = orig_cum[seg[0]]
    end = orig_cum[seg[-1] + 1]
    page_times.append({"start": round(start, 2), "end": round(end, 2), "dur": round(end - start, 2)})

print("=== v6 slidePageTimesWav (18 slides) ===")
for i, pt in enumerate(page_times):
    print(f"  {i:02d}: {pt['start']:6.2f}s → {pt['end']:6.2f}s  ({pt['dur']:.1f}s)")

total = page_times[-1]["end"]
print(f"\nTotal: {total:.2f}s")

out = Path(__file__).parent / "slide_page_times_v6.json"
out.write_text(json.dumps(page_times, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Saved → {out}")
