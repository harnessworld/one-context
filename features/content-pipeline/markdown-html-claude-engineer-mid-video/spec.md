---
id: markdown-html-claude-engineer-mid-video
title: Markdown 要被淘汰？Claude 工程师弃用真相（阿哲 / 小夏 对话口播）
status: 发布
category: content-pipeline
primary_repo_id: one-context
owner: ""
updated: "2026-05-10"
---

# 概述

面向开发者与技术爱好者的 **阿哲（技术视角）/ 小夏（行业观察）** 双人对白口播，围绕 Claude Code 团队工程师 Thariq 在 X 平台关于「弃用 Markdown、转向 HTML」的讨论展开：**Markdown 的历史优势、AI 协作下的痛点、HTML 的表达与交互、Claude Code 的工作流、落地场景与代价、工具生态位**。风格要求对话自然、有干货、不哗众取宠；体裁为对话式解读，**涉及具体人物、平台数据（如浏览量）与产品细节的表述，发布前须完成出处核查**。

> ⚠️ 稿中 **「几小时破 200 万浏览」、Thariq 原话转述、Opus 4.7 百万字上下文、生成慢 2–4 倍** 等，凡无一级或可核验二级来源佐证的，不得对外断定为精确事实；须在讲稿或 `review_record.md` 标注 ✅/⚠️/❌，必要时改为「据报道 / 帖文引发热议」等泛化表述。

# 目标与非目标

## 目标

- [ ] 维护 `production/content/01-script.md` 为主对白终稿（主播角色标注：**阿哲 / 小夏**）。
- [ ] 维护 `01-dialogue-volc.md`（`男：`/`女：` · **阿哲→男、小夏→女**）供 [`skills/volc-podcast-tts`](../../../skills/volc-podcast-tts/SKILL.md) action=3。
- [ ] 维护短视频剪辑版 `01-script-short.md`（开场钩子 + 结论 + 一句选型建议）。
- [ ] 补全 `00-structure.md` 段落时长与翻页备注。
- [ ] 补全 `05-publish-kit.md` 各平台标题、简介、话题。
- [ ] 迭代 `production/slides/presentation.html` 与口播对齐，满足 `html-video-from-slides` 的 `#P`、`section.s.slide`、`go(n)` 契约。
- [ ] 双人音频：真人录制 **或** 火山播客 TTS 导出单条 `.wav` 至 `production/media/`（本地，不提交 Git）。
- [ ] `wav-auto` 或 `wav` + `wav-durations.json` 成片；字幕按 [`skills/srt-proofread`](../../../skills/srt-proofread/SKILL.md) 校对并积累 `srtReplacements`。

## 非目标

- 不修改 `repos/` 内业务仓库代码。
- 不在未核实前将二手叙述包装为「已证实新闻」或官方立场。

# 用户与场景

技术内容创作者：中视频或音频口播；移动端观看；观众为关注 Claude / AI 编程工具链、文档协作与标记语言的开发者。

# 验收标准

- [ ] `production/` 骨架齐全（`content/`、`slides/`、`subtitles/`、`timing/`、`media/`、`tmp/`）。
- [ ] `production/content/` 下 **00-structure.md、01-script.md、01-dialogue-volc.md、01-script-short.md、05-publish-kit.md** 齐备且与选题口径一致。
- [ ] `presentation.html` 可键盘翻页；成片配置与 `outputFile`、字幕策略一致。
- [ ] 争议性数据与引语已通过核查或已降级表述。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）：one-context
- **分支 / PR**：—
- **主要路径或模块**：`features/content-pipeline/markdown-html-claude-engineer-mid-video/production/`

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）：—
- **其他需求目录**：同类对白写法可参考 `features/content-pipeline/anthropic-boris-engineering-future-mid-video/`、`features/content-pipeline/claudecode-prompt-caching-mid-video/`。

# 成片流水线（工具）

| 环节 | Skill / 命令入口 |
|------|------------------|
| 对白播客式 TTS（可选） | [`skills/volc-podcast-tts/SKILL.md`](../../../skills/volc-podcast-tts/SKILL.md) · action=3 |
| 幻灯与版式 | [`skills/html-deck-layout/SKILL.md`](../../../skills/html-deck-layout/SKILL.md) |
| HTML + WAV → MP4 | [`skills/html-video-from-slides/SKILL.md`](../../../skills/html-video-from-slides/SKILL.md) · `node cli.js wav-auto --project <production目录>` |
| 字幕校对 | [`skills/srt-proofread/SKILL.md`](../../../skills/srt-proofread/SKILL.md) |

# 开放问题（事实核查）

- **Thariq 帖文**：X（或镜像）上可引用的 **原帖链接** 是否已归档？所谓「不再使用 Markdown」是否为完整上下文（有无限定场景）？
- **传播数据**：「200 万浏览」等指标是否与平台公开数据一致？发布时间窗口？
- **「Claude Code 整个团队转向 HTML」**：这是个人实践还是团队口径？是否需改为「部分工程师的实践」？
- **性能与模型**：「Opus 4.7 百万字上下文」「慢 2–4 倍」等是否可在官方发布说明或作者原文中核对？
- **交互闭环**：双向控件与 Claude 同步的回传路径，表述是否与技术现实一致（避免夸大）？
