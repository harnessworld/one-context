# skills — 仓库内可复用技能（工具无关）

本目录存放 **跨 Cursor / Claude Code / OpenClaw 等** 共用的自动化流程，与 `knowledge/` 中「给人/模型读的规范」互补：此处偏重 **可执行脚本 + 单一入口**。

| 路径 | 说明 |
|------|------|
| [`cover-design/`](cover-design/) | **封面设计规范**；3 种预设风格（简约/科技/数据）；横竖版模板；被 `html-video-from-slides` 引用 |
| [`html-video-from-slides/`](html-video-from-slides/) | HTML 幻灯 + 口播 → MP4；**wav-auto** 仅需单个 WAV + HTML（Whisper 自动对齐）；见 `SKILL.md` · 目录分层见同目录 `README.md` |
| [`html-deck-layout/`](html-deck-layout/) | **Mobile PPT 生成器**（1920×1080）：prompt → 手机横屏幻灯片，6 主题 + 7 布局 + 4 全 deck 模板，自动 fill-deck、≥42px 字号、≥85% 覆盖率；可与 `html-video-from-slides` 联动成片；见 `SKILL.md` |
| [`srt-to-deck/`](srt-to-deck/) | **SRT 字幕 → 幻灯片 + 精准翻页时长**；Whisper 转写的 SRT → presentation.html + wav-durations.json；按话题拆页时锁定每页对应的 SRT 条目范围，从时间戳直接算出翻页时长；配合 html-video-from-slides wav 模式无需 Whisper 二次对齐；触发词：SRT转PPT/字幕转幻灯/口播转PPT/srt to presentation；见 `SKILL.md` |
| [`html-slides/`](html-slides/) | HTML 演示幻灯生成（从零/PPT转换，12种样式预设）；多语言 README；见 `SKILL.md` |
| [`fireworks-tech-graph/`](fireworks-tech-graph/) | **技术图表生成**；SVG 架构图/流程图/时序图/UML/ER/网络拓扑等 15+ 图表类型，7 种视觉风格，rsvg-convert 导出 PNG；触发词：画图/架构图/流程图/可视化；见 `SKILL.md` |
| [`skill-parallel-verify/`](skill-parallel-verify/) | **Skill 交付前并行验证**；5 个测试专家独立执行→测试主管判定语义等价→不一致自动修复循环；见 `SKILL.md` |
| [`windows-c-drive-cleanup/`](windows-c-drive-cleanup/) | Windows C 盘清理；**授权后** `invoke-c-drive-cleanup.ps1` 白名单自动清理；只读 `survey-c-drive-report.ps1`（五-A 自动 / 五-B 手动）；见 `SKILL.md` |
| [`project-audit/`](project-audit/) | **项目整理**；审计全量已追踪文件，识别错位/误提交文件，列出清单供确认后执行挪正/排除/清理；触发词：项目整理/审计/清理仓库；见 `SKILL.md` |
| [`doubao-dialogue-tts/`](doubao-dialogue-tts/) | **豆包/火山 TTS**：对口播对白脚本（男：/女：）逐句合成 **WAV**；V3 合成接口纯念稿、不走 AI 播客自动生成；见 `SKILL.md` |
| [`volc-podcast-tts/`](volc-podcast-tts/) | **火山播客 WebSocket v3**：长文本/URL/`nlp_texts` 双人播客流式音频（PCM/WAV/MP3）；与「逐句念稿」TTS 不同；见 `SKILL.md` |
| [`gitsync/`](gitsync/) | **安全 Git 同步**：fetch → 分叉诊断 → ff-only/merge/rebase → 冲突处理；备份分支 + stash，避免本地丢失；触发 `/gitsync`、`git sync`；见 `SKILL.md` |

各视频选题目录**不应**再复制一套 Node 脚本；应通过 `--project` 指向仅含素材的文件夹。
