# SVG Snippets — 可复用图形片段

> **用法**：从本文档复制 SVG 代码块到 `presentation.html` 的右侧图形区或 Grid 卡片内。按需修改文字、颜色。
>
> 颜色使用主题变量：`var(--accent-a)` / `var(--accent-b)` / `var(--accent-c)` / `var(--sky)` / `var(--danger)` / `var(--purple)` 等。
> 如需 static 色，直接写 hex。

---

## 1. 架构分层图（三层堆叠）

适用：系统架构、前后端分层、Session/Harness/Sandbox

```html
<svg viewBox="0 0 600 620" style="width:100%">
  <!-- 顶层 -->
  <ellipse cx="300" cy="120" rx="210" ry="90" fill="rgba(16,185,129,0.06)" stroke="var(--accent-b)" stroke-width="2.5"/>
  <text x="300" y="105" text-anchor="middle" fill="var(--accent-b)" font-size="28" font-weight="900">💾 层名 A</text>
  <text x="300" y="145" text-anchor="middle" fill="var(--dim,#64748B)" font-size="18">描述文字 · 关键特征</text>
  <!-- 箭头 -->
  <path d="M300 210 L300 260" stroke="var(--accent-b)" stroke-width="2" stroke-dasharray="6 4" opacity="0.3"/>
  <text x="330" y="244" fill="var(--dim,#64748B)" font-size="15">接口名</text>
  <!-- 中层 -->
  <ellipse cx="300" cy="340" rx="210" ry="90" fill="rgba(139,92,246,0.06)" stroke="var(--purple)" stroke-width="2.5"/>
  <text x="300" y="325" text-anchor="middle" fill="var(--purple)" font-size="28" font-weight="900">🧠 层名 B</text>
  <text x="300" y="365" text-anchor="middle" fill="var(--dim,#64748B)" font-size="18">描述文字 · 关键特征</text>
  <!-- 箭头 -->
  <path d="M300 430 L300 480" stroke="var(--purple)" stroke-width="2" stroke-dasharray="6 4" opacity="0.3"/>
  <text x="330" y="464" fill="var(--dim,#64748B)" font-size="15">接口名</text>
  <!-- 底层 -->
  <ellipse cx="300" cy="550" rx="210" ry="80" fill="rgba(56,189,248,0.06)" stroke="var(--sky)" stroke-width="2.5"/>
  <text x="300" y="536" text-anchor="middle" fill="var(--sky)" font-size="28" font-weight="900">🤲 层名 C</text>
  <text x="300" y="572" text-anchor="middle" fill="var(--dim,#64748B)" font-size="18">描述文字 · 关键特征</text>
  <!-- 回环箭头 -->
  <path d="M100 550 C-40 550 -40 120 100 120" fill="none" stroke="var(--accent-b)" stroke-width="2" stroke-dasharray="6 4" opacity="0.2"/>
  <text x="20" y="340" fill="var(--accent-b)" font-size="15" transform="rotate(-90 20 340)">🔄 replay</text>
</svg>
```

---

## 2. Agentic Loop 循环图

适用：Think→Act→Observe→Repeat、迭代流程、反馈回路

```html
<svg viewBox="0 0 800 420" style="width:100%">
  <circle cx="400" cy="210" r="140" fill="none" stroke="var(--accent-a)" stroke-width="3" opacity="0.15"/>
  <circle cx="400" cy="210" r="140" fill="none" stroke="var(--accent-a)" stroke-width="3" stroke-dasharray="40 345" stroke-dashoffset="-5" stroke-linecap="round" opacity="0.4"/>
  <defs><marker id="arrowLoop" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8" fill="var(--accent-a)"/></marker></defs>
  <path d="M460 78 L540 130" fill="none" stroke="var(--accent-a)" stroke-width="2" marker-end="url(#arrowLoop)" opacity="0.5"/>
  <path d="M540 290 L460 342" fill="none" stroke="var(--accent-a)" stroke-width="2" marker-end="url(#arrowLoop)" opacity="0.5"/>
  <path d="M340 342 L260 290" fill="none" stroke="var(--accent-a)" stroke-width="2" marker-end="url(#arrowLoop)" opacity="0.5"/>
  <path d="M260 130 L340 78" fill="none" stroke="var(--accent-a)" stroke-width="2" marker-end="url(#arrowLoop)" opacity="0.5"/>
  <!-- 四节点 -->
  <rect x="320" y="40" width="160" height="64" rx="16" fill="rgba(139,92,246,0.12)" stroke="var(--purple)" stroke-width="2"/>
  <text x="400" y="80" text-anchor="middle" fill="var(--purple)" font-size="24" font-weight="800">💭 Think</text>
  <rect x="520" y="150" width="160" height="64" rx="16" fill="rgba(56,189,248,0.12)" stroke="var(--sky)" stroke-width="2"/>
  <text x="600" y="190" text-anchor="middle" fill="var(--sky)" font-size="24" font-weight="800">⚡ Act</text>
  <rect x="320" y="310" width="160" height="64" rx="16" fill="rgba(16,185,129,0.12)" stroke="var(--accent-b)" stroke-width="2"/>
  <text x="400" y="350" text-anchor="middle" fill="var(--accent-b)" font-size="24" font-weight="800">👁️ Observe</text>
  <rect x="120" y="150" width="160" height="64" rx="16" fill="rgba(251,191,36,0.12)" stroke="var(--warn)" stroke-width="2"/>
  <text x="200" y="190" text-anchor="middle" fill="var(--warn)" font-size="24" font-weight="800">🔄 Repeat</text>
  <!-- 标注 -->
  <text x="400" y="24" text-anchor="middle" fill="var(--dim,#64748B)" font-size="16">推理 / 规划</text>
  <text x="680" y="190" fill="var(--dim,#64748B)" font-size="16">工具调用</text>
  <text x="400" y="395" text-anchor="middle" fill="var(--dim,#64748B)" font-size="16">获取结果</text>
  <text x="60" y="190" fill="var(--dim,#64748B)" font-size="16">循环迭代</text>
  <text x="400" y="230" text-anchor="middle" fill="var(--accent-a)" font-size="42" font-weight="900" opacity="0.2">LOOP</text>
</svg>
```

