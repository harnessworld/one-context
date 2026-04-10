# -*- coding: utf-8 -*-
"""Read sub.srt and print timestamps"""
import pathlib, re, sys

SRT = pathlib.Path(r"D:\harnessworld\one-context\features\develop\hermes-agent-short-video\production\sub.srt")
raw = SRT.read_bytes()
text = raw.decode('utf-8-sig')  # strips BOM

def to_f(s):
    h, rest = s.split(':', 1)
    m, rest2 = rest.split(':', 1)
    s_, ms = rest2.split(',')
    return int(h)*3600 + int(m)*60 + int(s_) + int(ms)/1000.0

entries = []
# split on blank lines, handle CRLF
blocks = re.split(r'\r?\n\r?\n', text.strip())
for block in blocks:
    lines = re.split(r'\r?\n', block)
    if len(lines) < 3:
        continue
    ts_m = re.match(r'(\d+)\s*\r?\n(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})', lines[0]+'\n'+lines[1])
    if not ts_m:
        continue
    idx = int(ts_m.group(1))
    start = to_f(ts_m.group(2))
    end = to_f(ts_m.group(3))
    content = '\n'.join(lines[2:]).strip()
    entries.append((idx, start, end, content))

print(f"Total: {len(entries)} entries")
sys.stdout.reconfigure(encoding='utf-8')
for idx, s, e, c in entries:
    print(f"{idx}\t{s:.3f}\t{e:.3f}\t{c[:80]}")
