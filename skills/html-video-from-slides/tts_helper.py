"""
TTS 辅助：由 lib/tts_pipeline.js 调用，使用 Python edge-tts 生成 MP3。
用法：python tts_helper.py <config.json>
"""
import sys
import asyncio
import json
import edge_tts


async def main():
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        config = json.load(f)

    communicate = edge_tts.Communicate(
        config["text"],
        config["voice"],
        rate=config.get("rate", "+0%"),
        pitch=config.get("pitch", "+0Hz"),
        volume=config.get("volume", "+0%"),
    )
    await communicate.save(config["output"])
    print(f"OK: {config['output']}")


asyncio.run(main())
