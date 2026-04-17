# skills — 仓库内可复用技能（工具无关）

本目录存放 **跨 Cursor / Claude Code / OpenClaw 等** 共用的自动化流程，与 `knowledge/` 中「给人/模型读的规范」互补：此处偏重 **可执行脚本 + 单一入口**。

| 路径 | 说明 |
|------|------|
| [`cover-design/`](cover-design/) | **封面设计规范**；3 种预设风格（简约/科技/数据）；横竖版模板；被 `html-video-from-slides` 引用 |
| [`html-video-from-slides/`](html-video-from-slides/) | HTML 幻灯 + 口播 → MP4；**wav-auto** 仅需单个 WAV + HTML（Whisper 自动对齐）；见 `SKILL.md` |
| [`html-deck-layout/`](html-deck-layout/) | **Mobile PPT 生成器**（1920×1080）：prompt → 手机横屏幻灯片，6 主题 + 7 布局 + 4 全 deck 模板，自动 fill-deck、≥42px 字号、≥85% 覆盖率；可与 `html-video-from-slides` 联动成片；见 `SKILL.md` |
| [`html-slides/`](html-slides/) | HTML 演示幻灯生成（从零/PPT转换，12种样式预设）；多语言 README；见 `SKILL.md` |
| [`fireworks-tech-graph/`](fireworks-tech-graph/) | **技术图表生成**；SVG 架构图/流程图/时序图/UML/ER/网络拓扑等 15+ 图表类型，7 种视觉风格，rsvg-convert 导出 PNG；触发词：画图/架构图/流程图/可视化；见 `SKILL.md` |
| [`skill-parallel-verify/`](skill-parallel-verify/) | **Skill 交付前并行验证**；5 个测试专家独立执行→测试主管判定语义等价→不一致自动修复循环；见 `SKILL.md` |
| [`windows-c-drive-cleanup/`](windows-c-drive-cleanup/) | Windows C 盘清理；**授权后** `invoke-c-drive-cleanup.ps1` 白名单自动清理；只读 `survey-c-drive-report.ps1`（五-A 自动 / 五-B 手动）；见 `SKILL.md` |
| [`project-audit/`](project-audit/) | **项目整理**；审计全量已追踪文件，识别错位/误提交文件，列出清单供确认后执行挪正/排除/清理；触发词：项目整理/审计/清理仓库；见 `SKILL.md` |

各视频选题目录**不应**再复制一套 Node 脚本；应通过 `--project` 指向仅含素材的文件夹。
