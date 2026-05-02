# -*- coding: utf-8 -*-
"""Rebuild presentation.html from presentation-open-design-guizang.html with wav-safe deck + layout tweaks."""
from pathlib import Path

base = Path("features/content-pipeline")
src = dst = None
for d in base.iterdir():
    if not d.is_dir() or "Worker" not in d.name:
        continue
    o = d / "production/slides/presentation-open-design-guizang.html"
    p = d / "production/slides/presentation.html"
    if o.exists():
        src, dst = o, p
        break
assert src and dst

t = src.read_text(encoding="utf-8")

OLD_DECK = """  /* ============ Deck 容器 + 翻页 ============ */
  /* width: NSLIDES * 100vw，会在 JS 里动态矫正 */
  #deck{position:fixed;inset:0;width:10000vw;height:100vh;display:flex;flex-wrap:nowrap;transition:transform .9s cubic-bezier(.77,0,.175,1);z-index:10;will-change:transform}
  .slide{width:100vw;height:100vh;flex:0 0 100vw;position:relative;padding:6vh 6vw 10vh 6vw;display:flex;flex-direction:column;overflow:hidden}
"""

NEW_DECK = """  /* ============ Deck：叠放单视口（wav 管线逐页 display:none 时禁用横向 translateX） ============ */
  #deck{position:fixed;inset:0;width:100vw!important;height:100vh;overflow:hidden;display:block;z-index:10;transition:none}
  #deck>.slide{display:none}
  #deck>.slide:first-of-type{display:flex}
  .slide{position:absolute;inset:0;width:100%;height:100%;flex-shrink:0;padding:6vh 6vw 10vh 6vw;display:flex;flex-direction:column;overflow:hidden}
"""

assert OLD_DECK in t, "deck block mismatch"
t = t.replace(OLD_DECK, NEW_DECK)

t = t.replace(
    "  .kicker{font-family:var(--mono);font-size:12px;letter-spacing:.3em;text-transform:uppercase;opacity:.6;margin-bottom:2.6vh}",
    "  .kicker{font-family:var(--mono);font-size:max(13px,.95vw);letter-spacing:.3em;text-transform:uppercase;opacity:.6;margin-bottom:2.6vh}",
)
t = t.replace(
    "  .body-zh{font-family:var(--sans-zh);font-weight:400;font-size:max(15px,1.22vw);line-height:1.75;opacity:.82;letter-spacing:.01em}",
    "  .body-zh{font-family:var(--sans-zh);font-weight:400;font-size:max(17px,1.35vw);line-height:1.75;opacity:.82;letter-spacing:.01em}",
)
t = t.replace(
    "  .pillar .d{font-family:var(--sans-zh);font-weight:400;font-size:max(14px,1.1vw);opacity:.76;line-height:1.6}",
    "  .pillar .d{font-family:var(--sans-zh);font-weight:400;font-size:max(16px,1.2vw);opacity:.76;line-height:1.6}",
)

OLD_STEP = """  .step-desc{
    font-family:var(--sans-zh);
    font-weight:400;
    font-size:max(12px,.95vw);
    line-height:1.45;
    opacity:.72;
  }

  /* ---------- 网格（layouts.md 所用） ---------- */
"""

NEW_STEP = """  .step-desc{
    font-family:var(--sans-zh);
    font-weight:400;
    font-size:max(14px,1.08vw);
    line-height:1.45;
    opacity:.72;
  }

  /* 疏页填密 */
  .frame-fill{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center}
  .compare-3{display:grid;grid-template-columns:1fr auto 1fr;gap:2.5vw;align-items:stretch;flex:1;min-height:0}
  .compare-mid{display:flex;align-items:center;justify-content:center;font-family:var(--serif-en);font-weight:800;font-size:min(4.2vw,68px);opacity:.32;min-width:3.5vw}
  .grid-stretch-rows{align-items:stretch!important}
  .grid-stretch-rows>.col,.grid-stretch-rows>div{min-height:0;display:flex;flex-direction:column;justify-content:center}
  .pillar-page .grid-4{flex:1;min-height:0;align-content:stretch;gap:3vh 5vw}

  /* ---------- 网格（layouts.md 所用） ---------- */
"""

assert OLD_STEP in t
t = t.replace(OLD_STEP, NEW_STEP)

