# Cover Elements — 装饰 SVG 图库

> 可配置的背景装饰图形，通过 CONFIG 的 `decoSVG` 字段内联替换。

---

## 使用方式

在 CONFIG 中将 SVG 字符串赋值给 `decoSVG`：

```javascript
const CONFIG = {
    // ...
    decoSVG: `<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <!-- 你的 SVG 内容 -->
    </svg>`,
    decoRotate: -15,    // 旋转角度
    decoOpacity: 0.7,   // 透明度
    decoScale: 1.2,     // 缩放
};
```

留空 `decoSVG: ""` 则使用默认手机图案。

---

## 图案 1：手机（默认）

短视频内容的标准装饰，模拟手机播放界面。

**推荐参数**：`decoRotate: -11` | `decoOpacity: 0.82` | `decoScale: 1`

```svg
<svg viewBox="0 0 210 400" xmlns="http://www.w3.org/2000/svg" fill="none">
    <defs>
        <linearGradient id="ph-screen" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0d2236"/>
            <stop offset="45%" stop-color="#122a42"/>
            <stop offset="100%" stop-color="#241432"/>
        </linearGradient>
        <linearGradient id="ph-glow" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#00d4e8" stop-opacity="0.55"/>
            <stop offset="55%" stop-color="#8b5cf6" stop-opacity="0.38"/>
            <stop offset="100%" stop-color="#00f0ff" stop-opacity="0.22"/>
        </linearGradient>
        <linearGradient id="ph-bar" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#00f0ff"/>
            <stop offset="100%" stop-color="#8b5cf6"/>
        </linearGradient>
    </defs>
    <rect x="8" y="6" width="194" height="388" rx="28" fill="#0c1220" stroke="rgba(255,255,255,0.38)" stroke-width="2.5"/>
    <rect x="18" y="18" width="174" height="364" rx="20" fill="url(#ph-screen)" stroke="rgba(0,240,255,0.35)" stroke-width="1.5"/>
    <ellipse cx="105" cy="120" rx="72" ry="88" fill="url(#ph-glow)"/>
    <circle cx="62" cy="44" r="4" fill="rgba(255,255,255,0.5)"/>
    <circle cx="78" cy="44" r="4" fill="rgba(255,255,255,0.28)"/>
    <circle cx="94" cy="44" r="4" fill="rgba(255,255,255,0.16)"/>
    <rect x="118" y="40" width="64" height="8" rx="4" fill="rgba(255,255,255,0.14)"/>
    <circle cx="105" cy="188" r="36" fill="rgba(0,0,0,0.42)" stroke="rgba(0,240,255,0.65)" stroke-width="2.5"/>
    <path d="M96 168 L96 208 L132 188 Z" fill="rgba(255,255,255,0.95)"/>
    <rect x="32" y="318" width="146" height="5" rx="2.5" fill="rgba(255,255,255,0.18)"/>
    <rect x="32" y="318" width="62" height="5" rx="2.5" fill="url(#ph-bar)"/>
    <text x="105" y="342" text-anchor="middle" fill="rgba(255,255,255,0.55)" font-size="13" font-family="system-ui,sans-serif" letter-spacing="1">0:15</text>
    <rect x="78" y="372" width="54" height="4" rx="2" fill="rgba(255,255,255,0.28)"/>
</svg>
```

**适用主题**：tech、growth

---

## 图案 2：芯片 / 处理器

AI 算力、芯片技术、硬件主题。

**推荐参数**：`decoRotate: -8` | `decoOpacity: 0.75` | `decoScale: 1.3`

