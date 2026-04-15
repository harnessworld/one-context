# Cover Presets — 风格预设

> 3 种开箱即用的封面风格，直接复制 HTML 即可使用。

---

## 风格一：简约型（Minimal）

**特点**：大标题 + 微装饰，留白充足，视觉干净。

**适用**：知识分享、教程、访谈、通用内容。

### 竖版 (1080×1920)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #0f0f0f;
      --fg: #f8f4ec;
      --muted: #8a8a8a;
      --accent: #e8d5a3;
    }
    body {
      width: 1080px;
      height: 1920px;
      background: var(--bg);
      color: var(--fg);
      font-family: system-ui, sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 80px 64px;
    }
    .badge {
      font-size: 28px;
      padding: 12px 32px;
      background: rgba(232,213,163,.15);
      border-radius: 40px;
      color: var(--accent);
      margin-bottom: 40px;
    }
    .title {
      font-size: 160px;
      font-weight: 900;
      line-height: 1.1;
      text-align: center;
      letter-spacing: -4px;
    }
    .subtitle {
      font-size: 64px;
      font-weight: 700;
      color: var(--muted);
      margin-top: 24px;
      text-align: center;
    }
    .desc {
      font-size: 40px;
      color: var(--muted);
      margin-top: 48px;
      text-align: center;
      max-width: 900px;
      line-height: 1.5;
    }
    .source {
      position: absolute;
      bottom: 48px;
      font-size: 28px;
      color: rgba(255,255,255,.3);
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="badge">【标签】</div>
  <div class="title">【主标题】</div>
  <div class="subtitle">【副标题】</div>
  <div class="desc">【说明文字，1-2 句，可空】</div>
  <div class="source">【来源】</div>
</body>
</html>
```

### 横版 (1440×1080)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #0f0f0f;
      --fg: #f8f4ec;
      --muted: #8a8a8a;
      --accent: #e8d5a3;
    }
    body {
      width: 1440px;
      height: 1080px;
      background: var(--bg);
      color: var(--fg);
      font-family: system-ui, sans-serif;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 64px 80px;
    }
    .badge {
      font-size: 24px;
      padding: 10px 28px;
      background: rgba(232,213,163,.15);
      border-radius: 32px;
      color: var(--accent);
      margin-bottom: 32px;
    }
    .title {
      font-size: 120px;
      font-weight: 900;
      line-height: 1.1;
      text-align: center;
      letter-spacing: -3px;
    }
    .subtitle {
      font-size: 48px;
      font-weight: 700;
      color: var(--muted);
      margin-top: 20px;
      text-align: center;
    }
    .desc {
      font-size: 32px;
      color: var(--muted);
      margin-top: 32px;
      text-align: center;
      max-width: 1100px;
      line-height: 1.5;
    }
    .source {
      position: absolute;
      bottom: 40px;
      font-size: 22px;
      color: rgba(255,255,255,.3);
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="badge">【标签】</div>
  <div class="title">【主标题】</div>
  <div class="subtitle">【副标题】</div>
  <div class="desc">【说明文字】</div>
  <div class="source">【来源】</div>
</body>
</html>
```

---

## 风格二：科技型（Tech）

**特点**：渐变标题 + 光晕装饰 + 几何元素，视觉冲击力强。

**适用**：技术分享、产品发布、数据报告、AI/科技类内容。

### 竖版 (1080×1920)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #0a0a0f;
      --fg: #f0f0f5;
      --muted: #7a7a8a;
      --accent-a: #6366f1;
      --accent-b: #06b6d4;
    }
    body {
      width: 1080px;
      height: 1920px;
      background: var(--bg);
      color: var(--fg);
      font-family: system-ui, sans-serif;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 80px 64px;
    }
    /* 光晕装饰 */
    .orb-1 {
      position: absolute;
      width: 600px;
      height: 600px;
      background: radial-gradient(circle, rgba(99,102,241,.2), transparent 70%);
      top: -200px;
      right: -100px;
      border-radius: 50%;
    }
    .orb-2 {
      position: absolute;
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, rgba(6,182,212,.15), transparent 70%);
      bottom: -150px;
      left: -100px;
      border-radius: 50%;
    }
    /* 进化条 */
    .evolution {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
      padding: 20px 40px;
      background: rgba(255,255,255,.05);
      border-radius: 50px;
      position: relative;
      z-index: 2;
    }
    .evolution .step {
      text-align: center;
    }
    .evolution .step-emoji {
      font-size: 48px;
    }
    .evolution .step-label {
      font-size: 22px;
      color: var(--muted);
      margin-top: 4px;
    }
    .evolution .arrow {
      color: rgba(255,255,255,.3);
      font-size: 24px;
    }
    /* Hero */
    .hero {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      position: relative;
      z-index: 2;
      gap: 20px;
    }
    .badge {
      font-size: 26px;
      padding: 10px 28px;
      background: linear-gradient(135deg, rgba(99,102,241,.2), rgba(6,182,212,.2));
      border-radius: 40px;
      color: var(--accent-b);
    }
    .title {
      font-size: 150px;
      font-weight: 900;
      line-height: 1.05;
      letter-spacing: -4px;
      background: linear-gradient(135deg, var(--accent-a) 0%, var(--accent-b) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .subtitle {
      font-size: 58px;
      font-weight: 700;
      color: var(--fg);
      letter-spacing: 2px;
    }
    .desc {
      font-size: 38px;
      color: var(--muted);
      max-width: 900px;
      line-height: 1.5;
    }
    /* Pill 卡 */
    .pills {
      display: flex;
      gap: 16px;
      position: relative;
      z-index: 2;
    }
    .pill {
      flex: 1;
      background: rgba(255,255,255,.05);
      border-radius: 20px;
      padding: 24px 20px;
      text-align: center;
    }
    .pill-emoji {
      font-size: 40px;
    }
    .pill-title {
      font-size: 38px;
      font-weight: 700;
      color: var(--accent-b);
      margin-top: 8px;
    }
    .pill-sub {
      font-size: 30px;
      color: var(--muted);
      margin-top: 4px;
    }
    .source {
      font-size: 24px;
      color: rgba(255,255,255,.25);
      text-align: center;
      letter-spacing: 3px;
      position: relative;
      z-index: 2;
    }
  </style>
</head>
<body>
  <div class="orb-1"></div>
  <div class="orb-2"></div>

  <div class="evolution">
    <div class="step"><div class="step-emoji">🌱</div><div class="step-label">创意</div></div>
    <div class="arrow">▶</div>
    <div class="step"><div class="step-emoji">📝</div><div class="step-label">脚本</div></div>
    <div class="arrow">▶</div>
    <div class="step"><div class="step-emoji">🎬</div><div class="step-label">成片</div></div>
    <div class="arrow">▶</div>
    <div class="step"><div class="step-emoji">🚀</div><div class="step-label">发布</div></div>
  </div>

  <div class="hero">
    <div class="badge">【标签】</div>
    <div class="title">【主标题】</div>
    <div class="subtitle">【副标题】</div>
    <div class="desc">【说明文字】</div>
  </div>

  <div class="pills">
    <div class="pill">
      <div class="pill-emoji">⏱</div>
      <div class="pill-title">【数值1】</div>
      <div class="pill-sub">【说明1】</div>
    </div>
    <div class="pill">
      <div class="pill-emoji">🎯</div>
      <div class="pill-title">【数值2】</div>
      <div class="pill-sub">【说明2】</div>
    </div>
    <div class="pill">
      <div class="pill-emoji">💡</div>
      <div class="pill-title">【数值3】</div>
      <div class="pill-sub">【说明3】</div>
    </div>
  </div>

  <div class="source">【来源】</div>
</body>
</html>
```

### 横版 (1440×1080)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #0a0a0f;
      --fg: #f0f0f5;
      --muted: #7a7a8a;
      --accent-a: #6366f1;
      --accent-b: #06b6d4;
    }
    body {
      width: 1440px;
      height: 1080px;
      background: var(--bg);
      color: var(--fg);
      font-family: system-ui, sans-serif;
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: center;
      padding: 64px 80px;
    }
    .orb-1 {
      position: absolute;
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, rgba(99,102,241,.15), transparent 70%);
      top: -150px;
      right: -100px;
      border-radius: 50%;
    }
    .orb-2 {
      position: absolute;
      width: 400px;
      height: 400px;
      background: radial-gradient(circle, rgba(6,182,212,.12), transparent 70%);
      bottom: -100px;
      left: -80px;
      border-radius: 50%;
    }
    .main {
      display: flex;
      flex: 1;
      gap: 60px;
      position: relative;
      z-index: 2;
    }
    .hero {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 16px;
    }
    .badge {
      font-size: 22px;
      padding: 8px 24px;
      background: linear-gradient(135deg, rgba(99,102,241,.2), rgba(6,182,212,.2));
      border-radius: 32px;
      color: var(--accent-b);
      width: fit-content;
    }
    .title {
      font-size: 100px;
      font-weight: 900;
      line-height: 1.05;
      letter-spacing: -3px;
      background: linear-gradient(135deg, var(--accent-a) 0%, var(--accent-b) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .subtitle {
      font-size: 42px;
      font-weight: 700;
      color: var(--fg);
      letter-spacing: 1px;
    }
    .desc {
      font-size: 28px;
      color: var(--muted);
      max-width: 700px;
      line-height: 1.5;
    }
    .pills {
      width: 380px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .pill {
      background: rgba(255,255,255,.05);
      border-radius: 16px;
      padding: 20px 24px;
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .pill-emoji {
      font-size: 36px;
    }
    .pill-content {
      flex: 1;
    }
    .pill-title {
      font-size: 32px;
      font-weight: 700;
      color: var(--accent-b);
    }
    .pill-sub {
      font-size: 24px;
      color: var(--muted);
    }
    .source {
      position: absolute;
      bottom: 40px;
      left: 80px;
      font-size: 20px;
      color: rgba(255,255,255,.25);
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="orb-1"></div>
  <div class="orb-2"></div>

  <div class="main">
    <div class="hero">
      <div class="badge">【标签】</div>
      <div class="title">【主标题】</div>
      <div class="subtitle">【副标题】</div>
      <div class="desc">【说明文字】</div>
    </div>
    <div class="pills">
      <div class="pill">
        <div class="pill-emoji">⏱</div>
        <div class="pill-content">
          <div class="pill-title">【数值1】</div>
          <div class="pill-sub">【说明1】</div>
        </div>
      </div>
      <div class="pill">
        <div class="pill-emoji">🎯</div>
        <div class="pill-content">
          <div class="pill-title">【数值2】</div>
          <div class="pill-sub">【说明2】</div>
        </div>
      </div>
      <div class="pill">
        <div class="pill-emoji">💡</div>
        <div class="pill-content">
          <div class="pill-title">【数值3】</div>
          <div class="pill-sub">【说明3】</div>
        </div>
      </div>
    </div>
  </div>

  <div class="source">【来源】</div>
</body>
</html>
```

---

## 风格三：数据型（Data）

**特点**：超大数字 + 对比色 + 简洁布局，数据冲击力强。

**适用**：业绩报告、数据总结、年度复盘、成果展示。

### 竖版 (1080×1920)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #0f0f0f;
      --fg: #ffffff;
      --muted: #888888;
      --accent: #22c55e;
      --accent-alt: #f97316;
    }
    body {
      width: 1080px;
      height: 1920px;
      background: var(--bg);
      color: var(--fg);
      font-family: system-ui, sans-serif;
      display: flex;
      flex-direction: column;
      padding: 80px 64px;
    }
    .header {
      text-align: center;
      margin-bottom: 60px;
    }
    .badge {
      font-size: 26px;
      padding: 10px 28px;
      background: rgba(34,197,94,.15);
      border-radius: 40px;
      color: var(--accent);
      display: inline-block;
    }
    .title {
      font-size: 56px;
      font-weight: 700;
      margin-top: 24px;
      color: var(--fg);
    }
    /* 核心大数字 */
    .stats-main {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
    }
    .big-number {
      font-size: 280px;
      font-weight: 900;
      line-height: 1;
      background: linear-gradient(135deg, var(--accent) 0%, #4ade80 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .big-label {
      font-size: 48px;
      font-weight: 600;
      color: var(--muted);
      margin-top: 16px;
    }
    /* 对比数据 */
    .stats-row {
      display: flex;
      gap: 32px;
      margin-top: 60px;
    }
    .stat-item {
      text-align: center;
      flex: 1;
    }
    .stat-num {
      font-size: 80px;
      font-weight: 800;
      color: var(--accent-alt);
    }
    .stat-label {
      font-size: 32px;
      color: var(--muted);
      margin-top: 8px;
    }
    /* 底部总结 */
    .summary {
      text-align: center;
      margin-top: 60px;
      padding-top: 40px;
      border-top: 1px solid rgba(255,255,255,.1);
    }
    .summary-text {
      font-size: 36px;
      color: var(--fg);
      line-height: 1.5;
    }
    .summary-text strong {
      color: var(--accent);
    }
    .source {
      font-size: 24px;
      color: rgba(255,255,255,.25);
      text-align: center;
      margin-top: 40px;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="badge">【标签】</div>
    <div class="title">【副标题/主题】</div>
  </div>

  <div class="stats-main">
    <div class="big-number">【大数字】</div>
    <div class="big-label">【指标名称】</div>
  </div>

  <div class="stats-row">
    <div class="stat-item">
      <div class="stat-num">【数字1】</div>
      <div class="stat-label">【说明1】</div>
    </div>
    <div class="stat-item">
      <div class="stat-num">【数字2】</div>
      <div class="stat-label">【说明2】</div>
    </div>
    <div class="stat-item">
      <div class="stat-num">【数字3】</div>
      <div class="stat-label">【说明3】</div>
    </div>
  </div>

  <div class="summary">
    <div class="summary-text">【总结句，用 <strong>高亮</strong> 关键词】</div>
  </div>

  <div class="source">【来源】</div>
</body>
</html>
```

### 横版 (1440×1080)

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    :root {
      --bg: #0f0f0f;
      --fg: #ffffff;
      --muted: #888888;
      --accent: #22c55e;
      --accent-alt: #f97316;
    }
    body {
      width: 1440px;
      height: 1080px;
      background: var(--bg);
      color: var(--fg);
      font-family: system-ui, sans-serif;
      display: flex;
      align-items: center;
      padding: 64px 80px;
    }
    .main {
      display: flex;
      flex: 1;
      gap: 80px;
    }
    .left {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .badge {
      font-size: 22px;
      padding: 8px 24px;
      background: rgba(34,197,94,.15);
      border-radius: 32px;
      color: var(--accent);
      width: fit-content;
    }
    .title {
      font-size: 44px;
      font-weight: 700;
      margin-top: 20px;
    }
    .big-number {
      font-size: 200px;
      font-weight: 900;
      line-height: 1;
      margin-top: 40px;
      background: linear-gradient(135deg, var(--accent) 0%, #4ade80 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .big-label {
      font-size: 36px;
      font-weight: 600;
      color: var(--muted);
      margin-top: 12px;
    }
    .right {
      width: 400px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 24px;
    }
    .stat-card {
      background: rgba(255,255,255,.05);
      border-radius: 16px;
      padding: 24px;
    }
    .stat-num {
      font-size: 56px;
      font-weight: 800;
      color: var(--accent-alt);
    }
    .stat-label {
      font-size: 26px;
      color: var(--muted);
      margin-top: 4px;
    }
    .summary {
      background: rgba(255,255,255,.03);
      border-radius: 16px;
      padding: 24px;
    }
    .summary-text {
      font-size: 28px;
      color: var(--fg);
      line-height: 1.5;
    }
    .summary-text strong {
      color: var(--accent);
    }
    .source {
      position: absolute;
      bottom: 40px;
      font-size: 20px;
      color: rgba(255,255,255,.25);
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="main">
    <div class="left">
      <div class="badge">【标签】</div>
      <div class="title">【副标题/主题】</div>
      <div class="big-number">【大数字】</div>
      <div class="big-label">【指标名称】</div>
    </div>
    <div class="right">
      <div class="stat-card">
        <div class="stat-num">【数字1】</div>
        <div class="stat-label">【说明1】</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">【数字2】</div>
        <div class="stat-label">【说明2】</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">【数字3】</div>
        <div class="stat-label">【说明3】</div>
      </div>
      <div class="summary">
        <div class="summary-text">【总结句】</div>
      </div>
    </div>
  </div>
  <div class="source">【来源】</div>
</body>
</html>
```

---

## 快速选择指南

| 内容类型 | 推荐风格 | 核心组件 |
|----------|----------|----------|
| 知识分享/教程 | 简约型 | Badge + 标题 + 副标题 |
| 技术/产品/数据 | 科技型 | 进化条 + 渐变标题 + Pill卡 |
| 业绩/报告/总结 | 数据型 | 大数字 + 对比数据 + 总结句 |
| 访谈/人物 | 简约型 | 大标题 + 极简装饰 |
| 流程/方法论 | 科技型 | 进化条 + 步骤展示 |