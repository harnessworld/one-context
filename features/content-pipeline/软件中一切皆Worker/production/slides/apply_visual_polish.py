# -*- coding: utf-8 -*-
"""Larger type + less whitespace + more inline SVG for video readability. UTF-8 safe."""
from pathlib import Path

base = Path("features/content-pipeline")
dst = None
for d in base.iterdir():
    if not d.is_dir() or "Worker" not in d.name:
        continue
    p = d / "production/slides/presentation.html"
    if p.exists():
        dst = p
        break
assert dst, "presentation.html not found"

t = dst.read_text(encoding="utf-8")

subs = [
(
  ".slide{position:absolute;inset:0;width:100%;height:100%;flex-shrink:0;padding:6vh 6vw 10vh 6vw;display:flex;flex-direction:column;overflow:hidden}",
  ".slide{position:absolute;inset:0;width:100%;height:100%;flex-shrink:0;padding:4.5vh 5vw 7vh 5vw;display:flex;flex-direction:column;overflow:hidden}",
),
(
  ".body-zh{font-family:var(--sans-zh);font-weight:400;font-size:max(17px,1.35vw);line-height:1.75;opacity:.82;letter-spacing:.01em}",
  ".body-zh{font-family:var(--sans-zh);font-weight:500;font-size:clamp(26px,1.95vw,46px);line-height:1.48;opacity:.9;letter-spacing:.01em}",
),
(
  ".body-serif{font-family:var(--serif-zh);font-weight:400;font-size:max(15px,1.3vw);line-height:1.65;opacity:.88}",
  ".body-serif{font-family:var(--serif-zh);font-weight:400;font-size:clamp(22px,1.75vw,40px);line-height:1.55;opacity:.9}",
),
(
  ".lead{font-family:var(--serif-zh);font-weight:400;font-size:1.9vw;line-height:1.4;opacity:.85}",
  ".lead{font-family:var(--serif-zh);font-weight:400;font-size:clamp(22px,2.15vw,40px);line-height:1.42;opacity:.88}",
),
(
  ".stat .l{font-family:var(--sans-zh);font-size:max(13px,1.05vw);opacity:.7;margin-top:1vh;font-weight:400;line-height:1.5}",
  ".stat .l{font-family:var(--sans-zh);font-size:clamp(18px,1.35vw,30px);opacity:.78;margin-top:1vh;font-weight:500;line-height:1.45}",
),
(
  ".callout{padding:3vh 2.4vw;border-left:3px solid currentColor;position:relative;font-family:var(--serif-zh);font-size:max(15px,1.2vw);line-height:1.55;opacity:.92}",
  ".callout{padding:2.6vh 2.2vw;border-left:3px solid currentColor;position:relative;font-family:var(--serif-zh);font-size:clamp(20px,1.55vw,36px);line-height:1.45;opacity:.94}",
),
(
  ".callout .q-big{font-family:var(--serif-zh);font-weight:600;font-size:max(17px,1.6vw);line-height:1.42}",
  ".callout .q-big{font-family:var(--serif-zh);font-weight:600;font-size:clamp(24px,2vw,40px);line-height:1.35}",
),
(
  ".rowline .k{font-family:var(--serif-zh);font-weight:700;font-size:1.7vw}",
  ".rowline .k{font-family:var(--serif-zh);font-weight:700;font-size:clamp(22px,2.2vw,38px)}",
),
(
  ".rowline .v{font-family:var(--sans-zh);font-weight:400;font-size:max(14px,1.2vw);opacity:.85;line-height:1.55}",
  ".rowline .v{font-family:var(--sans-zh);font-weight:400;font-size:clamp(20px,1.55vw,34px);opacity:.88;line-height:1.45}",
),
(
  ".pillar .t{font-family:var(--serif-zh);font-weight:700;font-size:2.4vw;line-height:1.1}",
  ".pillar .t{font-family:var(--serif-zh);font-weight:700;font-size:clamp(26px,2.85vw,48px);line-height:1.12}",
),
(
  ".pillar .d{font-family:var(--sans-zh);font-weight:400;font-size:max(16px,1.2vw);opacity:.76;line-height:1.6}",
  ".pillar .d{font-family:var(--sans-zh);font-weight:400;font-size:clamp(20px,1.65vw,36px);opacity:.82;line-height:1.48}",
),
(
  """  .h-md{
    font-family:var(--serif-zh);
    font-weight:600;
    font-size:2.3vw;
    line-height:1.3;
  }""",
  """  .h-md{
    font-family:var(--serif-zh);
    font-weight:600;
    font-size:clamp(28px,2.75vw,52px);
    line-height:1.22;
  }""",
),
(
  """  .lead{
    font-family:var(--serif-zh);
    font-weight:400;
    font-size:1.75vw;
    line-height:1.5;
    opacity:.86;
  }""",
  """  .lead{
    font-family:var(--serif-zh);
    font-weight:400;
    font-size:clamp(22px,2.05vw,40px);
    line-height:1.42;
    opacity:.88;
  }""",
),
(
  """  .step-title{
    font-family:var(--sans-zh);
    font-weight:700;
    font-size:1.55vw;
    letter-spacing:.01em;
    line-height:1.2;
  }
  .step-desc{
    font-family:var(--sans-zh);
    font-weight:400;
    font-size:max(14px,1.08vw);
    line-height:1.45;
    opacity:.72;
  }""",
  """  .step-title{
    font-family:var(--sans-zh);
    font-weight:700;
    font-size:clamp(22px,1.95vw,38px);
    letter-spacing:.01em;
    line-height:1.2;
  }
  .step-desc{
    font-family:var(--sans-zh);
    font-weight:400;
    font-size:clamp(18px,1.45vw,30px);
    line-height:1.42;
    opacity:.82;
  }""",
),
(
  "  .pillar-page .grid-4{flex:1;min-height:0;align-content:stretch;gap:3vh 5vw}",
  """  .pillar-page .grid-4{flex:1;min-height:0;align-content:stretch;gap:3vh 5vw}
  .viz-box{flex:1 1 0;min-height:min(36vh,380px);width:100%;display:flex;align-items:center;justify-content:center;margin-top:.6vh}
  .viz-box.compact{min-height:min(30vh,320px)}
  .viz-box svg{width:100%;height:auto;max-height:38vh;display:block}
  .frame-grow{flex:1;min-height:0;display:flex;flex-direction:column;gap:1.6vh}""",
),
]