```svg
<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" fill="none">
    <defs>
        <linearGradient id="ch-core" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0d1a2a"/>
            <stop offset="100%" stop-color="#1a0d2a"/>
        </linearGradient>
        <linearGradient id="ch-glow" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.2"/>
        </linearGradient>
    </defs>
    <!-- 核心 -->
    <rect x="80" y="80" width="140" height="140" rx="12" fill="url(#ch-core)" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <rect x="95" y="95" width="110" height="110" rx="6" fill="url(#ch-glow)" stroke="rgba(0,240,255,0.3)" stroke-width="1"/>
    <!-- 电路纹理 -->
    <line x1="110" y1="110" x2="110" y2="190" stroke="rgba(0,240,255,0.25)" stroke-width="1.5"/>
    <line x1="130" y1="110" x2="130" y2="190" stroke="rgba(139,92,246,0.2)" stroke-width="1.5"/>
    <line x1="150" y1="110" x2="150" y2="190" stroke="rgba(0,240,255,0.3)" stroke-width="1.5"/>
    <line x1="170" y1="110" x2="170" y2="190" stroke="rgba(139,92,246,0.2)" stroke-width="1.5"/>
    <line x1="190" y1="110" x2="190" y2="190" stroke="rgba(0,240,255,0.25)" stroke-width="1.5"/>
    <!-- 引脚 - 上 -->
    <line x1="110" y1="80" x2="110" y2="50" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="130" y1="80" x2="130" y2="50" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="150" y1="80" x2="150" y2="50" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="170" y1="80" x2="170" y2="50" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="190" y1="80" x2="190" y2="50" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <!-- 引脚 - 下 -->
    <line x1="110" y1="220" x2="110" y2="250" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="130" y1="220" x2="130" y2="250" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="150" y1="220" x2="150" y2="250" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="170" y1="220" x2="170" y2="250" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="190" y1="220" x2="190" y2="250" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <!-- 引脚 - 左 -->
    <line x1="80" y1="110" x2="50" y2="110" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="80" y1="130" x2="50" y2="130" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="80" y1="150" x2="50" y2="150" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="80" y1="170" x2="50" y2="170" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="80" y1="190" x2="50" y2="190" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <!-- 引脚 - 右 -->
    <line x1="220" y1="110" x2="250" y2="110" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="220" y1="130" x2="250" y2="130" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="220" y1="150" x2="250" y2="150" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="220" y1="170" x2="250" y2="170" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <line x1="220" y1="190" x2="250" y2="190" stroke="rgba(255,255,255,0.35)" stroke-width="2.5"/>
    <!-- 中心发光点 -->
    <circle cx="150" cy="150" r="18" fill="rgba(0,240,255,0.3)"/>
    <circle cx="150" cy="150" r="8" fill="rgba(0,240,255,0.6)"/>
</svg>
```

**适用主题**：tech、danger

---

## 图案 3：火箭

增长、突破、起飞主题。

**推荐参数**：`decoRotate: -25` | `decoOpacity: 0.7` | `decoScale: 1.1`

```svg
<svg viewBox="0 0 200 400" xmlns="http://www.w3.org/2000/svg" fill="none">
    <defs>
        <linearGradient id="rk-body" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1a2030"/>
            <stop offset="100%" stop-color="#201a30"/>
        </linearGradient>
        <linearGradient id="rk-flame" x1="50%" y1="0%" x2="50%" y2="100%">
            <stop offset="0%" stop-color="#FFD700" stop-opacity="0.8"/>
            <stop offset="40%" stop-color="#FF8C00" stop-opacity="0.6"/>
            <stop offset="100%" stop-color="#FF2A55" stop-opacity="0"/>
        </linearGradient>
    </defs>
    <!-- 火箭体 -->
    <path d="M100 30 Q130 80 130 180 L130 280 L70 280 L70 180 Q70 80 100 30Z" fill="url(#rk-body)" stroke="rgba(255,255,255,0.35)" stroke-width="2"/>
    <!-- 舱窗 -->
    <circle cx="100" cy="130" r="22" fill="#0a1520" stroke="rgba(0,240,255,0.5)" stroke-width="1.5"/>
    <circle cx="100" cy="130" r="16" fill="rgba(0,240,255,0.12)"/>
    <!-- 侧翼 -->
    <path d="M70 220 L40 290 L70 270Z" fill="url(#rk-body)" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
    <path d="M130 220 L160 290 L130 270Z" fill="url(#rk-body)" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
    <!-- 喷口 -->
    <rect x="82" y="275" width="36" height="14" rx="2" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.25)" stroke-width="1"/>
    <!-- 火焰 -->
    <path d="M85 289 Q90 340 100 380 Q110 340 115 289Z" fill="url(#rk-flame)"/>
    <!-- 装饰环 -->
    <line x1="70" y1="200" x2="130" y2="200" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
    <line x1="72" y1="170" x2="128" y2="170" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
</svg>
```

