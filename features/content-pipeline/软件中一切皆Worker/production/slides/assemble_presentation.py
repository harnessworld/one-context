# -*- coding: utf-8 -*-
"""Build presentation.html from strings_utf8.txt (UTF-8) + ASCII template. Run from repo: python assemble_presentation.py"""
from pathlib import Path

R = Path(__file__).resolve().parent
L = (R / "strings_utf8.txt").read_text(encoding="utf-8").splitlines()
# strip BOM/empty
L = [x.strip("\ufeff") for x in L]
while L and not L[-1].strip():
    L.pop()
assert len(L) >= 126, len(L)

def S(i: int) -> str:
    return L[i]

# fmt: off
# Indices follow strings_utf8.txt order (0-based)
html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920,initial-scale=1.0">
<title>""" + S(0) + r"""</title>
<link rel="stylesheet" href="../../../../../skills/html-deck-layout/assets/base.css">
<link rel="stylesheet" href="../../../../../skills/html-deck-layout/assets/fonts.css">
<link rel="stylesheet" href="../../../../../skills/html-deck-layout/assets/mobile-layout.css">
<link rel="stylesheet" href="../../../../../skills/html-deck-layout/assets/themes/mobile-tech.css">
<style>
body{margin:0;background:#000;display:flex;justify-content:center;align-items:center;min-height:100vh}
.wa{font-size:var(--fs-caption);color:var(--c-text-2);opacity:.55;position:absolute;bottom:16px;left:48px;z-index:2;max-width:42%}
.s.slide{position:relative;overflow:hidden}
.s.slide::before{
  content:"";position:absolute;inset:0;pointer-events:none;z-index:0;
  background:
    radial-gradient(ellipse 120% 85% at 12% 8%, rgba(99,102,241,.28), transparent 58%),
    radial-gradient(ellipse 90% 70% at 88% 90%, rgba(34,211,238,.18), transparent 52%),
    radial-gradient(ellipse 70% 50% at 50% 100%, rgba(168,85,247,.14), transparent 48%);
  opacity:.95;
}
.deco-orb{position:absolute;border-radius:50%;pointer-events:none;z-index:0;filter:blur(0)}
.deco-grid{position:absolute;inset:0;pointer-events:none;z-index:0;opacity:.055}
.s.slide>.slide-header,.s.slide>.col,.s.slide>.slide-footer{position:relative;z-index:1}
.s.slide>.wa{z-index:2}
.s.slide>.deco-orb,.s.slide>.deco-grid{z-index:0}
.card-diagram{min-height:280px}
.card-diagram svg{filter:drop-shadow(0 12px 32px rgba(0,0,0,.32))}
.split-panels{display:flex;gap:var(--sp-lg);align-items:stretch;min-height:0}
.split-panels .panel{
  flex:1;display:flex;flex-direction:column;justify-content:center;padding:var(--sp-lg);
  background:var(--c-surface);border-radius:16px;border:2px solid var(--c-surface-2);
  box-shadow:0 4px 24px rgba(0,0,0,.12);
}
.stat-hero{text-align:center;padding:var(--sp-md) 0}
.stat-hero .big{font-size:clamp(72px,8vw,120px);font-weight:900;line-height:1;letter-spacing:-.04em;
  background:linear-gradient(135deg,var(--c-accent-a),var(--c-accent-b));-webkit-background-clip:text;background-clip:text;color:transparent}
</style>
</head>
<body>
<div id="prog" style="width:0%"></div>
<div id="P">
<!-- s0: Cover -->
<section class="s slide is-active" id="s0">
<div class="deco-orb" style="width:420px;height:420px;top:-100px;right:-60px;background:radial-gradient(circle,rgba(56,189,248,.2),transparent 70%)"></div>
<div class="deco-orb" style="width:320px;height:320px;bottom:-80px;left:-40px;background:radial-gradient(circle,rgba(16,185,129,.14),transparent 70%)"></div>
<svg class="deco-grid" viewBox="0 0 1920 1080" preserveAspectRatio="none"><defs><pattern id="g0" width="64" height="64" patternUnits="userSpaceOnUse"><path d="M64 0L0 0 0 64" fill="none" stroke="var(--c-text-2)" stroke-width=".6"/></pattern></defs><rect width="100%" height="100%" fill="url(#g0)"/></svg>
<div class="col slide-main v-center">
<div style="text-align:center">
<div class="emoji-xl">&#127897;</div>
<h1 style="font-size:var(--fs-hero);font-weight:800;margin:24px 0 12px">""" + S(0) + r"""</h1>
<p style="font-size:var(--fs-subtitle);color:var(--c-text-2);margin:0 0 32px">""" + S(1) + r"""</p>
<span class="pill">""" + S(2) + r"""</span>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>01 / 15</span></div>
<span class="wa">""" + S(3) + r"""</span>
</section>

<!-- s1: Intro -->
<section class="s slide" id="s1">
<div class="deco-orb" style="width:300px;height:300px;top:10%;right:-40px;background:radial-gradient(circle,rgba(99,102,241,.18),transparent 70%)"></div>
<svg class="deco-grid" viewBox="0 0 1920 1080" preserveAspectRatio="none"><defs><pattern id="g1" width="80" height="80" patternUnits="userSpaceOnUse"><circle cx="40" cy="40" r="1.2" fill="var(--c-text-2)"/></pattern></defs><rect width="100%" height="100%" fill="url(#g1)"/></svg>
<div class="slide-header">
<span class="badge">""" + S(4) + r"""</span>
<h2>""" + S(5) + r"""</h2>
</div>
<div class="col slide-main fill-deck">
<div class="slide-cards grid-2x2">
<div class="g">
<div class="emoji-lg">&#128200;</div>
<h3 class="g-title">""" + S(6) + r"""</h3>
<p class="g-body">""" + S(7) + r"""</p>
</div>
<div class="g">
<div class="emoji-lg">&#128295;</div>
<h3 class="g-title">""" + S(8) + r"""</h3>
<p class="g-body">""" + S(9) + r"""</p>
</div>
<div class="g">
<div class="emoji-lg">&#127981;</div>
<h3 class="g-title">""" + S(10) + r"""</h3>
<p class="g-body">""" + S(11) + r"""</p>
</div>
<div class="g">
<div class="emoji-lg">&#127919;</div>
<h3 class="g-title">""" + S(12) + r"""</h3>
<p class="g-body">""" + S(13) + r"""</p>
</div>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>02 / 15</span></div>
<span class="wa">""" + S(14) + r"""</span>
</section>

<!-- s2: Myth 1 -->
<section class="s slide" id="s2">
<div class="deco-orb" style="width:280px;height:280px;bottom:-20px;left:5%;background:radial-gradient(circle,rgba(244,63,94,.12),transparent 70%)"></div>
<div class="slide-header">
<span class="badge">""" + S(15) + r"""</span>
<h2>""" + S(16) + r"""</h2>
</div>
<div class="col slide-main fill-deck" style="display:flex;gap:var(--sp-lg)">
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-d)">
<div class="emoji-lg" style="text-align:center">&#129504;</div>
<h3 style="text-align:center;font-size:var(--fs-card-title);color:var(--c-accent-d)">""" + S(17) + r"""</h3>
<p style="font-size:var(--fs-body);text-align:center;color:var(--c-text-1)">""" + S(18) + r"""<br>""" + S(19) + r"""<br>""" + S(20) + r"""</p>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-a)">
<div class="emoji-lg" style="text-align:center">&#9881;&#65039;</div>
<h3 style="text-align:center;font-size:var(--fs-card-title);color:var(--c-accent-a)">""" + S(21) + r"""</h3>
<p style="font-size:var(--fs-body);text-align:center;color:var(--c-text-1)">""" + S(22) + r"""<br>""" + S(23) + r"""<br>""" + S(24) + r"""</p>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>03 / 15</span></div>
<span class="wa">""" + S(25) + r"""</span>
</section>

