# Features index

在新建或归档需求时更新本表。`id` 建议与目录名 `features/<category>/<feature-id>/` 中的 `<feature-id>` 一致（或与 `spec.md` frontmatter 的 `id` 一致）。


| id                            | title                                                 | category | status | path                                              | primary_repo_id |
| ----------------------------- | ----------------------------------------------------- | -------- | ------ | ------------------------------------------------- | --------------- |
| agent-framework               | 智能体框架 — meta/agents.yaml + 适配器扩展 + worktree/deploy 约定 | core     | done   | `features/core/agent-framework/`                  | one-context     |
| auto-context-compression      | 自动上下文压缩 — 定时扫描 knowledge/features 等，去重与去陈旧            | core     | draft  | `features/core/auto-context-compression/`         | one-context     |
| agent-collaboration           | 智能体协作增强 — 状态流转、决策手册、条件知识、生成保护                         | core     | draft  | `features/core/agent-collaboration/`              | one-context     |
| profile-inheritance           | Profile 继承与 Mixin 机制                                  | core     | draft  | `features/core/profile-inheritance/`              | one-context     |
| claudecode-source-analysis    | Claude Code 源码解析知识整理                                  | knowledge | done   | `features/knowledge/claudecode-source-analysis/`    | one-context     |
| openclaw-source-analysis      | OpenClaw 源码解析知识整理                                     | knowledge | done   | `features/knowledge/openclaw-source-analysis/`      | one-context     |
| claude-caveman-mode           | 用穴居人模式让 Claude 省 Token                                | experiments | done   | `features/experiments/claude-caveman-mode/`           | one-context     |
| math-teacher-ai-platform      | 数学教师 AI 工作台 — Phase 1 可视化资产化与 AI 出题 MVP          | products | draft  | `features/products/math-teacher-ai-platform/`      | FunctionCanvas  |
| one-context-intro-short-video | one-context 中视频介绍（爆款口播框架）                             | content-pipeline  | 发布  | `features/content-pipeline/one-context-intro-short-video/` | one-context     |
| hermes-agent-short-video      | Hermes Agent 短视频口播成片（wav-auto）                          | content-pipeline  | 发布  | `features/content-pipeline/hermes-agent-short-video/`      | one-context     |
| anthropic-agent-harness-narration | Anthropic Agent Harness 哲学 — 口播稿                         | content-pipeline  | 发布  | `features/content-pipeline/anthropic-agent-harness-narration/` | one-context |
| anthropic-ai-blueprint-dialogue-mid-video | Anthropic AI 公司蓝图对话拆解（中视频） | content-pipeline | 发布 | `features/content-pipeline/anthropic-ai-blueprint-dialogue-mid-video/` | one-context |
| anthropic-boris-engineering-future-mid-video | 当顶尖工程师不再写代码：AI 重写软件开发未来（对话口播） | content-pipeline | 发布 | `features/content-pipeline/anthropic-boris-engineering-future-mid-video/` | one-context |
| ai-agent-security-2026-revelations-mid-video | 2026 AI Agent 安全启示录（对话口播） | content-pipeline | 发布 | `features/content-pipeline/ai-agent-security-2026-revelations-mid-video/` | one-context |
| claude-code-multi-agent-source-mid-video | Claude Code 多 Agent 机制源码解读（中视频口播） | content-pipeline | 发布 | `features/content-pipeline/claude-code-multi-agent-source-mid-video/` | one-context |
| openai-enterprise-ai-scaling-five-actions-mid-video | OpenAI 企业 AI 规模化落地五要点（中视频口播） | content-pipeline | 发布 | `features/content-pipeline/openai-enterprise-ai-scaling-five-actions-mid-video/` | one-context |
| markdown-html-claude-engineer-mid-video | Markdown 要被淘汰？Claude 工程师弃用真相（阿哲 / 小夏 对话口播） | content-pipeline | 发布 | `features/content-pipeline/markdown-html-claude-engineer-mid-video/` | one-context |
| damai-ticket-bot              | 大麦抢票助手 — 浏览器插件 + CLI 集成 one-context skill                 | integrations | draft  | `features/integrations/damai-ticket-bot/`              | one-context     |
| operator-spaces-paper-analysis | 算子空间论文深度分析 — 发现证明漏洞与改进机会 | research | in_progress | `features/research/operator-spaces-paper-analysis/` | paperwork |
| skill-windows-c-drive-cleanup | Windows C 盘空间清理 — 仓库内 Agent Skill                     | core     | done   | `features/core/skill-windows-c-drive-cleanup/`    | one-context     |
| skill-merge-to-main           | 选择性合并到主干（Agent Skill）                                  | core     | done   | `features/core/skill-merge-to-main/`               | one-context     |
| unified-adapter-rules         | 统一适配器规则源 — 声明式 manifest，消除 PROFILE_RULES 重复          | core     | done   | `features/core/unified-adapter-rules/`            | one-context     |
| ai-mid-mgmt-video             | AI 中视频管理 — 素材与发布工具链                                       | content-pipeline  | 发布  | `features/content-pipeline/ai-mid-mgmt-video/`             | one-context     |
| hermes-adapter                | Hermes Adapter — one-context 支持 Hermes Agent CLI                     | core     | draft  | `features/core/hermes-adapter/`                   | one-context     |
| gsd-integration               | GSD 集成 — one-context 上下文注入 GSD 工作流                              | core     | draft  | `features/core/gsd-integration/`                  | one-context     |
| trend-radar-integration        | TrendRadar 趋势雷达集成 — 热点情报 + MCP + 微信推送                         | integrations | in_progress | `features/integrations/trend-radar/`      | trend-radar    |
| short-video-reporting-paradigm | 短视频式汇报范式 — 用内容创作思路重塑职场汇报                             | content-pipeline | 发布 | `features/content-pipeline/short-video-reporting-paradigm/` | one-context |
| hyperframes-video              | HyperFrames WAV-to-Video — HTML Native 动画视频制作技能（占位 feature）              | content-pipeline | draft | `features/content-pipeline/hyperframes-video/` | one-context |
| ai-sme-opportunity             | 放下大厂滤镜：中小厂的 AI 机会（中视频）                                              | content-pipeline | 发布 | `features/content-pipeline/ai-sme-opportunity/` | one-context |
| sandbox-agent-era-mid-video    | Agent时代下最被低估的技术——沙箱（中视频口播）                    | content-pipeline | 发布 | `features/content-pipeline/sandbox-agent-era-mid-video/` | one-context |
| deepseek-v4-deploy-guide-mid-video | DeepSeek V4 部署与调用指南（中视频）                        | content-pipeline | 发布 | `features/content-pipeline/deepseek-v4-deploy-guide-mid-video/` | one-context |
| agent亲和架构底层原理剖析 | Agent 亲和架构底层原理剖析（口播视频） | content-pipeline | 发布 | `features/content-pipeline/agent亲和架构底层原理剖析/` | one-context |
| 软件中一切皆Worker | 软件中一切皆 Worker（口播视频） | content-pipeline | 发布 | `features/content-pipeline/软件中一切皆Worker/` | one-context |
| claudecode-prompt-caching-mid-video | Prompt Caching Is Everything —— Claude Code 团队最新文章 | content-pipeline | 发布 | `features/content-pipeline/claudecode-prompt-caching-mid-video/` | one-context |
| claudecode-sandbox-concurrency-mid-video | Claude Code 沙箱与并发机制解析 | content-pipeline | 发布 | `features/content-pipeline/claudecode-sandbox-concurrency-mid-video/` | one-context |
| keycompute-ai-gateway-rust-mid-video | Rust 构建 AI 算力中枢：KeyCompute 架构解析（中视频） | content-pipeline | 开发中 | `features/content-pipeline/keycompute-ai-gateway-rust-mid-video/` | one-context |
| claude-code-large-codebase-mid-video | Claude Code 大型代码库最佳实践 —— Anthropic 博客深度解析 | content-pipeline | 开发中 | `features/content-pipeline/claude-code-large-codebase-mid-video/` | one-context |


**Columns**

- **primary_repo_id**: `meta/repos.yaml` 里条目的 `id`（或主实现仓库）；无则填 `—`。
- **path**: 相对 one-context 根目录的路径，用反引号包起来便于复制。
