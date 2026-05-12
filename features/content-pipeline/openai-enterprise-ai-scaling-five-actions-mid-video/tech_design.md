# 技术方案 — OpenAI 企业 AI 规模化落地五要点（中视频口播）

关联：`spec.md`

## 上下文与约束

内容型 feature：成片依赖 `skills/html-deck-layout`、`skills/html-video-from-slides`；无代码仓库实现分支。

## 方案概览

按「五要点」拆页 + 口播终稿；可选单人或双人播客体裁。

## 接口与数据

- 输入：`production/content/01-script.md`、`production/slides/presentation.html`、单一口播 `.wav`
- 输出：`production/media/*.mp4`（本地，默认不提交）

## 依赖与风险

- 案例与数字须与 [OpenAI 企业指南](https://openai.com/business/guides-and-resources/how-enterprises-are-scaling-ai/) 或可查证来源对齐。
- 微信转载文仅为叙事入口，不宜作为唯一事实来源。

## 迁移与回滚

不适用。