for a, b in subs:
    if a not in t:
        raise SystemExit(f"MISSING FRAGMENT:\n{a[:120]}…")
    t = t.replace(a, b, 1)

OLD_S1 = """<section class="slide s light" id="s1">
  <div class="chrome"><div>开篇</div><div>02 / 15</div></div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker">为什么现在必须谈后端</div>
    <h2 class="h-xl">Agent 系统的复杂度爆炸</h2>
    <p class="lead" style="margin-bottom:4vh">AI Agent 正在重塑软件边界；难点在编排、状态与可观测性，而不是单次推理。</p>
    <div class="grid-4">
      <div class="pillar"><span class="ic">①</span><div class="t">复杂度指数上升</div><div class="d">链路更长、故障面更广</div></div>
      <div class="pillar"><span class="ic">②</span><div class="t">Harness 理念</div><div class="d">统一运行时与语义</div></div>
      <div class="pillar"><span class="ic">③</span><div class="t">生产困境</div><div class="d">真实业务里的失控感</div></div>
      <div class="pillar"><span class="ic">④</span><div class="t">本期脉络</div><div class="d">误区 → 本质 → 演进</div></div>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Intro</div></div>
  <span class="wa">我们先从复杂度爆炸与 Harness 理念谈起</span>
</section>"""

NEW_S1 = """<section class="slide s light" id="s1">
  <div class="chrome"><div>开篇</div><div>02 / 15</div></div>
  <div class="frame frame-grow" style="padding-top:2vh">
    <div class="kicker">为什么现在必须谈后端</div>
    <h2 class="h-xl">Agent 系统的复杂度爆炸</h2>
    <p class="lead" style="margin-bottom:1vh">AI Agent 正在重塑软件边界；难点在编排、状态与可观测性，而不是单次推理。</p>
    <div class="viz-box compact" aria-hidden="true">
      <svg viewBox="0 0 920 220" preserveAspectRatio="xMidYMid meet">
        <defs><marker id="arrV1" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#0a0a0b"/></marker></defs>
        <rect x="20" y="40" width="160" height="120" rx="12" fill="rgba(10,10,11,.07)" stroke="#0a0a0b" stroke-width="2"/>
        <text x="100" y="105" text-anchor="middle" font-size="26" font-weight="700" fill="#0a0a0b">单次推理</text>
        <text x="100" y="138" text-anchor="middle" font-size="22" fill="#18181a">模型调用</text>
        <line x1="190" y1="100" x2="248" y2="100" stroke="#0a0a0b" stroke-width="2" marker-end="url(#arrV1)"/>
        <rect x="260" y="25" width="200" height="150" rx="12" fill="rgba(10,10,11,.09)" stroke="#0a0a0b" stroke-width="2.5"/>
        <text x="360" y="78" text-anchor="middle" font-size="28" font-weight="800" fill="#0a0a0b">Agent 系统</text>
        <text x="360" y="118" text-anchor="middle" font-size="22" fill="#18181a">编排 · 状态 · 观测</text>
        <text x="360" y="152" text-anchor="middle" font-size="22" fill="#18181a">故障面指数放大</text>
        <line x1="468" y1="100" x2="528" y2="100" stroke="#0a0a0b" stroke-width="2" marker-end="url(#arrV1)"/>
        <rect x="540" y="40" width="170" height="120" rx="12" fill="rgba(10,10,11,.06)" stroke="#0a0a0b" stroke-width="2"/>
        <text x="625" y="92" text-anchor="middle" font-size="24" font-weight="700" fill="#0a0a0b">Harness</text>
        <text x="625" y="128" text-anchor="middle" font-size="22" fill="#18181a">统一语义</text>
        <line x1="718" y1="100" x2="778" y2="100" stroke="#0a0a0b" stroke-width="2" marker-end="url(#arrV1)"/>
        <rect x="790" y="50" width="120" height="100" rx="10" fill="rgba(10,10,11,.12)" stroke="#0a0a0b" stroke-width="2"/>
        <text x="850" y="112" text-anchor="middle" font-size="24" font-weight="700" fill="#0a0a0b">生产</text>
      </svg>
    </div>
    <div class="grid-4" style="flex:1;min-height:0;margin-top:1vh">
      <div class="pillar"><span class="ic">①</span><div class="t">复杂度指数上升</div><div class="d">链路更长、故障面更广</div></div>
      <div class="pillar"><span class="ic">②</span><div class="t">Harness 理念</div><div class="d">统一运行时与语义</div></div>
      <div class="pillar"><span class="ic">③</span><div class="t">生产困境</div><div class="d">真实业务里的失控感</div></div>
      <div class="pillar"><span class="ic">④</span><div class="t">本期脉络</div><div class="d">误区 → 本质 → 演进</div></div>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Intro</div></div>
  <span class="wa">我们先从复杂度爆炸与 Harness 理念谈起</span>
</section>"""

