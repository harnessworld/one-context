# -*- coding: utf-8 -*-
import re

content = open("sub.srt", encoding="utf-8").read()

pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)", re.DOTALL)
keywords = ["门槛", "复盘", "agentskills", "百闻", "5次", "15次", "本地闭环", "团队协作", "个人用户", "5+", "LLM分析", "怎么判断"]

for m in pattern.finditer(content):
    text = m.group(4).strip().replace("\n", " ")
    for kw in keywords:
        if kw in text:
            ts = m.group(2)
            print(f"{ts} | {text[:80]}")
            break
