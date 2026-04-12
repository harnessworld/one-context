# 发布素材包 — one-context 中视频

> 与口播事实一致，发布前请对照 [`01-timeline-and-script.md`](01-timeline-and-script.md) 核对清单；对外链接见 [`03-assets-and-links.md`](03-assets-and-links.md)。

## 成片元信息

| 项 | 内容 |
|----|------|
| 产品 | **one-context** — 跨仓库 AI 协作与共享上下文层，本地优先、MIT |
| 形式 | 双人问答口播 + 录屏 + 花字，约 **3 分 20 秒** |
| 主仓库 | https://github.com/harnessworld/one-context |
| Issues | https://github.com/harnessworld/one-context/issues |

## 一句话与记忆点（全平台通用）

- **一句话：** 多仓、多 AI 工具别再各抄一遍规范 —— **一处定义，处处同步**；one-context 用伞形仓把 registry、知识、需求链收成 **共享上下文层**。
- **记忆点（可上封面/角标）：** 「一处定义，处处同步」「共享上下文层（不是又一个模型）」

## 标题备选

| 场景 | 文案 |
|------|------|
| 工作标题（长） | 用 AI 写代码的人都踩过这些坑，这个开源项目一次全解决 |
| 抖音 / 视频号（短，≤30 字内优先） | 多工具多仓库，规范别抄三遍｜one-context |
| 抖音 / 视频号（情绪向） | 个人写代码快了，仓和仓的缝却裂开了？ |
| B站（信息密度） | 【开源】one-context：共享上下文层，Cursor/Claude 规范一次同步 + 跨仓 Workspace |
| 干货向 | 3 分钟看懂：umbrella + onecxt adapt，多端配置从「打地鼠」到一条命令 |

## B站 — 简介（可整段粘贴）

```
多工具、多仓库一起用 AI 时，规范抄 N 遍、跨仓上下文断档、方案写着写着变改码——这些结构性问题，单靠「换模型」解决不了。

one-context（MIT）在伞形仓里维护 meta、knowledge、features 等权威清单，用本地 CLI「onecxt」做适配与校验：同一套语义生成 Cursor / Claude Code / OpenClaw 等原生配置（onecxt adapt），跨仓任务用 workspaces + onecxt sync，还可 onecxt context export 打包上下文。6 个标准智能体角色 + owns，把需求链和产物分工写清楚；knowledge/ + onecxt doctor 减少知识漂移。

仓库：github.com/harnessworld/one-context
安装：克隆后 pip install -e ./packages/one-context，再 onecxt doctor

本期口播中若出现「高速公路 / 乡间小道」等场景化比喻，叙事节奏参考：姚琪琳《AI时代，我想把所有人拉进同一个代码仓库》（微信公号文），非产品事实源；产品细节以仓库 README 为准。

Cursor、Claude Code、OpenClaw 等名为各自权利人商标，与本项目无关。
```

## B站 — 章节时间轴（可选，复制到「笔记/章节」）

| 时间 | 章节 |
|------|------|
| 0:00 | 开场：工具新，管道旧？ |
| 0:30 | 写一次处处同步 · onecxt adapt |
| 1:08 | 跨仓 Workspace · 不必物理 monorepo |
| 1:42 | 6 角色 · owns · features 文档链 |
| 2:18 | knowledge 层 · knowledge-keeper · doctor |
| 2:42 | 轻依赖 · 本地优先 |
| 3:00 | 总结与开源地址 · 下期预告 |

## 抖音 / 视频号 — 短简介（≤300 字示例）

```
one-context：开源共享上下文层。规范写在 umbrella（meta/knowledge），onecxt adapt 一次生成各 AI 工具配置；多仓用 workspaces + sync，不必硬并 monorepo。6 角色 + features 链控越权，doctor 校验。MIT｜github.com/harnessworld/one-context

安装：pip install -e ./packages/one-context → onecxt doctor

比喻出处见 B 站长简介；商标归各自权利人。
```

## 话题与标签建议

**抖音 / 视频号话题（按平台可选 3～5 个）：**  
`#程序员` `#开源` `#AI编程` `#Cursor` `#ClaudeCode` `#微服务` `#团队协作`

**B站标签：**  
开源, AI编程, Cursor, Claude Code, 软件开发, 微服务, 上下文工程, Python, CLI

**检索用英文（简介末尾或小字）：**  
one-context, umbrella repo, onecxt adapt, workspace, context export

## 置顶评论（可直接发）

```
开源：github.com/harnessworld/one-context（MIT）
安装：克隆后 pip install -e ./packages/one-context，再 onecxt doctor
Cursor、Claude Code、OpenClaw 等名为各自权利人商标，与本项目无关。
```

## 封面文案（三行择一主视觉）

1. **多工具 / 多仓库 / 一处定义**  
2. **共享上下文层**（副标：不是又一个模型）  
3. **onecxt adapt · 写一次处处同步**

## 发布前检查

- [ ] 简介或置顶已写清仓库与安装方式；许可证 **MIT**  
- [ ] 未写「靠 MCP 协议做多端适配」（事实以 [`01-timeline-and-script.md`](01-timeline-and-script.md) 为准）  
- [ ] 智能体数量：**6**；命令：**onecxt**；仓库：**harnessworld/one-context**  
- [ ] 若成片使用姚文类比，简介中已 **注明参考出处**（链接见 [`03-assets-and-links.md`](03-assets-and-links.md)）  
- [ ] 商标免责声明已带（评论区或简介末行）

## 素材路径提示（本仓）

| 用途 | 路径（相对本 feature） |
|------|-------------------------|
| 成片 | `production/final_auto.mp4`（以实际导出文件名为准） |
| 工程说明 | `production/VIDEO-BUILD.md` |
| 封面（已定稿标题） | `videos/cover.png`（1080×1920）；版式源 `cover.html`，重生成：`npm install` 后 `node gen_cover.js` |

---

*文档随审片与平台规则迭代；改标题或简介时同步更新本节与 `03-assets-and-links.md` 封面备选。*