OLD_S2_COL = """    <div class="col" style="gap:2.4vh">
      <div class="tag">现实</div>
      <p class="body-zh">难点在任务编排、状态、流程与可观测性；模型只是零件，<span class="hi">后端才是系统</span>。</p>
      <div class="rule" style="margin:2vh 0"></div>
      <p class="body-zh" style="opacity:.78;font-size:max(16px,1.22vw)">→ 编排与状态管理 · → 可观测与排障 · → 发布与治理同样消耗脑力</p>
    </div>"""

NEW_S2_COL = """    <div class="col" style="gap:2vh;flex:1;min-height:0">
      <div class="tag">现实</div>
      <p class="body-zh">难点在任务编排、状态、流程与可观测性；模型只是零件，<span class="hi">后端才是系统</span>。</p>
      <div class="viz-box compact" style="margin-top:1vh;min-height:min(28vh,300px)" aria-hidden="true">
        <svg viewBox="0 0 640 280" preserveAspectRatio="xMidYMid meet">
          <defs><marker id="arrV2" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="rgba(241,239,234,.75)"/></marker></defs>
          <rect x="40" y="30" width="240" height="200" rx="14" fill="rgba(241,239,234,.07)" stroke="rgba(241,239,234,.5)" stroke-width="2"/>
          <text x="160" y="95" text-anchor="middle" fill="rgba(241,239,234,.95)" font-size="30" font-weight="700">「推理」</text>
          <text x="160" y="135" text-anchor="middle" fill="rgba(241,239,234,.78)" font-size="24">模型 / Prompt</text>
          <text x="160" y="185" text-anchor="middle" fill="rgba(241,239,234,.55)" font-size="22">仅占一层</text>
          <path d="M290 140 L330 140" stroke="rgba(241,239,234,.6)" stroke-width="3" marker-end="url(#arrV2)"/>
          <rect x="340" y="20" width="260" height="230" rx="14" fill="rgba(241,239,234,.09)" stroke="rgba(241,239,234,.55)" stroke-width="2.5"/>
          <text x="470" y="65" text-anchor="middle" fill="rgba(241,239,234,.95)" font-size="30" font-weight="800">「系统」</text>
          <text x="470" y="108" text-anchor="middle" fill="rgba(241,239,234,.82)" font-size="24">编排 · 状态机</text>
          <text x="470" y="148" text-anchor="middle" fill="rgba(241,239,234,.82)" font-size="24">Tracing · SLO</text>
          <text x="470" y="188" text-anchor="middle" fill="rgba(241,239,234,.82)" font-size="24">发布 · 治理 · 成本</text>
          <text x="470" y="232" text-anchor="middle" fill="rgba(241,239,234,.6)" font-size="22">后端承载主体复杂度</text>
        </svg>
      </div>
      <div class="rule" style="margin:1vh 0"></div>
      <p class="body-zh" style="opacity:.84;font-size:clamp(22px,1.65vw,38px)">编排与状态 · 可观测与排障 · 发布与治理 —— 同样消耗主力脑力</p>
    </div>"""

OLD_S3_TOP = """  <div class="frame pillar-page" style="padding-top:3vh">
    <div class="kicker">协作成本</div>
    <h2 class="h-xl">多 Agent = 天然提效？</h2>
    <div class="grid-4" style="margin-top:3vh">"""

