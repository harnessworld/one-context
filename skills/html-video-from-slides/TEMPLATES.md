# Presentation HTML 模板库

> **用法**：AI 生成 presentation.html 时，**直接复制对应模板的 HTML 结构**，只替换文字内容和颜色变量。禁止自行设计布局，禁止使用 `position:absolute` 定位内容区，禁止使用 `margin-top/margin-bottom` 在 flex 容器内制造死空间。

## 核心原则：最少内容量（Minimum Fill Table）

每种模板要求最少内容量，AI 生成后必须对照验证。不足时 **先加文字行，再考虑拆页**。

| 模板类型 | 单元格可用高度 | 必须达到 | 最少内容要求 |
|----------|----------------|----------|--------------|
| Cover 封面 | 1032px 整页 | ≥ 85% | 进化条(in-flow) + 标题(≥180px) + 副标题(≥70px) + 正文(≥2行×40px) + Pill行 |
| Split 左右 | 1032px 整页 | ≥ 85% | 左侧：标题+正文**≥6行(40px)**+卡片；右侧：SVG 填满 |
| Grid 2×2 | 每格 ~505px | ≥ 85% = 429px | emoji(96px)+标题(56px)+**正文≥4行(40px×1.65=264px)**+底tag(42px) = 458px ✓ |
| Slim header + 大卡 | 每卡 ~940px | ≥ 85% = 799px | emoji(100px)+标题(60px)+**正文≥6行(40px×1.65=396px)**+separator+sub-note(2行×34px=100px) = 712px；再加 justify-content:space-between 把 100px 富余分到边距 |
| 两大卡并排 | 每卡 ~940px | ≥ 85% = 799px | emoji(100px)+标题(60px)+**正文≥6行(40px×1.65=396px)**+separator+sub-note(2行) |
| Takeaways 2×2 | 每格 ~510px（无header时） | ≥ 85% = 433px | number(80px)+标题(54px)+**正文≥4行(38px×1.6=244px)**+底tag(42px) = 420px；补 justify-content:space-between |

**自测方法（每格必查）**：
```
格子可用高度（减去 padding）× 0.85 ≤ (emoji + title + body行数×字号×line-height + 底部装饰)
```

填充不达标的强制处理：
1. 正文不足 → 追加文字行（增加解释、背景、价值描述）
2. 仍不足 → 加底部 tag/separator/sub-note
3. 还不足 → 增大 emoji、标题字号
4. 最后才考虑拆页

---

## 禁止模式（必须避免）

```html
<!-- ❌ 绝对禁止：脱离文档流的内容定位 -->
<div style="position:absolute;top:24px;...">进化条</div>
<div class="col f1" style="justify-content:center;margin-top:90px">主内容</div>
<!-- 后果：进化条不占高度，margin-top 制造死空间，内容区缩水 50% -->

<!-- ❌ 绝对禁止：用 <br> 空行当视觉间距 -->
<div style="font-size:40px;line-height:1.6">
  第一段文字<br>
  <br>          ← 空行当 spacer，浪费 64px，且让 justify-content:center 更空旷
  <strong>第二段文字</strong>
</div>
<!-- 正确做法：用 separator div 或 margin-top：不产生空白区，且 space-between 能正确分配 -->

<!-- ❌ 绝对禁止：大卡/Split 左列用 justify-content:center 却没有足量内容 -->
<div style="display:flex;flex-direction:column;justify-content:center">
  <!-- 内容 600px → 卡片 850px → 上下各空 125px，手机上看像浮在空中 -->
</div>
<!-- 正确做法：justify-content:space-between + 底部 separator/tag 元素 -->

<!-- ❌ 绝对禁止：Grid 2×2 + 独立 header 行同时存在 -->
<div class="col f1" style="gap:18px">
  <div style="text-align:center"><!-- header 占 120px --></div>
  <div style="display:grid;...;flex:1"><!-- grid 被压缩 --></div>
</div>

<!-- ❌ 绝对禁止：Pills/卡片内用全局 .t5 (28px) 做主标签 -->
<div class="g" style="padding:20px 40px">
  <div style="font-size:26px">Session 持久层</div><!-- 太小 -->
</div>
```

## 字数上限（每个文字块）

