# Diagram Prompts — 画图提示词知识库

画图有两种场景，从这里找不同的参考：

## 场景一：技术图表（代码生成）

用 fireworks-tech-graph 等 skill 生成 SVG/PNG 架构图、流程图、序列图。

→ 走这条路：**布局决策 + 图表语法模板**

1. **选布局** → 读 [design-atoms.md](design-atoms.md) 的"二、布局骨架"和"四、连接语言"，决定用什么结构
2. **选风格** → 读 [design-atoms.md](design-atoms.md) 的"六、情绪基调"，决定图表气质
3. **抄模板** → 从 [demos.md](demos.md) 找对应图表类型的 PlantUML/Mermaid/Graphviz 语法模板，填入内容

## 场景二：文生图（AI 绘图）

用 Claude / DALL-E / Midjourney 等生成像素级信息图、概念图、科普长图。

→ 走这条路：**内容标签路由 → 参考模板 → 改内容不改骨架**

1. **提取内容标签** → 从用户描述中识别"画什么"（架构图/流程图/蓝图/安全流程…）
2. **查路由表** → 在 [ROUTING.md](ROUTING.md) 中用标签匹配推荐的 prompt-N
3. **参考模板** → 打开对应 prompt-N，改内容，保持视觉风格
4. **对照参考图** → [images/](images/) 目录的 exemplar-*.png/jpg 是该提示词的最终效果图，用于校准
5. **微调视觉** → 如需调整配色/布局细节，再查 [design-atoms.md](design-atoms.md)

### 三种入口

| 入口 | 路由方式 |
|------|---------|
| 用户用自然语言描述 | 从描述提取内容标签 → 查 ROUTING.md |
| 用户提供本目录 exemplar 图 | images/ 目录文件名直接对应 prompt-N（编号一致） |
| 用户提供外部参考图 | skill 读图 → 生成内容标签 → 查 ROUTING.md |

## 文件索引

| 文件 | 场景一 | 场景二 | 用途 |
|------|:------:|:------:|------|
| [ROUTING.md](ROUTING.md) | | ★ | 内容标签路由表 — "画什么"→ 推荐哪个 prompt |
| [demos.md](demos.md) | ★ | | PlantUML / Mermaid / Graphviz 可复制模板 |
| [design-atoms.md](design-atoms.md) | ★ | ★(微调时) | 视觉策略参考 — 色彩、布局、层级的可选维度 |
| [prompts.md](prompts.md) | | ★ | 色系/风格速查表 |
| prompt-1 ~ prompt-21 | | ★ | 100% 视觉还原提示词 |
| [images/](images/) | | ★ | 参考图片（exemplar-*.png/jpg） |

## 提示词与色系对照

| # | 主题 | 色系 | 风格 | 参考图 |
|---|------|------|------|--------|
| 1 | AI 同事蒸馏为 Skill | teal/cyan | 手绘草图 | `exemplar-ai-colleague-to-skill-pipeline.png` |
| 2 | Codex Agent Loop — SSE 工具流 | purple/magenta | 技术架构 | `exemplar-codex-agent-loop-part3-sse-tool-flow.png` |
| 3 | Codex Agent Loop — 缓存压缩 | orange/warm | 技术信息图 | `exemplar-codex-agent-loop-part4-cache-compression.png` |
| 4 | persona.md 分层蓝图 | steel blue | 蓝图放射 | `exemplar-persona-md-blueprint.png` |
| 5 | work.md 六模块蓝图 | blue-gray ink | 手绘蓝图 | `exemplar-work-md-blueprint.png` |
| 6 | 故障场景编排流程 | teal/gray | 协同流程 | `exemplar-work-persona-incident-flow.png` |
| 7 | knowledge/ 知识库结构 | teal/cyan monochrome | 专业蓝图 | *(AI-generated)* |
| 8 | Hermes Agent 运行时架构 | orange/blue/gray | 科普拆解 | `exemplar-hermes-agent-runtime-architecture.jpg` |
| 9 | Hermes 多入口统一核心 | teal/blue | 科普拆解 | `exemplar-hermes-multi-entry-unified-core.jpg` |
| 10 | Hermes Skills 系统学习 | teal/warm wood | 科普拆解 | `exemplar-hermes-skills-system-learning-agent.jpg` |
| 11 | Hermes Agent 安全门禁 | green/yellow | 科普拆解 | `exemplar-hermes-agent-security-runtime-gates.jpg` |
| 12 | Keep 健身产品营销生态图 | purple/gold | 暗色品牌 | `exemplar-keep-fitness-marketing-deck.jpg` |
| 13 | SkillRouter 论文管道架构 | pastel/soft blue | 扁平学术 | `exemplar-skillrouter-pipeline-architecture.jpg` |
| 14 | 企业级 AI 基建全景图 | orange/blue/gray | 环形全景 | `exemplar-enterprise-ai-infra-panorama.jpg` |
| 15 | 提示词与工作流编排 | orange/blue/gray | 科普拆解 | `exemplar-prompt-workflow-orchestration.jpg` |
| 16 | 知识库与检索增强 | orange/blue/gray | 科普拆解 | `exemplar-knowledge-base-rag.jpg` |
| 17 | 工具调用与业务系统集成 | orange/blue/gray | 科普拆解 | `exemplar-tool-call-business-integration.jpg` |
| 18 | 上下文、记忆与状态管理 | black/white/gray | 科普拆解 | `exemplar-context-memory-state-management.jpg` |
| 19 | 评测、观测与反馈闭环 | orange/blue/gray | 科普拆解 | `exemplar-eval-observability-feedback-loop.jpg` |
| 20 | 安全、权限与治理 | orange/blue/gray | 科普拆解 | `exemplar-security-permission-governance.jpg` |
| 21 | 部署、性能、成本与资产管理 | orange/blue/gray | 科普拆解 | `exemplar-deploy-performance-cost-mgmt.jpg` |