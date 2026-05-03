# html-video-from-slides — 目录说明

权威用法见根目录 **`SKILL.md`**（适配器只索引该文件）。

| 路径 | 内容 |
|------|------|
| **`pipeline/video-pipeline.step.yaml`** | **端到端编排入口**（需 `/step` 类编排器）；详情 **`references/VIDEO_PIPELINE.md`** |
| **`cli.js`** | **单步 CLI**：`tts` / `wav` / `wav-auto` / `srt-map` / `timing-check` / `cover`（step 计划内部也会调用） |
| **`lib/`** | Node 流水线实现 |
| **`scripts/`** | Python：`align_wav_slides.py`、`t2s_srt.py`、`tts_helper.py`；辅助 `test_ss.js` |
| **`assets/`** | 经典桌面幻灯素材：`base.css`、`theme-*.css`、`reference.html`（复制到素材目录使用） |
| **`references/`** | 文档：`TEMPLATES.md`、`svg-snippets.md`、`DESIGN-STANDARD.md`、`VIDEO_PIPELINE.md` |
| **`pipeline/`** | `video-pipeline.step.yaml`（仅在与 `/step` 编排器联用时需要） |
| **`examples/`** | `*.example.json` 配置样例 |
| **`package.json`** | Node 依赖（Playwright 等） |
| **`requirements-whisper.txt`** | Whisper 相关 pip 提示 |
