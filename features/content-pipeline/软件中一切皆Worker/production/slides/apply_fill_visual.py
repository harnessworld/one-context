# -*- coding: utf-8 -*-
"""Fill sparse slides: bottom viz strips / flex-grow diagrams. UTF-8 only."""
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

S0_OLD = """<section class="slide s hero dark" id="s0">
  <div class="chrome"><div>斗包 AI 播客</div><div>Vol · Agent 后端</div></div>
  <div class="frame" style="display:grid;gap:4vh;align-content:center;min-height:78vh">
    <div class="kicker">Harness · Worker / Trigger / Function</div>
    <h1 class="h-hero">重新定义AI时代的软件</h1>
    <h2 class="h-sub">用统一原语把传统软件与 Agent 后端对齐</h2>
    <p class="lead" style="max-width:62vw">Mike Piccolo 视角下的复杂度收敛：先把一切落成 Worker，再用 Trigger 驱动、用 Function 封装能力。</p>
    <div class="meta-row"><span>斗包</span><span>·</span><span>AI 播客</span><span>·</span><span>01 / 15</span></div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Cover</div></div>
  <span class="wa">欢迎收听斗包 AI 播客节目</span>
</section>"""

S0_NEW = """<section class="slide s hero dark" id="s0">
  <div class="chrome"><div>斗包 AI 播客</div><div>Vol · Agent 后端</div></div>
  <div class="frame frame-grow" style="justify-content:center;gap:2.4vh;min-height:0;padding-top:1vh">
    <div class="kicker">Harness · Worker / Trigger / Function</div>
    <h1 class="h-hero">重新定义AI时代的软件</h1>
    <h2 class="h-sub">用统一原语把传统软件与 Agent 后端对齐</h2>
    <p class="lead" style="max-width:62vw">Mike Piccolo 视角下的复杂度收敛：先把一切落成 Worker，再用 Trigger 驱动、用 Function 封装能力。</p>
    <div class="meta-row"><span>斗包</span><span>·</span><span>AI 播客</span><span>·</span><span>01 / 15</span></div>
    <div class="viz-box compact" style="min-height:min(24vh,240px);max-height:28vh;margin-top:1.5vh;opacity:.92" aria-hidden="true">
      <svg viewBox="0 0 880 160" preserveAspectRatio="xMidYMid meet">
        <defs><marker id="arrC0" markerWidth="9" markerHeight="6" refX="9" refY="3" orient="auto"><polygon points="0 0,9 3,0 6" fill="rgba(241,239,234,.55)"/></marker></defs>
        <text x="440" y="28" text-anchor="middle" fill="rgba(241,239,234,.45)" font-size="16" font-family="IBM Plex Mono,monospace" letter-spacing=".2em">本期骨架</text>
        <rect x="48" y="52" width="220" height="88" rx="12" fill="rgba(241,239,234,.07)" stroke="rgba(241,239,234,.4)" stroke-width="1.5"/>
        <text x="158" y="98" text-anchor="middle" fill="rgba(241,239,234,.92)" font-size="26" font-weight="700" font-family="Noto Serif SC,serif">Worker</text>
        <text x="158" y="128" text-anchor="middle" fill="rgba(241,239,234,.65)" font-size="20">运行单元</text>
        <line x1="276" y1="96" x2="318" y2="96" stroke="rgba(241,239,234,.45)" stroke-width="2" marker-end="url(#arrC0)"/>
        <rect x="328" y="52" width="220" height="88" rx="12" fill="rgba(241,239,234,.09)" stroke="rgba(241,239,234,.48)" stroke-width="2"/>
        <text x="438" y="98" text-anchor="middle" fill="rgba(241,239,234,.95)" font-size="26" font-weight="700" font-family="Noto Serif SC,serif">Trigger</text>
        <text x="438" y="128" text-anchor="middle" fill="rgba(241,239,234,.68)" font-size="20">驱动编排</text>
        <line x1="556" y1="96" x2="598" y2="96" stroke="rgba(241,239,234,.45)" stroke-width="2" marker-end="url(#arrC0)"/>
        <rect x="608" y="52" width="220" height="88" rx="12" fill="rgba(241,239,234,.07)" stroke="rgba(241,239,234,.4)" stroke-width="1.5"/>
        <text x="718" y="98" text-anchor="middle" fill="rgba(241,239,234,.92)" font-size="26" font-weight="700" font-family="Noto Serif SC,serif">Function</text>
        <text x="718" y="128" text-anchor="middle" fill="rgba(241,239,234,.65)" font-size="20">能力边界</text>
      </svg>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Cover</div></div>
  <span class="wa">欢迎收听斗包 AI 播客节目</span>
</section>"""

