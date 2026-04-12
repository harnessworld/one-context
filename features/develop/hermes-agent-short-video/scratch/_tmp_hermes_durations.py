# -*- coding: utf-8 -*-
"""
Hermes Agent: 根据 sub.srt 真实时间戳，人工划分23页幻灯片时长
→ wav-durations.json
"""
from __future__ import annotations
import pathlib, json, sys

PROD = pathlib.Path(r"D:\harnessworld\one-context\features\develop\hermes-agent-short-video\production")
SRT = PROD / "sub.srt"
OUT = PROD / "wav-durations.json"

# ── SRT 真实时间（手动划分，基于口播文字稿+PPT结构）─────────────────────────
# 188条字幕，WAV总长 546.6s
# 每页 slide 对应口播内容的时间范围（对照口播文字稿人工划定）
SLIDE_TIMES = [
    # (slide, start_s, end_s, description)
    (0,  0.0,   6.92,  "封面 欢迎收听豆包AI"),
    (1,  6.92,  14.14, "Hello 大家好 本期 Hermes"),
    (2,  14.14, 24.16, "开源 自动生成技能 悬念"),
    (3,  24.16, 37.74, "OpenClaw 插件多 配置麻烦"),
    (4,  37.74, 42.46, "周报重来 头大"),
    (5,  42.46, 53.86, "PART01 设计理念路数"),
    (6,  53.86, 69.12, "OpenClaw 交通枢纽 调度员"),
    (7,  69.12, 97.62, "Hermes 自我进化 画风不同"),
    (8,  97.62, 124.22,"插件市场 markdown记忆"),
    (9,  124.22,149.20,"自动归纳 技能 记忆冷热"),
    (10, 149.20,177.70,"框架选择 团队选OpenClaw"),
    (11, 177.70,203.72,"个人选Hermes 隐私本地"),
    (12, 203.72,246.62,"PART02 自动生成技能门槛"),
    (13, 246.62,289.90,"LLM判断 模板 复盘"),
    (14, 289.90,336.54,"agentskills.io 规范共享"),
    (15, 336.54,374.98,"40%提速 自我进化"),
    (16, 374.98,392.90,"PART03 前景 适合人群"),
    (17, 392.90,432.00,"创业 企业 科研 学生"),
    (18, 432.00,435.34,"数字助理 管家"),
    (19, 435.34,470.30,"团队协作 客服运维原型"),
    (20, 470.30,495.26,"本地闭环 跨会话记忆"),
    (21, 495.26,524.86,"工具平台 沙盒MIT"),
    (22, 524.86,546.60,"感谢收听 拜拜"),
]

durations = [round(end - start, 2) for _, start, end, _ in SLIDE_TIMES]
total = round(sum(durations), 2)
wav_total = 546.60

print(f"Total duration: {total}s | WAV: {wav_total}s | Diff: {wav_total - total:.2f}s")
print()
for slide, start, end, desc in SLIDE_TIMES:
    print(f"  slide {slide:2d}: {durations[slide]:.2f}s  [{start:.1f}–{end:.1f}s]  {desc}")

# write
result = {
    'slideDurationsSec': durations,
    'totalSec': total,
    'note': 'Hermes Agent SRT manual mapping (口播文字稿 aligned to 23 slides)'
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\nSaved: {OUT}")
