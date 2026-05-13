#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 SRT 字幕全文做繁体→简体（OpenCC），时间轴与序号不变。
依赖: pip install opencc-python-reimplemented

用法:
  python t2s_srt.py path/to/sub.srt
  python t2s_srt.py path/to/sub.srt -o path/out.srt
"""

from __future__ import annotations

import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="SRT 繁体转简体（OpenCC t2s）")
    ap.add_argument("srt", help="输入 .srt 路径")
    ap.add_argument(
        "-o",
        "--output",
        default=None,
        help="输出路径（默认覆盖输入文件）",
    )
    args = ap.parse_args()

    try:
        from opencc import OpenCC  # type: ignore
    except ImportError:
        print(
            "缺少依赖: pip install opencc-python-reimplemented",
            file=sys.stderr,
        )
        return 2

    path_in = args.srt
    path_out = args.output or path_in

    try:
        raw = open(path_in, encoding="utf-8-sig").read()
    except OSError as e:
        print(f"无法读取: {path_in} ({e})", file=sys.stderr)
        return 1

    cc = OpenCC("t2s")
    # 去掉 BOM 再转，避免重复 BOM
    body = raw.lstrip("\ufeff")
    converted = cc.convert(body)
    out = "\ufeff" + converted if not converted.startswith("\ufeff") else converted

    try:
        open(path_out, "w", encoding="utf-8", newline="\n").write(out)
    except OSError as e:
        print(f"无法写入: {path_out} ({e})", file=sys.stderr)
        return 1

    print(f"已写入: {path_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
