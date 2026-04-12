# Claude Code Source Analysis — 源码解析参考资料索引

> 本文档整理了关于 Claude Code 源码解析、架构分析的权威文章和资源，供 agent 框架建设参考。
> 更新日期：2026-04-02

---

## 一、官方资源（最高优先级）

### Anthropic 工程博客

| # | 标题 | 链接 | 核心主题 |
|---|------|------|----------|
| 1 | Building Effective AI Agents | https://www.anthropic.com/research/building-effective-agents | Agent 设计原则：简单可组合的模式优于复杂框架 |
| 2 | Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 上下文工程：如何为 agent 构建有效的上下文 |
| 3 | Writing effective tools for AI agents | https://www.anthropic.com/engineering/writing-tools-for-agents | 工具设计：有意义的上下文返回、token 效率优化 |
| 4 | Claude Code auto mode: a safer way to skip permissions | https://www.anthropic.com/engineering/claude-code-auto-mode | 权限模型：93% 的权限提示被批准，自动化决策设计 |
| 5 | How we built our multi-agent research system | https://www.anthropic.com/engineering/multi-agent-research-system | 多 agent 编排：启发式规则、工具匹配、意图对齐 |
| 6 | Introducing advanced tool use | https://www.anthropic.com/engineering/advanced-tool-use | 高级工具使用：动态发现、学习和执行工具 |
| 7 | Measuring AI agent autonomy in practice | https://www.anthropic.com/research/measuring-agent-autonomy | Agent 自主性度量：跨会话链接、端到端工作流可视化 |

### 官方文档与仓库

| # | 标题 | 链接 | 说明 |
|---|------|------|------|
| 8 | How Claude Code works | https://code.claude.com/docs/en/how-claude-code-works | Agent 循环由推理模型 + 工具两个核心组件驱动 |
| 9 | Best Practices for Claude Code | https://code.claude.com/docs/en/best-practices | Anthropic 内部验证的有效模式 |
| 10 | anthropics/claude-code (GitHub) | https://github.com/anthropics/claude-code | 完整开源仓库 |
| 11 | Tool use with Claude (API Docs) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | 工具使用基础文档 |

---

## 二、英文深度分析

| # | 标题 | 作者/平台 | 链接 | 核心主题 |
|---|------|-----------|------|----------|
| 12 | How Claude Code is built | Gergely Orosz / Pragmatic Engineer | https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built | 整体架构、发展历史 |
| 13 | Claude Code Architecture (Reverse Engineered) | Vikash Rungta / Substack | https://vrungta.substack.com/p/claude-code-architecture-reverse | 五个核心设计支柱、架构逆向 |
| 14 | Everyone Analyzed Features, Nobody Analyzed Architecture | Medium / Data Science Collective | https://medium.com/data-science-collective/everyone-analyzed-claude-codes-features-nobody-analyzed-its-architecture-1173470ab622 | 50 万行源码的架构解析 |
| 15 | Anatomy of a Claude Code Session | Code with Mukesh | https://codewithmukesh.com/blog/anatomy-claude-code-session/ | 会话生命周期、agent loop 执行流 |
| 16 | Under the Hood of Claude Code | Medium / @yuxiaojian | https://medium.com/@yuxiaojian/under-the-hood-of-claude-code-its-not-magic-it-s-engineering-e1336c5669d4 | 核心迭代循环、工程基础 |
| 17 | Claude Code Agent — Complete Architecture Deep Dive | GitHub Gist / yanchuk | https://gist.github.com/yanchuk/0c47dd351c2805236e44ec3935e9095d | 核心循环、内存系统、编排、权限、UI |
| 18 | Deep Dive into AI Coding Agent Architecture | Redreamality | https://redreamality.com/blog/claude-code-source-leak-architecture-analysis/ | 多端支持、桥接层架构分层 |
| 19 | Context Engineering & Reuse Pattern | Hugging Face Blog | https://huggingface.co/blog/kobe0938/context-engineering-reuse-pattern-claude-code | 上下文管理、内存重用模式 |
| 20 | Agent design lessons from Claude Code | Jannes Klaas | https://jannesklaas.github.io/ai/2025/07/20/claude-code-agent-design.html | 长会话支持、工具设计经验 |
| 21 | Tools and system prompt of Claude Code | GitHub Gist / armstrongl | https://gist.github.com/armstrongl/7320839f0da33308c6335fee905f1d42 | 11 个内置工具、系统提示词全文 |

