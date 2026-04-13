# -*- coding: utf-8 -*-
"""烧录字幕 - 双反斜杠解决 ffmpeg 路径解析 bug"""
import subprocess, json, re, pathlib, os

PROD = pathlib.Path(r"D:\harnessworld\one-context\features\develop\hermes-agent-short-video\production")
video = str(PROD / "final_auto.mp4")
out = str(PROD / "final_auto_sub.mp4")
tmp_dir = str(PROD / "temp_video_wav")

cfg = json.loads((PROD / "video-input.json").read_text(encoding="utf-8"))
replacements = cfg.get("srtReplacements", [])
sub_cfg = cfg.get("subtitle", {})

# read + apply replacements
raw = (PROD / "sub.srt").read_bytes().decode("utf-8-sig")
for rep in replacements:
    raw = raw.replace(rep["from"], rep["to"])

# word-wrap
chars_per_line = sub_cfg.get("charsPerLine", 24)
def wrap_line(line, n):
    if len(line) <= n: return line
    return "\n".join(line[i:i+n] for i in range(0, len(line), n))

blocks = re.split(r"\r?\n\r?\n", raw.strip())
wrapped_blocks = []
for block in blocks:
    lines = re.split(r"\r?\n", block)
    if len(lines) >= 3:
        content_lines = [wrap_line(l, chars_per_line) for l in lines[2:]]
        wrapped_blocks.append("\n".join([lines[0], lines[1]] + content_lines))
    else:
        wrapped_blocks.append(block)
wrapped = "\n\n".join(wrapped_blocks)

# Convert to ASS
font = sub_cfg.get("fontName", "Microsoft YaHei")
size = sub_cfg.get("fontSize", 18)
margin = sub_cfg.get("marginV", 18)
bold = 1 if sub_cfg.get("bold", True) else 0
ass_colour = "&H0000FFFF&"  # yellow

events = []
for block in wrapped.strip().split("\n\n"):
    lines = block.strip().split("\n")
    if len(lines) < 3: continue
    m = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})", lines[1])
    if not m: continue
    def ts(g): return int(m.group(g))*3600 + int(m.group(g+1))*60 + int(m.group(g+2)) + int(m.group(g+3))/1000.0
    start, end = ts(1), ts(5)
    content = "\n".join(lines[2:]).replace("\\","\\\\").replace("{","\\{").replace("}","\\}")
    ss = f"{int(start//3600)}:{int((start%3600)//60):02d}:{start%60:05.2f}"
    es = f"{int(end//3600)}:{int((end%3600)//60):02d}:{end%60:05.2f}"
    events.append(f"Dialogue: 0,{ss},{es},Default,,0,0,0,,{content}")

header = f"""[Script Info]
Title: Hermes
ScriptType: v4.00+
Collisions: Normal

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{size},{ass_colour},{ass_colour},{ass_colour},&H00000000,{bold},1,2,0,2,10,10,{margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass_content = header + "\n".join(events)

ass_path = os.path.join(tmp_dir, "hermes.ass")
with open(ass_path, "w", encoding="utf-8-sig") as f:
    f.write(ass_content)

print(f"ASS: {ass_path}")

# Key: use cmd.exe /c with DOUBLED backslashes so cmd preserves them
# cmd.exe strips one level of backslash escaping
def cmd_quote(s):
    # Double backslashes for cmd.exe
    s = s.replace("\\", "\\\\")
    # Escape double quotes
    s = s.replace('"', '\\"')
    return f'"{s}"'

video_q = cmd_quote(video)
out_q = cmd_quote(out)
ass_q = cmd_quote(ass_path)

# Build command string with double-backslashed paths
cmd_str = f'ffmpeg -y -i {video_q} -vf ass={ass_q} -c:a copy {out_q}'
print(f"CMD: {cmd_str}")

result = subprocess.run(
    ["cmd.exe", "/c", cmd_str],
    capture_output=True
)
print("returncode:", result.returncode)
if result.stderr:
    stderr = result.stderr.decode("gbk", errors="replace")
    print("stderr:", stderr[-2000:])
