# -*- coding: utf-8 -*-
"""一次性：修正 Whisper 常见误字（不改时间轴）。执行后删本脚本即可。"""
import re
from pathlib import Path

p = Path(__file__).resolve().parent / "sub.srt"
t = p.read_text(encoding="utf-8")

# 顺序：长短语优先
REPL = [
    ("血距人模式", "穴居人模式"),
    ("血军人模式", "穴居人模式"),
    ("削剧人模式", "穴居人模式"),
    ("血距人代码", "穴居人代码"),
    ("血距人语", "穴居人语"),
    ("血距人", "穴居人"),
    ("血军人", "穴居人"),
    ("墨尾", "末尾"),
    ("投肯", "Token"),
    ("Evroportic", "Anthropic"),
    ("缸序", "刚需"),
    ("负利效应", "复利效应"),
    ("点赞书", "点赞数"),
    ("旧时期时代", "旧石器时代"),
    ("经检", "精简"),
    ("词评统计", "词频统计"),
    ("测试用力", "测试用例"),
    ("Altropic", "Anthropic"),
    ("N号活吃", "穴居人式"),
    ("西字如今", "言简意赅"),
    ("Open Cloud", "OpenClaw"),
    ("Cloud Code", "Claude Code"),
]
for a, b in REPL:
    t = t.replace(a, b)
# 播客里多数 Cloud 指 Claude（ASR 混淆）
t = re.sub(r"(?<![A-Za-z])Cloud(?![A-Za-z])", "Claude", t)

p.write_text(t, encoding="utf-8")
print("OK:", p)