NEW_S3_TOP = """  <div class="frame pillar-page frame-grow" style="padding-top:2vh">
    <div class="kicker">协作成本</div>
    <h2 class="h-xl">多 Agent = 天然提效？</h2>
    <div class="viz-box compact" aria-hidden="true">
      <svg viewBox="0 0 880 200" preserveAspectRatio="xMidYMid meet">
        <circle cx="440" cy="100" r="28" fill="rgba(10,10,11,.12)" stroke="#0a0a0b" stroke-width="2"/>
        <text x="440" y="108" text-anchor="middle" font-size="22" font-weight="700" fill="#0a0a0b">任务</text>
        <circle cx="220" cy="55" r="52" fill="none" stroke="#0a0a0b" stroke-width="1.8" stroke-dasharray="6 4" opacity=".45"/>
        <circle cx="660" cy="55" r="52" fill="none" stroke="#0a0a0b" stroke-width="1.8" stroke-dasharray="6 4" opacity=".45"/>
        <circle cx="220" cy="145" r="52" fill="none" stroke="#0a0a0b" stroke-width="1.8" stroke-dasharray="6 4" opacity=".45"/>
        <circle cx="660" cy="145" r="52" fill="none" stroke="#0a0a0b" stroke-width="1.8" stroke-dasharray="6 4" opacity=".45"/>
        <rect x="188" y="28" width="64" height="54" rx="8" fill="rgba(10,10,11,.08)" stroke="#0a0a0b"/>
        <text x="220" y="62" text-anchor="middle" font-size="20" font-weight="700" fill="#0a0a0b">A1</text>
        <rect x="628" y="28" width="64" height="54" rx="8" fill="rgba(10,10,11,.08)" stroke="#0a0a0b"/>
        <text x="660" y="62" text-anchor="middle" font-size="20" font-weight="700" fill="#0a0a0b">A2</text>
        <rect x="188" y="118" width="64" height="54" rx="8" fill="rgba(10,10,11,.08)" stroke="#0a0a0b"/>
        <text x="220" y="152" text-anchor="middle" font-size="20" font-weight="700" fill="#0a0a0b">A3</text>
        <rect x="628" y="118" width="64" height="54" rx="8" fill="rgba(10,10,11,.08)" stroke="#0a0a0b"/>
        <text x="660" y="152" text-anchor="middle" font-size="20" font-weight="700" fill="#0a0a0b">A4</text>
        <path d="M272 75 Q356 40 400 88" fill="none" stroke="#0a0a0b" stroke-width="1.5" opacity=".35"/>
        <path d="M608 75 Q524 40 480 88" fill="none" stroke="#0a0a0b" stroke-width="1.5" opacity=".35"/>
        <path d="M272 125 Q356 160 400 112" fill="none" stroke="#0a0a0b" stroke-width="1.5" opacity=".35"/>
        <path d="M608 125 Q524 160 480 112" fill="none" stroke="#0a0a0b" stroke-width="1.5" opacity=".35"/>
        <text x="440" y="188" text-anchor="middle" font-size="22" fill="#18181a" opacity=".85">连线越多 · 同步越贵 · 排障越难</text>
      </svg>
    </div>
    <div class="grid-4" style="margin-top:1vh;flex:1;min-height:0">"""

OLD_S5 = """<section class="slide s light" id="s5">
  <div class="chrome"><div>痛点</div><div>06 / 15</div></div>
  <div class="frame grid-2-6-6" style="padding-top:5vh">
    <div>
      <div class="kicker">表面</div>
      <h2 class="h-md">集成很忙</h2>
      <p class="body-zh">外部对接、胶水代码、联调与协议适配……时间被占满。</p>
    </div>
    <div>
      <div class="kicker">真正要命</div>
      <h2 class="h-md">内部混乱</h2>
      <p class="body-zh">Agent 内部状态与流程失控；边界不清、重试补偿混乱；缺少统一语义与 Tracing——<span class="hi">比集成更致命</span>。</p>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Risk</div></div>
  <span class="wa">很多人盯着集成难题，内部混乱更要命</span>
</section>"""

NEW_S5 = """<section class="slide s light" id="s5">
  <div class="chrome"><div>痛点</div><div>06 / 15</div></div>
  <div class="frame frame-grow" style="padding-top:2vh">
    <div class="grid-2-6-6" style="flex:0 0 auto">
      <div>
        <div class="kicker">表面</div>
        <h2 class="h-md">集成很忙</h2>
        <p class="body-zh">外部对接、胶水代码、联调与协议适配……时间被占满。</p>
      </div>
      <div>
        <div class="kicker">真正要命</div>
        <h2 class="h-md">内部混乱</h2>
        <p class="body-zh">Agent 内部状态与流程失控；边界不清、重试补偿混乱；缺少统一语义与 Tracing——<span class="hi">比集成更致命</span>。</p>
      </div>
    </div>
    <div class="viz-box" style="flex:1;margin-top:1vh" aria-hidden="true">
      <svg viewBox="0 0 900 260" preserveAspectRatio="xMidYMid meet">
        <path d="M450 28 L720 240 L180 240 Z" fill="rgba(10,10,11,.06)" stroke="#0a0a0b" stroke-width="2"/>
        <text x="450" y="68" text-anchor="middle" font-size="24" font-weight="700" fill="#0a0a0b">水面 · 看得见的集成</text>
        <text x="450" y="210" text-anchor="middle" font-size="28" font-weight="800" fill="#0a0a0b">水下 · 状态 / 重试 / 观测</text>
        <text x="450" y="246" text-anchor="middle" font-size="22" fill="#18181a">体积更大 · 也更致命</text>
        <line x1="120" y1="120" x2="780" y2="120" stroke="#0a0a0b" stroke-width="1.5" stroke-dasharray="8 6" opacity=".5"/>
        <text x="130" y="112" font-size="20" fill="#18181a">API 胶水</text>
      </svg>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Risk</div></div>
  <span class="wa">很多人盯着集成难题，内部混乱更要命</span>
</section>"""

