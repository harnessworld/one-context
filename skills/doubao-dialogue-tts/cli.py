#!/usr/bin/env python3
"""CLI: 对口播脚本调用火山豆包 TTS V3，导出 WAV。"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_REPO_LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
if _REPO_LIB not in sys.path:
    sys.path.insert(0, _REPO_LIB)

from volc_v3_tts import (  # noqa: E402
    DEFAULT_RESOURCE_ID,
    DEFAULT_VOICE_FEMALE,
    DEFAULT_VOICE_MALE,
    dialogue_to_wav,
    mono_text_to_wav,
)


def load_env_file(path: Path) -> None:
    """Fill os.environ from KEY=VALUE lines; never overwrite existing env."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def main() -> int:
    skill_dir = Path(__file__).resolve().parent
    load_env_file(skill_dir / "local.env")
    p = argparse.ArgumentParser(description="豆包/火山 TTS：对白脚本 → WAV")
    p.add_argument("--input", "-i", help="对白脚本 UTF-8 文本路径")
    p.add_argument("--output", "-o", required=True, help="输出 .wav 路径")
    p.add_argument("--mono", action="store_true", help="整篇单人朗读（不使用男/女前缀）")
    p.add_argument(
        "--speaker",
        default=DEFAULT_VOICE_FEMALE,
        help=f"单人模式音色（默认 {DEFAULT_VOICE_FEMALE}）",
    )
    p.add_argument("--voice-male", default=DEFAULT_VOICE_MALE)
    p.add_argument("--voice-female", default=DEFAULT_VOICE_FEMALE)
    p.add_argument("--resource-id", default=os.environ.get("VOLCENGINE_TTS_RESOURCE_ID", DEFAULT_RESOURCE_ID))
    p.add_argument("--sample-rate", type=int, default=24000)
    p.add_argument("--pause-ms", type=int, default=280, help="对白句间静音长度")
    p.add_argument("--api-key", default=os.environ.get("VOLCENGINE_TTS_API_KEY", ""))
    p.add_argument("--app-id", default=os.environ.get("VOLCENGINE_TTS_APP_ID", ""))
    p.add_argument("--access-key", default=os.environ.get("VOLCENGINE_TTS_ACCESS_KEY", ""))
    args = p.parse_args()

    key = (args.api_key or "").strip()
    app_id = (args.app_id or "").strip()
    access_key = (args.access_key or "").strip()
    if not key and not (app_id and access_key):
        print(
            "ERROR: 设置环境变量 VOLCENGINE_TTS_API_KEY，或同时提供 --app-id 与 --access-key（旧版控制台）",
            file=sys.stderr,
        )
        return 2

    if args.mono:
        if not args.input:
            print("ERROR: --mono 需要 --input 文本文件", file=sys.stderr)
            return 2
        with open(args.input, encoding="utf-8") as f:
            text = f.read()
        mono_text_to_wav(
            text=text,
            out_wav=args.output,
            api_key=key,
            speaker=args.speaker,
            resource_id=args.resource_id,
            sample_rate=args.sample_rate,
            app_id=app_id or None,
            access_key=access_key or None,
        )
        print(args.output)
        return 0

    if not args.input:
        print("ERROR: 需要 --input 脚本路径（或使用 --mono）", file=sys.stderr)
        return 2
    with open(args.input, encoding="utf-8") as f:
        script = f.read()
    dialogue_to_wav(
        script=script,
        out_wav=args.output,
        api_key=key,
        resource_id=args.resource_id,
        voice_male=args.voice_male,
        voice_female=args.voice_female,
        sample_rate=args.sample_rate,
        pause_ms=args.pause_ms,
        app_id=app_id or None,
        access_key=access_key or None,
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
