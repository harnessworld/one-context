---
id: ai-agent-security-2026-revelations-mid-video
title: 2026 AI Agent 安全启示录（对话口播）
status: 发布
category: content-pipeline
primary_repo_id: one-context
owner: ""
updated: "2026-05-09"
---

# 概述

面向开发者与安全关注者的 **阿程 / 小夏** 双人对白口播，梳理 AI Agent 在生产与协作中的典型风险叙事与治理思路。体裁为对话式科普，**非一手新闻报道**；涉及具体人物、案例与数字的表述，发布前须完成出处核查。

> ⚠️ 稿中 **Jason Zhu / 李明（删库）/ 工具清单与 star 数 /「11k star skill 挖矿」** 等，凡无一级或可靠二级来源佐证的，不得对外断定为事实；须在讲稿或 `review_record.md` 标注 ✅/⚠️/❌，必要时改为泛化表述或删除点名。

# 目标与非目标

## 目标

- [ ] 完成开放问题中的事实核查与出处归档。
- [ ] 维护 `production/content/01-script.md` 为主对白终稿；维护 `01-dialogue-volc.md`（`女：`/`男：` · **小夏→女、阿程→男**）供 [`skills/volc-podcast-tts`](../../../skills/volc-podcast-tts/SKILL.md) action=3。
- [ ] 维护约 1 分钟版 `01-script-short.md`（四类事故名、敏感案例谨慎表述、Jason Zhu / Governance 相关金句若保留须已核实、结尾「先安全再高效」）。
- [ ] 补全 `00-structure.md` 段落时长与翻页备注（单页口播建议 ≥20s）。
- [ ] 补全 `05-publish-kit.md` 各平台标题、简介、话题。
- [ ] 迭代 `production/slides/presentation.html` 与口播对齐，满足 `html-video-from-slides` 的 `#P`、`section.s.slide`、`go(n)` 契约。
- [ ] 双人音频：真人录制 **或** 火山播客 TTS 导出单条 `.wav` 至 `production/media/`（本地，不提交 Git）。
- [ ] `wav-auto` 或 `wav` + `wav-durations.json` 成片；字幕按 [`skills/srt-proofread`](../../../skills/srt-proofread/SKILL.md) 校对并积累 `srtReplacements`。

## 非目标

- 不修改 `repos/` 内业务仓库代码。
- 不在未核实前将二手叙述包装为「已证实新闻」。

# 用户与场景

技术内容创作者：中视频口播；观众为关注 Agent 工程化、安全与治理的开发者及技术管理者。

# 验收标准

- [ ] `production/` 骨架齐全（`content/`、`slides/`、`subtitles/`、`timing/`、`media/`、`tmp/`）。
- [ ] `production/content/` 下 **00-structure.md、01-script.md、01-dialogue-volc.md、01-script-short.md、05-publish-kit.md** 五文件齐备且与选题口径一致。
- [ ] `presentation.html` 可键盘翻页；成片配置与 `outputFile`、字幕策略一致。
- [ ] 敏感案例表述已通过核查或已降级为「传闻/讨论」类措辞。

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）：one-context
- **分支 / PR**：—
- **主要路径或模块**：`features/content-pipeline/ai-agent-security-2026-revelations-mid-video/production/`

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）：—
- **其他需求目录**：同类对白与流水线写法可参考 `features/content-pipeline/anthropic-boris-engineering-future-mid-video/`；Agent 安全/沙箱主题可参考 `features/content-pipeline/sandbox-agent-era-mid-video/`。

# 成片流水线（工具）

| 环节 | Skill / 命令入口 |
|------|------------------|
| 对白播客式 TTS（可选） | [`skills/volc-podcast-tts/SKILL.md`](../../../skills/volc-podcast-tts/SKILL.md) · action=3 |
| 幻灯与版式 | [`skills/html-deck-layout/SKILL.md`](../../../skills/html-deck-layout/SKILL.md) |
| HTML + WAV → MP4 | [`skills/html-video-from-slides/SKILL.md`](../../../skills/html-video-from-slides/SKILL.md) · `node cli.js wav-auto --project <production目录>` |
| 字幕校对 | [`skills/srt-proofread/SKILL.md`](../../../skills/srt-proofread/SKILL.md) |

# 开放问题（事实核查）

- **Jason Zhu**：在 X（或其他平台）的**可引用原帖或整理页**是否已保存？引语是否与上下文一致？
- **「李明 / `/var/data/` 生产库」等删库叙事**：是否存在可核验的公开一手来源？若无，对外口径是否已改为「未经核实的业界传闻」或删除点名？
- **「30 个工具、GitHub 总星 97.6k」** 及 **Agent Armor / Agent Governance Toolkit / Governor / Cordum** 等名称与数字是否与原文或官方仓库一致？
- **「11k star skill 挖矿」**：是否特指某一仓库？点名则须链接；否则是否已泛化表述？
- **四类事故分类**：是否为原创框架？若引用 OWASP / 厂商白皮书，是否已标注来源？
