# Anthropic Managed Agents & Trustworthy Agents

> 来源：[Managed Agents: Decoupling the Brain from the Hands](https://www.anthropic.com/engineering/managed-agents) / [Trustworthy Agents in Practice](https://www.anthropic.com/research/trustworthy-agents)
> 作者：Anthropic Engineering
> 发布日期：2025 / 2026-04-09
> 收录日期：2026-04-12

两篇互补的 Anthropic 官方博客：一篇讲 Agent 架构拆分（怎么造），一篇讲 Agent 信任框架（怎么管）。合在一起是当前最完整的 Agent 基础设施设计参考。

## Part 1: Managed Agents — 脑手分离

### 核心架构：三层解耦

| 层 | 职责 | 关键属性 |
|---|---|---|
| **Session** | Append-only event log，记录 Agent 所有行为 | 持久化，不在容器内；容器死了日志还在 |
| **Harness** | 调用 Claude、路由 tool call、管理上下文 | **无状态**；所有状态从 Session 读取 |
| **Sandbox** | 代码执行、文件编辑环境 | **隔离**；碰不到凭证和敏感数据 |

### 接口抽象

三层之间通过接口约定通信，具体实现可替换：

- `execute(name, input) → string` — Harness 调用 Sandbox
- `provision({resources})` — 初始化新 Sandbox
- `wake(sessionId)` — 恢复 Harness
- `getSession(id)` — 读取事件日志
- `emitEvent(id, event)` — 持久化事件

> 接口比实现更持久，类似 OS 虚拟化硬件：`read()` 不关心背后是磁盘还是 SSD。

### 宠物 → 牲口

旧架构（所有组件塞单容器）= 宠物：不可替代，挂了得抢救。
新架构（Harness 无状态 + Session 外置）= 牲口：随时杀掉重建，`wake(sessionId)` 恢复。

### 性能收益

- **p50 首 Token 延迟（TTFT）下降 ~60%**
- **p95 TTFT 下降 >90%**
- 原因：推理不再等容器配置完成，拿到 Session ID 即可开始

### 安全设计

- **凭证永远不进 Sandbox**：Git token 在初始化时注入 local git remote（push/pull 无需接触 token）；OAuth token 留在外部 vault，通过 MCP 代理访问
- Prompt injection 即使成功也偷不到钥匙
- 攻破 Sandbox ≠ 拿到凭证

### Harness 演化观

Harness 编码的是"Claude 自己做不了什么"的假设，但这些假设会随模型升级变得过时。例如 context resets 对 Claude Opus 4.5 已成 dead weight。所以接口要稳定，实现要可换。

---

## Part 2: Trustworthy Agents — 信任框架

### Agent 四层模型

| 层 | 说明 | 风险面 |
|---|---|---|
| **Model** | 智力来源 | 核心能力，单代际可显著改变 Agent 能力 |
| **Harness** | 指令 + 护栏 | 配置不当可被利用 |
| **Tools** | 可调用的服务/应用 | 权限过宽是常见漏洞 |
| **Environment** | 运行环境与数据访问 | 不同环境风险等级不同 |

> 四层都要做安全，只管模型不够。

### 五大信任原则

1. **人类控制** (Human Control)
2. **价值对齐** (Alignment with Human Values)
3. **安全交互** (Secure Interactions)
4. **透明度** (Transparency)
5. **隐私保护** (Privacy)

### Plan Mode — 战略审批 vs 逐步审批

传统：每步操作需用户确认 → 微观管理，效率低，用户可能疲劳忽略提示。
Plan Mode：Agent 先展示完整行动计划 → 用户审方向，不审每步细节 → 从微观管理变为目标管理。

### Prompt Injection 纵深防御

| 层 | 措施 |
|---|---|
| 训练 | 教 Claude 识别恶意指令 |
| 生产 | 实时流量监控 |
| 外部 | 红队持续测试 |
| 架构 | Sandbox 凭证隔离（见 Part 1） |

### 关键洞察

- **护栏悖论**：Agent 越快，护栏越重要。两篇文章合在一起就是这个悖论的工程实现。
- Harness 正从应用层沉入基础设施层，类比云计算演进：自建服务器 → EC2 → Lambda。
- MCP 捐给 Linux 基金会的 Agentic AI Foundation：当 Agent 变成牲口，接口就得变成标准件。