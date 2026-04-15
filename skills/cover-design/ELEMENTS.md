# Cover Elements — 组件库

> 可组合的封面组件，按需拼装。

---

## Hero 标题

### A. 纯色标题

```html
<div style="font-size:160px;font-weight:900;color:#f8f4ec;line-height:1.05;letter-spacing:-4px">
  【主标题】
</div>
```

### B. 渐变标题（科技感）

```html
<div style="font-size:160px;font-weight:900;line-height:1.05;letter-spacing:-4px;background:linear-gradient(135deg,#6366f1,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
  【主标题】
</div>
```

### C. 渐变标题（数据感 - 绿色系）

```html
<div style="font-size:160px;font-weight:900;line-height:1.05;background:linear-gradient(135deg,#22c55e,#4ade80);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
  【主标题】
</div>
```

### D. 渐变标题（暖色系）

```html
<div style="font-size:160px;font-weight:900;line-height:1.05;letter-spacing:-4px;background:linear-gradient(135deg,#f97316,#eab308);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
  【主标题】
</div>
```

---

## 副标题

```html
<!-- 简约型 -->
<div style="font-size:60px;font-weight:700;color:#8a8a8a">
  【副标题】
</div>

<!-- 科技型 -->
<div style="font-size:60px;font-weight:700;color:#f0f0f5;letter-spacing:2px">
  【副标题】
</div>
```

---

## Badge 标签

```html
<!-- 简约型 -->
<div style="font-size:28px;padding:12px 32px;background:rgba(232,213,163,.15);border-radius:40px;color:#e8d5a3">
  【标签】
</div>

<!-- 科技型 -->
<div style="font-size:26px;padding:10px 28px;background:linear-gradient(135deg,rgba(99,102,241,.2),rgba(6,182,212,.2));border-radius:40px;color:#06b6d4">
  【标签】
</div>

<!-- 数据型 -->
<div style="font-size:26px;padding:10px 28px;background:rgba(34,197,94,.15);border-radius:40px;color:#22c55e">
  【标签】
</div>
```

---

## 进化条

展示流程/演进/阶段，**可选组件**。

```html
<!-- 竖版用 -->
<div style="display:flex;justify-content:center;align-items:center;gap:20px;padding:20px 40px;background:rgba(255,255,255,.05);border-radius:50px">
  <div style="text-align:center">
    <div style="font-size:48px">🌱</div>
    <div style="font-size:22px;color:#8a8a8a;margin-top:4px">阶段一</div>
  </div>
  <div style="color:rgba(255,255,255,.3);font-size:24px">▶</div>
  <div style="text-align:center">
    <div style="font-size:48px">📝</div>
    <div style="font-size:22px;color:#8a8a8a;margin-top:4px">阶段二</div>
  </div>
  <div style="color:rgba(255,255,255,.3);font-size:24px">▶</div>
  <div style="text-align:center">
    <div style="font-size:48px">🎬</div>
    <div style="font-size:22px;color:#8a8a8a;margin-top:4px">阶段三</div>
  </div>
  <div style="color:rgba(255,255,255,.3);font-size:24px">▶</div>
  <div style="text-align:center">
    <div style="font-size:48px">🚀</div>
    <div style="font-size:22px;color:#8a8a8a;margin-top:4px">阶段四</div>
  </div>
</div>
```

**变体：3 阶段**

```html
<div style="display:flex;justify-content:center;align-items:center;gap:32px;padding:20px 48px;background:rgba(255,255,255,.05);border-radius:50px">
  <div style="text-align:center">
    <div style="font-size:48px">📋</div>
    <div style="font-size:22px;color:#8a8a8a;margin-top:4px">规划</div>
  </div>
  <div style="color:rgba(255,255,255,.3);font-size:28px">━━▶</div>
  <div style="text-align:center">
    <div style="font-size:48px">🔨</div>
    <div style="font-size:22px;color:#8a8a8a;margin-top:4px">执行</div>
  </div>
  <div style="color:rgba(255,255,255,.3);font-size:28px">━━▶</div>
  <div style="text-align:center">
    <div style="font-size:48px">✅</div>
    <div style="font-size:22px;color:#8a8a8a;margin-top:4px">交付</div>
  </div>
</div>
```

---

## Pill 卡片

展示并列信息块，**可选组件**。

### 竖版 3 列

```html
<div style="display:flex;gap:16px">
  <div style="flex:1;background:rgba(255,255,255,.05);border-radius:20px;padding:24px 20px;text-align:center">
    <div style="font-size:40px">⏱</div>
    <div style="font-size:38px;font-weight:700;color:#06b6d4;margin-top:8px">5分钟</div>
    <div style="font-size:30px;color:#8a8a8a;margin-top:4px">视频时长</div>
  </div>
  <div style="flex:1;background:rgba(255,255,255,.05);border-radius:20px;padding:24px 20px;text-align:center">
    <div style="font-size:40px">🎯</div>
    <div style="font-size:38px;font-weight:700;color:#6366f1;margin-top:8px">3个</div>
    <div style="font-size:30px;color:#8a8a8a;margin-top:4px">核心要点</div>
  </div>
  <div style="flex:1;background:rgba(255,255,255,.05);border-radius:20px;padding:24px 20px;text-align:center">
    <div style="font-size:40px">💡</div>
    <div style="font-size:38px;font-weight:700;color:#22c55e;margin-top:8px">实战</div>
    <div style="font-size:30px;color:#8a8a8a;margin-top:4px">案例演示</div>
  </div>
</div>
```

### 横版侧边栏

