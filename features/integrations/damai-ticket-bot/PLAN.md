# 大麦抢票 Bot — 实现方案

> 状态：规划中
> 创建：2026-04-11

## 核心思路

**OpenCLI + 直接接口调用**，绕过 Selenium 风控：

```
OpenCLI（Chrome 插件）
    ↓ 共享 Cookie（零风控登录）
Python 抢票脚本（直接调大麦接口）
    ↓ 带真实 Cookie 发请求
大麦接口（无法区分机器/真人）
```

**关键优势：**
- Cookie 来自真实浏览器登录态 → 零人机检测
- 直接调接口 → 毫秒级响应，不依赖页面渲染
- 用户只需扫码登录一次 → 后续全自动

---

## 技术方案

### 1. Cookie 获取（OpenCLI）

- 安装 `@jackwener/opencli`
- 安装 Chrome 插件
- 扫码登录大麦一次
- 后续 OpenCLI 可导出 Cookie 供脚本使用

**安装命令（待执行）：**
```bash
npm install -g @jackwener/opencli
```

### 2. 抢票脚本（直接调接口）

**参考项目：**
- `flyiyou/Automatic_ticket_purchase`（V2.1, Go, 2026-03，混合方案）
- `shiyutim/tickets`（Rust + Tauri，4月9日实测成功抢到周杰伦4张票）
- `Kenshin-liu/damai`（Node.js/Puppeteer, 2026-04-01）

**脚本职责：**
1. 读取 OpenCLI 导出的 Cookie
2. 构造抢票请求（场次、票价、观演人、数量）
3. 定时轮询检测余票
4. 有票时立即提交订单
5. 抢到后通知用户（15分钟内付款）

**签名处理：**
- 方案A：直接用 Cookie 里的 token 调接口（如果大麦不校验签名）
- 方案B：参考 flyiyou 的 signcode.js（已有签名逻辑）
- 方案C：mitmproxy 抓包提取签名参数

### 3. 观演人预填

- 提前在大麦 App 设置好实名观演人（姓名+身份证）
- 抢票时只需传 ID，不需要再填信息

---

## 参考资料

- GitHub: https://github.com/jackwener/opencli
- GitHub: https://github.com/flyiyou/Automatic_ticket_purchase
- GitHub: https://github.com/shiyutim/tickets
- GitHub: https://github.com/Kenshin-liu/damai

---

## 当前进度

- [x] 依赖安装（selenium, requests, beautifulsoup4, pyexecjs）
- [x] ChromeDriver 147 下载并就位（`Automatic_ticket_purchase/chromedriver_windows.exe`）
- [x] flyiyou 项目代码读完，架构清晰
- [x] **OpenCLI 安装完成**（v1.7.0，532 命令，84 平台）
- [x] **OpenCLI Chrome 扩展已加载并连接**
- [ ] 确认目标演出（item_id + ticket_price + viewer 名字）
- [ ] 扫码登录一次，保存 cookies.pkl
- [ ] 测试跑通

---

## 2026-04-11 进展记录

### OpenCLI 安装与测试

1. **安装 OpenCLI**
   ```bash
   npm install -g @jackwener/opencli
   ```
   版本：1.7.0，内置 532 个命令，支持 84 个平台。

2. **安装 Chrome 扩展**
   - 下载 `opencli-extension.zip` 从 GitHub releases
   - 解压到 `C:\Users\superman\AppData\Local\opencli-extension`
   - Chrome 加载已解压的扩展程序
   - 验证：`opencli doctor` 显示全部 ✅

3. **尝试自动生成大麦 CLI**
   ```bash
   opencli generate "https://www.damai.cn/"
   ```
   结果：**BLOCKED** — 大麦是 SSR 站点，没有公开 JSON API 端点。

4. **尝试录制 API 调用**
   ```bash
   opencli record "https://www.damai.cn/" --site damai --timeout 120000
   ```
   状态：已启动，等待用户在浏览器中操作录制。

### 结论

- OpenCLI 不内置大麦支持
- 自动分析无法穿透大麦的 SSR + 私有 API
- 需要手动录制或回到 flyiyou Python 方案

### 待办

- [ ] 确认目标演出（item_id + ticket_price + viewer）
- [ ] 完成 OpenCLI 录制或回到 flyiyou 方案
- [ ] 扫码登录，保存 cookies
- [ ] 测试（用低价票或测试场）