t = t.replace(
    "  .chrome{font-family:var(--mono);font-size:max(11px,.78vw);letter-spacing:.2em;text-transform:uppercase;opacity:.62}\n  .foot{font-family:var(--mono);font-size:max(11px,.78vw);letter-spacing:.18em;text-transform:uppercase;opacity:.5}",
    "  .chrome{font-family:var(--mono);font-size:max(13px,.9vw);letter-spacing:.2em;text-transform:uppercase;opacity:.62}\n  .foot{font-family:var(--mono);font-size:max(13px,.88vw);letter-spacing:.18em;text-transform:uppercase;opacity:.5}",
)

OLD_JS = """// 关键：矫正 deck 宽度为 total * 100vw，否则翻页会错位
deck.style.width=(total*100)+'vw';

slides.forEach((s,i)=>{
  const b=document.createElement('button');
  b.className='dot';b.dataset.i=i;b.setAttribute('aria-label','Page '+(i+1));
  b.onclick=()=>go(i);
  nav.appendChild(b);
});

function go(n){
  idx=Math.max(0,Math.min(total-1,n));
  deck.style.transform=`translateX(${-idx*100}vw)`;
"""

NEW_JS = """deck.style.width='100vw';
deck.style.transform='translateX(0)';

slides.forEach((s,i)=>{
  const b=document.createElement('button');
  b.className='dot';b.dataset.i=i;b.setAttribute('aria-label','Page '+(i+1));
  b.onclick=()=>go(i);
  nav.appendChild(b);
});

function go(n){
  idx=Math.max(0,Math.min(total-1,n));
  slides.forEach((s,i)=>{
    if(i===idx){ s.style.display='flex'; s.style.flexDirection='column'; }
    else { s.style.display='none'; }
  });
  deck.style.width='100vw';
  deck.style.transform='translateX(0)';
"""

assert OLD_JS in t, "JS block not found"
t = t.replace(OLD_JS, NEW_JS)

OLD_S2 = """<section class="slide s dark" id="s2">
  <div class="chrome"><div>误区 ①</div><div>03 / 15</div></div>
  <div class="frame grid-2-6-6" style="padding-top:5vh">
    <div class="col" style="gap:3vh">
      <div class="kicker">Myth</div>
      <h2 class="h-xl">大模型万能？</h2>
      <p class="lead">堆更大模型就能做好 Agent 系统、就能解决工程问题——这是常见错觉。</p>
      <div class="callout"><span class="q-big">误区</span><br>把「推理」当成「系统」的全部。</div>
    </div>
    <div class="col" style="gap:3vh;justify-content:center">
      <div class="tag">现实</div>
      <p class="body-zh">难点在任务编排、状态、流程与可观测性；模型只是零件，<span class="hi">后端才是系统</span>。</p>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Myth 1</div></div>
  <span class="wa">模型只是零件，后端才是系统</span>
</section>"""

NEW_S2 = """<section class="slide s dark" id="s2">
  <div class="chrome"><div>误区 ①</div><div>03 / 15</div></div>
  <div class="frame grid-2-6-6 grid-stretch-rows frame-fill" style="padding-top:3vh">
    <div class="col" style="gap:2.6vh">
      <div class="kicker">Myth</div>
      <h2 class="h-xl">大模型万能？</h2>
      <p class="lead">堆更大模型就能做好 Agent 系统、就能解决工程问题——这是常见错觉。</p>
      <div class="callout"><span class="q-big">误区</span><br>把「推理」当成「系统」的全部。</div>
    </div>
    <div class="col" style="gap:2.4vh">
      <div class="tag">现实</div>
      <p class="body-zh">难点在任务编排、状态、流程与可观测性；模型只是零件，<span class="hi">后端才是系统</span>。</p>
      <div class="rule" style="margin:2vh 0"></div>
      <p class="body-zh" style="opacity:.78;font-size:max(16px,1.22vw)">→ 编排与状态管理 · → 可观测与排障 · → 发布与治理同样消耗脑力</p>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Myth 1</div></div>
  <span class="wa">模型只是零件，后端才是系统</span>
</section>"""

assert OLD_S2 in t
t = t.replace(OLD_S2, NEW_S2)

OLD_S3 = """<section class="slide s light" id="s3">
  <div class="chrome"><div>误区 ②</div><div>04 / 15</div></div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker">协作成本</div>
    <h2 class="h-xl">多 Agent = 天然提效？</h2>
    <div class="grid-4" style="margin-top:4vh">
"""

NEW_S3 = """<section class="slide s light" id="s3">
  <div class="chrome"><div>误区 ②</div><div>04 / 15</div></div>
  <div class="frame pillar-page" style="padding-top:3vh">
    <div class="kicker">协作成本</div>
    <h2 class="h-xl">多 Agent = 天然提效？</h2>
    <div class="grid-4" style="margin-top:3vh">
"""

