---
id: trend-radar-integration
title: TrendRadar 趋势雷达集成 — one-context 热点情报中枢
category: integrations
status: in_progress
created: 2026-04-17
updated: 2026-04-17
primary_repo_id: trend-radar
tags: [mcp, trend-monitoring, notification, wechat, integration]
authors: [one-context team]
---

## 背景

**sansan0/TrendRadar** 是当前最火的热点监控开源工具（33k+ ⭐，2025-04 开源，v6.6.1），具备：
- 35 个平台热点聚合（抖音、知乎、B站、华尔街见闻、财联社、雪球、富途等）
- MCP v4.0.2 支持 → AI Agent 可直接调用
- 企微 / 个人微信 / TG / 钉钉 / 飞书 / 邮件多渠道推送
- Docker 30s 部署，GitHub Pages 在线版
- AI 对话分析（趋势追踪、情感分析、相似检索等 13 种工具）

one-context 的股吧情绪扫描（skills/stock-sentiment/）与 TrendRadar 有高度协同价值：
- **股吧** → 社区舆情（散户情绪）
- **TrendRadar** → 热点事件与新闻趋势（机构/媒体视角）

两者结合可构建完整的「**热点发现 → 舆情量化 → 智能推送**」闭环。

## 目标

1. 将 TrendRadar 纳入 `meta/repos.yaml`，作为 one-context 的热点情报数据源之一
2. 创建 `features/integrations/trend-radar/` 规范集成路径（本地部署 / GitHub Pages / MCP 调用）
3. 将 TrendRadar MCP server 注册为 one-context 的可用工具（通过 OpenClaw MCP 集成）
4. 输出集成指南：`knowledge/` 下创建 TrendRadar 使用手册

## 非目标

- 不维护 TrendRadar 源码本身（保持 upstream 独立）
- 不强制要求本地 Docker 部署（优先 GitHub Pages 在线版 + MCP 连接）
- 不替代现有的 `skills/stock-sentiment/` 股吧工具（两者并行，各司其职）

## 用户故事

| 角色 | 故事 |
|------|------|
| 吾师兄 | 「我想在 one-context 里查'AI Agent'最近的热度趋势，直接问 AI 就能拿到，不用开浏览器」 |
| 吾师兄 | 「热点事件发生后，TrendRadar 自动推送到微信，AI 帮我分析情绪变化」 |
| AI Agent | 「发现某只自选股上了 TrendRadar 热点榜时，自动关联股吧舆情，生成综合研判」 |

## 验收标准

- [ ] `meta/repos.yaml` 中有 TrendRadar 条目，`id: trend-radar`
- [ ] `features/integrations/trend-radar/spec.md` 完成本文档
- [ ] TrendRadar MCP server 可通过 one-context 工具链调用（参考 OpenClaw MCP 集成方式）
- [ ] `knowledge/` 下有 TrendRadar 使用手册（部署方式、API 调用、频道配置）
- [ ] 可演示：AI 对 TrendRadar 热点数据做自然语言查询（通过 MCP）

## 实现路径

### Phase 1：基础设施登记（今天）
- [ ] `meta/repos.yaml` 加 TrendRadar 条目
- [ ] 创建 `features/integrations/trend-radar/` 目录和文档
- [ ] 写 `knowledge/` 使用手册

### Phase 2：MCP 集成
- TrendRadar 自带 MCP server（`src/mcp_server.py`）
- 参考 OpenClaw 的 MCP 集成方式（`openclaw-config/skills/mcp/`）
- 将 TrendRadar MCP 注册到 one-context 的工具链

### Phase 3：与股吧情绪工具联动
- 当 TrendRadar 热点事件涉及某只自选股时
- 自动触发 `skills/stock-sentiment/` 的情绪分析
- 生成综合研判推送到微信

## 技术细节

### 仓库信息
```
URL: https://github.com/sansan0/TrendRadar
id: trend-radar
category: integrations
Stars: 33,328+ (2026-04)
Latest: v6.6.1 (MCP v4.0.2)
```

### 部署方式
1. **GitHub Pages**（推荐，最快）：`https://sansan0.github.io/TrendRadar`
2. **Docker**：单命令 `docker run -p 3000:3000 wantcat/trendradar`
3. **Fork 一键**（官方推荐）：GitHub 点 Fork → Settings → GitHub Pages → 启用

### MCP 调用方式
TrendRadar MCP server 暴露的工具包括：
- `search_news` — 关键词搜索新闻
- `get_hot_list` — 获取各平台热榜
- `get_trending_topics` — 趋势话题
- `sentiment_analysis` — 情感分析

### 数据源
- 来自 [ourongxing/newsnow](https://github.com/ourongxing/newsnow) API
- 覆盖：抖音、知乎、B站、微博、微信公众号、36kr、虎嗅、财联社、华尔街见闻、雪球、富途等

## 相关需求

| 相关需求 | 关系 |
|---------|------|
| `skills/stock-sentiment/` | 并行：股吧舆情（散户视角）vs TrendRadar 热点（媒体/机构视角）|
| `features/develop/damai-ticket-bot/` | 同级：外部工具集成 |
| `features/integrations/trend-radar/` | 本文档 |

## 已知限制

- newsnow API 依赖作者服务器，请勿高频调用（Docker 部署时控制推送频率）
- 个人微信推送需要 Bark / ntfy 等中转（TrendRadar 支持）
- MCP server 需要 Python 3.10+，本地部署时注意环境

## 参考资料

- [TrendRadar GitHub](https://github.com/sansan0/TrendRadar)
- [TrendRadar GitHub Pages](https://sansan0.github.io/TrendRadar)
- [newsnow API](https://github.com/ourongxing/newsnow)
- [MCP Protocol](https://modelcontextprotocol.io/)
