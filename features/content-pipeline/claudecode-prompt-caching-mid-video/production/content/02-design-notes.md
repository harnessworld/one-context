# 幻灯片设计迭代记录

<!-- PPT 视觉设计决策与迭代，供后续复刻或修改时参考 -->

## 迭代 1：初始版本 → 用户反馈 → 重写

### 用户反馈原文（2026-05-02）

> 第4页你是不是应用图片了，我看图片显示的有问题。而且整个ppt发现字太多了点，可视化，图形，图像化的元素少了点，用户可能没有那么多时间看字，最好是字和图搭配就能让用户看懂，而且还会感叹技术果然好牛逼的那种感觉。

### 问题诊断

| 页面 | 问题 | 根因 |
|------|------|------|
| s3（五层提示结构） | 图片显示太小、不清晰 | 采用左右分栏（text 50% + image 50%），原文截图是竖长型，被压缩进半宽区域后几乎无法阅读 |
| s5（Compaction） | 同上，截图文字在分栏中失真 | 同理，分栏布局对含有大量文字的原始截图不友好 |
| 全局 | 文字密度过高，像文章而非幻灯片 | 每页正文 2-3 段，单段 60-100 字，远超小屏幕可读上限 |
| 全局 | 缺乏"技术震撼感" | 纯文字+少量 emoji，没有图形化表达缓存机制、前缀匹配等抽象概念 |

### 改进措施

#### 1. 布局策略变更

- **图片页（s3, s5）**：从「左文右图」改为「上图下文」
  - 图片区域占 55-60% 高度，使用 `object-fit: contain` + 白色底框，保证截图文字清晰可读
  - 下方仅用 3-5 个 token 级短语或 emoji band 辅助说明
- **对比页（s2, s5-bottom）**：引入 `.cache-bar` 可视化条带
  - 用彩色分段条模拟 prompt prefix 的组成（SYS / TOOLS / CONF / SESS / MSG）
  - 红色段 = 破坏前缀 = cache miss；绿色段 = 连续前缀 = cache hit
  - 一眼即可理解"前缀匹配"的核心机制

#### 2. 文字削减策略

- 全文正文削减约 60%
- 单页正文控制在 **≤2 句话**，外加 1 条 `.dim` helper line
- 规则页（s4）每卡片 = 1 个 emoji + 1 句 bold 规则 + 1 句补充
- 原则页（s6）每卡片 = 1 个 emoji + 1 句总结

#### 3. 图形化元素新增

| 元素 | 用途 | 出现页 |
|------|------|--------|
| `.cache-bar` + `.cache-seg` | 模拟 prompt prefix 分段 | s2, s5 |
| `.band` + emoji | 五层结构的速记标签 | s3 |
| `.card-rd` / `.card-gn` | 红色 = 反例/陷阱，绿色 = 正例/最佳实践 | s4, s5 |
| `clamp()` 响应式字号 | 保证小屏幕下最小可读字号 ≥16px | 全局 |

#### 4. 样式选型

- 采用 **guizang 杂志风**（参考 `repos/reference/open-design/skills/guizang-ppt/`）
- WebGL 双背景（light/dark 自动切换）
- `clamp()` 字体：标题最小 32px，正文最小 16px，kicker 最小 11px
- 无大留白，图片/色块/文字紧凑排列，适配小屏幕播放

### 关键 CSS 类索引

```css
/* 前缀匹配可视化条带 */
.cache-bar { display:flex; height:clamp(40px,6vh,70px); border-radius:4px; overflow:hidden }
.cache-seg  { display:flex; align-items:center; justify-content:center; color:#fff; font-weight:600 }
.cache-seg.sys { background:#6366f1 }
.cache-seg.tool { background:#8b5cf6 }
.cache-seg.proj { background:#06b6d4 }
.cache-seg.sess { background:#10b981 }
.cache-seg.msg { background:#f59e0b }
.cache-seg.broken { background:#ef4444 }
.cache-seg.renew { background:#22c55e }

/* 全宽图片容器（白底） */
.frame-img-fit { background:#fff; flex:1; min-height:0; display:flex; align-items:center; justify-content:center; border-radius:6px; overflow:hidden }
.frame-img-fit > img { width:100%; height:100%; object-fit:contain; padding:2vh 2vw }

/*  accent 卡片 */
.card-rd { border-left:4px solid #ef4444 }
.card-gn { border-left:4px solid #22c55e }

/* emoji 带 */
.band { display:flex; align-items:center; gap:1.2vw; padding:1.4vh 1.8vw; border-radius:4px }
```

### 启发与复用建议

- **原始截图不适合直接嵌在分栏中**：含有大量文字的博客截图应优先使用「全宽 top image + 底部 micro caption」模式
- **技术概念 → 色段条带**：前缀匹配、缓存命中/失效等抽象概念，用彩色分段条比用文字解释快 10 倍
- **红绿语义**：在技术教学中，红色 = 陷阱/错误做法，绿色 = 最佳实践，对比强烈且无需额外解释
- **小屏幕 PPT 的核心指标**：字距 ≥1.5vh，行距 ≥1.4，最小字号 ≥16px，每页总字数 ≤80 汉字（封面/过渡页除外）
