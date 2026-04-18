# Karpathy 编程原则 → CLAUDE.md — 溯源参考

> 来源：[Andrej Karpathy 的编程经验被做成了 CLAUDE.md](https://mp.weixin.qq.com/s/85onPibogScWkEyfs1l3sQ) · 仓库 [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)
> 作者：Andrej Karpathy / forrestchang（整理）
> 发布日期：2026-04
> 收录日期：2026-04-12

---

## 1. 四条核心原则

| # | 原则 | 针对的问题 | 本项目已对应规则 |
|---|------|-----------|----------------|
| 1 | **先思考再编码** | 错误假设导致返工 | Architect/PM agent: "Always create a plan before making changes" |
| 2 | **简单优先** | 过度设计 | 多 agent: "prefer minimal, reversible changes" |
| 3 | **外科手术式修改** | 顺手"改进"相邻代码、注释、格式 | Dev agent: "Keep changes focused and scoped to the immediate task"；onecxt-hard-rules: ≤2 sentences |
| 4 | **目标驱动执行** | 模糊指令导致偏离 | 规格模板 spec.md / acceptance criteria |

---

## 2. 与本项目的关系

本项目的 agent profiles 与 standards 已将上述原则内化为行为约束，本文档仅作为**溯源参考**——记录"为什么这些规则存在"的原始出处。

不引入外部 CLAUDE.md 文件，避免与现有 onecxt adapter 体系冲突。

---

## 3. 原文关键摘录

- "Think before you code" — 让 AI 先输出分析和计划，再动手。
- "Simple is better" — 不引入不必要的抽象、配置项或兼容层。
- "Surgical changes only" — 只改必须改的行，不顺手润色、重构或加注释。
- "Goal-driven execution" — 把「添加验证」转化为「先写失败测试，再让测试通过」。