```html
<div style="width:380px;display:flex;flex-direction:column;gap:16px">
  <div style="background:rgba(255,255,255,.05);border-radius:16px;padding:20px 24px;display:flex;align-items:center;gap:16px">
    <div style="font-size:36px">⏱</div>
    <div style="flex:1">
      <div style="font-size:32px;font-weight:700;color:#06b6d4">5分钟</div>
      <div style="font-size:24px;color:#8a8a8a">视频时长</div>
    </div>
  </div>
  <div style="background:rgba(255,255,255,.05);border-radius:16px;padding:20px 24px;display:flex;align-items:center;gap:16px">
    <div style="font-size:36px">🎯</div>
    <div style="flex:1">
      <div style="font-size:32px;font-weight:700;color:#6366f1">3个</div>
      <div style="font-size:24px;color:#8a8a8a">核心要点</div>
    </div>
  </div>
</div>
```

---

## 大数字

数据型封面核心组件。

```html
<!-- 超大数字 + 标签 -->
<div style="font-size:280px;font-weight:900;line-height:1;background:linear-gradient(135deg,#22c55e,#4ade80);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
  100+
</div>
<div style="font-size:48px;font-weight:600;color:#888888;margin-top:16px">
  行业案例
</div>
```

---

## 光晕装饰

科技型封面背景装饰。

```html
<!-- 光晕 1：右上角 -->
<div style="position:absolute;width:600px;height:600px;background:radial-gradient(circle,rgba(99,102,241,.2),transparent 70%);top:-200px;right:-100px;border-radius:50%"></div>

<!-- 光晕 2：左下角 -->
<div style="position:absolute;width:500px;height:500px;background:radial-gradient(circle,rgba(6,182,212,.15),transparent 70%);bottom:-150px;left:-100px;border-radius:50%"></div>

<!-- 光晕 3：中央偏后 -->
<div style="position:absolute;width:800px;height:800px;background:radial-gradient(circle,rgba(34,197,94,.1),transparent 70%);top:50%;left:50%;transform:translate(-50%,-50%);border-radius:50%;z-index:0"></div>
```

---

## 来源行

```html
<!-- 简约型 -->
<div style="font-size:24px;color:rgba(255,255,255,.3);letter-spacing:2px">
  来源：【数据来源】
</div>

<!-- 科技型 -->
<div style="font-size:24px;color:rgba(255,255,255,.25);letter-spacing:3px">
  SOURCE: 【DATA SOURCE】
</div>

<!-- 数据型 -->
<div style="font-size:24px;color:rgba(255,255,255,.25);letter-spacing:2px">
  统计周期：2024年Q1 | 数据来源：【来源】
</div>
```

---

## 说明文字

```html
<div style="font-size:40px;color:#8a8a8a;max-width:900px;line-height:1.5;text-align:center">
  【说明文字，1-2 句，可用 <strong style="color:#e8d5a3">strong</strong> 高亮关键词】
</div>
```

---

## 组合示例

### 简约型 + 副标题 + 来源

```html
<body style="width:1080px;height:1920px;background:#0f0f0f;color:#f8f4ec;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:80px 64px">
  <div style="font-size:28px;padding:12px 32px;background:rgba(232,213,163,.15);border-radius:40px;color:#e8d5a3;margin-bottom:40px">【标签】</div>
  <div style="font-size:160px;font-weight:900;line-height:1.1;text-align:center;letter-spacing:-4px">【主标题】</div>
  <div style="font-size:60px;font-weight:700;color:#8a8a8a;margin-top:24px;text-align:center">【副标题】</div>
  <div style="position:absolute;bottom:48px;font-size:28px;color:rgba(255,255,255,.3)">【来源】</div>
</body>
```

### 科技型 + 进化条 + Pill

```html
<!-- 结构：进化条(上) + Hero(中) + Pill(下)，用 justify-content:space-between 撑满 -->
<body style="width:1080px;height:1920px;background:#0a0a0f;color:#f0f0f5;display:flex;flex-direction:column;justify-content:space-between;padding:80px 64px;position:relative;overflow:hidden">
  <!-- 光晕 -->
  <div style="position:absolute;width:600px;height:600px;background:radial-gradient(circle,rgba(99,102,241,.2),transparent 70%);top:-200px;right:-100px;border-radius:50%"></div>

  <!-- 上：进化条 -->
  <div style="display:flex;justify-content:center;gap:20px;padding:20px 40px;background:rgba(255,255,255,.05);border-radius:50px;position:relative;z-index:2">
    <!-- 进化条内容 -->
  </div>

  <!-- 中：Hero -->
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;position:relative;z-index:2;gap:20px">
    <div style="font-size:26px;padding:10px 28px;background:linear-gradient(135deg,rgba(99,102,241,.2),rgba(6,182,212,.2));border-radius:40px;color:#06b6d4">【标签】</div>
    <div style="font-size:150px;font-weight:900;line-height:1.05;letter-spacing:-4px;background:linear-gradient(135deg,#6366f1,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent">【主标题】</div>
    <div style="font-size:58px;font-weight:700;color:#f0f0f5;letter-spacing:2px">【副标题】</div>
  </div>

  <!-- 下：Pill -->
  <div style="display:flex;gap:16px;position:relative;z-index:2">
    <!-- Pill 卡片 -->
  </div>
</body>
```

---

## 字号速查表

| 元素 | 竖版 | 横版 |
|------|------|------|
| 主标题 | 140-180px | 100-130px |
| 副标题 | 56-64px | 42-52px |
| 说明文字 | 36-42px | 28-34px |
| Badge | 24-28px | 20-24px |
| Pill 标题 | 36-42px | 28-34px |
| Pill 副说明 | 28-32px | 22-26px |
| 进化条 emoji | 44-52px | 36-44px |
| 进化条 label | 20-24px | 18-22px |
| 大数字 | 240-300px | 180-220px |
| 来源行 | 22-28px | 18-24px |