**适用主题**：growth、finance

---

## 图案 4：上升图表

数据、金融、趋势主题。

**推荐参数**：`decoRotate: 5` | `decoOpacity: 0.65` | `decoScale: 1.4`

```svg
<svg viewBox="0 0 320 280" xmlns="http://www.w3.org/2000/svg" fill="none">
    <defs>
        <linearGradient id="gt-area" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#00FF88" stop-opacity="0.25"/>
            <stop offset="100%" stop-color="#00FF88" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="gt-line" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#00FF88"/>
        </linearGradient>
    </defs>
    <!-- 网格线 -->
    <line x1="40" y1="40" x2="40" y2="240" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
    <line x1="40" y1="240" x2="290" y2="240" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>
    <line x1="40" y1="160" x2="290" y2="160" stroke="rgba(255,255,255,0.06)" stroke-width="1" stroke-dasharray="4 4"/>
    <line x1="40" y1="80" x2="290" y2="80" stroke="rgba(255,255,255,0.06)" stroke-width="1" stroke-dasharray="4 4"/>
    <!-- 柱形 -->
    <rect x="60" y="190" width="24" height="50" rx="3" fill="rgba(255,215,0,0.15)"/>
    <rect x="100" y="170" width="24" height="70" rx="3" fill="rgba(255,215,0,0.15)"/>
    <rect x="140" y="150" width="24" height="90" rx="3" fill="rgba(255,215,0,0.2)"/>
    <rect x="180" y="120" width="24" height="120" rx="3" fill="rgba(0,255,136,0.2)"/>
    <rect x="220" y="90" width="24" height="150" rx="3" fill="rgba(0,255,136,0.25)"/>
    <rect x="260" y="55" width="24" height="185" rx="3" fill="rgba(0,255,136,0.3)"/>
    <!-- 趋势线面积 -->
    <path d="M72 190 L112 170 L152 150 L192 120 L232 90 L272 55 L272 240 L72 240Z" fill="url(#gt-area)"/>
    <!-- 趋势线 -->
    <path d="M72 190 L112 170 L152 150 L192 120 L232 90 L272 55" stroke="url(#gt-line)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- 数据点 -->
    <circle cx="192" cy="120" r="6" fill="#00FF88" opacity="0.6"/>
    <circle cx="272" cy="55" r="6" fill="#00FF88" opacity="0.8"/>
    <!-- 箭头 -->
    <path d="M264 48 L272 55 L264 62" stroke="#00FF88" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.6"/>
</svg>
```

**适用主题**：finance、growth

---

## 图案 5：书本/知识

教程、知识分享、学习主题。

**推荐参数**：`decoRotate: -5` | `decoOpacity: 0.6` | `decoScale: 1.2`