---

## 三、中文深度分析

| # | 标题 | 平台 | 链接 | 核心主题 |
|---|------|------|------|----------|
| 22 | Claude Code 源码深度解析 | 知乎 | https://zhuanlan.zhihu.com/p/2022442135182406883 | Agentic Loop 五步流水线、上下文压缩、四层安全防御 |
| 23 | Claude Code 架构全解密 | 知乎 | https://zhuanlan.zhihu.com/p/2022378958767887638 | "工具即能力"设计理念、权限分层 |
| 24 | 51万行代码裸奔之夜：源码深度拆解 | 腾讯云 | https://cloud.tencent.com/developer/article/2648751 | 完整工作机制、构建配置实践 |
| 25 | 五大核心机制与实战心法 | 博客园 | https://www.cnblogs.com/jeecg158/p/19712242 | 五大核心机制协同、实战应用 |
| 26 | learn-claude-code: The Agent Loop | 腾讯云 | https://cloud.tencent.com/developer/article/2634424 | ReAct 范式、核心 30 行代码实现 |
| 27 | Agent 进化：从 Workflow 到 While Loop | CSDN | https://adg.csdn.net/695337e85b9f5f31781be26b.html | 范式演进、"大模型+简单架构"哲学 |
| 28 | Claude Code Agent Teams 运行机制深度分析 | 知乎 | https://zhuanlan.zhihu.com/p/2011414794905859760 | Subagent 瞬时子进程、上下文隔离 |
| 29 | Tool 设计要高度服务于 Agent 决策 | 知乎 | https://zhuanlan.zhihu.com/p/1910264332509516608 | 工具参数设计、决策支撑原则 |
| 30 | Claude Code 系统提示词和 11 个内置 Tool 拆解 | 53AI | https://www.53ai.com/news/LargeLanguageModel/2025032089304.html | 系统提示词全文、工具生态 |
| 31 | 用上下文工程来实现 SubAgent | 知乎 | https://zhuanlan.zhihu.com/p/1948151539949601997 | Subagent 实现几乎完全依赖提示词工程 |
| 32 | 发现它好用的秘密藏在反常识的 Agent 设计里 | 知乎 | https://zhuanlan.zhihu.com/p/1943399204027373513 | 系统提示词 2800 tokens、启发式规则 |
| 33 | 基于抓包数据逆向分析工作机制 | 博客园 | https://www.cnblogs.com/noonafter/p/19729742 | 网络协议层分析、渐进式披露机制 |
| 34 | 沙箱隔离减少 84% 中断确认请求 | 腾讯云 | https://cloud.tencent.com/developer/article/2595615 | 沙箱设计、权限请求优化 |

---

## 四、开源研究项目

| # | 项目 | 链接 | 说明 |
|---|------|------|------|
| 35 | ThreeFish-AI/analysis_claude_code | https://github.com/ThreeFish-AI/analysis_claude_code | Claude Code v1.0.33 逆向工程分析资料库 |
| 36 | learn-claude-code（14.4k star） | https://github.com/anthropics/courses （待确认具体仓库地址） | Agent Loop 最小可行实现、v1_basic_agent.py |

> **注意**：本索引中的链接来自 AI 搜索引擎汇总，部分 URL（尤其知乎长 ID、CSDN adg 链接）可能已失效。使用前建议验证链接有效性。