| 位置 | 上限 | 说明 |
|------|------|------|
| 卡片 body 每行 | 18 个汉字 | 超过自动换行影响可读性 |
| 每个卡片 body | 5 行（不含 br 空行） | 超过拆成第二张卡片/页面 |
| Slim header 标题 | 12 个汉字 | 超过字号自动变小 |
| Bottom tag/总结 | 20 个汉字 | 一行显示 |

> **字多 ≠ 信息密度高**。Slide 是骨架，口播讲细节。删掉"换模型不动 Sandbox"这类重复出现的相似句，一张 slide 保留 **3~5 个核心词组**，字数 ≤ 120 个汉字。

---

## 模板一：封面（Cover）

**布局原理**：`col f1` + `justify-content:space-between`，三段全部在文档流中，不用 `position:absolute`。

**高度预算**：
- 上段（进化条）：~130px
- 中段（hero，`flex:1`）：自动填满剩余 ~740px
- 下段（pill 卡 + 来源）：~160px
- 总计：~1030px ≈ 100% 填充 ✓

```html
<!-- ══ COVER TEMPLATE ══ -->
<div class="s on" id="s0">
<div class="wa">【该页口播关键词，逐词摘自 SRT 第一段】</div>
<div class="orb" style="width:720px;height:720px;background:radial-gradient(circle,rgba(76,175,114,.09),transparent 70%);top:-220px;left:-160px"></div>
<div class="orb" style="width:560px;height:560px;background:radial-gradient(circle,rgba(212,168,67,.07),transparent 70%);bottom:-120px;right:-120px"></div>
<div class="animal-wm" style="right:-40px;bottom:-90px;opacity:.02;color:var(--accent-a)">【主题动物 emoji】</div>

<!-- ✅ 正确：三段全部在文档流内，用 space-between 撑满画布 -->
<div class="col f1" style="justify-content:space-between;z-index:3">

  <!-- 上段：进化条（IN FLOW，不用 position:absolute） -->
  <div style="display:flex;justify-content:center">
    <div class="g" style="display:flex;align-items:center;gap:24px;padding:16px 44px;border-radius:60px">
      <div style="text-align:center"><div style="font-size:56px">【emoji1】</div><div style="font-size:20px;color:var(--muted);margin-top:4px">【label1】</div></div>
      <div style="color:rgba(212,168,67,.4);font-size:26px;font-weight:900">──────▶</div>
      <div style="text-align:center"><div style="font-size:56px">【emoji2】</div><div style="font-size:20px;color:var(--muted);margin-top:4px">【label2】</div></div>
      <div style="color:rgba(212,168,67,.4);font-size:26px;font-weight:900">──────▶</div>
      <div style="text-align:center"><div style="font-size:56px">【emoji3】</div><div style="font-size:20px;color:var(--muted);margin-top:4px">【label3】</div></div>
      <div style="color:rgba(212,168,67,.4);font-size:26px;font-weight:900">──────▶</div>
      <div style="text-align:center"><div style="font-size:56px">【emoji4】</div><div style="font-size:20px;color:var(--muted);margin-top:4px">【label4】</div></div>
    </div>
  </div>

  <!-- 中段：Hero 主内容（flex:1 吃满剩余空间） -->
  <!-- ✅ 不用 margin-top；用 justify-content:center 在 flex:1 内部垂直居中 -->
  <div class="col f1" style="align-items:center;text-align:center;justify-content:center;gap:14px">
    <div class="chip ch-g" style="font-size:22px;padding:8px 28px">【badge 文字】</div>
    <!-- 主标题：190px，1~2 行 -->
    <div style="font-size:190px;font-weight:900;line-height:.95;letter-spacing:-6px;background:linear-gradient(135deg,var(--accent-a) 0%,var(--accent-al) 45%,var(--accent-b) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">【主标题】</div>
    <!-- 副标题：72px -->
    <div style="font-size:72px;font-weight:800;color:var(--cream);letter-spacing:2px">【副标题】</div>
    <!-- 说明文字：40px，max-width 限制行宽 -->
    <div style="font-size:40px;color:var(--muted);max-width:1300px;line-height:1.5">【1~2 句说明，可用 strong 高亮关键词】</div>
  </div>

  <!-- 下段：Pill 卡 + 来源（IN FLOW，不用 position:absolute） -->
  <div class="col" style="gap:12px">
    <div class="row" style="gap:14px">
      <!-- 每个 pill flex:1，高度自然撑开，标题 36px -->
      <div class="g 【卡片主题 class】" style="flex:1;padding:22px 32px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px">
        <div style="font-size:44px">【emoji】</div>
        <div style="font-size:36px;font-weight:800;color:var(--accent-b)">【Pill 标题】</div>
        <div style="font-size:28px;color:var(--muted)">【副说明】</div>
      </div>
      <div class="g 【卡片主题 class】" style="flex:1;padding:22px 32px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px">
        <div style="font-size:44px">【emoji】</div>
        <div style="font-size:36px;font-weight:800;color:var(--accent-a)">【Pill 标题】</div>
        <div style="font-size:28px;color:var(--muted)">【副说明】</div>
      </div>
      <div class="g 【卡片主题 class】" style="flex:1;padding:22px 32px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px">
        <div style="font-size:44px">【emoji】</div>
        <div style="font-size:36px;font-weight:800;color:var(--sky)">【Pill 标题】</div>
        <div style="font-size:28px;color:var(--muted)">【副说明】</div>
      </div>
    </div>
    <!-- 来源行（IN FLOW） -->
    <div style="text-align:center;font-size:24px;color:rgba(240,232,208,.22);letter-spacing:4px">【来源说明】</div>
  </div>

</div><!-- /col f1 space-between -->
</div><!-- /slide -->
```