```svg
<svg viewBox="0 0 280 320" xmlns="http://www.w3.org/2000/svg" fill="none">
    <defs>
        <linearGradient id="bk-cover" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1a1a2e"/>
            <stop offset="100%" stop-color="#16213e"/>
        </linearGradient>
    </defs>
    <!-- 书本主体 -->
    <path d="M40 40 L40 280 Q80 260 140 270 L140 30 Q80 20 40 40Z" fill="url(#bk-cover)" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
    <path d="M140 30 Q200 20 240 40 L240 280 Q200 260 140 270Z" fill="url(#bk-cover)" stroke="rgba(255,255,255,0.25)" stroke-width="1.5"/>
    <!-- 书脊 -->
    <line x1="140" y1="30" x2="140" y2="270" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
    <!-- 左页文字线 -->
    <line x1="60" y1="80" x2="120" y2="75" stroke="rgba(0,240,255,0.2)" stroke-width="2" stroke-linecap="round"/>
    <line x1="60" y1="100" x2="125" y2="95" stroke="rgba(0,240,255,0.15)" stroke-width="2" stroke-linecap="round"/>
    <line x1="60" y1="120" x2="120" y2="117" stroke="rgba(0,240,255,0.15)" stroke-width="2" stroke-linecap="round"/>
    <line x1="60" y1="140" x2="110" y2="138" stroke="rgba(0,240,255,0.12)" stroke-width="2" stroke-linecap="round"/>
    <line x1="60" y1="160" x2="125" y2="156" stroke="rgba(0,240,255,0.15)" stroke-width="2" stroke-linecap="round"/>
    <line x1="60" y1="180" x2="115" y2="178" stroke="rgba(0,240,255,0.12)" stroke-width="2" stroke-linecap="round"/>
    <line x1="60" y1="200" x2="120" y2="198" stroke="rgba(0,240,255,0.15)" stroke-width="2" stroke-linecap="round"/>
    <line x1="60" y1="220" x2="108" y2="218" stroke="rgba(0,240,255,0.12)" stroke-width="2" stroke-linecap="round"/>
    <line x1="60" y1="240" x2="125" y2="238" stroke="rgba(0,240,255,0.15)" stroke-width="2" stroke-linecap="round"/>
    <!-- 右页文字线 -->
    <line x1="160" y1="75" x2="220" y2="80" stroke="rgba(139,92,246,0.2)" stroke-width="2" stroke-linecap="round"/>
    <line x1="160" y1="95" x2="220" y2="100" stroke="rgba(139,92,246,0.15)" stroke-width="2" stroke-linecap="round"/>
    <line x1="160" y1="115" x2="215" y2="120" stroke="rgba(139,92,246,0.15)" stroke-width="2" stroke-linecap="round"/>
    <line x1="160" y1="135" x2="210" y2="138" stroke="rgba(139,92,246,0.12)" stroke-width="2" stroke-linecap="round"/>
    <line x1="160" y1="155" x2="220" y2="160" stroke="rgba(139,92,246,0.15)" stroke-width="2" stroke-linecap="round"/>
    <line x1="160" y1="175" x2="218" y2="178" stroke="rgba(139,92,246,0.12)" stroke-width="2" stroke-linecap="round"/>
    <line x1="160" y1="195" x2="220" y2="200" stroke="rgba(139,92,246,0.15)" stroke-width="2" stroke-linecap="round"/>
    <line x1="160" y1="215" x2="212" y2="218" stroke="rgba(139,92,246,0.12)" stroke-width="2" stroke-linecap="round"/>
    <line x1="160" y1="235" x2="220" y2="240" stroke="rgba(139,92,246,0.15)" stroke-width="2" stroke-linecap="round"/>
    <!-- 页面发光 -->
    <ellipse cx="140" cy="150" rx="80" ry="90" fill="rgba(0,240,255,0.04)"/>
</svg>
```

**适用主题**：tech、growth

---

## 自定义 SVG 指南

### 尺寸与定位

装饰图形容器固定为：`width: 520px; height: 990px`，居中偏下（`top: 52%`）。

- SVG 的 `viewBox` 决定自身比例
- 通过 `decoScale` 控制整体大小
- 通过 `decoRotate` 控制旋转角度

### 颜色适配

SVG 内的颜色**不会**随主题自动变化。建议：

1. 使用半透明色（`rgba`），让底层主题色微微透出
2. 避免使用纯白/纯黑，用 `rgba(255,255,255,0.x)` 保持层次
3. 渐变 `id` 使用唯一前缀，避免与默认手机 SVG 的 `id` 冲突

### 在 CONFIG 中写入

JavaScript 字符串中需要转义：
- 反引号 → 用普通引号替代
- 确保 `<` / `>` 不会被 HTML 解析器误读（放在 `<script>` 中的模板字符串即可）

---

## 图案速查

| 图案 | 推荐旋转 | 推荐透明度 | 推荐缩放 | 适合主题 |
|------|---------|-----------|---------|----------|
| 手机（默认） | -11° | 0.82 | 1.0 | tech, growth |
| 芯片 | -8° | 0.75 | 1.3 | tech, danger |
| 火箭 | -25° | 0.70 | 1.1 | growth, finance |
| 上升图表 | 5° | 0.65 | 1.4 | finance, growth |
| 书本 | -5° | 0.60 | 1.2 | tech, growth |