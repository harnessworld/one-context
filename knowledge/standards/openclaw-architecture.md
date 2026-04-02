# OpenClaw 源码架构解析

> 基于对 [OpenClaw](https://github.com/openclaw/openclaw) 项目源码及权威技术文章的系统性梳理，提炼出对 agent 建设有指导意义的架构模式和设计理念。

## 1. 项目概述

| 属性 | 说明 |
|------|------|
| **定位** | 开源、本地优先的个人 AI 助手/智能体平台 |
| **原名** | Clawdbot → Moltbot → OpenClaw |
| **技术栈** | TypeScript（90%+）、Node.js 24、pnpm、WebSocket |
| **许可证** | MIT |
| **活跃度** | 344K+ Star、68K+ Fork，每日发版（vYYYY.M.D 日历版本） |
| **口号** | "Your own personal AI assistant. Any OS. Any Platform." |

## 2. 核心架构

OpenClaw 采用 **Gateway 中心化控制面** 架构模式：

```
消息渠道 (WhatsApp/Telegram/Slack/Discord/微信/飞书/...)
               |
               v
        ┌─────────────┐
        │   Gateway    │  ← WebSocket 控制面 (ws://127.0.0.1:18789)
        │  (核心枢纽)   │
        └──────┬──────┘
               |
    ┌──────────┼──────────┬──────────┐
    v          v          v          v
 Pi Agent   CLI 工具   WebChat UI   设备节点
 (RPC 模式)                       (macOS/iOS/Android)
```

核心三层：
1. **Gateway 控制平面** — 会话/通道/工具/事件管理
2. **Agent 运行时** — Pi Agent RPC 模式，工具流式调用和块流式输出
3. **工具与技能层** — bundled/managed/workspace 三级技能体系

## 3. 模块划分

| 模块 | 职责 | 对 agent 建设的参考价值 |
|------|------|------------------------|
| `gateway/` | WebSocket 控制面，会话/通道/工具/事件管理 | **核心**：中心化调度器设计 |
| `agents/` | Agent 运行时 | **核心**：Agent 生命周期管理 |
| `channels/` | 24+ 消息渠道适配器 | 统一接口 + 适配器模式 |
| `sessions/` | 会话模型（主会话、群组隔离、激活模式） | 会话隔离与状态管理 |
| `routing/` | 消息路由（通道路由、多 Agent 路由） | 多 Agent 路由策略 |
| `plugins/` + `plugin-sdk/` | 插件系统 | 扩展机制设计 |
| `skills/` | 技能系统（bundled/managed/workspace） | 分层技能管理 |
| `mcp/` | MCP 协议支持 | 标准化工具协议 |
| `context-engine/` | 上下文引擎 | 上下文管理策略 |
| `flows/` | 工作流 | 任务编排 |
| `canvas-host/` | A2UI 可视化工作区 | Agent 驱动 UI |
| `security/` | DM 配对、权限控制 | 安全模型 |
| `node-host/` | 设备节点管理 | 分布式能力编排 |
| `media/` + `media-understanding/` | 媒体处理管线 | 多模态处理 |

## 4. 关键设计模式（对 agent 建设的启示）

### 4.1 Gateway 中心化控制面

**模式**：所有客户端通过单一 WebSocket 端点连接 Gateway，Gateway 负责会话管理、事件分发、工具调度。

**启示**：
- 解耦"控制面"与"执行面"，Gateway 不执行 AI 推理，只做路由和调度
- 所有 Agent 实例通过统一协议与 Gateway 通信，便于横向扩展
- 适用于需要管理多 Agent 实例的场景

### 4.2 多渠道适配器模式

**模式**：每个消息平台实现统一的 channel 接口。WhatsApp 用 Baileys、Telegram 用 grammY、Slack 用 Bolt、Discord 用 discord.js。

**启示**：
- 抽象统一的 Channel 接口，新平台只需实现适配器
- 消息格式标准化，上层业务逻辑与渠道解耦
- 可直接复用到我们的 agent 渠道接入层

### 4.3 Node 模式（设备节点）

**模式**：设备通过 `node.list` / `node.describe` / `node.invoke` 协议暴露本地能力（摄像头、屏幕录制、系统通知等），实现"Gateway 运行逻辑，设备执行动作"的分离。

**启示**：
- 能力注册 + 远程调用的解耦模式
- Agent 不需要知道能力的具体实现，只需要知道能力的描述
- 类似 MCP 的 tool 注册机制，可参考其发现协议（Bonjour/mDNS）

### 4.4 Pi Agent RPC 运行时

**模式**：Agent 以 RPC 方式运行，支持工具流式调用和块流式输出。

**启示**：
- Agent 运行时独立于 Gateway，可单独扩展和替换
- 流式输出支持中间结果反馈，提升用户体验
- RPC 模式便于多 Agent 实例并行运行

### 4.5 多 Agent 路由

**模式**：支持将不同通道/账号/对话路由到隔离的 Agent 实例（独立工作区 + 独立会话）。

**启示**：
- 每个 Agent 有独立的上下文和工作区，互不干扰
- 路由规则可基于通道、用户、话题等多维度
- Agent 间通过 `sessions_list` / `sessions_history` 协调工作

### 4.6 分层技能系统

**模式**：技能分为 bundled（内置）、managed（托管）、workspace（工作区级别）三层。

**启示**：
- 内置技能保证基础能力，托管技能支持社区扩展，工作区技能支持定制
- 技能安装门控 + UI 管理，控制技能的可用范围
- 类似我们的 knowledge/playbooks 分层思路

### 4.7 A2UI（Agent-to-UI）

**模式**：Agent 驱动的可视化工作区，支持 push/reset/eval/snapshot。

**启示**：
- Agent 不仅输出文本，还能驱动 UI 变化
- Canvas 模式让 Agent 具备可视化交互能力
- 适用于需要 Agent 展示结构化结果的场景

### 4.8 安全模型（DM Pairing）

**模式**：未知发送者需配对码验证，防止 prompt injection。

**启示**：
- 开放渠道下的 Agent 需要身份验证机制
- 防范外部消息对 Agent 的 prompt injection 攻击
- 安全边界应在渠道接入层就建立

## 5. 网络架构特色

OpenClaw 采用混合模式网络架构：

- **局域网**：Bonjour 协议（mDNS）实现设备自动发现
- **广域网**：Tailscale Serve/Funnel 实现安全穿透
- **模型认证**：OAuth vs API key 轮转 + 故障回退（Model Failover）

这种"即插即用"的网络设计值得 agent 平台参考，特别是在设备节点动态加入/退出的场景。

## 6. 参考资料

> 以下链接均经过搜索引擎交叉验证，确认可访问且内容与 AI 智能体平台 OpenClaw 相关。

### 权威技术解析（已验证）

| 文章 | 来源 | 重点内容 |
|------|------|---------|
| [OpenClaw 超完整解说：架构设计与智能体内核](https://zhuanlan.zhihu.com/p/2011197075765884377) | 知乎 | 混合模式架构、Gateway/Node 自动解析、Bonjour 协议 |
| [一文彻底搞懂 OpenClaw 的架构设计与运行原理（万字图文）](https://zhuanlan.zhihu.com/p/2010385772486878215) | 知乎 | 会话管理、记忆系统、工具权限控制、消息路由全景 |
| [目前最详细的 OpenClaw 工作原理解析](https://zhuanlan.zhihu.com/p/2002719503394567324) | 知乎 | 开源自托管 AI 代理网关定位、本地优先设计理念 |
| [万字解析 OpenClaw 源码架构 — 消息渠道集成简介](https://juejin.cn/post/7615828983318249522) | 稀土掘金 | 渠道插件 SDK + 运行时两层设计 |
| [万字解析 OpenClaw 源码架构 — 架构概览](https://juejin.cn/post/7615060828946169891) | 稀土掘金 | CLI 入口、引导向导、工作空间配置全流程 |
| [万字解析 OpenClaw 源码架构 — 工具与自动化](https://juejin.cn/post/7615466537084354611) | 稀土掘金 | 核心组件、依赖关系、性能考量 |
| [万字长文：OpenClaw 源码深度解析 — 架构设计与核心模块实现](https://juejin.cn/post/7622944302651047962) | 稀土掘金 | 会话管理、工具调度、技能引擎源码级分析 |
| [仅 4000 行代码复刻 OpenClaw 核心战力（Nanobot）](https://cloud.tencent.com/developer/article/2639516) | 腾讯云 | 香港大学精简实现，理解核心本质 |
| [通过 Nanobot 源码学习 OpenClaw 架构（1）总体](https://zhuanlan.zhihu.com/p/2021696771953313160) | 知乎 | 微内核架构 + 极致可读性的设计哲学 |

### 注意事项

网络上存在同名的 **OpenClaw 加密货币/区块链项目**，与本文讨论的 AI 智能体平台无关。Forbes、Yahoo Finance、KuCoin 等渠道的 OpenClaw 文章多指向加密项目，不在本知识范围内。

## 7. 架构适用场景分析

OpenClaw 的架构并非银弹。理解它**适合什么、不适合什么**，才能在我们的 agent 建设中做出正确的架构选型。

### 7.1 适合的场景

| 场景 | 为什么适合 | OpenClaw 中的体现 |
|------|-----------|------------------|
| **多渠道个人助手** | Gateway 中心化 + Channel 适配器天然支持"一个 Agent，多端接入" | 24+ 渠道（WhatsApp/Telegram/Slack/微信/飞书等）统一接入 |
| **单用户、长会话交互** | Session 模型围绕"一个用户的持续对话"设计，上下文引擎针对个人记忆优化 | main 会话 + 激活模式，DM Pairing 一对一认证 |
| **设备能力编排** | Node 协议让 Agent 可以调用分布在多个设备上的能力（摄像头、屏幕、文件系统） | macOS/iOS/Android 设备节点通过 list/describe/invoke 注册 |
| **本地优先 + 隐私敏感** | 数据不出本地网络，Gateway 运行在用户自己的设备上 | 局域网 mDNS 发现、Tailscale 安全穿透 |
| **技能/插件快速扩展** | 三级技能体系（bundled/managed/workspace）让社区和个人都能方便扩展 | 技能安装门控 + UI 管理 |
| **需要流式交互反馈** | Pi Agent RPC 模式原生支持工具流和块流式输出 | 实时打字效果、中间结果展示 |

### 7.2 不适合的场景

| 场景 | 为什么不适合 | 需要什么替代方案 |
|------|-------------|-----------------|
| **多租户 SaaS 平台** | Gateway 围绕单用户设计，没有租户隔离、配额管理、计费等 SaaS 基础设施 | 需要多租户控制面 + 独立 Agent 池 + 用量计量 |
| **高并发企业级服务** | 单 Gateway 实例是瓶颈，没有集群化、负载均衡的原生支持 | 需要无状态 Gateway 集群 + 分布式 Session 存储 |
| **复杂多 Agent 协作工作流** | 多 Agent 路由是"隔离"模式（各自独立工作区），缺乏 Agent 间的深度协作编排 | 需要 DAG 编排引擎、共享状态、任务拆分/汇聚机制 |
| **企业审计与合规** | 本地优先设计意味着日志、审计、数据留存不集中 | 需要集中式日志、操作审计、数据合规管控 |
| **离线/弱网环境** | 依赖 LLM API 调用，网络中断则 Agent 无法推理 | 需要本地小模型 fallback 或离线任务队列 |
| **纯后端自动化（无人值守）** | 围绕"对话"交互设计，不适合定时批处理、数据管道等无交互场景 | 需要任务调度框架 + 事件驱动架构 |

### 7.3 架构选型决策指引

根据你的 agent 建设目标，可以用以下决策树快速判断 OpenClaw 架构的适用程度：

```
你的 agent 需要面向终端用户对话交互吗？
├── 是 → 需要接入多个消息渠道吗？
│   ├── 是 → ★★★ 高度适合，直接参考 Gateway + Channel 适配器模式
│   └── 否 → ★★ 部分适合，可简化为单渠道 + Agent 运行时
├── 否 → 是后端自动化/工作流编排吗？
│   ├── 是 → ★ 不太适合，参考 DAG 编排框架（如 LangGraph、CrewAI）
│   └── 否 → 是多 Agent 深度协作吗？
│       ├── 是 → ★ 不太适合，OpenClaw 的多 Agent 是隔离模式而非协作模式
│       └── 否 → 需要具体场景具体分析
```

### 7.4 与我们 one-context 场景的对照

| one-context 特点 | OpenClaw 可借鉴 | OpenClaw 不适用 |
|-----------------|----------------|----------------|
| 多 Agent 角色协作（PM/Architect/Dev/QA/SRE） | 技能分层体系、Agent 运行时设计 | 隔离式多 Agent 路由（我们需要协作式） |
| 跨仓库工作（worktree 模式） | Node 模式的能力注册思路 | Gateway 单用户假设 |
| 知识驱动（knowledge/ 标准） | Context Engine 的上下文管理 | 面向对话的 Session 模型 |
| CLI + IDE 为主的交互 | Pi Agent RPC + 流式输出 | 多消息渠道适配器（我们不需要 WhatsApp 等） |

## 8. 对我们 agent 建设的核心建议

结合第 7 节的场景分析，以下是经过筛选的、与 one-context 多 Agent 协作场景真正匹配的借鉴方向：

**直接可借鉴（★★★）：**

1. **Agent 运行时 RPC 化**：参考 Pi Agent 的 RPC + 流式输出模式，让我们的 PM/Architect/Dev/QA/SRE Agent 各自独立运行，通过统一协议通信
2. **能力注册 + 发现机制**：参考 Node 模式的 list/describe/invoke 协议，结合 MCP 标准，让 Agent 动态发现和调用跨仓库的工具能力
3. **分层技能体系**：借鉴 bundled/managed/workspace 三级设计，对应我们的 knowledge/standards（内置）、knowledge/playbooks（托管）、workspace 级知识（定制）
4. **上下文引擎**：参考 Context Engine 的设计，优化我们 Agent 在长对话和跨会话场景下的上下文管理

**需改造后借鉴（★★）：**

5. **控制面/执行面分离**：Gateway 的解耦思路有价值，但需从"单用户多渠道路由"改造为"多 Agent 协作编排"——我们需要的是协作式调度器，而非隔离式路由器
6. **插件 SDK 两层设计**：渠道插件的"编译期 SDK + 运行时注入"模式可参考，但我们的扩展点是 Agent 角色和知识层，而非消息渠道

**不适用（★）：**

7. ~~多消息渠道适配器~~：我们以 CLI + IDE 为主，不需要 WhatsApp/Telegram 等适配器
8. ~~DM Pairing 安全模型~~：我们不面向开放消息渠道，不需要配对码验证
9. ~~单用户 Session 模型~~：我们需要多 Agent 共享状态，而非单用户会话隔离
