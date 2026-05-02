# -*- coding: utf-8 -*-
"""Merge guizang-ppt (Open Design) template + Worker deck content; wav-pipeline compatible."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]  # one-context
TEMPLATE = REPO / "tmp/open-design/skills/guizang-ppt/assets/template.html"
OUT = ROOT / "presentation-open-design-guizang.html"

WA = [
    "欢迎收听斗包 AI 播客节目",
    "我们先从复杂度爆炸与 Harness 理念谈起",
    "模型只是零件，后端才是系统",
    "多 Agent 不是银弹，抽象不对照样崩",
    "Walker Trigger Function 口播常混，工程上写作 Worker",
    "很多人盯着集成难题，内部混乱更要命",
    "用 worker、trigger、function 构建整个系统",
    "把 agent 与后端服务真正融在一起，复杂度才不再爆炸",
    "Agent 不再是外挂脚本，而是正式工作负载",
    "AI 基础设施从拼模型走向拼平台与治理",
    "Harness 厚薄没有绝对答案，要看团队边界",
    "底层都是 Worker、Trigger、Function 三块积木",
    "Harness 更像配置层，核心能力在 Worker 与 Function",
    "架构会迭代，但统一抽象会留下来",
    "欢迎关注更多 AI Agent 后端实践",
]

SLIDES = [
    # 0 cover
    """<section class="slide s hero dark" id="s0">
  <div class="chrome"><div>斗包 AI 播客</div><div>Vol · Agent 后端</div></div>
  <div class="frame" style="display:grid;gap:4vh;align-content:center;min-height:78vh">
    <div class="kicker">Harness · Worker / Trigger / Function</div>
    <h1 class="h-hero">重新定义AI时代的软件</h1>
    <h2 class="h-sub">用统一原语把传统软件与 Agent 后端对齐</h2>
    <p class="lead" style="max-width:62vw">Mike Piccolo 视角下的复杂度收敛：先把一切落成 Worker，再用 Trigger 驱动、用 Function 封装能力。</p>
    <div class="meta-row"><span>斗包</span><span>·</span><span>AI 播客</span><span>·</span><span>01 / 15</span></div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Cover</div></div>
  <span class="wa">{wa}</span>
</section>""",
    # 1 intro grid
    """<section class="slide s light" id="s1">
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
  <span class="wa">{wa}</span>
</section>""",
    # 2 myth 1 split
    """<section class="slide s dark" id="s2">
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
  <span class="wa">{wa}</span>
</section>""",
    # 3 myth 2 grid
    """<section class="slide s light" id="s3">
  <div class="chrome"><div>误区 ②</div><div>04 / 15</div></div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker">协作成本</div>
    <h2 class="h-xl">多 Agent = 天然提效？</h2>
    <div class="grid-4" style="margin-top:4vh">
      <div class="pillar"><span class="ic">↔</span><div class="t">协作开销</div><div class="d">角色越多，同步越贵</div></div>
      <div class="pillar"><span class="ic">◎</span><div class="t">状态分裂</div><div class="d">上下文与边界更难控</div></div>
      <div class="pillar"><span class="ic">?</span><div class="t">排障地狱</div><div class="d">分布式链路定位变难</div></div>
      <div class="pillar"><span class="ic">∑</span><div class="t">收益不确定</div><div class="d">抽象不对可能更慢更贵</div></div>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Myth 2</div></div>
  <span class="wa">{wa}</span>
</section>""",
    # 4 W/T/F diagram
    """<section class="slide s dark" id="s4">
  <div class="chrome"><div>本质</div><div>05 / 15</div></div>
  <div class="frame" style="padding-top:4vh">
    <div class="kicker">三原语</div>
    <h2 class="h-xl">Worker · Trigger · Function</h2>
    <div class="fill" style="min-height:52vh;display:flex;align-items:center;justify-content:center">
      <svg viewBox="0 0 1600 420" preserveAspectRatio="xMidYMid meet" style="width:100%;max-height:52vh">
        <defs><marker id="arr" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="rgba(241,239,234,.85)"/></marker></defs>
        <rect x="40" y="110" width="440" height="220" rx="16" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.45)" stroke-width="2"/>
        <text x="260" y="200" text-anchor="middle" fill="rgba(241,239,234,.95)" font-size="36" font-weight="700" font-family="Noto Serif SC,serif">Worker</text>
        <text x="260" y="250" text-anchor="middle" fill="rgba(241,239,234,.75)" font-size="22">运行单元 · 服务 / Agent / 任务</text>
        <line x1="480" y1="220" x2="580" y2="220" stroke="rgba(241,239,234,.5)" stroke-width="2" marker-end="url(#arr)"/>
        <rect x="580" y="110" width="440" height="220" rx="16" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.45)" stroke-width="2"/>
        <text x="800" y="200" text-anchor="middle" fill="rgba(241,239,234,.95)" font-size="36" font-weight="700" font-family="Noto Serif SC,serif">Trigger</text>
        <text x="800" y="250" text-anchor="middle" fill="rgba(241,239,234,.75)" font-size="22">驱动与编排 · 事件 / 定时 / 人工</text>
        <line x1="1020" y1="220" x2="1120" y2="220" stroke="rgba(241,239,234,.5)" stroke-width="2" marker-end="url(#arr)"/>
        <rect x="1120" y="110" width="440" height="220" rx="16" fill="rgba(241,239,234,.08)" stroke="rgba(241,239,234,.45)" stroke-width="2"/>
        <text x="1340" y="200" text-anchor="middle" fill="rgba(241,239,234,.95)" font-size="36" font-weight="700" font-family="Noto Serif SC,serif">Function</text>
        <text x="1340" y="250" text-anchor="middle" fill="rgba(241,239,234,.75)" font-size="22">能力边界 · 工具 / API / 领域能力</text>
        <text x="800" y="380" text-anchor="middle" fill="rgba(241,239,234,.9)" font-size="26" font-weight="600">统一原语 → 复杂度收敛</text>
      </svg>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Primitives</div></div>
  <span class="wa">{wa}</span>
