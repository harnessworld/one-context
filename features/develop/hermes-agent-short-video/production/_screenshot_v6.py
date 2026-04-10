# -*- coding: utf-8 -*-
"""从 presentation-v6.html 生成每页截图 (1920×1080)"""
from __future__ import annotations

import asyncio
import time
from pathlib import Path

from playwright.async_api import async_playwright

HTML = Path(__file__).parent / "presentation-v6.html"
OUT_DIR = Path(__file__).parent
PREFIX = "slide_v6"

# 1920×1080
W, H = 1920, 1080


async def main() -> None:
    out_dir = OUT_DIR
    out_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": W, "height": H})
        await page.goto(HTML.as_uri())
        await page.wait_for_load_state("networkidle")

        # 等待 JS 初始化
        await page.wait_for_timeout(800)

        # 获取总页数
        total = await page.evaluate("document.querySelectorAll('.slide').length")
        print(f"Total slides: {total}")

        for i in range(total):
            # 调用 SlidePresentation.goTo
            await page.evaluate(f"document.querySelectorAll('.slide')[{i}].scrollIntoView()")
            await page.wait_for_timeout(600)  # 等 scroll snap 完成

            # 等待 reveal 动画
            await page.wait_for_timeout(400)

            path = out_dir / f"{PREFIX}_{i:02d}.png"
            await page.screenshot(path=path.as_posix(), animations="disabled")
            print(f"  [{i+1}/{total}] {path.name}")

        await browser.close()
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
