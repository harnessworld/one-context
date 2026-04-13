# GBrain — AI Agent 长期记忆系统

**权威入口**：[garrytan/gbrain](https://github.com/garrytan/gbrain) · 许可证 **MIT** · 作者 **Garry Tan (Y Combinator 总裁)** · Stars **6.9k+**

**更新日期**：2026-04-13

**来源**：微信公众号文章《GBrain：AI Agent 的外置永久大脑》

---

## 1. 定位

面向 AI Agent 的开源个人知识记忆系统，作为 Agent 的"外置永久大脑"。将散落在 Markdown、Obsidian、会议纪要、邮件里的知识，变成能被智能体高效调用的结构化记忆库。

**与 Hermes/OpenClaw 的关系**：互补的三层记忆架构

| 层级 | 职责 |
|------|------|
| GBrain | 长期世界知识库（人物、公司、交易、会议、观点等客观事实） |
| Agent Memory | 偏好、决策、运行配置、行为规则等业务状态 |
| Session Context | 当前对话内容，即时交互上下文 |

---

## 2. 核心设计

### 2.1 Compiled Truth + Timeline 双层结构

每个 Markdown 页面分为两部分：
- **Compiled Truth**：当前最佳理解（最新结论）
- **Timeline**：历史证据链（可追溯）

人类可直接编辑 Markdown，`gbrain sync` 自动同步。

### 2.2 混合检索

```
Query → 多查询扩展(Claude Haiku)
      → 向量检索(HNSW) + 关键词检索(tsvector)
      → RRF Fusion: score = sum(1/(60 + rank))
      → 四层去重（每页最优块 / 余弦>0.85 / 类型多样性<60% / 单页上限）
      → 过时提醒
      → 返回结果
```

### 2.3 智能分块策略

| 策略 | 适用场景 | 特点 |
|------|----------|------|
| 递归分块 | 时间线、批量导入 | 5级分隔符、300词块、50词重叠、速度快 |
| 语义分块 | 精炼结论内容 | 句子向量 + 余弦相似度 + Savitzky-Golay 边界检测 |
| LLM 引导分块 | 高价值内容 | Claude Haiku 滑动窗口识别主题转变、成本最高 |

### 2.4 实体丰富化

自动识别人物、公司、观点等实体，查记忆库 → 带上下文回应 → 写入 gbrain → 更新索引。

### 2.5 Dream Cycle（夜间巩固）

Cron 定时任务：补充缺失实体、修复错误引用、整理记忆。

---

## 3. 技术栈

| 组件 | 用途 |
|------|------|
| Postgres + pgvector | 混合检索引擎 |
| OpenAI API | 向量嵌入（text-embedding-3-large） |
| Anthropic API | 多查询扩展 + LLM 分块（Haiku） |
| Markdown | 唯一真相源 |

**部署模式**：
- 零配置：`gbrain init` → PGLite 本地嵌入式数据库
- 生产级：`gbrain migrate --to supabase` → 托管 Postgres

---

## 4. 集成方式

### 4.1 CLI 独立使用

```bash
git clone https://github.com/garrytan/gbrain.git && cd gbrain
bun install && bun link
gbrain init
gbrain import ~/notes/
gbrain query "what themes show up across my notes?"
```

### 4.2 MCP 服务端

```json
// Claude Code (~/.claude/server.json)
{
  "mcpServers": {
    "gbrain": {
      "command": "gbrain",
      "args": ["serve"]
    }
  }
}
```

暴露 30+ MCP 工具：`get_page`、`put_page`、`search`、`query`、`add_link`、`traverse_graph`、`sync_brain` 等。

---

## 5. 适用场景判断

### 适合引入 GBrain

- 知识库文档数 > 500
- 多个 Agent 需要共享"谁在什么时候说了什么"的长期记忆
- 经常出现"我知道有这个信息但找不到"的情况
- 需要自动整理、去重、关联知识

### 暂不需要引入

- 知识库规模小（< 100 文档）
- 文件系统 + grep 检索已足够
- 不愿承担 Postgres + API 密钥的运维复杂度
- 现有 Agent Memory + Session Context 已满足需求

### one-context 现状评估

one-context 已有清晰的知识结构（`standards/playbooks/references/prompts/tools`），且 Hermes 自带 `memory` + `session_search` 覆盖了部分记忆需求。

**建议**：暂不引入，但可借鉴设计思路：
- Compiled Truth + Timeline 双层结构
- 反向链接机制（`[[wiki-link]]` 语法）
- 定期整理 cron 任务

待知识库规模增长后再评估。

---

## 6. 可借鉴设计

### 6.1 双层结构实践

在 `references/` 中，每个主题一个文件：

```markdown
# 某系统分析

## 结论（Compiled Truth）

当前最佳理解...

## 时间线（Timeline）

- 2026-04-01：初始调研...
- 2026-04-10：补充发现...
```

### 6.2 轻量级知识整理

```bash
# 定期扫描孤立文档
find knowledge -name "*.md" -mtime +30 -exec echo "可能过期: {}" \;
```

---

## 7. 相关资源

- GitHub：https://github.com/garrytan/gbrain
- 技能包：`docs/GBRAIN_SKILLPACK.md`（Agent 如何使用 GBrain 的完整指令）
- 验证清单：`docs/GBRAIN_VERIFY.md`