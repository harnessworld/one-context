# one-context 中视频介绍 — 制作入口

本目录是伞形需求 **`one-context-intro-short-video`** 的根，约定见 [`spec.md`](spec.md)。

## 目录

| 路径 | 说明 |
|------|------|
| [`spec.md`](spec.md) | 需求范围、验收、与 VideoFactory 的关系 |
| [`production/README.md`](production/README.md) | 制作框架说明（读这个开始干活） |
| [`production/00-brief.md`](production/00-brief.md) | 定位、时长、角色、记忆点 slogan |
| [`production/01-timeline-and-script.md`](production/01-timeline-and-script.md) | 分段时间轴 + 台词表（随审片迭代） |
| [`production/02-shots-checklist.md`](production/02-shots-checklist.md) | 镜头 / 录屏 / B-roll 清单 |
| [`production/03-assets-and-links.md`](production/03-assets-and-links.md) | 引用文档、仓库链接、封面与评论区文案 |
| [`production/04-style-reference.md`](production/04-style-reference.md) | 对标长文叙事手法与 one-context 边界（勿与物理 monorepo 混谈） |
| [`production/05-publish-kit.md`](production/05-publish-kit.md) | **发布素材**：各平台标题、简介、话题、置顶评论、章节轴、检查清单 |
| [`skills/html-video-from-slides/`](../../../skills/html-video-from-slides/) | **HTML 幻灯 → MP4** 单入口（Cursor / Claude Code / OpenClaw 共用） |
| [`production/VIDEO-BUILD.md`](production/VIDEO-BUILD.md) | **HTML → MP4**（调用 [`skills/html-video-from-slides/`](../../../skills/html-video-from-slides/)） |

## 与 VideoFactory 的关系

`meta/repos.yaml` 已登记 [VideoFactory](https://github.com/CarmanMS/VideoFactory)。本地执行 `onecxt sync VideoFactory` 后，可在 `repos/develop/VideoFactory/` 中放置工程文件、Premiere / 剪映工程或导出目录；**权威口播与事实核对仍以本 umbrella 仓库为准**（避免子仓长期漂移）。