<!-- s3: Myth 2 -->
<section class="s slide" id="s3">
<div class="slide-header">
<span class="badge">""" + S(26) + r"""</span>
<h2>""" + S(27) + r"""</h2>
</div>
<div class="col slide-main fill-deck">
<div class="slide-cards grid-2x2">
<div class="g">
<div class="emoji-lg">&#129309;</div>
<h3 class="g-title">""" + S(28) + r"""</h3>
<p class="g-body">""" + S(29) + r"""</p>
</div>
<div class="g">
<div class="emoji-lg">&#129520;</div>
<h3 class="g-title">""" + S(30) + r"""</h3>
<p class="g-body">""" + S(31) + r"""</p>
</div>
<div class="g">
<div class="emoji-lg">&#128269;</div>
<h3 class="g-title">""" + S(32) + r"""</h3>
<p class="g-body">""" + S(33) + r"""</p>
</div>
<div class="g">
<div class="emoji-lg">&#128201;</div>
<h3 class="g-title">""" + S(34) + r"""</h3>
<p class="g-body">""" + S(35) + r"""</p>
</div>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>04 / 15</span></div>
<span class="wa">""" + S(36) + r"""</span>
</section>

<!-- s4: Core - W/T/F -->
<section class="s slide" id="s4">
<div class="slide-header">
<span class="badge">""" + S(37) + r"""</span>
<h2>""" + S(38) + r"""</h2>
</div>
<div class="col slide-main fill-deck">
<div class="card-diagram">
<svg viewBox="0 0 1800 700" preserveAspectRatio="xMidYMid meet">
<rect x="80" y="180" width="460" height="340" rx="20" fill="var(--c-accent-a)" opacity="0.1" stroke="var(--c-accent-a)" stroke-width="3"/>
<text x="310" y="260" text-anchor="middle" font-size="36" fill="var(--c-text-2)" font-weight="600">WORKER</text>
<text x="310" y="320" text-anchor="middle" font-size="52" fill="var(--c-accent-a)" font-weight="800">Worker</text>
<text x="310" y="380" text-anchor="middle" font-size="28" fill="var(--c-text-2)">""" + S(39) + r"""</text>
<text x="310" y="430" text-anchor="middle" font-size="24" fill="var(--c-text-2)">""" + S(40) + r"""</text>
<rect x="670" y="180" width="460" height="340" rx="20" fill="var(--c-accent-b)" opacity="0.1" stroke="var(--c-accent-b)" stroke-width="3"/>
<text x="900" y="260" text-anchor="middle" font-size="36" fill="var(--c-text-2)" font-weight="600">TRIGGER</text>
<text x="900" y="320" text-anchor="middle" font-size="52" fill="var(--c-accent-b)" font-weight="800">Trigger</text>
<text x="900" y="380" text-anchor="middle" font-size="28" fill="var(--c-text-2)">""" + S(41) + r"""</text>
<text x="900" y="430" text-anchor="middle" font-size="24" fill="var(--c-text-2)">""" + S(42) + r"""</text>
<rect x="1260" y="180" width="460" height="340" rx="20" fill="var(--c-accent-c)" opacity="0.1" stroke="var(--c-accent-c)" stroke-width="3"/>
<text x="1490" y="260" text-anchor="middle" font-size="36" fill="var(--c-text-2)" font-weight="600">FUNCTION</text>
<text x="1490" y="320" text-anchor="middle" font-size="52" fill="var(--c-accent-c)" font-weight="800">Function</text>
<text x="1490" y="380" text-anchor="middle" font-size="28" fill="var(--c-text-2)">""" + S(43) + r"""</text>
<text x="1490" y="430" text-anchor="middle" font-size="24" fill="var(--c-text-2)">""" + S(44) + r"""</text>
<line x1="540" y1="350" x2="670" y2="350" stroke="var(--c-text-2)" stroke-width="2" stroke-dasharray="8,4"/>
<line x1="1130" y1="350" x2="1260" y2="350" stroke="var(--c-text-2)" stroke-width="2" stroke-dasharray="8,4"/>
<text x="900" y="620" text-anchor="middle" font-size="32" fill="var(--c-accent-e)" font-weight="700">""" + S(45) + r"""</text>
</svg>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>05 / 15</span></div>
<span class="wa">""" + S(46) + r"""</span>
</section>