---

## 3. 对比面板（Before / After）

适用：旧 vs 新、问题 vs 方案、宠物 vs 牲口

```html
<svg viewBox="0 0 400 80" style="width:100%">
  <rect x="10" y="15" width="150" height="50" rx="12" fill="rgba(239,68,68,0.08)" stroke="var(--danger)" stroke-width="2"/>
  <text x="85" y="47" text-anchor="middle" fill="var(--danger)" font-size="22" font-weight="700">Before</text>
  <text x="200" y="45" fill="var(--dim,#64748B)" font-size="24">→</text>
  <rect x="240" y="15" width="150" height="50" rx="12" fill="rgba(16,185,129,0.08)" stroke="var(--accent-b)" stroke-width="2"/>
  <text x="315" y="47" text-anchor="middle" fill="var(--accent-b)" font-size="22" font-weight="700">After</text>
</svg>
```

---

## 4. 数据环 / 百分比环

适用：百分比、完成度、占比可视化

```html
<svg viewBox="0 0 200 200" style="width:200px">
  <!-- 背景环 -->
  <circle cx="100" cy="100" r="80" fill="none" stroke="var(--bdr)" stroke-width="12"/>
  <!-- 数据环：stroke-dasharray = 2πr × 百分比, 2πr -->
  <!-- 例：75% → 2×3.1416×80×0.75 ≈ 377, 总 502 -->
  <circle cx="100" cy="100" r="80" fill="none" stroke="var(--accent-a)" stroke-width="12" stroke-linecap="round" stroke-dasharray="377 502" transform="rotate(-90 100 100)"/>
  <text x="100" y="95" text-anchor="middle" fill="var(--cream)" font-size="48" font-weight="900">75%</text>
  <text x="100" y="125" text-anchor="middle" fill="var(--muted)" font-size="18">说明文字</text>
</svg>
```

**常用百分比的 dasharray 值**（r=80，周长=502.65）：

| 百分比 | dash 值 |
|--------|---------|
| 25% | 126 |
| 50% | 251 |
| 60% | 302 |
| 75% | 377 |
| 90% | 452 |

---

## 5. 横向时间线

适用：发展阶段、版本演进、1.0→2.0→3.0

```html
<svg viewBox="0 0 800 120" style="width:100%">
  <!-- 主线 -->
  <line x1="60" y1="60" x2="740" y2="60" stroke="var(--bdr)" stroke-width="3" stroke-linecap="round"/>
  <!-- 节点 -->
  <circle cx="150" cy="60" r="20" fill="var(--bg)" stroke="var(--accent-c)" stroke-width="3"/>
  <text x="150" y="66" text-anchor="middle" fill="var(--accent-c)" font-size="18" font-weight="900">1.0</text>
  <text x="150" y="100" text-anchor="middle" fill="var(--muted)" font-size="16">阶段一</text>

  <circle cx="400" cy="60" r="20" fill="var(--bg)" stroke="var(--sky)" stroke-width="3"/>
  <text x="400" y="66" text-anchor="middle" fill="var(--sky)" font-size="18" font-weight="900">2.0</text>
  <text x="400" y="100" text-anchor="middle" fill="var(--muted)" font-size="16">阶段二</text>

  <circle cx="650" cy="60" r="20" fill="var(--bg)" stroke="var(--accent-b)" stroke-width="3"/>
  <text x="650" y="66" text-anchor="middle" fill="var(--accent-b)" font-size="18" font-weight="900">3.0</text>
  <text x="650" y="100" text-anchor="middle" fill="var(--muted)" font-size="16">阶段三</text>

  <!-- 箭头 -->
  <path d="M160 55 L380 55" fill="none" stroke="var(--accent-a)" stroke-width="2" opacity="0.3"/>
  <path d="M410 55 L630 55" fill="none" stroke="var(--accent-a)" stroke-width="2" opacity="0.3"/>
</svg>
```

