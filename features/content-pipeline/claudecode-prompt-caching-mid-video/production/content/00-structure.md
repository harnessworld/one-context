# 话题大纲

<!-- 视频的话题拆分、每段核心要点、预计时长 -->

总目标：5–8min 中视频深度解析，面向 AI Infra / Agent 工程师
风格：干货讲解 + 关键截图辅助，不引入无关信息

---

## 1. 开场钩子（0:00–0:40）
- **画面建议**：原文《Lessons from building Claude Code: Prompt caching is everything》截图
- **核心钩子**：Anthropic 宣布 prompt caching 直接导致 Claude Code 的成本和延迟下降一个数量级——团队甚至把缓存命中率当成 SEV 来处理
- **问题提出**：如果你正在做长上下文 Agent，没有 caching，你的产品从经济模型上就是不可持续的

## 2. 缓存的底层机制：前缀匹配（0:40–1:20）
- **配图**：Lay out your prompt for caching.png
- **要点**：API 的缓存是「前缀匹配」——从最开头到 `cache_control` 断点之间的内容被缓存
- **`任何前缀变动 = 整段失效`**：顺序就是架构，不是优化

## 3. 提示结构：从静态到动态（1:20–2:20）
- **配图**：Lay out your prompt for caching.png（复用，逐层讲解）
- **讲解 Claude Code 的五层提示结构**（从上到下缓存范围递减）：
  1. Base System Instructions → 全局缓存
  2. Tools 定义 → 全局缓存
  3. CLAUDE.md & Memory → 项目级缓存
  4. Session State → 会话级缓存
  5. Messages → 逐轮增长（唯一动态部分）
- **关键教训**：静态前置，动态后置。把变化的塞到底部

## 4. 用 message 做更新，不要碰系统提示（2:20–3:00）
- **反直觉点**：信息过时了（时间戳变了、文件改了），第一反应是改系统提示——但那样 cache miss，代价高昂
- **正确做法**：通过 message 传递更新，Claude Code 用 `<system-reminder>` 标签在下一轮注入新信息
- **类比**：你不需要拆掉承重墙，只需要贴一张便签

## 5. 不要在中途换模型或工具（3:00–4:00）
- **模型切换陷阱**：缓存是模型绑定的。100k token 的 Opus 缓存，换 Haiku 反而更贵——因为全部缓存作废
- **工具切换陷阱**：工具定义属于前缀，加减工具 = 整个会话缓存失效
- **Plan Mode 的缓存友好设计**：不是缩小工具集，而是把 `EnterPlanMode` 做成一个工具本身，所有工具始终在场，只有 message 变
- **defer_loading 模式**：几十个 MCP 工具不现实，保留 stubs（轻量签名），实际 schema 延迟加载

## 6. Compaction 的致命陷阱与正确做法（4:00–5:20）
- **配图**：Compacting without breaking the cache.png
- **陷阱**：用不同系统提示做总结调用 → 前缀完全不同 → 全部不命中 → 反而支付全额费用
- **正确做法：cache-safe forking**
  - 复用**完全相同**的系统提示、工具、会话上下文
  - 将 compaction prompt 作为**新的 user message** 追加到末尾
  - 这样 API 视角几乎完全匹配父会话，前缀复用，仅支付新 token 成本
- **代价**：需要预留 compaction buffer（窗口空间给总结输出）
- **结论**：总结一次的成本可以降到 1/10

## 7. Lessons Learned 总结（5:20–6:20）
- **设计原则**：整个系统围绕前缀匹配约束设计
- **更新原则**：用 message 替代系统提示变更
- **状态原则**：用工具建模状态（如 plan mode），不换工具集或模型
- **监控原则**：缓存命中率 = 运营核心指标（类似 uptime）
- **总结**：Prompt caching 从 day one 就必须是架构基础，不是上线后的补丁

## 8. 收束与 CTA（6:20–6:50）
- **收束**：如果你的 Agent 还没把 caching 当架构设计，现在是最佳启动时机
- **关联 one-context 实践**：CLADE.md 分层 + agents 分层 + features 分层，天然就是缓存友好的提示结构
- **CTA**：欢迎在评论区分享你项目的缓存策略，或留言想听的其他主题

---

## 视频资产mapping

| 时间点 | 画面/配图 | 说明 |
|--------|----------|------|
| 0:00–0:40 | 原文标题页 | 锚定出处 |
| 1:20–2:20 | 图1：Lay out your prompt for caching.png | 提示结构分层解读 |
| 4:00–5:20 | 图2：Compacting without breaking the cache.png | 三步总结对比，配合 schema 讲解 |

## 字幕/章节轴

```
0:00  开场：Caching 是 Agent 产品的经济底盘
0:40  前缀匹配机制
1:20  五层提示结构
2:20  用 message 做更新，别碰系统提示
3:00  不要中途换模型或工具
4:00  Compaction 的正确做法
5:20  七条经验总结
6:20  收束：从你的架构 day one 就开始
```