<!-- s5: Biggest Pitfall -->
<section class="s slide" id="s5">
<div class="slide-header">
<span class="badge">""" + S(47) + r"""</span>
<h2>""" + S(48) + r"""</h2>
</div>
<div class="col slide-main fill-deck" style="display:flex;gap:var(--sp-lg)">
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-d)">
<h3 style="font-size:var(--fs-card-title);color:var(--c-accent-d);margin-bottom:var(--sp-md)">""" + S(49) + r"""</h3>
<ul style="font-size:var(--fs-body);color:var(--c-text-1);list-style:none;padding:0">
<li>· 外部系统对接、胶水代码堆叠</li>
<li>· 协议与适配层越来越厚</li>
<li>· 集成测试与联调占用大量时间</li>
<li>· 但链路一断仍难定位根因</li>
</ul>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-a)">
<h3 style="font-size:var(--fs-card-title);color:var(--c-accent-a);margin-bottom:var(--sp-md)">""" + S(50) + r"""</h3>
<ul style="font-size:var(--fs-body);color:var(--c-text-1);list-style:none;padding:0">
<li>· Agent 内部状态与流程失控</li>
<li>· 任务边界不清、重试与补偿混乱</li>
<li>· 缺少统一语义与 Tracing</li>
<li>· 运维与排障成本指数上升</li>
</ul>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>06 / 15</span></div>
<span class="wa">很多人盯着集成难题，内部混乱更要命</span>
</section>

