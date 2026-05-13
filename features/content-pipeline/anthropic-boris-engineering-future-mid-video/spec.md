---
id: anthropic-boris-engineering-future-mid-video
title: 当顶尖工程师不再写代码：AI 重写软件开发未来（对话口播）
status: draft
category: content-pipeline
primary_repo_id: one-context
owner: ""
updated: "2026-05-08"
---

# 概述

基于 Anthropic 工程侧公开叙事（含 Boris、Claude Code、Agent 化开发等）创作的 **A/B 双人对白**口播稿，面向开发者与 tech 受众，兼顾播客听感与短视频信息密度。体裁为对话式解读，非一手访谈实录。

> ⚠️ 稿中涉及 **具体人物职务、场合（如红杉现场）、数字（如「2026 年至今零代码」「单日 150 PR」）、产品说法（Loop）** 等，发布前须取得 **可核验的一级或二级来源**（视频、官方博文、可靠媒体报道），并在讲稿或 `review_record.md` 中标注 ✅/⚠️/❌。

# 目标与非目标

## 目标

- [ ] 完成关键事实核查与出处归档（见下方开放问题）。
- [ ] 维护 `production/content/01-script.md` 为主对白终稿；按需产出 **≤3 分钟短视频版**（见 `production/content/01-script-short.md`）及 **重音 / 停顿 / 互动卡点** 标注约定。
- [ ] 补全 `production/content/00-structure.md` 段落时长与剪辑备注。
- [ ] 补全 `production/content/05-publish-kit.md` 各平台标题、简介、话题。
- [ ] 生成 `production/slides/presentation.html`（与口播段落对齐，满足 `html-video-from-slides` DOM/`go(n)` 契约）；**翻页节奏**：每页口播 **≥20s**，不足则合并幻灯页（见 `production/content/00-structure.md`）。
- [ ] 双人音频：真人录制 **或** `skills/volc-podcast-tts`（action=3 对白）导出 **单条** `.wav` 至 `production/media/`（本地，不提交 Git）。
- [ ] 使用 `skills/html-video-from-slides`：`wav-auto` 或（有精确翻页时）`wav` + `wav-durations.json` 成片。
- [ ] Whisper 字幕后按 `skills/srt-proofread` 校对专名与数字，必要时积累 `timing/video-input.json` 的 `srtReplacements`。

## 非目标

- 不修改 `repos/` 内业务仓库代码。
- 不在未核实前将口述内容断言为「一手引语」对外宣传。

# 用户与场景

技术内容创作者：中长视频 / 播客切片 / 短视频改编；观众为关注 AI 编程与组织变革的 engineer、管理者与创作者。

# 验收标准

- [ ] `production/` 目录骨架完整（含 `content/`、`slides/`、`subtitles/`、`timing/`、`media/`、`tmp/`）。
- [ ] `production/content/01-script.md` 与选题口径一致，事实核查状态可追溯。
- [ ] 成片所用 `presentation.html` 含可用 `go(n)`；`video-input.json`（若使用）与 `outputFile`、字幕策略一致。
- [ ] 导出 MP4 路径与配置一致；如需烧录字幕，`burnSubtitles` 与校对后 `sub.srt` 一致。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）：one-context
- **分支 / PR**：—
- **主要路径或模块**：`features/content-pipeline/anthropic-boris-engineering-future-mid-video/production/`

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）：—
- **其他需求目录**：同类对白拆解可参考 `features/content-pipeline/anthropic-ai-blueprint-dialogue-mid-video/`。

# 成片流水线（工具）

| 环节 | Skill / 命令入口 |
|------|------------------|
| 对白播客式 TTS（可选） | [`skills/volc-podcast-tts/SKILL.md`](../../../skills/volc-podcast-tts/SKILL.md) · action=3 |
| 幻灯与版式 | [`skills/html-deck-layout/SKILL.md`](../../../skills/html-deck-layout/SKILL.md) |
| HTML + WAV → MP4 | [`skills/html-video-from-slides/SKILL.md`](../../../skills/html-video-from-slides/SKILL.md) · `node cli.js wav-auto --project <production目录>` |
| 字幕校对 | [`skills/srt-proofread/SKILL.md`](../../../skills/srt-proofread/SKILL.md) |

# 开放问题（事实核查）

- Boris **姓名拼写与职务**是否与当场活动一致？Primary 来源链接？
- **「红杉现场」** 具体活动名称、日期、是否有官方回放或文字实录？
- **「2026 年至今一行代码未写」** 是否为原话或摘要？上下文条件（个人习惯 vs 团队常态）？
- **「一天 150 个 PR」** 统计口径（合并数、打开数、机器人 PR）与出处？
- **Claude Code「前 6 个月」「自用 10%」** 等叙述是否有可追溯演讲/采访？
- **「Loop」** 作为产品或内部代号：对外称谓与功能边界？
- **印刷机类比**（识字率、文献量、成本倍数）为修辞类比还是引用具体研究？若引用需标注来源。
- **「工程经理、产品、设计…财务都写代码」**：概括性陈述是否需要收窄为「团队内现象举例」以避免夸大？