</section>""",
    # 5 internal chaos
    """<section class="slide s light" id="s5">
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
  <span class="wa">{wa}</span>
</section>""",
    # 6 three-model features
    """<section class="slide s dark" id="s6">
  <div class="chrome"><div>三模型</div><div>07 / 15</div></div>
  <div class="frame" style="padding-top:4vh">
    <h2 class="h-xl">革命性特性</h2>
    <p class="lead" style="margin-bottom:3vh">用同一套语言描述 Agent 与后端：Agent 本身也是 Worker；与微服务并列扩展；任意语言实现 Function。</p>
    <div class="grid-3">
      <div class="stat"><span class="m">Unified</span><span class="n">1 套语义</span><span class="l">调度、观测、排障对齐</span></div>
      <div class="stat"><span class="m">Scale</span><span class="n">水平扩展</span><span class="l">动态扩缩与治理一体化</span></div>
      <div class="stat"><span class="m">Interop</span><span class="n">多语言</span><span class="l">Function 边界清晰可替换</span></div>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Features</div></div>
  <span class="wa">{wa}</span>
</section>""",
    # 7 traditional vs 3-model
    """<section class="slide s light" id="s7">
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
  <span class="wa">{wa}</span>
</section>""",
    # 8 first-class
    """<section class="slide s hero dark" id="s8">
  <div class="chrome"><div>影响</div><div>09 / 15</div></div>
  <div class="frame center" style="min-height:72vh">
    <div class="kicker">范式迁移</div>
    <div class="big-num" style="font-size:12vw">1st-class</div>
    <h2 class="h-sub" style="margin-top:3vh">Agent 成为后端一等公民</h2>
    <p class="lead" style="max-width:70vw;margin-top:2vh">与微服务、批任务并列的第一类负载：调度、配额、发布与治理走同一套平台。</p>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Citizen</div></div>
  <span class="wa">{wa}</span>
</section>""",
    # 9 AI infra
    """<section class="slide s light" id="s9">
  <div class="chrome"><div>基础设施</div><div>10 / 15</div></div>
  <div class="frame" style="padding-top:5vh">
    <h2 class="h-xl">AI 基础设施新范式</h2>
    <div class="pipeline-section"><div class="pipeline-label">三根支柱</div>
    <div class="pipeline" data-cols="3">
      <div class="step"><div class="step-nb">01</div><div class="step-title">统一调度</div><div class="step-desc">GPU/CPU 与队列策略可组合</div></div>
      <div class="step"><div class="step-nb">02</div><div class="step-title">统一观测</div><div class="step-desc">指标、日志、链路同源</div></div>
      <div class="step"><div class="step-nb">03</div><div class="step-title">统一治理</div><div class="step-desc">配额、审计、成本与合规</div></div>
    </div></div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Infra</div></div>
  <span class="wa">{wa}</span>
</section>""",
    # 10 thin vs thick
    """<section class="slide s dark" id="s10">
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
  <span class="wa">{wa}</span>