<!-- s6: Three-Model Features -->
<section class="s slide" id="s6">
<div class="slide-header">
<span class="badge">""" + S(51) + r"""</span>
<h2>""" + S(52) + r"""</h2>
</div>
<div class="col slide-main fill-deck">
<div class="card-diagram">
<svg viewBox="0 0 1800 700" preserveAspectRatio="xMidYMid meet">
<circle cx="900" cy="350" r="140" fill="var(--c-accent-a)" opacity="0.15" stroke="var(--c-accent-a)" stroke-width="3"/>
<text x="900" y="330" text-anchor="middle" font-size="32" fill="var(--c-accent-a)" font-weight="700">Worker</text>
<text x="900" y="370" text-anchor="middle" font-size="32" fill="var(--c-accent-b)" font-weight="700">Trigger</text>
<text x="900" y="410" text-anchor="middle" font-size="32" fill="var(--c-accent-c)" font-weight="700">Function</text>
<rect x="700" y="40" width="400" height="90" rx="16" fill="var(--c-surface-2)" stroke="var(--c-accent-a)" stroke-width="2"/>
<text x="900" y="95" text-anchor="middle" font-size="28" fill="var(--c-text-1)" font-weight="600">Agent 本身也是一个 Worker</text>
<line x1="900" y1="130" x2="900" y2="210" stroke="var(--c-accent-a)" stroke-width="2"/>
<rect x="60" y="260" width="380" height="90" rx="16" fill="var(--c-surface-2)" stroke="var(--c-accent-b)" stroke-width="2"/>
<text x="250" y="315" text-anchor="middle" font-size="28" fill="var(--c-text-1)" font-weight="600">""" + S(53) + r"""</text>
<line x1="440" y1="305" x2="760" y2="345" stroke="var(--c-accent-b)" stroke-width="2"/>
<rect x="1360" y="260" width="380" height="90" rx="16" fill="var(--c-surface-2)" stroke="var(--c-accent-c)" stroke-width="2"/>
<text x="1550" y="315" text-anchor="middle" font-size="28" fill="var(--c-text-1)" font-weight="600">""" + S(54) + r"""</text>
<line x1="1360" y1="305" x2="1040" y2="345" stroke="var(--c-accent-c)" stroke-width="2"/>
<rect x="120" y="510" width="360" height="90" rx="16" fill="var(--c-surface-2)" stroke="var(--c-accent-e)" stroke-width="2"/>
<text x="300" y="565" text-anchor="middle" font-size="28" fill="var(--c-text-1)" font-weight="600">""" + S(55) + r"""</text>
<line x1="380" y1="510" x2="800" y2="400" stroke="var(--c-accent-e)" stroke-width="2"/>
<rect x="1320" y="510" width="360" height="90" rx="16" fill="var(--c-surface-2)" stroke="var(--c-accent-d)" stroke-width="2"/>
<text x="1500" y="565" text-anchor="middle" font-size="28" fill="var(--c-text-1)" font-weight="600">""" + S(56) + r"""</text>
<line x1="1420" y1="510" x2="1000" y2="400" stroke="var(--c-accent-d)" stroke-width="2"/>
</svg>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>07 / 15</span></div>
<span class="wa">""" + S(57) + r"""</span>
</section>

