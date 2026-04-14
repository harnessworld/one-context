# skills — 仓库内可复用技能（工具无关）

本目录存放 **跨 Cursor / Claude Code / OpenClaw 等** 共用的自动化流程，与 `knowledge/` 中「给人/模型读的规范」互补：此处偏重 **可执行脚本 + 单一入口**。

| 路径 | 说明 |
|------|------|
| [`html-video-from-slides/`](html-video-from-slides/) | HTML 幻灯 + 口播 → MP4；**wav-auto** 仅需单个 WAV + HTML（Whisper 自动对齐）；见 `SKILL.md` |
| [`html-deck-layout/`](html-deck-layout/) | 全屏 `presentation.html` **版式**：防空白、`fill-deck`、字号与示意图区；改幻灯视觉时必读；见 `SKILL.md` |
| [`openclaw-slides/`](openclaw-slides/) | OpenClaw 演示幻灯生成；多语言 README（中/英/日/德/法/西/意/俄）；见 `SKILL.md` |
| [`windows-c-drive-cleanup/`](windows-c-drive-cleanup/) | Windows C 盘清理；**授权后** `invoke-c-drive-cleanup.ps1` 白名单自动清理；只读 `survey-c-drive-report.ps1`（五-A 自动 / 五-B 手动）；见 `SKILL.md` |

各视频选题目录**不应**再复制一套 Node 脚本；应通过 `--project` 指向仅含素材的文件夹。
