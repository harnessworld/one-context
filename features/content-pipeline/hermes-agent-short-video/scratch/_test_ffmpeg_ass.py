# -*- coding: utf-8 -*-
"""诊断 ffmpeg ass filter Windows 路径 bug"""
import subprocess, pathlib, os

tmp = r"D:\harnessworld\one-context\features\develop\hermes-agent-short-video\production\temp_video_wav"

# Create minimal ASS file
ass_content = (
    "[Script Info]\nTitle: Test\nScriptType: v4.00+\n\n"
    "[V4+ Styles]\n"
    "Format: Name, Fontname, Fontsize, PrimaryColour\n"
    "Style: Default,Arial,20,&H0000FFFF&\n\n"
    "[Events]\n"
    "Format: Layer, Start, End, Style, Text\n"
    "Dialogue: 0,0:00:00.00,0:00:05.00,Default,,Hello World\n"
)

test_ass = os.path.join(tmp, "test.ass")
with open(test_ass, "w", encoding="utf-8-sig", newline="") as f:
    f.write(ass_content)

video = r"D:\harnessworld\one-context\features\develop\hermes-agent-short-video\production\final_auto.mp4"
out = os.path.join(tmp, "test_out.mp4")

print(f"ASS file exists: {os.path.exists(test_ass)}")
print(f"ASS content:\n{open(test_ass, encoding='utf-8-sig').read()}")

# Test 1: subprocess list (baseline)
print("\n=== Test 1: subprocess list ===")
r = subprocess.run(["ffmpeg", "-y", "-i", video, "-vf", f"ass={test_ass}", "-t", "1", "-c:a", "copy", out], capture_output=True)
print("rc:", r.returncode)
if r.stderr:
    print("ERR:", r.stderr.decode("utf-8", errors="replace")[:500])

# Test 2: shell=True with quoted string
print("\n=== Test 2: shell=True ===")
cmd = f'ffmpeg -y -i "{video}" -vf "ass={test_ass}" -t 1 -c:a copy "{out}"'
print("CMD:", cmd)
r = subprocess.run(cmd, shell=True, capture_output=True)
print("rc:", r.returncode)
if r.stderr:
    print("ERR:", r.stderr.decode("utf-8", errors="replace")[:500])

# Test 3: cmd /c with bat
print("\n=== Test 3: cmd /c bat ===")
bat = os.path.join(tmp, "_test.bat")
with open(bat, "w") as f:
    f.write(f'chcp 65001 >nul\nffmpeg -y -i "{video}" -vf "ass={test_ass}" -t 1 -c:a copy "{out}"\n')
r = subprocess.run(["cmd", "/c", bat], capture_output=True)
print("rc:", r.returncode)
if r.stderr:
    print("ERR:", r.stderr.decode("utf-8", errors="replace")[:500])