<!-- s7: Solve Traditional -->
<section class="s slide" id="s7">
<div class="slide-header">
<span class="badge">""" + S(58) + r"""</span>
<h2>""" + S(59) + r"""</h2>
</div>
<div class="col slide-main fill-deck" style="display:flex;gap:var(--sp-lg)">
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-d)">
<h3 style="font-size:var(--fs-card-title);color:var(--c-accent-d);margin-bottom:var(--sp-md)">""" + S(60) + r"""</h3>
<ul style="font-size:var(--fs-body);color:var(--c-text-1);list-style:none;padding:0">
<li>· Agent 与业务系统两套语言</li>
<li>· 桥接层厚重，Tracing 割裂</li>
<li>· 状态分散、重试策略不统一</li>
<li>· 变更牵一发动全身</li>
</ul>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-a)">
<h3 style="font-size:var(--fs-card-title);color:var(--c-accent-a);margin-bottom:var(--sp-md)">""" + S(61) + r"""</h3>
<ul style="font-size:var(--fs-body);color:var(--c-text-1);list-style:none;padding:0">
<li>· Agent 与后端无缝融合</li>
<li>· 统一语义，观测与排障对齐</li>
<li>· 全链路可追踪</li>
<li>· 一切先落成 Worker 再组合</li>
</ul>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>08 / 15</span></div>
<span class="wa">""" + S(62) + r"""</span>
</section>

<!-- s8: AI Infra Part 1 -->
<section class="s slide" id="s8">
<div class="slide-header">
<span class="badge">""" + S(63) + r"""</span>
<h2>""" + S(64) + r"""</h2>
</div>
<div class="col slide-main v-center">
<div style="text-align:center">
<div class="emoji-xl">&#11088;</div>
<div style="font-size:var(--fs-stat);font-weight:900;color:var(--c-accent-a);margin:24px 0">1st-class</div>
<p style="font-size:var(--fs-subtitle);color:var(--c-text-1)">""" + S(65) + r"""</p>
<p style="font-size:var(--fs-body);color:var(--c-text-2);margin-top:var(--sp-md)">""" + S(66) + r"""</p>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>09 / 15</span></div>
<span class="wa">""" + S(67) + r"""</span>
</section>

<!-- s9: AI Infra Part 2 -->
<section class="s slide" id="s9">
<div class="slide-header">
<span class="badge">""" + S(68) + r"""</span>
<h2>""" + S(69) + r"""</h2>
</div>
<div class="col slide-main fill-deck">
<div style="display:flex;gap:var(--sp-lg);margin-bottom:var(--sp-md)">
<div style="flex:1;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-b)">
<h3 style="font-size:var(--fs-card-title);color:var(--c-accent-b);margin-bottom:var(--sp-sm)">""" + S(70) + r"""</h3>
<p style="font-size:var(--fs-body);color:var(--c-text-1)">""" + S(71) + r"""</p>
</div>
<div style="flex:1;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-a)">
<h3 style="font-size:var(--fs-card-title);color:var(--c-accent-a);margin-bottom:var(--sp-sm)">""" + S(72) + r"""</h3>
<p style="font-size:var(--fs-body);color:var(--c-text-1)">""" + S(73) + r"""</p>
</div>
<div style="flex:1;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-e)">
<h3 style="font-size:var(--fs-card-title);color:var(--c-accent-e);margin-bottom:var(--sp-sm)">""" + S(74) + r"""</h3>
<p style="font-size:var(--fs-body);color:var(--c-text-1)">""" + S(75) + r"""</p>
</div>
</div>
<div class="card-diagram" style="min-height:220px">
<svg viewBox="0 0 1600 240" preserveAspectRatio="xMidYMid meet">
<defs><marker id="arr9" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="var(--c-accent-a)"/></marker></defs>
<rect x="40" y="60" width="280" height="100" rx="14" fill="var(--c-accent-b)" opacity="0.12" stroke="var(--c-accent-b)" stroke-width="2"/>
<text x="180" y="125" text-anchor="middle" font-size="26" fill="var(--c-text-1)">""" + S(76) + r"""</text>
<line x1="320" y1="110" x2="420" y2="110" stroke="var(--c-accent-a)" stroke-width="3" marker-end="url(#arr9)"/>
<rect x="420" y="50" width="360" height="120" rx="16" fill="var(--c-accent-a)" opacity="0.15" stroke="var(--c-accent-a)" stroke-width="2"/>
<text x="600" y="105" text-anchor="middle" font-size="28" font-weight="700" fill="var(--c-accent-a)">""" + S(77) + r"""</text>
<text x="600" y="145" text-anchor="middle" font-size="22" fill="var(--c-text-2)">Worker / Trigger / Function</text>
<line x1="780" y1="110" x2="880" y2="110" stroke="var(--c-accent-a)" stroke-width="3" marker-end="url(#arr9)"/>
<rect x="880" y="60" width="280" height="100" rx="14" fill="var(--c-accent-c)" opacity="0.12" stroke="var(--c-accent-c)" stroke-width="2"/>
<text x="1020" y="125" text-anchor="middle" font-size="26" fill="var(--c-text-1)">""" + S(78) + r"""</text>
<line x1="1160" y1="110" x2="1260" y2="110" stroke="var(--c-accent-e)" stroke-width="3" marker-end="url(#arr9)"/>
<rect x="1260" y="70" width="300" height="80" rx="12" fill="var(--c-surface-2)" stroke="var(--c-accent-e)" stroke-width="2"/>
<text x="1410" y="125" text-anchor="middle" font-size="24" fill="var(--c-text-1)">""" + S(79) + r"""</text>
</svg>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>10 / 15</span></div>
<span class="wa">""" + S(80) + r"""</span>
</section>