OLD_S6_MID = """    <div class="grid-3">
      <div class="stat"><span class="m">Unified</span><span class="n">1 套语义</span><span class="l">调度、观测、排障对齐</span></div>
      <div class="stat"><span class="m">Scale</span><span class="n">水平扩展</span><span class="l">动态扩缩与治理一体化</span></div>
      <div class="stat"><span class="m">Interop</span><span class="n">多语言</span><span class="l">Function 边界清晰可替换</span></div>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Features</div></div>"""

NEW_S6_MID = """    <div class="grid-3">
      <div class="stat"><span class="m">Unified</span><span class="n">1 套语义</span><span class="l">调度、观测、排障对齐</span></div>
      <div class="stat"><span class="m">Scale</span><span class="n">水平扩展</span><span class="l">动态扩缩与治理一体化</span></div>
      <div class="stat"><span class="m">Interop</span><span class="n">多语言</span><span class="l">Function 边界清晰可替换</span></div>
    </div>
    <div class="viz-box compact" style="margin-top:1vh" aria-hidden="true">
      <svg viewBox="0 0 900 200" preserveAspectRatio="xMidYMid meet">
        <defs><marker id="arrV6" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="rgba(241,239,234,.8)"/></marker></defs>
        <rect x="40" y="50" width="220" height="110" rx="12" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.45)" stroke-width="2"/>
        <text x="150" y="108" text-anchor="middle" fill="rgba(241,239,234,.92)" font-size="26" font-weight="700">统一语义</text>
        <text x="150" y="138" text-anchor="middle" fill="rgba(241,239,234,.65)" font-size="22">调度观测同源</text>
        <line x1="270" y1="105" x2="330" y2="105" stroke="rgba(241,239,234,.5)" stroke-width="2" marker-end="url(#arrV6)"/>
        <rect x="340" y="40" width="220" height="130" rx="12" fill="rgba(241,239,234,.1)" stroke="rgba(241,239,234,.5)" stroke-width="2.5"/>
        <text x="450" y="95" text-anchor="middle" fill="rgba(241,239,234,.95)" font-size="28" font-weight="800">水平扩展</text>
        <text x="450" y="130" text-anchor="middle" fill="rgba(241,239,234,.72)" font-size="22">Worker 网格</text>
        <text x="450" y="158" text-anchor="middle" fill="rgba(241,239,234,.72)" font-size="22">配额 · 治理</text>
        <line x1="570" y1="105" x2="630" y2="105" stroke="rgba(241,239,234,.5)" stroke-width="2" marker-end="url(#arrV6)"/>
        <rect x="640" y="50" width="220" height="110" rx="12" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.45)" stroke-width="2"/>
        <text x="750" y="108" text-anchor="middle" fill="rgba(241,239,234,.92)" font-size="26" font-weight="700">多语言</text>
        <text x="750" y="138" text-anchor="middle" fill="rgba(241,239,234,.65)" font-size="22">Function 边界</text>
      </svg>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Features</div></div>"""

OLD_S7 = """<section class="slide s light" id="s7">
  <div class="chrome"><div>对比</div><div>08 / 15</div></div>
  <div class="frame compare-3 frame-fill" style="padding-top:3vh">
    <div class="callout" style="flex:1;justify-content:center;display:flex;flex-direction:column;gap:1.6vh;padding:3vh 2.4vw">
      <div class="kicker">传统</div>
      <p class="body-zh">Agent 与业务两套语言；桥接厚重；Tracing 割裂；状态分散。</p>
      <p class="body-zh" style="opacity:.72;margin-top:auto">痛点：两套心智模型 + 观测割裂。</p>
    </div>
    <div class="compare-mid">VS</div>
    <div class="callout" style="flex:1;justify-content:center;display:flex;flex-direction:column;gap:1.6vh;padding:3vh 2.4vw">
      <div class="kicker">三模型</div>
      <p class="body-zh">Agent 与后端无缝融合；统一语义与全链路追踪；一切先落成 Worker 再组合。</p>
      <p class="body-zh" style="opacity:.72;margin-top:auto">收益：同一套运行时语义与治理面。</p>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Compare</div></div>
  <span class="wa">把 agent 与后端服务真正融在一起，复杂度才不再爆炸</span>
</section>"""

