# 话题大纲

<!-- 视频的话题拆分、每段核心要点、预计时长 -->

## 开场（~1min）

- 痛点引入：多 LLM Provider 统一接入、智能调度、精确计费——市面方案要么性能差，要么功能缺
- KeyCompute 登场：94.7% Rust、18 crate monorepo、从路由到计费到节点调度全链路覆盖
- 核心看点预告：唯一执行层、两层路由、后置计费、PC 变算力节点

## 一、架构总览与设计哲学（~2min）

- 18 crate 拆分策略：编译隔离、单一职责、crate 可见性约束
- 三大设计原则：架构约束（谁能做什么）、后置计费（不阻塞不预扣）、类型驱动（编译期契约）
- 七阶段启动生命周期：从配置加载到优雅关闭
- AES 加密存储 API Key + Argon2 密码哈希——安全优先的密钥管理

## 二、LLM Gateway：唯一执行层（~2.5min）

- GatewayExecutor = 系统调用层——所有上游请求必经之地
- Retry-Fallback 链：primary 失败 → 依次尝试 fallback target → 全部失败才报错
- 流式背压处理：tokio::spawn + mpsc::channel(100) 立即返回 Receiver，避免死锁
- Token 计量：tiktoken o200k_base 精确计数 + Provider Usage 事件权威修正（双重保险）

## 三、两层路由引擎（~2.5min）

- Layer1 Provider 排序：成本×0.3 + 延迟×0.25 + 成功率×0.25 + 健康度×0.2
- 延迟分档制：<100ms 优秀 / 100-300ms 良好 / 300ms-1s 一般 / >1s 较差
- 路由引擎只读无副作用——不写状态，只基于快照做决策
- Layer2 账号选择：租户隔离 + 优先级排序 + 冷却机制（轻量熔断）
- 健康反馈闭环：执行层成功/失败 → 更新健康状态 → 影响下次路由

## 四、Node Gateway：PC 变算力节点（~2min）

- pull-based 长轮询：无需公网 IP、端口映射、VPN
- 工作流：注册 → 心跳保活 → BRPOP 领任务 → 本地 Ollama 执行 → POST 提交结果
- node: 前缀触发独立路径——不走 Provider 排序，不 fallback（尊重用户明确意图）
- 容错设计：complete_grace_secs 宽限期、sweeper 补推、failure_threshold 排除
- NodeCapabilityIndex trait：SQL 查询验证，不信任客户端自报负载

## 五、后置计费：不可变主账本（~1.5min）

- 三不原则：不参与路由、不预扣余额、不反向影响执行结果
- rust_decimal::Decimal 128 位定点——避免浮点累积误差
- 流结束后一次性写入 usage_logs
- 支持三种结算状态：success / partial / upstream_error

## 六、Provider 适配器 Trait 抽象（~1min）

- ProviderAdapter trait：Send + Sync 保证并发安全
- HttpTransport trait 依赖注入——测试可完全 mock 网络层
- 零修改扩展：新 Provider 只需实现 trait + 创建独立 crate
- 已支持：OpenAI / Claude / Gemini / DeepSeek / Ollama / vLLM

## 总结与启发（~1.5min）

- 唯一执行层 → 安全审计简化，故障定位清晰
- 后置计费 → 消除高并发瓶颈
- 两层路由 + 健康闭环 → 自适应高可用
- PC 算力纳管 → 去中心化计算的想象空间
- 类型驱动 + 编译隔离 → Rust 工程级保障