<!-- s10: Thin vs Thick Harness -->
<section class="s slide" id="s10">
<div class="slide-header">
<span class="badge">""" + S(81) + r"""</span>
<h2>""" + S(82) + r"""</h2>
</div>
<div class="col slide-main fill-deck" style="display:flex;gap:var(--sp-lg)">
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-a)">
<div class="emoji-lg" style="text-align:center">&#129517;</div>
<h3 style="text-align:center;font-size:var(--fs-card-title);color:var(--c-accent-a)">""" + S(83) + r"""</h3>
<p style="font-size:var(--fs-body);text-align:center;color:var(--c-text-1)">只做连接与编排壳<br>业务语义下沉到 Worker<br>迭代快、边界清晰</p>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:var(--sp-lg);background:var(--c-surface);border-radius:16px;border:2px solid var(--c-accent-d)">
<div class="emoji-lg" style="text-align:center">&#129521;</div>
<h3 style="text-align:center;font-size:var(--fs-card-title);color:var(--c-accent-d)">""" + S(84) + r"""</h3>
<p style="font-size:var(--fs-body);text-align:center;color:var(--c-text-1)">承载大量策略与状态<br>易成新的单体瓶颈<br>升级与测试成本高</p>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>11 / 15</span></div>
<span class="wa">""" + S(85) + r"""</span>
</section>

<!-- s11: Boundary Dissolution Part 1 -->
<section class="s slide" id="s11">
<div class="slide-header">
<span class="badge">""" + S(86) + r"""</span>
<h2>""" + S(87) + r"""</h2>
</div>
<div class="col slide-main fill-deck">
<div class="card-diagram">
<svg viewBox="0 0 1800 650" preserveAspectRatio="xMidYMid meet">
<rect x="80" y="80" width="700" height="220" rx="16" fill="var(--c-accent-a)" opacity="0.1" stroke="var(--c-accent-a)" stroke-width="2"/>
<text x="430" y="140" text-anchor="middle" font-size="32" fill="var(--c-accent-a)" font-weight="700">""" + S(88) + r"""</text>
<text x="200" y="210" text-anchor="middle" font-size="26" fill="var(--c-text-1)">Worker</text>
<text x="430" y="210" text-anchor="middle" font-size="26" fill="var(--c-text-1)">Trigger</text>
<text x="660" y="210" text-anchor="middle" font-size="26" fill="var(--c-text-1)">Function</text>
<rect x="1020" y="80" width="700" height="220" rx="16" fill="var(--c-accent-b)" opacity="0.1" stroke="var(--c-accent-b)" stroke-width="2"/>
<text x="1370" y="140" text-anchor="middle" font-size="32" fill="var(--c-accent-b)" font-weight="700">""" + S(89) + r"""</text>
<text x="1140" y="210" text-anchor="middle" font-size="26" fill="var(--c-text-1)">Worker</text>
<text x="1370" y="210" text-anchor="middle" font-size="26" fill="var(--c-text-1)">Trigger</text>
<text x="1600" y="210" text-anchor="middle" font-size="26" fill="var(--c-text-1)">Function</text>
<text x="900" y="210" text-anchor="middle" font-size="60" fill="var(--c-accent-e)" font-weight="900">=</text>
<rect x="300" y="400" width="1200" height="180" rx="20" fill="var(--c-accent-e)" opacity="0.1" stroke="var(--c-accent-e)" stroke-width="3"/>
<text x="900" y="480" text-anchor="middle" font-size="36" fill="var(--c-accent-e)" font-weight="700">""" + S(90) + r"""</text>
<text x="900" y="540" text-anchor="middle" font-size="28" fill="var(--c-text-2)">""" + S(91) + r"""</text>
<line x1="430" y1="300" x2="700" y2="400" stroke="var(--c-accent-a)" stroke-width="2" marker-end="url(#arr2)"/>
<line x1="1370" y1="300" x2="1100" y2="400" stroke="var(--c-accent-b)" stroke-width="2" marker-end="url(#arr2)"/>
<defs><marker id="arr2" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="var(--c-accent-e)"/></marker></defs>
</svg>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>12 / 15</span></div>
<span class="wa">""" + S(92) + r"""</span>
</section>