---

## 模板二：Split 左文右图

**高度预算**：左右各 flex:1，左列必须用 `justify-content:space-between` + 三段结构，绝不用 `center`。

**左列三段结构（撑满 1032px）**：
- 顶段：chip + 装饰线 + 主标题（~300px）
- 中段：body 正文（flex:1，自然撑满剩余）
- 底段：总结卡 / 金句（~120px）

```html
<div class="s" id="sN">
<div class="wa">【关键词】</div>
<div class="orb" style="..."></div>
<div class="animal-wm" style="...">【emoji】</div>

<div class="row f1" style="gap:28px;align-items:stretch">
  <!-- 左侧文字区：✅ space-between + 三段 -->
  <div class="col" style="flex:0 0 44%;justify-content:space-between;gap:0">

    <!-- 顶段：badge + 装饰线 + 主标题 -->
    <div class="col" style="gap:14px">
      <div class="chip 【class】">【badge】</div>
      <div style="height:3px;background:linear-gradient(90deg,var(--accent-a),var(--accent-b),transparent);border-radius:2px;width:160px"></div>
      <!-- 主标题：88px，允许 2 行 -->
      <div style="font-size:88px;font-weight:900;line-height:1.05">【标题 1~2 行】</div>
    </div>

    <!-- 中段：body，flex:1 吃满空间 -->
    <!-- ✅ 正文 ≥ 4 行，用 margin-top 分组，禁用 <br> 空行 -->
    <div style="font-size:40px;color:var(--muted);line-height:1.65;flex:1;display:flex;flex-direction:column;justify-content:center">
      【第 1 行，可 strong 高亮】<br>
      【第 2 行】<br>
      【第 3 行】<br>
      <div style="margin-top:18px">
        <strong style="color:var(--cream)">【强调结论行 1】</strong><br>
        <strong style="color:var(--cream)">【强调结论行 2】</strong>
      </div>
    </div>

    <!-- 底段：总结卡（始终存在，撑到底部） -->
    <div class="g 【class】" style="padding:22px 26px">
      <div style="font-size:34px;font-weight:800;color:var(--accent-b);margin-bottom:10px">【小标题】</div>
      <div style="font-size:32px;color:var(--muted);line-height:1.6">【3 条要点，每条 ≤ 16 汉字】</div>
    </div>

  </div>

  <!-- 右侧图形区：flex:1，居中 -->
  <div class="f1 col" style="justify-content:center;align-items:center">
    <svg viewBox="0 0 660 680" style="width:100%;max-height:960px">
      【SVG 图形内容】
    </svg>
  </div>
</div>
</div>
```

---

## 模板三：全屏 Grid 2×2（无 header）

**高度预算**：`display:grid;grid-template-rows:1fr 1fr` 强制两行等高，无任何 header 行压缩空间。每格约 505px 高，内容轻松填满。