</section>""",
    # 11 boundary align
    """<section class="slide s light" id="s11">
  <div class="chrome"><div>边界</div><div>12 / 15</div></div>
  <div class="frame" style="padding-top:4vh">
    <h2 class="h-xl">底层抽象正在对齐</h2>
    <p class="lead">Harness 层与业务后端：同一套积木 —— Worker、Trigger、Function。</p>
    <div class="fill" style="display:flex;align-items:center;justify-content:center;min-height:46vh">
      <svg viewBox="0 0 1400 320" preserveAspectRatio="xMidYMid meet" style="width:100%">
        <rect x="80" y="60" width="520" height="200" rx="14" fill="rgba(10,10,11,.06)" stroke="rgba(10,10,11,.35)" stroke-width="2"/>
        <text x="340" y="130" text-anchor="middle" font-size="28" font-weight="700" fill="#0a0a0b">Harness</text>
        <text x="340" y="180" text-anchor="middle" font-size="20" fill="#18181a">W / T / F</text>
        <text x="700" y="200" font-size="48" fill="#0a0a0b" font-weight="800">=</text>
        <rect x="800" y="60" width="520" height="200" rx="14" fill="rgba(10,10,11,.06)" stroke="rgba(10,10,11,.35)" stroke-width="2"/>
        <text x="1060" y="130" text-anchor="middle" font-size="28" font-weight="700" fill="#0a0a0b">业务后端</text>
        <text x="1060" y="180" text-anchor="middle" font-size="20" fill="#18181a">W / T / F</text>
      </svg>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Align</div></div>
  <span class="wa">{wa}</span>
</section>""",
    # 12 harness thinner
    """<section class="slide s dark" id="s12">
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
  <span class="wa">{wa}</span>
</section>""",
    # 13 future
    """<section class="slide s light" id="s13">
  <div class="chrome"><div>未来</div><div>14 / 15</div></div>
  <div class="frame" style="padding-top:5vh">
    <h2 class="h-xl">动态权衡与持续演进</h2>
    <div class="grid-4" style="margin-top:3vh">
      <div class="pillar"><span class="ic">$</span><div class="t">成本与延迟</div><div class="d">按峰谷伸缩与降级</div></div>
      <div class="pillar"><span class="ic">§</span><div class="t">安全与合规</div><div class="d">策略与审计可插拔</div></div>
      <div class="pillar"><span class="ic">◎</span><div class="t">可观测性</div><div class="d">从调用图到业务指标</div></div>
      <div class="pillar"><span class="ic">∞</span><div class="t">工程文化</div><div class="d">平台工程 + 领域专家</div></div>
    </div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Future</div></div>
  <span class="wa">{wa}</span>
</section>""",
    # 14 thanks
    """<section class="slide s hero light" id="s14">
  <div class="chrome"><div>致谢</div><div>15 / 15</div></div>
  <div class="frame center" style="min-height:72vh">
    <div class="kicker">感谢收听</div>
    <h1 class="h-hero">下期再会</h1>
    <p class="lead" style="max-width:62vw;margin-top:3vh">拥抱变化，把 AI Agent 做成可靠后端。</p>
    <div class="meta-row" style="margin-top:4vh"><span>斗包 AI 播客</span><span>·</span><span>Agent 后端实践</span></div>
  </div>
  <div class="foot"><div>Agent 后端演进</div><div>Thanks</div></div>
  <span class="wa">{wa}</span>
</section>""",
]


def main():
    if not TEMPLATE.is_file():
        raise SystemExit(f"Missing template: {TEMPLATE}")
    text = TEMPLATE.read_text(encoding="utf-8")
    if "<!-- SLIDES_HERE -->" not in text:
        raise SystemExit("Template missing SLIDES_HERE placeholder")

    if len(SLIDES) != 15 or len(WA) != 15:
        raise SystemExit("Slides/WA count must be 15")

    blocks = []
    for i, (body, wa) in enumerate(zip(SLIDES, WA)):
        blocks.append(body.format(wa=wa))

    slides_html = "\n\n".join(blocks)

    text = text.replace("<title>[必填] 替换为 PPT 标题 · Deck Title</title>",
                        "<title>重新定义AI时代的软件 · Open Design Guizang</title>", 1)
    text = text.replace("<!-- SLIDES_HERE -->", slides_html, 1)

    # wav pipeline: Playwright calls go(n) in quick succession — remove navigation lock
    text = text.replace("let idx=0,total=slides.length,lock=false;",
                        "let idx=0,total=slides.length;", 1)
    text = text.replace(
        "function go(n){\n  if(lock)return;\n  idx=Math.max(0,Math.min(total-1,n));",
        "function go(n){\n  idx=Math.max(0,Math.min(total-1,n));",
        1,
    )
    text = text.replace(
        "  document.body.classList.toggle('light-bg',th==='light');\n  lock=true;setTimeout(()=>lock=false,700);\n}",
        "  document.body.classList.toggle('light-bg',th==='light');\n}",
        1,
    )

    # Anchor text styling (html-video-from-slides .wa)
    inject_css = """
  /* one-context wav pipeline: whisper anchor */
  .wa{position:absolute;bottom:10vh;left:6vw;right:6vw;font-family:var(--mono);font-size:max(10px,.78vw);letter-spacing:.12em;opacity:.42;z-index:25;pointer-events:none;line-height:1.45}
"""
    text = text.replace("</style>", inject_css + "\n</style>", 1)

    OUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT} ({len(text)} bytes)")


if __name__ == "__main__":
    main()