---

## 6. 流程图（线性三步）

适用：步骤流程、Pipeline、数据处理链

```html
<svg viewBox="0 0 800 80" style="width:100%">
  <rect x="5" y="15" width="220" height="50" rx="12" fill="rgba(139,92,246,0.08)" stroke="var(--purple)" stroke-width="2"/>
  <text x="115" y="47" text-anchor="middle" fill="var(--purple)" font-size="20" font-weight="700">步骤一</text>
  <text x="245" y="45" fill="var(--dim,#64748B)" font-size="22">→</text>
  <rect x="275" y="15" width="220" height="50" rx="12" fill="rgba(56,189,248,0.08)" stroke="var(--sky)" stroke-width="2"/>
  <text x="385" y="47" text-anchor="middle" fill="var(--sky)" font-size="20" font-weight="700">步骤二</text>
  <text x="515" y="45" fill="var(--dim,#64748B)" font-size="22">→</text>
  <rect x="545" y="15" width="220" height="50" rx="12" fill="rgba(16,185,129,0.08)" stroke="var(--accent-b)" stroke-width="2"/>
  <text x="655" y="47" text-anchor="middle" fill="var(--accent-b)" font-size="20" font-weight="700">步骤三</text>
</svg>
```

---

## 7. 数值对比箭头

适用：Token 数量对比、性能对比、降本增效

```html
<svg viewBox="0 0 600 100" style="width:100%">
  <!-- 左数值 -->
  <rect x="10" y="10" width="240" height="80" rx="14" fill="rgba(239,68,68,0.08)" stroke="var(--danger)" stroke-width="2"/>
  <text x="130" y="50" text-anchor="middle" fill="var(--danger)" font-size="36" font-weight="900">180</text>
  <text x="130" y="76" text-anchor="middle" fill="var(--muted)" font-size="16">旧方案</text>
  <!-- 箭头 -->
  <text x="300" y="58" text-anchor="middle" fill="var(--accent-a)" font-size="32" font-weight="900">→</text>
  <!-- 右数值 -->
  <rect x="350" y="10" width="240" height="80" rx="14" fill="rgba(16,185,129,0.08)" stroke="var(--accent-b)" stroke-width="2"/>
  <text x="470" y="50" text-anchor="middle" fill="var(--accent-b)" font-size="36" font-weight="900">45</text>
  <text x="470" y="76" text-anchor="middle" fill="var(--muted)" font-size="16">新方案</text>
</svg>
```

---

## 8. 矩阵层级堆叠（单容器 vs 分层）

适用：Monolith vs Microservices、耦合 vs 解耦

```html
<svg viewBox="0 0 500 440" style="width:100%">
  <!-- 外框 -->
  <rect x="30" y="20" width="440" height="400" rx="20" fill="var(--danger,rgba(239,68,68,0.04))" stroke="var(--danger,rgba(239,68,68,0.2))" stroke-width="2.5" stroke-dasharray="12 6" opacity="0.5"/>
  <text x="250" y="55" text-anchor="middle" fill="var(--danger,rgba(239,68,68,0.5))" font-size="20" font-weight="800">📦 CONTAINER</text>
  <!-- 层1 -->
  <rect x="70" y="70" width="360" height="100" rx="14" fill="rgba(139,92,246,0.08)" stroke="var(--purple)" stroke-width="2"/>
  <text x="250" y="110" text-anchor="middle" fill="var(--purple)" font-size="22" font-weight="800">🧠 层 A</text>
  <text x="250" y="140" text-anchor="middle" fill="var(--dim,#64748B)" font-size="16">描述</text>
  <!-- 层2 -->
  <rect x="70" y="185" width="360" height="100" rx="14" fill="rgba(56,189,248,0.08)" stroke="var(--sky)" stroke-width="2"/>
  <text x="250" y="225" text-anchor="middle" fill="var(--sky)" font-size="22" font-weight="800">⚡ 层 B</text>
  <text x="250" y="255" text-anchor="middle" fill="var(--dim,#64748B)" font-size="16">描述</text>
  <!-- 层3 -->
  <rect x="70" y="300" width="360" height="100" rx="14" fill="rgba(16,185,129,0.08)" stroke="var(--accent-b)" stroke-width="2"/>
  <text x="250" y="340" text-anchor="middle" fill="var(--accent-b)" font-size="22" font-weight="800">💾 层 C</text>
  <text x="250" y="370" text-anchor="middle" fill="var(--dim,#64748B)" font-size="16">描述</text>
</svg>
```

---

## 使用原则

1. **复制后只改文字**：节点名、描述、百分比——不改结构
2. **颜色跟主题走**：用 CSS 变量（`var(--accent-a)` 等），不用硬编码 hex
3. **viewBox 定尺寸**：外层容器用 `style="width:100%"` 或固定宽度
4. **组合使用**：Split 布局右侧放一个 SVG；Grid 卡片内放缩小的流程图