S6_OLD = """  <div class="frame" style="padding-top:4vh">
    <h2 class="h-xl">革命性特性</h2>
    <p class="lead" style="margin-bottom:3vh">用同一套语言描述 Agent 与后端：Agent 本身也是 Worker；与微服务并列扩展；任意语言实现 Function。</p>
    <div class="grid-3">
      <div class="stat"><span class="m">Unified</span><span class="n">1 套语义</span><span class="l">调度、观测、排障对齐</span></div>
      <div class="stat"><span class="m">Scale</span><span class="n">水平扩展</span><span class="l">动态扩缩与治理一体化</span></div>
      <div class="stat"><span class="m">Interop</span><span class="n">多语言</span><span class="l">Function 边界清晰可替换</span></div>
    </div>
    <div class="viz-box compact" style="margin-top:1vh" aria-hidden="true">"""

S6_NEW = """  <div class="frame frame-grow" style="padding-top:3vh">
    <h2 class="h-xl">革命性特性</h2>
    <p class="lead" style="margin-bottom:2vh">用同一套语言描述 Agent 与后端：Agent 本身也是 Worker；与微服务并列扩展；任意语言实现 Function。</p>
    <div class="grid-3">
      <div class="stat"><span class="m">Unified</span><span class="n">1 套语义</span><span class="l">调度、观测、排障对齐</span></div>
      <div class="stat"><span class="m">Scale</span><span class="n">水平扩展</span><span class="l">动态扩缩与治理一体化</span></div>
      <div class="stat"><span class="m">Interop</span><span class="n">多语言</span><span class="l">Function 边界清晰可替换</span></div>
    </div>
    <div class="viz-box compact" style="flex:1;margin-top:1vh;min-height:min(30vh,320px)" aria-hidden="true">"""

S8_OLD = """<section class="slide s hero dark" id="s8">
  <div class="chrome"><div>影响</div><div>09 / 15</div></div>
  <div class="frame center" style="min-height:72vh">
    <div class="kicker">范式迁移</div>
    <div class="big-num" style="font-size:12vw">1st-class</div>
    <h2 class="h-sub" style="margin-top:3vh">Agent 成为后端一等公民</h2>
    <p class="lead" style="max-width:70vw;margin-top:2vh">与微服务、批任务并列的第一类负载：调度、配额、发布与治理走同一套平台。</p>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Citizen</div></div>
  <span class="wa">Agent 不再是外挂脚本，而是正式工作负载</span>
</section>"""

S8_NEW = """<section class="slide s hero dark" id="s8">
  <div class="chrome"><div>影响</div><div>09 / 15</div></div>
  <div class="frame frame-grow" style="min-height:0;padding-top:2vh;text-align:center">
    <div style="flex:0 0 auto">
      <div class="kicker">范式迁移</div>
      <div class="big-num" style="font-size:12vw">1st-class</div>
      <h2 class="h-sub" style="margin-top:2.4vh">Agent 成为后端一等公民</h2>
      <p class="lead" style="max-width:70vw;margin:2vh auto 0">与微服务、批任务并列的第一类负载：调度、配额、发布与治理走同一套平台。</p>
    </div>
    <div class="viz-box compact" style="flex:1;min-height:min(34vh,360px);max-height:40vh;margin-top:2vh;width:100%" aria-hidden="true">
      <svg viewBox="0 0 920 200" preserveAspectRatio="xMidYMid meet">
        <rect x="36" y="118" width="820" height="56" rx="10" fill="rgba(241,239,234,.06)" stroke="rgba(241,239,234,.35)" stroke-width="1.5"/>
        <text x="446" y="154" text-anchor="middle" fill="rgba(241,239,234,.88)" font-size="22" font-weight="600">同一平台平面 · 调度 · 配额 · 发布 · 治理</text>
        <rect x="70" y="36" width="200" height="64" rx="10" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.42)"/>
        <text x="170" y="78" text-anchor="middle" fill="rgba(241,239,234,.9)" font-size="22" font-weight="700">微服务</text>
        <rect x="360" y="28" width="200" height="80" rx="10" fill="rgba(241,239,234,.12)" stroke="rgba(241,239,234,.55)" stroke-width="2"/>
        <text x="460" y="68" text-anchor="middle" fill="rgba(241,239,234,.95)" font-size="24" font-weight="800">Agent</text>
        <text x="460" y="96" text-anchor="middle" fill="rgba(241,239,234,.65)" font-size="18">一等负载</text>
        <rect x="650" y="36" width="200" height="64" rx="10" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.42)"/>
        <text x="750" y="78" text-anchor="middle" fill="rgba(241,239,234,.9)" font-size="22" font-weight="700">批任务</text>
        <line x1="170" y1="100" x2="170" y2="118" stroke="rgba(241,239,234,.4)" stroke-width="2"/>
        <line x1="460" y1="108" x2="460" y2="118" stroke="rgba(241,239,234,.5)" stroke-width="2.5"/>
        <line x1="750" y1="100" x2="750" y2="118" stroke="rgba(241,239,234,.4)" stroke-width="2"/>
      </svg>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Citizen</div></div>
  <span class="wa">Agent 不再是外挂脚本，而是正式工作负载</span>
</section>"""