**禁止**：在此模板外层再加任何 `<div class="col f1">` + header。

```html
<div class="s" id="sN">
<div class="wa">【关键词】</div>
<div class="orb" style="..."></div>
<div class="animal-wm" style="...">【emoji】</div>

<!-- ✅ grid 直接是 .s 的 flex 子元素，flex:1 吃满全部高度 -->
<div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px;flex:1;width:100%">

  <!-- 每格：emoji 84px + 标题 52px + 正文 38px，合计约 340px，格子 505px，填充 67% + padding -->
  <div class="g 【主题 class】" style="padding:32px 36px;display:flex;align-items:flex-start;gap:22px">
    <div style="font-size:84px;line-height:1;flex-shrink:0">【emoji】</div>
    <div>
      <div style="font-size:52px;font-weight:900;color:【颜色】;margin-bottom:10px">【格子标题】</div>
      <div style="font-size:38px;color:var(--muted);line-height:1.55">【说明，2~3 行，strong 高亮】</div>
    </div>
  </div>

  <div class="g 【主题 class】" style="padding:32px 36px;display:flex;align-items:flex-start;gap:22px">
    <div style="font-size:84px;line-height:1;flex-shrink:0">【emoji】</div>
    <div>
      <div style="font-size:52px;font-weight:900;color:【颜色】;margin-bottom:10px">【格子标题】</div>
      <div style="font-size:38px;color:var(--muted);line-height:1.55">【说明，2~3 行，strong 高亮】</div>
    </div>
  </div>

  <div class="g 【主题 class】" style="padding:32px 36px;display:flex;align-items:flex-start;gap:22px">
    <div style="font-size:84px;line-height:1;flex-shrink:0">【emoji】</div>
    <div>
      <div style="font-size:52px;font-weight:900;color:【颜色】;margin-bottom:10px">【格子标题】</div>
      <div style="font-size:38px;color:var(--muted);line-height:1.55">【说明，2~3 行，strong 高亮】</div>
    </div>
  </div>

  <div class="g 【主题 class】" style="padding:32px 36px;display:flex;align-items:flex-start;gap:22px">
    <div style="font-size:84px;line-height:1;flex-shrink:0">【emoji】</div>
    <div>
      <div style="font-size:52px;font-weight:900;color:【颜色】;margin-bottom:10px">【格子标题】</div>
      <div style="font-size:38px;color:var(--muted);line-height:1.55">【说明，2~3 行，strong 高亮】</div>
    </div>
  </div>

</div><!-- /grid -->
</div><!-- /slide -->
```

---

## 模板四：Slim Header + 两大数字卡

**高度预算**：
- slim header（inline 一行）：~80px
- gap：14px
- 两大数字卡（`flex:1 row`）：~938px
- 总计：~1032px ✓

```html
<div class="s" id="sN">
<div class="wa">【关键词】</div>
<div class="orb" style="..."></div>
<div class="animal-wm" style="...">【emoji】</div>

<div class="col f1" style="gap:14px">

  <!-- ✅ Slim header：badge + 标题 + 说明 全部同行，约 80px 高 -->
  <div class="row g" style="align-items:center;gap:20px;padding:16px 28px;flex-shrink:0">
    <div class="chip 【class】" style="flex-shrink:0">【badge】</div>
    <div style="font-size:64px;font-weight:900;line-height:1;flex:1">【页面标题】</div>
    <div style="font-size:30px;color:var(--muted);text-align:right;flex-shrink:0;line-height:1.4">【2 行辅助说明】</div>
  </div>

  <!-- 两大数字卡（flex:1 row 吃满剩余高度） -->
  <div class="row f1" style="gap:14px">
    <div class="g g-hi f1" style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;gap:14px">
      <div style="font-size:28px;color:var(--muted);letter-spacing:2px;font-weight:700">【指标名称】</div>
      <!-- 超大数字：170px -->
      <div style="font-size:170px;font-weight:900;line-height:1;background:linear-gradient(135deg,var(--accent-a),var(--accent-al),var(--accent-b));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">【数字】</div>
      <div style="font-size:40px;color:var(--muted);font-weight:700">【涵义，如"↓ 大幅下降"】</div>
      <div style="height:1px;width:80%;background:linear-gradient(90deg,transparent,rgba(212,168,67,.2),transparent)"></div>
      <div style="font-size:32px;color:var(--muted);text-align:center;line-height:1.55">【2 行解释】</div>
    </div>

    <div class="g g-hi f1" style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;gap:14px">
      <div style="font-size:28px;color:var(--muted);letter-spacing:2px;font-weight:700">【指标名称】</div>
      <div style="font-size:170px;font-weight:900;line-height:1;background:linear-gradient(135deg,var(--accent-al),var(--accent-c));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">【数字】</div>
      <div style="font-size:40px;color:var(--muted);font-weight:700">【涵义】</div>
      <div style="height:1px;width:80%;background:linear-gradient(90deg,transparent,rgba(212,168,67,.2),transparent)"></div>
      <div style="font-size:32px;color:var(--muted);text-align:center;line-height:1.55">【2 行解释】</div>
    </div>
  </div>

</div>
</div>
```