NEW_S7 = """<section class="slide s light" id="s7">
  <div class="chrome"><div>对比</div><div>08 / 15</div></div>
  <div class="frame frame-grow" style="padding-top:2vh">
    <div class="viz-box compact" style="min-height:min(22vh,240px);max-height:26vh" aria-hidden="true">
      <svg viewBox="0 0 800 140" preserveAspectRatio="xMidYMid meet">
        <rect x="40" y="35" width="300" height="80" rx="10" fill="rgba(10,10,11,.07)" stroke="#0a0a0b"/>
        <text x="190" y="72" text-anchor="middle" font-size="22" font-weight="700" fill="#0a0a0b">Agent 栈</text>
        <text x="190" y="100" text-anchor="middle" font-size="20" fill="#18181a">业务栈（割裂）</text>
        <text x="400" y="88" text-anchor="middle" font-size="36" font-weight="900" fill="#0a0a0b" opacity=".25">≠</text>
        <rect x="460" y="35" width="300" height="80" rx="10" fill="rgba(10,10,11,.1)" stroke="#0a0a0b" stroke-width="2"/>
        <text x="610" y="72" text-anchor="middle" font-size="22" font-weight="800" fill="#0a0a0b">W / T / F 一体</text>
        <text x="610" y="100" text-anchor="middle" font-size="20" fill="#18181a">同一运行时语义</text>
      </svg>
    </div>
    <div class="compare-3 frame-fill" style="flex:1;min-height:0;padding-top:1vh">
    <div class="callout" style="flex:1;justify-content:center;display:flex;flex-direction:column;gap:1.6vh;padding:3vh 2.4vw">
      <div class="kicker">传统</div>
      <p class="body-zh">Agent 与业务两套语言；桥接厚重；Tracing 割裂；状态分散。</p>
      <p class="body-zh" style="opacity:.72;margin-top:auto">痛点：两套心智模型 + 观测割裂。</p>
    </div>
    <div class="compare-mid">VS</div>
    <div class="callout" style="flex:1;justify-content:center;display:flex;flex-direction:column;gap:1.6vh;padding:3vh 2.4vw">
      <div class="kicker">三模型</div>
      <p class="body-zh">Agent 与后端无缝融合；统一语义与全链路追踪；一切先落成 Worker 再组合。</p>
      <p class="body-zh" style="opacity:.72;margin-top:auto">收益：同一套运行时语义与治理面。</p>
    </div>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Compare</div></div>
  <span class="wa">把 agent 与后端服务真正融在一起，复杂度才不再爆炸</span>
</section>"""

OLD_S9 = """  <div class="frame" style="padding-top:5vh">
    <h2 class="h-xl">AI 基础设施新范式</h2>
    <div class="pipeline-section"><div class="pipeline-label">三根支柱</div>
    <div class="pipeline" data-cols="3">
      <div class="step"><div class="step-nb">01</div><div class="step-title">统一调度</div><div class="step-desc">GPU/CPU 与队列策略可组合</div></div>
      <div class="step"><div class="step-nb">02</div><div class="step-title">统一观测</div><div class="step-desc">指标、日志、链路同源</div></div>
      <div class="step"><div class="step-nb">03</div><div class="step-title">统一治理</div><div class="step-desc">配额、审计、成本与合规</div></div>
    </div></div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Infra</div></div>"""

NEW_S9 = """  <div class="frame frame-grow" style="padding-top:2vh">
    <h2 class="h-xl">AI 基础设施新范式</h2>
    <div class="pipeline-section"><div class="pipeline-label">三根支柱</div>
    <div class="pipeline" data-cols="3">
      <div class="step"><div class="step-nb">01</div><div class="step-title">统一调度</div><div class="step-desc">GPU/CPU 与队列策略可组合</div></div>
      <div class="step"><div class="step-nb">02</div><div class="step-title">统一观测</div><div class="step-desc">指标、日志、链路同源</div></div>
      <div class="step"><div class="step-nb">03</div><div class="step-title">统一治理</div><div class="step-desc">配额、审计、成本与合规</div></div>
    </div></div>
    <div class="viz-box compact" style="flex:1;margin-top:1vh" aria-hidden="true">
      <svg viewBox="0 0 720 200" preserveAspectRatio="xMidYMid meet">
        <rect x="60" y="120" width="600" height="56" rx="10" fill="rgba(10,10,11,.08)" stroke="#0a0a0b"/>
        <text x="360" y="156" text-anchor="middle" font-size="24" font-weight="700" fill="#0a0a0b">平台平面 · 调度 / 观测 / 治理</text>
        <rect x="100" y="40" width="140" height="64" rx="8" fill="rgba(10,10,11,.06)" stroke="#0a0a0b"/>
        <text x="170" y="82" text-anchor="middle" font-size="22" font-weight="700" fill="#0a0a0b">GPU 队列</text>
        <rect x="290" y="40" width="140" height="64" rx="8" fill="rgba(10,10,11,.06)" stroke="#0a0a0b"/>
        <text x="360" y="82" text-anchor="middle" font-size="22" font-weight="700" fill="#0a0a0b">Tracing</text>
        <rect x="480" y="40" width="140" height="64" rx="8" fill="rgba(10,10,11,.06)" stroke="#0a0a0b"/>
        <text x="550" y="82" text-anchor="middle" font-size="22" font-weight="700" fill="#0a0a0b">配额审计</text>
        <line x1="170" y1="104" x2="170" y2="120" stroke="#0a0a0b" stroke-width="2"/>
        <line x1="360" y1="104" x2="360" y2="120" stroke="#0a0a0b" stroke-width="2"/>
        <line x1="550" y1="104" x2="550" y2="120" stroke="#0a0a0b" stroke-width="2"/>
      </svg>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Infra</div></div>"""

OLD_S10_MID = """    <div class="compare-mid">VS</div>
    <div style="gap:2vh">
      <div class="tag">厚 Harness</div>"""

