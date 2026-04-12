---
id: damai-ticket-bot
title: 大麦抢票助手
status: draft
category: develop
primary_repo_id: one-context
owner: ""
updated: "2026-04-11"
---

# 概述

在 one-context 中集成大麦网（damai.cn）抢票助手，作为可调用的 skill/工具，支持喊「帮我抢 XXX 演唱会门票」触发自动化抢票流程。

目标用户：大厂吾师兄（技术视频创作者，常关注演唱会/演出抢票场景）。

# 背景调研（已确认）

## 现有开源项目参考

| 项目 | 语言 | 状态 | 特点 |
|------|------|------|------|
| [flyiyou/Automatic_ticket_purchase](https://github.com/flyiyou/Automatic_ticket_purchase) | Go | ✅ 活跃 (2026-03) | V2.1，支持选座、连座 |
| [shiyutim/tickets](https://github.com/shiyutim/tickets) | Rust/Tauri/Vue | 一般 | 原生 App，非 Selenium |
| [hahafather007/damai_crawler](https://github.com/hahafather007/damai_crawler) | Python+Selenium | ✅ 活跃 (2026-04) | 简单易用，支持邮件通知 |
| [1443690715/Automatic_ticket_purchase](https://github.com/1443690715/Automatic_ticket_purchase) | Go | ⚠️ 停止维护 | 同上，大麦已迁移手机端 |

**结论**：大麦反爬日趋严格，Selenium 方案易被风控，Go 调接口 + 手机端抓包方案更稳定。

## 候选方向（待选）

### 方向 A：浏览器插件（Browser Extension）
- Manifest V3，注入 JS 自动刷新/选座/提交
- 优点：部署简单、反爬最小、资源占用低
- 缺点：需手动触发，不能后台运行
- 适合：开票时坐在电脑前盯着的场景

### 方向 B：CLI 工具
- 命令行程序 + JSON 配置文件
- 可集成进 one-context workflow，喊「抢票」触发
- 优点：可编程、集成度高、轻量
- 缺点：需要命令行基础
- 适合：提前设好脚本，比赛/抢票时后台跑

### 方向 C：桌面 GUI 应用
- Rust + Tauri，原生窗口，选项配置界面
- 优点：用户体验最好
- 缺点：开发周期长、打包分发麻烦
- 适合：不做为 one-context 集成首选

**推荐**：方向 A + B 结合 — 浏览器插件做核心抢票逻辑，CLI 做触发入口。

# 目标

- [ ] 确定技术方向（A/B/C）
- [ ] 选定参考项目（推荐 go 版 `flyiyou` 或 python 版 `hahafather007`）
- [ ] fork 并适配 one-context 项目结构
- [ ] 完成集成到 one-context skill/CLI
- [ ] 本地测试通过（需要真实抢票环境验证）

# 非目标

- 不保证 100% 抢到票（大麦风控策略可能随时变化）
- 不做云端部署方案（暂无服务器资源）
- 不做 iOS/Android 移动端

# 用户场景

1. 用户喊：「帮我抢 周杰伦 2026-05-01 580元票」
2. one-context 解析参数：艺人、日期、价位
3. 触发抢票逻辑，自动完成登录/刷新/选座/提交
4. 抢到后通知用户付款

# 技术要点（待定方向后展开）

- 大麦登录态维护（Cookie / Token）
- 座位选择策略（价位优先、区域偏好）
- 并发刷新频率控制（避免被风控）
- 抢票成功通知（微信/邮件）

# 关联

- **Skill 目录**: `skills/damai-ticket-bot/`
- **参考项目**: `flyiyou/Automatic_ticket_purchase` (Go), `hahafather007/damai_crawler` (Python)

# 开放问题

- [ ] 选方向 A（插件）、B（CLI）、还是 A+B？
- [ ] 用 Go 还是 Python 实现？
- [ ] 是否需要对接 one-context 的 cron 定时任务能力？
- [ ] 是否需要登录态（Cookie 持久化）？
