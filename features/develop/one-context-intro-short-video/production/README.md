# 制作框架说明

## workflow

1. **00-brief** — 确认平台、时长、人设、是否微调 slogan；不改则作为唯一 brief。
2. **01-timeline-and-script** — 按秒迭代台词；改一句就同步总时长（目标 **200s**）。
3. **02-shots-checklist** — 每段台词勾对应镜头：真人 / 录屏 / 图示 / 花字。
4. **03-assets-and-links** — 录屏命令、README 引用段落、GitHub 链接、评论区置顶文案。
5. **04-style-reference** — 叙事手法对标与合规（化用外部文章时注明出处）。
6. **出片** → 使用 **`skills/html-video-from-slides/cli.js`**；优先 **`wav-auto`**（仅 HTML + 单个 WAV，自动对齐）；见 [`VIDEO-BUILD.md`](VIDEO-BUILD.md)。
7. 定稿后 → 可在 `repos/develop/VideoFactory` 建子目录，仅放素材与配置，**仍通过 `--project` 指向该目录调用 CLI**。

## 事实源（口播必查）

- 根目录 [`README.md`](../../../../README.md)
- 智能体为 **6** 个：`pm`, `architect`, `dev`, `qa`, `sre`, `knowledge-keeper`
- 核心 CLI：`onecxt doctor | sync | adapt | context export`
- **不要**把多端适配说成 **MCP**：适配是 `onecxt adapt` + 适配器**生成配置文件**，见 `01-timeline-and-script.md` 顶部「事实澄清」。

## 文件状态

| 文件 | 状态 |
|------|------|
| 00-brief | 已填骨架，可改 |
| 01-timeline-and-script | **已定稿主台词**（200s）；审片可微调 |
| 02-shots-checklist | 模板待勾 |
| 03-assets-and-links | 链接已填；评论区置顶文案可补 |
| 04-style-reference | 已填：对标姚文 + 与 monorepo 边界 |
| VIDEO-BUILD | 已对齐仓库 [`skills/html-video-from-slides/`](../../../../skills/html-video-from-slides/) |