S10_FRAME_OLD = '<div class="frame compare-3 grid-stretch-rows frame-fill" style="padding-top:3vh">'
S10_FRAME_NEW = '<div class="frame compare-3 grid-stretch-rows frame-fill frame-grow" style="padding-top:3vh">'

S10_MID_OLD = """    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.8vh;min-width:10vw">
      <div class="compare-mid">VS</div>
      <svg viewBox="0 0 200 200" width="120" height="120" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
        <rect x="30" y="40" width="140" height="36" rx="6" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.5)"/>
        <rect x="30" y="118" width="140" height="52" rx="6" fill="rgba(241,239,234,.14)" stroke="rgba(241,239,234,.55)" stroke-width="2"/>
        <text x="100" y="64" text-anchor="middle" fill="rgba(241,239,234,.85)" font-size="18" font-weight="600">薄 · 壳层</text>
        <text x="100" y="150" text-anchor="middle" fill="rgba(241,239,234,.9)" font-size="18" font-weight="700">厚 · 策略堆叠</text>
      </svg>
    </div>"""

S10_MID_NEW = """    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.2vh;min-width:12vw;flex:1;min-height:min(46vh,520px);padding:1vh 0">
      <div class="compare-mid">VS</div>
      <svg viewBox="0 0 240 320" preserveAspectRatio="xMidYMid meet" aria-hidden="true" style="width:min(22vw,200px);height:auto">
        <rect x="20" y="24" width="200" height="56" rx="8" fill="rgba(241,239,234,.09)" stroke="rgba(241,239,234,.48)" stroke-width="1.5"/>
        <text x="120" y="58" text-anchor="middle" fill="rgba(241,239,234,.88)" font-size="20" font-weight="700">薄 Harness</text>
        <line x1="120" y1="80" x2="120" y2="108" stroke="rgba(241,239,234,.45)" stroke-width="2"/>
        <polygon points="120,118 108,102 132,102" fill="rgba(241,239,234,.55)"/>
        <rect x="28" y="124" width="184" height="72" rx="10" fill="rgba(241,239,234,.06)" stroke="rgba(241,239,234,.4)"/>
        <text x="120" y="158" text-anchor="middle" fill="rgba(241,239,234,.82)" font-size="17" font-weight="600">Worker 承载语义</text>
        <text x="120" y="182" text-anchor="middle" fill="rgba(241,239,234,.58)" font-size="15">壳层连接</text>
        <line x1="120" y1="204" x2="120" y2="232" stroke="rgba(241,239,234,.45)" stroke-width="2"/>
        <polygon points="120,242 108,226 132,226" fill="rgba(241,239,234,.55)"/>
        <rect x="16" y="248" width="208" height="64" rx="10" fill="rgba(241,239,234,.14)" stroke="rgba(241,239,234,.58)" stroke-width="2"/>
        <text x="120" y="278" text-anchor="middle" fill="rgba(241,239,234,.92)" font-size="20" font-weight="800">厚 Harness</text>
        <text x="120" y="300" text-anchor="middle" fill="rgba(241,239,234,.62)" font-size="15">策略 · 状态上收</text>
      </svg>
    </div>"""

S11_OLD = """  <div class="frame" style="padding-top:4vh">
    <h2 class="h-xl">底层抽象正在对齐</h2>
    <p class="lead">Harness 层与业务后端：同一套积木 —— Worker、Trigger、Function。</p>
    <div class="fill" style="display:flex;align-items:center;justify-content:center;min-height:46vh">
      <svg viewBox="0 0 1400 320" preserveAspectRatio="xMidYMid meet" style="width:100%">
        <rect x="80" y="60" width="520" height="200" rx="14" fill="rgba(10,10,11,.06)" stroke="rgba(10,10,11,.35)" stroke-width="2"/>
        <text x="340" y="125" text-anchor="middle" font-size="34" font-weight="700" fill="#0a0a0b">Harness</text>
        <text x="340" y="175" text-anchor="middle" font-size="28" fill="#18181a">W / T / F</text>
        <text x="700" y="200" font-size="56" fill="#0a0a0b" font-weight="800">=</text>
        <rect x="800" y="60" width="520" height="200" rx="14" fill="rgba(10,10,11,.06)" stroke="rgba(10,10,11,.35)" stroke-width="2"/>
        <text x="1060" y="125" text-anchor="middle" font-size="34" font-weight="700" fill="#0a0a0b">业务后端</text>
        <text x="1060" y="175" text-anchor="middle" font-size="28" fill="#18181a">W / T / F</text>
      </svg>
    </div>
  </div>"""