<!-- s12: Boundary Dissolution Part 2 -->
<section class="s slide" id="s12">
<div class="slide-header">
<span class="badge">""" + S(93) + r"""</span>
<h2>""" + S(94) + r"""</h2>
</div>
<div class="col slide-main fill-deck">
<div class="card-diagram" style="min-height:520px;background:var(--c-surface);border-radius:var(--r-md);padding:var(--card-pad)">
<svg viewBox="0 0 1760 560" preserveAspectRatio="xMidYMid meet">
<defs>
<linearGradient id="g12a" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="var(--c-accent-a)" stop-opacity="0.35"/><stop offset="100%" stop-color="var(--c-accent-a)" stop-opacity="0.08"/></linearGradient>
<linearGradient id="g12b" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="var(--c-accent-b)" stop-opacity="0.35"/><stop offset="100%" stop-color="var(--c-accent-b)" stop-opacity="0.08"/></linearGradient>
<linearGradient id="g12e" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="var(--c-accent-e)"/><stop offset="100%" stop-color="var(--c-accent-c)"/></linearGradient>
<marker id="m12" markerWidth="12" markerHeight="8" refX="11" refY="4" orient="auto"><polygon points="0 0,12 4,0 8" fill="var(--c-accent-e)"/></marker>
</defs>
<rect x="40" y="40" width="480" height="200" rx="20" fill="url(#g12a)" stroke="var(--c-accent-a)" stroke-width="2.5"/>
<text x="280" y="95" text-anchor="middle" font-size="30" font-weight="800" fill="var(--c-accent-a)">""" + S(95) + r"""</text>
<text x="280" y="140" text-anchor="middle" font-size="24" fill="var(--c-text-1)">""" + S(96) + r"""</text>
<text x="280" y="180" text-anchor="middle" font-size="22" fill="var(--c-text-2)">""" + S(97) + r"""</text>
<rect x="640" y="40" width="480" height="200" rx="20" fill="url(#g12b)" stroke="var(--c-accent-b)" stroke-width="2.5"/>
<text x="880" y="95" text-anchor="middle" font-size="30" font-weight="800" fill="var(--c-accent-b)">""" + S(98) + r"""</text>
<text x="880" y="140" text-anchor="middle" font-size="24" fill="var(--c-text-1)">""" + S(99) + r"""</text>
<text x="880" y="180" text-anchor="middle" font-size="22" fill="var(--c-text-2)">""" + S(100) + r"""</text>
<rect x="1240" y="40" width="480" height="200" rx="20" fill="var(--c-surface-2)" stroke="var(--c-accent-e)" stroke-width="2.5"/>
<text x="1480" y="100" text-anchor="middle" font-size="30" font-weight="800" fill="var(--c-accent-e)">""" + S(101) + r"""</text>
<text x="1480" y="150" text-anchor="middle" font-size="24" fill="var(--c-text-1)">""" + S(102) + r"""</text>
<text x="1480" y="190" text-anchor="middle" font-size="22" fill="var(--c-text-2)">""" + S(103) + r"""</text>
<line x1="520" y1="140" x2="630" y2="140" stroke="url(#g12e)" stroke-width="4" marker-end="url(#m12)"/>
<line x1="1120" y1="140" x2="1230" y2="140" stroke="url(#g12e)" stroke-width="4" marker-end="url(#m12)"/>
<rect x="120" y="300" width="1520" height="200" rx="22" fill="var(--c-accent-e)" fill-opacity="0.08" stroke="var(--c-accent-e)" stroke-width="2"/>
<text x="880" y="355" text-anchor="middle" font-size="32" font-weight="800" fill="var(--c-accent-e)">""" + S(104) + r"""</text>
<text x="880" y="405" text-anchor="middle" font-size="26" fill="var(--c-text-1)">""" + S(105) + r"""</text>
<path d="M 280 420 L 440 420 L 500 460 L 1320 460 L 1380 420 L 1480 420" fill="none" stroke="var(--c-accent-a)" stroke-width="3" stroke-dasharray="10 6" opacity="0.9"/>
<circle cx="280" cy="420" r="14" fill="var(--c-accent-a)"/><circle cx="880" cy="460" r="14" fill="var(--c-accent-b)"/><circle cx="1480" cy="420" r="14" fill="var(--c-accent-c)"/>
<text x="280" y="450" text-anchor="middle" font-size="22" fill="var(--c-text-2)">""" + S(106) + r"""</text>
<text x="880" y="505" text-anchor="middle" font-size="22" fill="var(--c-text-2)">""" + S(107) + r"""</text>
<text x="1480" y="450" text-anchor="middle" font-size="22" fill="var(--c-text-2)">""" + S(108) + r"""</text>
</svg>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>13 / 15</span></div>
<span class="wa">""" + S(109) + r"""</span>
</section>