assert OLD_S3 in t
t = t.replace(OLD_S3, NEW_S3)

t = t.replace(
    '<div class="pillar"><span class="ic">?</span><div class="t">排障地狱</div>',
    '<div class="pillar"><span class="ic">⚠</span><div class="t">排障地狱</div>',
)

OLD_S7 = """<section class="slide s light" id="s7">
  <div class="chrome"><div>对比</div><div>08 / 15</div></div>
  <div class="frame grid-2-6-6" style="padding-top:5vh">
    <div class="callout">
      <div class="kicker">传统</div>
      <p class="body-zh">Agent 与业务两套语言；桥接厚重；Tracing 割裂；状态分散。</p>
    </div>
    <div class="callout">
      <div class="kicker">三模型</div>
      <p class="body-zh">Agent 与后端无缝融合；统一语义与全链路追踪；一切先落成 Worker 再组合。</p>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Compare</div></div>
  <span class="wa">把 agent 与后端服务真正融在一起，复杂度才不再爆炸</span>
</section>"""

NEW_S7 = """<section class="slide s light" id="s7">
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

assert OLD_S7 in t
t = t.replace(OLD_S7, NEW_S7)

OLD_S10 = """<section class="slide s dark" id="s10">
  <div class="chrome"><div>争论</div><div>11 / 15</div></div>
  <div class="frame grid-2-6-6" style="padding-top:5vh">
    <div>
      <div class="tag">薄 Harness</div>
      <h2 class="h-md">连接与编排壳</h2>
      <p class="body-zh" style="margin-top:2vh">业务语义下沉到 Worker；迭代快、边界清晰。</p>
    </div>
    <div>
      <div class="tag">厚 Harness</div>
      <h2 class="h-md">策略与状态上收</h2>
      <p class="body-zh" style="margin-top:2vh">易成新的单体瓶颈；升级与测试成本高。</p>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Harness</div></div>
  <span class="wa">Harness 厚薄没有绝对答案，要看团队边界</span>
</section>"""

NEW_S10 = """<section class="slide s dark" id="s10">
  <div class="chrome"><div>争论</div><div>11 / 15</div></div>
  <div class="frame compare-3 grid-stretch-rows frame-fill" style="padding-top:3vh">
    <div style="gap:2vh">
      <div class="tag">薄 Harness</div>
      <h2 class="h-md">连接与编排壳</h2>
      <p class="body-zh" style="margin-top:2vh">业务语义下沉到 Worker；迭代快、边界清晰。</p>
      <p class="body-zh" style="opacity:.75;margin-top:1.6vh">适合：团队已有成熟运行时，Harness 只做胶水与策略声明。</p>
    </div>
    <div class="compare-mid">VS</div>
    <div style="gap:2vh">
      <div class="tag">厚 Harness</div>
      <h2 class="h-md">策略与状态上收</h2>
      <p class="body-zh" style="margin-top:2vh">易成新的单体瓶颈；升级与测试成本高。</p>
      <p class="body-zh" style="opacity:.75;margin-top:1.6vh">适合：要强治理、统一配额审计，但要警惕演进速度与耦合。</p>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Harness</div></div>
  <span class="wa">Harness 厚薄没有绝对答案，要看团队边界</span>
</section>"""

assert OLD_S10 in t
t = t.replace(OLD_S10, NEW_S10)

for a, b in [
    ('font-size="22">运行单元', 'font-size="26">运行单元'),
    ('font-size="22">驱动与编排', 'font-size="26">驱动与编排'),
    ('font-size="22">能力边界', 'font-size="26">能力边界'),
    ('font-size="26" font-weight="600">统一原语', 'font-size="28" font-weight="600">统一原语'),
]:
    t = t.replace(a, b)

t = t.replace(
    '<text x="340" y="180" text-anchor="middle" font-size="20" fill="#18181a">W / T / F</text>',
    '<text x="340" y="180" text-anchor="middle" font-size="24" fill="#18181a">W / T / F</text>',
)
t = t.replace(
    '<text x="1060" y="180" text-anchor="middle" font-size="20" fill="#18181a">W / T / F</text>',
    '<text x="1060" y="180" text-anchor="middle" font-size="24" fill="#18181a">W / T / F</text>',
)

dst.write_text(t, encoding="utf-8")
print("OK", dst)