NEW_S10_MID = """    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.8vh;min-width:10vw">
      <div class="compare-mid">VS</div>
      <svg viewBox="0 0 200 200" width="120" height="120" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
        <rect x="30" y="40" width="140" height="36" rx="6" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.5)"/>
        <rect x="30" y="118" width="140" height="52" rx="6" fill="rgba(241,239,234,.14)" stroke="rgba(241,239,234,.55)" stroke-width="2"/>
        <text x="100" y="64" text-anchor="middle" fill="rgba(241,239,234,.85)" font-size="18" font-weight="600">薄 · 壳层</text>
        <text x="100" y="150" text-anchor="middle" fill="rgba(241,239,234,.9)" font-size="18" font-weight="700">厚 · 策略堆叠</text>
      </svg>
    </div>
    <div style="gap:2vh">
      <div class="tag">厚 Harness</div>"""

OLD_S11_SVG = """        <text x="340" y="130" text-anchor="middle" font-size="28" font-weight="700" fill="#0a0a0b">Harness</text>
        <text x="340" y="180" text-anchor="middle" font-size="24" fill="#18181a">W / T / F</text>
        <text x="700" y="200" font-size="48" fill="#0a0a0b" font-weight="800">=</text>
        <rect x="800" y="60" width="520" height="200" rx="14" fill="rgba(10,10,11,.06)" stroke="rgba(10,10,11,.35)" stroke-width="2"/>
        <text x="1060" y="130" text-anchor="middle" font-size="28" font-weight="700" fill="#0a0a0b">业务后端</text>
        <text x="1060" y="180" text-anchor="middle" font-size="24" fill="#18181a">W / T / F</text>"""

NEW_S11_SVG = """        <text x="340" y="125" text-anchor="middle" font-size="34" font-weight="700" fill="#0a0a0b">Harness</text>
        <text x="340" y="175" text-anchor="middle" font-size="28" fill="#18181a">W / T / F</text>
        <text x="700" y="200" font-size="56" fill="#0a0a0b" font-weight="800">=</text>
        <rect x="800" y="60" width="520" height="200" rx="14" fill="rgba(10,10,11,.06)" stroke="rgba(10,10,11,.35)" stroke-width="2"/>
        <text x="1060" y="125" text-anchor="middle" font-size="34" font-weight="700" fill="#0a0a0b">业务后端</text>
        <text x="1060" y="175" text-anchor="middle" font-size="28" fill="#18181a">W / T / F</text>"""

OLD_S12 = """<section class="slide s dark" id="s12">
  <div class="chrome"><div>融合</div><div>13 / 15</div></div>
  <div class="frame" style="padding-top:5vh">
    <h2 class="h-xl">Harness 退居配置层</h2>
    <p class="lead">声明 Agent 与触发策略；后端实现 Function；平台统一发布、配额与审计——核心能力沉到 Worker 与 Function。</p>
    <div class="rowline" style="margin-top:4vh;border-top:0">
      <span class="k">配置</span><span class="v">Harness 配 Worker、配 Trigger</span><span class="m">YAML</span>
    </div>
    <div class="rowline">
      <span class="k">运行时</span><span class="v">统一 Worker 语义与观测</span><span class="m">Ops</span>
    </div>
    <div class="rowline">
      <span class="k">业务</span><span class="v">领域服务即 Function</span><span class="m">Code</span>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Fusion</div></div>
  <span class="wa">Harness 更像配置层，核心能力在 Worker 与 Function</span>
</section>"""

NEW_S12 = """<section class="slide s dark" id="s12">
  <div class="chrome"><div>融合</div><div>13 / 15</div></div>
  <div class="frame grid-2-8-4 frame-grow" style="padding-top:2vh;align-items:stretch">
    <div class="viz-box compact" style="min-height:min(52vh,520px);margin-top:0;justify-content:flex-start;padding-top:2vh">
      <svg viewBox="0 0 420 380" preserveAspectRatio="xMidYMid meet" style="max-height:52vh">
        <defs><marker id="arrV12" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="rgba(241,239,234,.75)"/></marker></defs>
        <text x="210" y="28" text-anchor="middle" fill="rgba(241,239,234,.55)" font-size="18" font-family="IBM Plex Mono,monospace">STACK</text>
        <rect x="60" y="44" width="300" height="70" rx="10" fill="rgba(241,239,234,.07)" stroke="rgba(241,239,234,.45)"/>
        <text x="210" y="88" text-anchor="middle" fill="rgba(241,239,234,.92)" font-size="24" font-weight="700">配置 · Harness</text>
        <line x1="210" y1="114" x2="210" y2="132" stroke="rgba(241,239,234,.45)" stroke-width="2" marker-end="url(#arrV12)"/>
        <rect x="40" y="136" width="340" height="86" rx="10" fill="rgba(241,239,234,.1)" stroke="rgba(241,239,234,.5)" stroke-width="2"/>
        <text x="210" y="178" text-anchor="middle" fill="rgba(241,239,234,.95)" font-size="26" font-weight="800">运行时 · Worker 语义</text>
        <text x="210" y="208" text-anchor="middle" fill="rgba(241,239,234,.68)" font-size="22">观测 · 调度 · 配额</text>
        <line x1="210" y1="222" x2="210" y2="248" stroke="rgba(241,239,234,.45)" stroke-width="2" marker-end="url(#arrV12)"/>
        <rect x="60" y="252" width="300" height="90" rx="10" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.45)"/>
        <text x="210" y="298" text-anchor="middle" fill="rgba(241,239,234,.92)" font-size="24" font-weight="700">业务 · Function</text>
        <text x="210" y="328" text-anchor="middle" fill="rgba(241,239,234,.65)" font-size="22">领域实现下沉</text>
      </svg>
    </div>
    <div style="display:flex;flex-direction:column;justify-content:center;gap:0;min-height:0">
    <h2 class="h-xl" style="margin-bottom:1vh">Harness 退居配置层</h2>
    <p class="lead" style="margin-bottom:2vh">声明 Agent 与触发策略；后端实现 Function；平台统一发布、配额与审计——核心能力沉到 Worker 与 Function。</p>
    <div class="rowline" style="margin-top:1vh;border-top:0">
      <span class="k">配置</span><span class="v">Harness 配 Worker、配 Trigger</span><span class="m">YAML</span>
    </div>
    <div class="rowline">
      <span class="k">运行时</span><span class="v">统一 Worker 语义与观测</span><span class="m">Ops</span>
    </div>
    <div class="rowline">
      <span class="k">业务</span><span class="v">领域服务即 Function</span><span class="m">Code</span>
    </div>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Fusion</div></div>
  <span class="wa">Harness 更像配置层，核心能力在 Worker 与 Function</span>
</section>"""