<!-- s13: Future Direction -->
<section class="s slide" id="s13">
<div class="slide-header">
<span class="badge">""" + S(110) + r"""</span>
<h2>""" + S(111) + r"""</h2>
</div>
<div class="col slide-main fill-deck">
<div class="slide-cards grid-2x2">
<div class="g">
<div class="emoji-lg">&#9878;&#65039;</div>
<h3 class="g-title">""" + S(112) + r"""</h3>
<p class="g-body">""" + S(113) + r"""</p>
</div>
<div class="g">
<div class="emoji-lg">&#128737;&#65039;</div>
<h3 class="g-title">""" + S(114) + r"""</h3>
<p class="g-body">""" + S(115) + r"""</p>
</div>
<div class="g">
<div class="emoji-lg">&#128202;</div>
<h3 class="g-title">""" + S(116) + r"""</h3>
<p class="g-body">""" + S(117) + r"""</p>
</div>
<div class="g">
<div class="emoji-lg">&#128260;</div>
<h3 class="g-title">""" + S(118) + r"""</h3>
<p class="g-body">""" + S(119) + r"""</p>
</div>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>14 / 15</span></div>
<span class="wa">""" + S(120) + r"""</span>
</section>

<!-- s14: Thanks -->
<section class="s slide" id="s14">
<div class="col slide-main v-center">
<div style="text-align:center">
<div class="emoji-xl">&#128588;</div>
<h1 style="font-size:var(--fs-hero);font-weight:800;margin:24px 0 12px">""" + S(121) + r"""</h1>
<p style="font-size:var(--fs-subtitle);color:var(--c-text-2);margin:0 0 32px">""" + S(122) + r"""</p>
<span class="pill">""" + S(123) + r"""</span>
</div>
</div>
<div class="slide-footer"><span>""" + S(125) + r"""</span><span>15 / 15</span></div>
<span class="wa">""" + S(124) + r"""</span>
</section>

</div>
<div id="pn"></div>
<script>
(function(){
var PW=1920,PH=1080;
function fit(){var el=document.getElementById('P'),r=Math.min(window.innerWidth/PW,window.innerHeight/PH),x=(window.innerWidth-PW*r)/2,y=(window.innerHeight-PH*r)/2;el.style.transform='scale('+r+')';el.style.transformOrigin='0 0';el.style.left=x+'px';el.style.top=y+'px'}
window.addEventListener('resize',fit);fit();
var slides=document.querySelectorAll('.s.slide'),total=slides.length,cur=0;
function ui(){document.getElementById('pn').textContent=(cur+1)+' / '+total;var b=document.getElementById('prog');if(b)b.style.width=(cur/(total-1)*100)+'%'}
function go(i){if(i<0||i>=total)return;slides[cur].classList.remove('is-active');cur=i;slides[cur].classList.add('is-active');ui()}
document.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '){e.preventDefault();go(cur+1)}else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){e.preventDefault();go(cur-1)}});
document.addEventListener('click',function(e){if(e.clientX>window.innerWidth*0.3)go(cur+1);else go(cur-1)});
ui();
})();
</script>
</body>
</html>
"""
# fmt: on

(R / "presentation.html").write_text(html, encoding="utf-8", newline="\n")
print("Wrote", R / "presentation.html", "chars", len(html))