---

## 模板五：两大卡并排（拆分内容，2 项/页）

**高度预算**：
- slim header：~80px
- gap：14px
- 两大卡（`flex:1 row`）：~938px（或去掉 header 则全部给大卡）
- 总计：~1032px ✓
- 每张卡宽 ~913px、高 ~938px，内容极度充裕

```html
<div class="s" id="sN">
<div class="wa">【关键词】</div>
<div class="orb" style="..."></div>
<div class="animal-wm" style="...">【emoji】</div>

<div class="col f1" style="gap:14px">
  <!-- slim header -->
  <div class="row g" style="align-items:center;gap:20px;padding:14px 26px;flex-shrink:0">
    <div class="chip 【class】" style="flex-shrink:0">【badge】</div>
    <div style="font-size:60px;font-weight:900;line-height:1;flex:1">【页面标题】</div>
    <div style="font-size:26px;color:var(--muted);flex-shrink:0;font-weight:700">【如 "1/2"】</div>
  </div>

  <!-- 两大卡（flex:1 吃满剩余高度） -->
  <div class="row f1" style="gap:14px">
    <div class="g 【class】 f1" style="padding:44px 48px;display:flex;flex-direction:column;justify-content:center">
      <!-- emoji: 100px -->
      <div style="font-size:100px;margin-bottom:20px;line-height:1">【emoji】</div>
      <!-- 卡片标题: 60px -->
      <div style="font-size:60px;font-weight:900;color:【颜色】;margin-bottom:18px">【卡片标题】</div>
      <!-- 正文: 40px，4~5 行 -->
      <div style="font-size:40px;color:var(--muted);line-height:1.65">
        【第 1 行，可用 strong 高亮】<br>
        【第 2 行】<br>
        【第 3 行】<br>
        <br>
        <strong style="color:【高亮色】">【强调结论 1~2 行】</strong>
      </div>
    </div>

    <div class="g 【class】 f1" style="padding:44px 48px;display:flex;flex-direction:column;justify-content:center">
      <div style="font-size:100px;margin-bottom:20px;line-height:1">【emoji】</div>
      <div style="font-size:60px;font-weight:900;color:【颜色】;margin-bottom:18px">【卡片标题】</div>
      <div style="font-size:40px;color:var(--muted);line-height:1.65">
        【第 1 行】<br>
        【第 2 行】<br>
        【第 3 行】<br>
        <br>
        <strong style="color:【高亮色】">【强调结论】</strong>
      </div>
    </div>
  </div>
</div>
</div>
```

---

## AI 生成 Checklist（每页生成后必须验证）

```
□ 1. 页面内无 position:absolute 定位的内容区（orb/watermark 除外）
□ 2. 内容全部在文档流中，由 flexbox/grid 分配空间
□ 3. Cover 用 justify-content:space-between，三段全在流中
□ 4. Grid 2×2 直接是 flex 子元素，无外层 header div
□ 5. Slim header 仅一行（badge + 标题 + 辅助文字同行）
□ 6. 卡片标题 ≥ 52px，卡片正文 ≥ 38px，Cover pill 标题 ≥ 36px
□ 7. 任何正文（说明、注释）≥ 28px，无例外
□ 8. .wa 存在且包含该页口播关键词
□ 9. 若内容感觉"撑不满"：先加大字号，再考虑拆页
□ 10. 无动画、无 transition（截图是静态的）
```
