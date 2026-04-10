# 检查 ASS 文件原始格式
from pathlib import Path
ass = Path(r"D:\harnessworld\one-context\features\develop\hermes-agent-short-video\production\_sub.ass")
lines = ass.read_text(encoding="utf-8", errors="replace").split("\n")
print("=== Format line ===")
print(lines[11])
print("\n=== First 5 Dialogue lines ===")
for i, line in enumerate(lines[12:17], 12):
    print(f"{i}: {line}")
