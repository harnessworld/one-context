# -*- coding: utf-8 -*-
import subprocess, json, re, pathlib, os

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
    if len(line) <= n:
        return line
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
    if len(lines) < 3:
        continue
    m = re.match(
        r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2}),(\d{3})",
        lines[1]
    )
    if not m:
        continue
    def ts(g):
        return (int(m.group(g)) * 3600 + int(m.group(g+1)) * 60 +
                int(m.group(g+2)) + int(m.group(g+3)) / 1000.0)
    start, end = ts(1), ts(5)
    content = "\n".join(lines[2:]).replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
    ss = "%d:%02d:%05.2f" % (int(start // 3600), int((start % 3600) // 60), start % 60)
    es = "%d:%02d:%05.2f" % (int(end // 3600), int((end % 3600) // 60), end % 60)
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

print("ASS written:", ass_path)
print("Video:", video)
print("Output:", out)

cmd = ["ffmpeg", "-y", "-i", video, "-vf", "ass=" + ass_path, "-c:a", "copy", out]
# Use shell=True so Python passes the path string directly to cmd
# ffmpeg must receive the actual backslash path
cmd_str = 'ffmpeg -y -i "%s" -vf "ass=%s" -c:a copy "%s"' % (video, ass_path, out)
print("CMD:", cmd_str)
r = subprocess.run(cmd_str, shell=True, capture_output=True)
print("returncode:", r.returncode)
if r.returncode != 0 and r.stderr:
    print("ERR:", r.stderr.decode("utf-8", errors="replace")[-3000:])
else:
    print("SUCCESS!")
    sz = os.path.getsize(out)
    print("Output size:", sz, "bytes", "(%.1f MB)" % (sz / 1024 / 1024))