S11_NEW = """  <div class="frame frame-grow" style="padding-top:3vh">
    <h2 class="h-xl">底层抽象正在对齐</h2>
    <p class="lead" style="margin-bottom:.6vh">Harness 层与业务后端：同一套积木 —— Worker、Trigger、Function。</p>
    <div class="viz-box compact" style="flex:1;min-height:min(44vh,460px);margin-top:1vh;display:flex;align-items:center">
      <svg viewBox="0 0 1400 340" preserveAspectRatio="xMidYMid meet" style="width:100%;max-height:48vh">
        <rect x="80" y="60" width="520" height="200" rx="14" fill="rgba(10,10,11,.06)" stroke="rgba(10,10,11,.35)" stroke-width="2"/>
        <text x="340" y="125" text-anchor="middle" font-size="34" font-weight="700" fill="#0a0a0b">Harness</text>
        <text x="340" y="175" text-anchor="middle" font-size="28" fill="#18181a">W / T / F</text>
        <text x="700" y="200" font-size="56" fill="#0a0a0b" font-weight="800">=</text>
        <rect x="800" y="60" width="520" height="200" rx="14" fill="rgba(10,10,11,.06)" stroke="rgba(10,10,11,.35)" stroke-width="2"/>
        <text x="1060" y="125" text-anchor="middle" font-size="34" font-weight="700" fill="#0a0a0b">业务后端</text>
        <text x="1060" y="175" text-anchor="middle" font-size="28" fill="#18181a">W / T / F</text>
        <text x="700" y="310" text-anchor="middle" font-size="22" fill="#18181a" opacity=".72">同一套原语 · 两侧独立演进 · 观测可对齐</text>
      </svg>
    </div>
  </div>"""

S14_OLD = """<section class="slide s hero light" id="s14">
  <div class="chrome"><div>致谢</div><div>15 / 15</div></div>
  <div class="frame center" style="min-height:72vh">
    <div class="kicker">感谢收听</div>
    <h1 class="h-hero">下期再会</h1>
    <p class="lead" style="max-width:62vw;margin-top:3vh">拥抱变化，把 AI Agent 做成可靠后端。</p>
    <div class="meta-row" style="margin-top:4vh"><span>斗包 AI 播客</span><span>·</span><span>Agent 后端实践</span></div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Thanks</div></div>
  <span class="wa">欢迎关注更多 AI Agent 后端实践</span>
</section>"""

S14_NEW = """<section class="slide s hero light" id="s14">
  <div class="chrome"><div>致谢</div><div>15 / 15</div></div>
  <div class="frame frame-grow" style="min-height:0;justify-content:center;gap:2vh;text-align:center;padding-top:2vh">
    <div class="kicker">感谢收听</div>
    <h1 class="h-hero">下期再会</h1>
    <p class="lead" style="max-width:62vw;margin:2vh auto 0">拥抱变化，把 AI Agent 做成可靠后端。</p>
    <div class="meta-row" style="margin-top:2vh"><span>斗包 AI 播客</span><span>·</span><span>Agent 后端实践</span></div>
    <div class="viz-box compact" style="min-height:min(22vh,220px);max-height:26vh;margin-top:1vh;opacity:.85" aria-hidden="true">
      <svg viewBox="0 0 720 140" preserveAspectRatio="xMidYMid meet">
        <path d="M40 88 Q180 28 360 88 T680 88" fill="none" stroke="rgba(10,10,11,.18)" stroke-width="3" stroke-linecap="round"/>
        <circle cx="160" cy="72" r="10" fill="#0a0a0b" opacity=".35"/><circle cx="360" cy="52" r="12" fill="#0a0a0b" opacity=".45"/><circle cx="560" cy="72" r="10" fill="#0a0a0b" opacity=".35"/>
        <text x="360" y="118" text-anchor="middle" fill="#18181a" font-size="20" opacity=".65">W · T · F → 可靠后端</text>
      </svg>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Thanks</div></div>
  <span class="wa">欢迎关注更多 AI Agent 后端实践</span>
</section>"""

blocks = [
    (S0_OLD, S0_NEW),
    (S6_OLD, S6_NEW),
    (S8_OLD, S8_NEW),
    (S10_FRAME_OLD, S10_FRAME_NEW),
    (S10_MID_OLD, S10_MID_NEW),
    (S11_OLD, S11_NEW),
    (S14_OLD, S14_NEW),
]

for old, new in blocks:
    if old not in t:
        raise SystemExit(f"MISSING FRAGMENT ({len(old)} chars):\n{old[:120]}…")
    t = t.replace(old, new, 1)

dst.write_text(t, encoding="utf-8")
print("fill visual OK", dst)