OLD_S13 = """  <div class="frame" style="padding-top:5vh">
    <h2 class="h-xl">动态权衡与持续演进</h2>
    <div class="grid-4" style="margin-top:3vh">"""

NEW_S13 = """  <div class="frame frame-grow" style="padding-top:2vh">
    <h2 class="h-xl">动态权衡与持续演进</h2>
    <div class="viz-box compact" style="min-height:min(24vh,260px)" aria-hidden="true">
      <svg viewBox="0 0 640 160" preserveAspectRatio="xMidYMid meet">
        <ellipse cx="320" cy="80" rx="280" ry="62" fill="none" stroke="#0a0a0b" stroke-width="2" opacity=".35"/>
        <circle cx="160" cy="80" r="12" fill="#0a0a0b"/><text x="160" y="115" text-anchor="middle" font-size="20" fill="#18181a">成本</text>
        <circle cx="320" cy="52" r="12" fill="#0a0a0b"/><text x="320" y="38" text-anchor="middle" font-size="20" fill="#18181a">安全</text>
        <circle cx="480" cy="80" r="12" fill="#0a0a0b"/><text x="480" y="115" text-anchor="middle" font-size="20" fill="#18181a">观测</text>
        <circle cx="320" cy="108" r="12" fill="#0a0a0b"/><text x="320" y="148" text-anchor="middle" font-size="20" fill="#18181a">文化</text>
        <text x="320" y="82" text-anchor="middle" font-size="22" font-weight="700" fill="#0a0a0b" opacity=".85">持续权衡环</text>
      </svg>
    </div>
    <div class="grid-4" style="margin-top:1vh;flex:1;min-height:0">"""

blocks = [
    (OLD_S1, NEW_S1),
    (OLD_S2_COL, NEW_S2_COL),
    (OLD_S3_TOP, NEW_S3_TOP),
    (OLD_S5, NEW_S5),
    (OLD_S6_MID, NEW_S6_MID),
    (OLD_S7, NEW_S7),
    (OLD_S9, NEW_S9),
    (OLD_S10_MID, NEW_S10_MID),
    (OLD_S11_SVG, NEW_S11_SVG),
    (OLD_S12, NEW_S12),
    (OLD_S13, NEW_S13),
]

for old, new in blocks:
    if old not in t:
        raise SystemExit(f"BLOCK NOT FOUND:\n{old[:100]}…")
    t = t.replace(old, new, 1)

# Larger primitives diagram (s4)
t = t.replace('font-size="36" font-weight="700" font-family="Noto Serif SC,serif">Worker',
              'font-size="42" font-weight="700" font-family="Noto Serif SC,serif">Worker', 1)
t = t.replace('font-size="36" font-weight="700" font-family="Noto Serif SC,serif">Trigger',
              'font-size="42" font-weight="700" font-family="Noto Serif SC,serif">Trigger', 1)
t = t.replace('font-size="36" font-weight="700" font-family="Noto Serif SC,serif">Function',
              'font-size="42" font-weight="700" font-family="Noto Serif SC,serif">Function', 1)
t = t.replace('font-size="26">运行单元', 'font-size="30">运行单元', 1)
t = t.replace('font-size="26">驱动与编排', 'font-size="30">驱动与编排', 1)
t = t.replace('font-size="26">能力边界', 'font-size="30">能力边界', 1)
t = t.replace('font-size="28" font-weight="600">统一原语', 'font-size="32" font-weight="600">统一原语', 1)

dst.write_text(t, encoding="utf-8")
print("visual polish OK", dst)
