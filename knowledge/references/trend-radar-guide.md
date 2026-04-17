# TrendRadar 趋势雷达 — 使用指南

> **来源**：[sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) · 33k+ ⭐ · v6.6.1 · MCP v4.0.2
> **数据源**：[ourongxing/newsnow](https://github.com/ourongxing/newsnow)（35 个平台）
> **集成状态**：`meta/repos.yaml` id=`trend-radar`

---

## 快速开始

### 方式一：GitHub Pages 在线版（推荐）
直接访问：**https://sansan0.github.io/TrendRadar**

无需部署，打开即用。

### 方式二：Docker 本地部署
```bash
docker run -d -p 3000:3000 --name trendradar wantcat/trendradar
# 访问 http://localhost:3000
```

### 方式三：Fork + GitHub Pages（官方推荐）
1. Fork https://github.com/sansan0/TrendRadar
2. Settings → Pages → Source: `GitHub Actions`
3. 等待 Workflow 完成（约 2 分钟）
4. 访问 `https://<your-username>.github.io/TrendRadar`

---

## 支持的平台（35 个）

| 分类 | 平台 |
|------|------|
| 短视频 | 抖音、快手、视频号、小红书 |
| 社交/社区 | 微博、知乎、B站、贴吧、即刻、Threads |
| 新闻/财经 | 财联社、华尔街见闻、36kr、虎嗅、雪球、富途、东方财富、同花顺 |
| 传统媒体 | 微信公众号、腾讯新闻、网易新闻、凤凰网 |
| 其他 | 即时热榜、今日头条等 |

---

## 推送配置

### 个人微信推送（推荐 Bark）
TrendRadar 支持 Bark（iOS 推送）+ ntfy + 通用 Webhook。

### 企微机器人推送
在 TrendRadar 设置 → 推送渠道 → 企业微信 → 填入 Webhook URL。

### Telegram / 钉钉 / 飞书
设置 → 推送渠道 → 对应平台 → 填入 Bot Token / Webhook。

---

## MCP 集成（one-context 工具链）

TrendRadar 自带 MCP server，位于 `src/mcp_server.py`。

### 暴露的工具
| 工具 | 功能 |
|------|------|
| `search_news` | 关键词搜索新闻 |
| `get_hot_list` | 获取各平台热榜 |
| `get_trending_topics` | 趋势话题分析 |
| `sentiment_analysis` | 情感分析 |

### MCP Server 启动
```bash
# 安装依赖
pip install trendradar mcp

# 启动 MCP server
python src/mcp_server.py --port 8765

# 或通过 Docker
docker run -p 8765:8765 wantcat/trendradar --mcp
```

### 在 one-context 中注册（Phase 2 待完成）
参考 OpenClaw MCP 集成方式，将 TrendRadar MCP 工具注册到 one-context 工具链。

---

## 与股吧情绪工具的协同

| 数据源 | 视角 | 场景 |
|--------|------|------|
| **TrendRadar** | 热点事件（媒体/机构/博主） | 热点爆发初期、事件追踪 |
| **skills/stock-sentiment/** | 社区舆情（散户） | 情绪量化、买卖信号 |

**联动工作流**：
1. TrendRadar 发现某股/某行业上热榜
2. 自动触发股吧情绪扫描（`batch_fetch.py`）
3. 生成综合研判推送到微信

---

## 注意事项

1. **API 压力**：newsnow API 由作者提供服务器，请勿高频调用。Docker 部署时控制推送频率。
2. **数据延迟**：热榜数据通常有 5-30 分钟延迟。
3. **微信推送**：个人微信需要 Bark（iOS）或 ntfy（Android）中转。
4. **MCP 调用**：需要 Python 3.10+，本地部署时注意环境。

---

## 相关文档

- [TrendRadar GitHub](https://github.com/sansan0/TrendRadar)
- [TrendRadar GitHub Pages](https://sansan0.github.io/TrendRadar)
- [newsnow API](https://github.com/ourongxing/newsnow)
- `features/integrations/trend-radar/spec.md` — one-context 集成规范
