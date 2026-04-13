# 素材与链接

## 叙事参考（非产品事实源）

| 内容 | 说明 |
|------|------|
| 行业长文（场景 + 金句节奏） | 姚琪琳 [《AI时代，我想把所有人拉进同一个代码仓库》](https://mp.weixin.qq.com/s/ftpGWAgtShMNUXSigSy_Hg) — 口播若化用其中比喻，**简介/置顶注明出处**；见 [`04-style-reference.md`](04-style-reference.md) |

## 权威事实（口播核对）

| 内容 | 路径或说明 |
|------|------------|
| 产品总览 | 仓库根 [`README.md`](../../../../README.md) |
| CLI 安装 | [`packages/one-context/README.md`](../../../../packages/one-context/README.md) |
| 架构补充 | [`docs/architecture.md`](../../../../docs/architecture.md) |

## 对外链接（评论区 / 简介）

| 用途 | URL |
|------|-----|
| 主仓库 | `https://github.com/harnessworld/one-context` |
| Issues | `https://github.com/harnessworld/one-context/issues` |

## 安装口令（口播用）

```bash
pip install -e ./packages/one-context
onecxt doctor
```

（开发测可带 `[dev]`，口播面向普通用户时只说可编辑安装或 `pip install one-context` 若已发 PyPI —— **以实际发布方式为准**。）

## 可选协作仓

- VideoFactory：`meta/repos.yaml` → `id` 与 `url` 对应 [CarmanMS/VideoFactory](https://github.com/CarmanMS/VideoFactory)；本地路径默认 `repos/develop/VideoFactory`。

## 评论区置顶文案（草稿）

```
开源：github.com/harnessworld/one-context（MIT）
安装：克隆后 pip install -e ./packages/one-context，再 onecxt doctor
Cursor、Claude Code、OpenClaw 等名为各自权利人商标，与本项目无关。
```

## 封面 / 标题备选（待选）

- 标题：见 `00-brief.md` 工作标题
- 封面文案：可拆「多工具 / 多仓库 / 一处定义」三行之一作为主视觉
