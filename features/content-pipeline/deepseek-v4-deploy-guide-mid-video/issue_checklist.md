# Issue Checklist — 口播稿评审

## 评审对象

- `features/content-pipeline/deepseek-v4-deploy-guide-mid-video/production/content/01-script.md`

---

## P0 阻塞（不改不能录制）

| # | 问题 | 位置 | 修改方向 | 负责 | 状态 |
|---|------|------|---------|------|------|
| P0-01 | 开场 Hook 失败："真的很碎"太软，没有冲击力 | 00 开场第 1 句 | 换成方案 C 故事代入型：朋友八卡 A100 tensor 并行 latency 比四卡还高的故事 | 作者 | resolved |
| P0-02 | 结尾 CTA 模板化："点个赞"是 2019 年范式，和目标受众不匹配 | 04 总结段 | 换成"打开你的 vLLM 配置对照三条检查清单，今晚就能少改一轮配置" + 下期预告钩子（INT8 比 FP8 还慢） | 作者 | resolved |
| P0-03 | 关键模糊表述："月调用量超过一定规模"没有量化 | 02.1 部署路径 | 补充基于成本的估算规则：月费用 ≈ 一张 A100 80G 月租时为经济拐点 | 作者 | resolved |
| P0-04 | 不确定参数名直接给出："enable_thinking"加括号说"可能微调"会让观众困惑 | 03.1 API 调用方式 | 改成确定性表述：推理模式显式开关默认关闭，目前叫 `enable_thinking`，即便改名逻辑不会变 | 作者 | resolved |

---

## P1 必须改（不改影响质量）

| # | 问题 | 位置 | 修改方向 | 负责 | 状态 |
|---|------|------|---------|------|------|
| P1-01 | "视频分两段"占用开场黄金时间 | 00 开场段 | 删除，开场直接进入故事 + 决策图承诺，受众切分移到 01 节尾 | 作者 | resolved |
| P1-02 | 02.1 四种路径节奏太平，平均用力导致疲劳 | 02.1 段 | 重构为三层递进（L0 API → L1 Docker → L2 Docker+vLLM），量化画成叠加开关 | 作者 | resolved |
| P1-03 | temperature 建议给出具体数字（0.8→0.6）但没有足够依据 | 03.2 传参段 | 改成场景化区间：代码推理 0.0-0.3、对话 0.5-0.7、创意 0.8-1.2 | 作者 | resolved |
| P1-04 | HTTP 429/503 解释对开发者是冗余常识 | 03.2 传参段 | 各一句话带过，保留 Context length exceeded | 作者 | resolved |
| P1-05 | 运维篇缺少部署后监控/告警的引导 | 02.3 末尾 | 增加"部署后第一小时检查清单"（GPU util ≥80%、alloc vs reserved、P99 SLA） | 作者 | resolved |
| P1-06 | 02.2 四个概念平均用力，第四个（max_model_len）观众可能已走神 | 02.2 核心概念 | max_model_len 保留但简化表述；tensor 并行去掉技术黑话、补硬数字 | 作者 | resolved |
| P1-07 | 调用篇缺最小可运行代码示例 | 新增 03.2 段落 | 增加了从 `import openai` → `usage` 解析的完整 Python 示例（含 enable_thinking 注释） | 作者 | resolved |
| P1-08 | reasoning tokens 计费逻辑没有可执行指导 | 03.4 V3 差异 | 解释了 `total_tokens` 含 reasoning、`completion_tokens` 不含，并给出 billing 兜底代码 | 作者 | resolved |
| P1-09 | stop_reason 没有给出具体枚举值 | 03.4 V3 差异 | 列出具体值（stop / eos / completed），建议 `in [...]` 兜底 | 作者 | resolved |

---

## P2 建议改（改了更舒服）

| # | 问题 | 位置 | 修改方向 | 负责 | 状态 |
|---|------|------|---------|------|------|
| P2-01 | 调用篇 01 认识 V4 对开发者前置铺垫太长 | 01 认识 V4 | 增加"对开发来说，这三件事对应三个你要调的参数" | 作者 | resolved |
| P2-02 | streaming SSE "格式偏差"警告是虚警 | 03.3 传参段 | 完全删除，将 streaming 改为代码示例中的自然提及 | 作者 | resolved |
| P2-03 | Docker 并发上限"几十个 vs 几百个"太粗略 | 02.1 Docker 段 | 给出 A100 80G 裸跑约 10~20 并发的参考数字 | 作者 | resolved |
| P2-04 | 长上下文后半段是老生常谈的 prompt engineering | 03.3 传参段 | 压缩为一句"长上下文的使用技巧跟其它模型一样，核心信息放首尾" | 作者 | resolved |
| P2-05 | temperature 建议覆盖不同场景 | 03.3 传参段 | 按场景给出区间建议（代码推理 0.0-0.3、对话 0.5-0.7、创意 0.8-1.2） | 作者 | resolved |

---

## 后续追踪

- [ ] 作者根据 Issue Checklist 逐条修改后，标记为 resolved
- [ ] 修改完成后，启动第二轮 review 确认 P0 + P1 全部关闭
