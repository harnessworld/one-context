# -*- coding: utf-8 -*-
import subprocess, json, re, pathlib, os

_SCRATCH = pathlib.Path(__file__).resolve().parent
PROD = pathlib.Path(r"D:\harnessworld\one-context\features\develop\hermes-agent-short-video\production")
video = str(PROD / "final_auto.mp4")
out = str(PROD / "final_auto_sub.mp4")
tmp_dir = str(PROD / "tmp")

cfg = json.loads((PROD / "video-input.json").read_text(encoding="utf-8"))
replacements = cfg.get("srtReplacements", [])
sub_cfg = cfg.get("subtitle", {})

raw = (PROD / "sub.srt").read_bytes().decode("utf-8-sig")
for rep in replacements:
    raw = raw.replace(rep["from"], rep["to"])

chars_per_line = sub_cfg.get("charsPerLine", 24)
def wrap_line(line, n):
    if len(line) <= n: return line
    return "\n".join(line[i:i+n] for i in range(0, len(line), n))

blocks = re.split(r"\r?\n\r?\n", raw.strip())
wrapped_blocks = []
for block in blocks:
    lines = re.split(r"\r?\n", block)
    if len(lines) >= 3:
        cl = [wrap_line(l, chars_per_line) for l in lines[2:]]
        wrapped_blocks.append("\n".join([lines[0], lines[1]] + cl))
    else:
        wrapped_blocks.append(block)
wrapped = "\n\n".join(wrapped_blocks)

font = sub_cfg.get("fontName", "Microsoft YaHei")
size = sub_cfg.get("fontSize", 18)
margin = sub_cfg.get("marginV", 18)
bold = 1 if sub_cfg.get("bold", True) else 0
ass_colour = "&H0000FFFF&"

events = []
for block in wrapped.strip().split("\n\n"):
    lines = block.strip().split("\n")
    if len(lines) < 3: continue
    m = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})", lines[1])
    if not m: continue
    def ts(g):
        return int(m.group(g))*3600 + int(m.group(g+1))*60 + int(m.group(g+2)) + int(m.group(g+3))/1000.0
    start, end = ts(1), ts(5)
    content = "\n".join(lines[2:]).replace("\\","\\\\").replace("{","\\{").replace("}","\\}")
    ss = "%d:%02d:%05.2f" % (int(start//3600), int((start%3600)//60), start%60)
    es = "%d:%02d:%05.2f" % (int(end//3600), int((end%3600)//60), end%60)
    events.append("Dialogue: 0,%s,%s,Default,,0,0,0,,%s" % (ss, es, content))

header = (
    "[Script Info]\nTitle: Hermes\nScriptType: v4.00+\nCollisions: Normal\n\n"
    "[V4+ Styles]\n"
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    "Style: Default,%s,%d,%s,%s,%s,&H00000000,%d,1,2,0,2,10,10,%d,1\n\n"
    "[Events]\n"
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
) % (font, size, ass_colour, ass_colour, ass_colour, bold, margin)

ass_content = header + "\n".join(events)
ass_path = os.path.join(tmp_dir, "hermes.ass")
with open(ass_path, "w", encoding="utf-8-sig", newline="") as f:
    f.write(ass_content)

# Write output for exec tool to read
with open(_SCRATCH / "_ffmpeg_cmd.txt", "w", encoding="utf-8") as f:
    f.write("VIDEO=" + video + "\n")
    f.write("ASS=" + ass_path + "\n")
    f.write("OUT=" + out + "\n")
    f.write("ASS_CONTENT_LINE_COUNT=%d\n" % len(ass_content.split("\n")))

print("DONE_PREP")
print("VIDEO:", video)
print("ASS:", ass_path)
print("OUT:", out)
print("ASS lines:", len(ass_content.split("\n")))
