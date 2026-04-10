# -*- coding: utf-8 -*-
"""
Hermes 播客幻灯：版式与 features/develop/ai-mid-mgmt-video/production/presentation.html 同源
（1920×1080、biz-bg/vignette/grid/top、wrap-split、viz-box、part-num、stat、strip、card）。

满足 skills/html-video-from-slides：go(n)、.slide 内可见文案为口播原句或子串，便于 wav-auto。
"""
from __future__ import annotations

import pathlib
import re

HERE = pathlib.Path(__file__).resolve()
# production/ → hermes-agent-short-video/ → develop/
AI_MID = HERE.parent.parent.parent / "ai-mid-mgmt-video" / "production" / "presentation.html"
OUT = HERE.parent / "presentation.html"


def load_biz_css() -> str:
    raw = AI_MID.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", raw, re.DOTALL)
    if not m:
        raise SystemExit("ai-mid-mgmt presentation: missing <style>")
    css = m.group(1)
    return (
        css
        + """
.pill-purple{background:rgba(129,140,246,0.14);color:#ddd6fe;border-color:rgba(167,139,250,0.45);}
.sub-compact{font-size:40px;font-weight:600;line-height:1.48;color:var(--ink2);max-width:1520px;text-align:left;}
.sub-compact strong{color:#fff;font-weight:800;}
.viz-tall{min-height:520px;}
.viz-short{min-height:280px;max-width:900px;margin:0 auto;}
"""
    )


BIZ = '<div class="biz-bg"></div><div class="biz-vignette"></div><div class="biz-grid"></div><div class="biz-top"></div>'


def slide(idx: int, active: bool, inner: str) -> str:
    a = " active" if active else ""
    return f'<div class="slide{a}" id="slide-{idx}">\n{BIZ}\n{inner}\n</div>'


def p(txt: str) -> str:
    return f'    <p class="sub sub-compact">{txt}</p>'


def main() -> None:
    css = load_biz_css()
    parts: list[str] = []
    i = 0

    def add(inner: str) -> None:
        nonlocal i, parts
        parts.append(slide(i, i == 0, inner))
        i += 1

    # 0 封面
    add(
        f"""  <div class="wrap wrap-split">
    <div class="txt">
      <div class="pill pill-muted">豆包 AI 播客 · 讲稿可视化</div>
      <div class="title title-lg">Hermes<br><span class="hl">Agent</span></div>
      {p("欢迎收听豆包AI播客节目。")}
      {p("请不吝点赞 订阅 转发 打赏支持明镜与点点栏目")}
    </div>
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 400 360" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="hg0" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#38bdf8"/><stop offset="100%" style="stop-color:#6366f1"/></linearGradient>
        </defs>
        <rect x="20" y="20" width="360" height="320" rx="24" fill="rgba(15,23,42,0.55)" stroke="rgba(148,163,184,0.2)"/>
        <circle cx="200" cy="170" r="100" fill="none" stroke="rgba(56,189,248,0.25)" stroke-width="2"/>
        <circle cx="200" cy="170" r="70" fill="none" stroke="rgba(129,140,246,0.2)" stroke-width="2"/>
        <circle cx="200" cy="170" r="40" fill="url(#hg0)" opacity="0.35"/>
        <polygon points="200,120 230,200 170,200" fill="#a78bfa" opacity="0.9"/>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="pill pill-ok">开场</div>
    <div class="title title-sm">本期聊聊 <span class="hl">Hermes Agent</span></div>
    {p("Hello 大家好,欢迎收听。")}
    {p("我们的播客啊,今天咱们要聊一聊")}
    {p("最近技术圈特别火的一个东西啊,叫Hermes Agent。")}
  </div>"""
    )

    add(
        f"""  <div class="wrap wrap-split">
    <div class="txt">
      <div class="pill pill-warn">悬念</div>
      <div class="title title-sm">开源 · <span class="accent-w">自动生成技能</span></div>
      {p("这个东西到底是个什么来头,为什么?")}
      {p("他一开源就能够引来这么多开发者的关注,说他能够自动生成技能。")}
      {p("这东西到底有多神奇?")}
    </div>
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 400 320" xmlns="http://www.w3.org/2000/svg">
        <rect x="40" y="60" width="320" height="200" rx="20" fill="rgba(245,158,11,0.08)" stroke="rgba(251,191,36,0.4)"/>
        <text x="200" y="130" text-anchor="middle" fill="#fde68a" font-size="28" font-weight="800">?</text>
        <text x="200" y="180" text-anchor="middle" fill="#94a3b8" font-size="20" font-weight="600">开源关注</text>
        <text x="200" y="220" text-anchor="middle" fill="#cbd5e1" font-size="18" font-weight="600">自动生成技能</text>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap wrap-split">
    <div class="txt">
      <div class="pill pill-warn">痛点</div>
      <div class="title title-sm">用 <span class="accent-r">OpenClaw</span> 时</div>
      {p("说到这个我真的是深有体会,")}
      {p("因为之前我用那个<strong>OpenClaw</strong>的时候,")}
      {p("就是这个插件啊什么的,虽然说很多,")}
      {p("但是真的用起来特别麻烦,")}
      {p("就是你每一次都要去手动的配置这个技能啊,")}
    </div>
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
        <rect x="50" y="70" width="300" height="160" rx="16" fill="rgba(251,113,133,0.1)" stroke="#fb7185"/>
        <text x="200" y="140" text-anchor="middle" fill="#fecaca" font-size="22" font-weight="800">手动配置</text>
        <text x="200" y="185" text-anchor="middle" fill="#94a3b8" font-size="18">插件很多 · 很麻烦</text>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="pill pill-warn">重复劳动</div>
    <div class="title title-sm">周报也要<span class="accent-r">重来一遍</span></div>
    {p("然后你每周,比如说你要写周报,")}
    {p("你都要重新来一遍,")}
    {p("这个事情真的是让我特别头大。")}
    <div class="strip" style="margin-top:24px;"><div class="strip-t">配置技能 · 每次从零开始</div></div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="part-row" style="justify-content:center;"><span class="part-tag">PART</span><span class="part-num">01</span></div>
    <div class="part-title" style="text-align:center;width:100%;">设计理念</div>
    <div class="title title-sm"><span class="hl">Hermes Agent</span> 和 OpenClaw</div>
    {p("咱们先来讲第一个,")}
    {p("就是这个<strong>Hermes Agent</strong>和<strong>OpenClaw</strong>,")}
    {p("他们在核心的设计理念上面的差别。")}
    {p("你觉得这两个东西最大的不一样是啥?")}
    {p("这两个我觉得就完全是两个路数,")}
  </div>"""
    )

    add(
        f"""  <div class="wrap wrap-split">
    <div class="txt">
      <div class="pill">OpenClaw</div>
      <div class="title title-sm"><span class="accent">交通枢纽</span> · 调度员</div>
      {p("你可以想象一下<strong>OpenClaw</strong>,")}
      {p("它其实更像是一个<strong>交通枢纽</strong>,")}
      {p("就是它把各个聊天平台啊什么的都接进来,")}
      {p("然后它就专注于这个消息的转发啊,")}
      {p("和这个任务的分发啊,")}
      {p("它就像是一个<strong>幕后的调度员</strong>。")}
    </div>
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 420 340" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="hubg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#38bdf8"/><stop offset="100%" stop-color="#818cf8"/></linearGradient></defs>
        <circle cx="210" cy="170" r="44" fill="url(#hubg)" opacity="0.9"/>
        <text x="210" y="178" text-anchor="middle" fill="#0f172a" font-size="15" font-weight="900">枢纽</text>
        <circle cx="210" cy="50" r="22" fill="#334155" stroke="#64748b"/>
        <circle cx="360" cy="140" r="22" fill="#334155" stroke="#64748b"/>
        <circle cx="60" cy="140" r="22" fill="#334155" stroke="#64748b"/>
        <circle cx="210" cy="290" r="22" fill="#334155" stroke="#64748b"/>
        <line x1="210" y1="126" x2="210" y2="72" stroke="#38bdf8" stroke-width="4"/>
        <line x1="246" y1="160" x2="338" y2="145" stroke="#38bdf8" stroke-width="4"/>
        <line x1="174" y1="160" x2="82" y2="145" stroke="#38bdf8" stroke-width="4"/>
        <line x1="210" y1="214" x2="210" y2="268" stroke="#818cf8" stroke-width="4"/>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap wrap-split">
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 400 340" xmlns="http://www.w3.org/2000/svg">
        <path d="M200,70 A100,100 0 1,1 199,70" fill="none" stroke="#34d399" stroke-width="5"/>
        <polygon points="310,170 295,160 295,180" fill="#34d399"/>
        <circle cx="200" cy="170" r="48" fill="rgba(52,211,153,0.2)" stroke="#34d399" stroke-width="3"/>
        <text x="200" y="182" text-anchor="middle" fill="#a7f3d0" font-size="16" font-weight="800">进化</text>
      </svg>
    </div>
    <div class="txt">
      <div class="pill pill-ok">Hermes Agent</div>
      <div class="title title-sm">另一个<span class="hl">画风</span></div>
      {p("那<strong>Hermes Agent</strong>是不是就完全是另一个画风了?")}
      {p("没错没错。")}
      {p("<strong>Hermes Agent</strong>,他就像是一个可以<strong>自我进化</strong>的一个助手。")}
      {p("他就是每做一件事情,他都能总结经验,")}
      {p("然后他会把这个经验变成自己的一个技能,")}
      {p("他也特别强调这种持续的学习和这个<strong>闭环的反馈</strong>。")}
      {p("他的核心是让自己变得越来越聪明,")}
      {p("而不是说我要去连接很多很多的外部的平台。")}
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="pill pill-muted">对比 · OpenClaw</div>
    <div class="title title-sm">插件市场 · <span class="accent">markdown</span> 记忆</div>
    <div class="compare">
      <div class="card card-a"><div class="card-h">技能侧</div><p class="card-p">下载多 · 手动配置</p></div>
      <div class="card card-b"><div class="card-h">记忆侧</div><p class="card-p">markdown 记关键信息</p></div>
    </div>
    {p("那如果我们再把镜头拉近一点,")}
    {p("就是具体到比如说技能的管理和这个<strong>记忆的存储</strong>,")}
    {p("这两个东西还有哪些比较鲜明的差别呢?")}
    {p("这个技能的话就是<strong>OpenClaw</strong>,它是类似于一个<strong>插件市场</strong>。")}
    {p("你可以去下载很多很多的技能,但是它这个技能的话都是需要你去手动配置的。")}
    {p("然后它的这个记忆的话,就是主要是靠一些markdown的文件去帮你记录一些关键的信息。")}
    {p("就感觉上手会比较友好。")}
  </div>"""
    )

    add(
        f"""  <div class="wrap wrap-split">
    <div class="txt">
      <div class="pill pill-purple">Hermes Agent</div>
      <div class="title title-sm"><span class="hl">自动归纳</span> 技能</div>
      {p("对,然后<strong>Hermes Agent</strong>,他就厉害了,")}
      {p("他是可以在使用的过程当中<strong>自动去归纳出技能</strong>。")}
      {p("他的这个记忆是分了很多层的,有热有冷。")}
      {p("就是他的这个无论是技能还是记忆,")}
      {p("他都更强调一种<strong>智能化的管理</strong>和这种<strong>长期的成长</strong>。")}
      {p("而不是说像OpenClaw,他就只是一个配置和存储的一个便捷性。")}
    </div>
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
        <rect x="100" y="60" width="200" height="44" rx="8" fill="rgba(251,191,36,0.25)" stroke="#fbbf24"/>
        <rect x="100" y="120" width="200" height="44" rx="8" fill="rgba(56,189,248,0.2)" stroke="#38bdf8"/>
        <rect x="100" y="180" width="200" height="44" rx="8" fill="rgba(129,140,246,0.2)" stroke="#818cf8"/>
        <text x="200" y="90" text-anchor="middle" fill="#fde68a" font-size="14" font-weight="700">热</text>
        <text x="200" y="150" text-anchor="middle" fill="#7dd3fc" font-size="14" font-weight="700">温</text>
        <text x="200" y="210" text-anchor="middle" fill="#c4b5fd" font-size="14" font-weight="700">冷</text>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="pill pill-purple">怎么选</div>
    <div class="title title-sm"><span class="hl">AI框架</span> 权衡</div>
    {p("如果说咱们现在有不同的使用场景,")}
    {p("那我们在选择这两个<strong>AI框架</strong>的时候要怎么去<strong>权衡</strong>呢?")}
    {p("如果说你是一个企业,或者说你是一个团队,")}
    {p("你需要有一个东西帮你在多个平台上面去处理大量的消息,")}
    {p("或者说做一些比较复杂的自动化的任务,")}
    {p("那<strong>OpenClaw</strong>可能是一个更好的选择,")}
    {p("因为他的这个<strong>多渠道的连接</strong>和这个管理是非常非常强的。")}
    {p("那如果说我只是一个个人用户,或者说我是一个小的团队呢?")}
  </div>"""
    )

    add(
        f"""  <div class="wrap wrap-split">
    <div class="txt">
      <div class="pill pill-ok">个人 / 小团队</div>
      <div class="title title-sm">隐私 · 本地 · <span class="hl">互补</span></div>
      {p("如果你更看重的是个性化的体验,")}
      {p("然后本地的执行的效率,包括你的隐私的安全,")}
      {p("那<strong>Hermes Agent</strong>就会比较适合你,因为他能自学习,")}
      {p("也可以很方便的在你的本地,或者是说边缘设备上面去部署。")}
      {p("而且他其实跟<strong>OpenClaw</strong>是可以互补的,")}
      {p("就是你可以把他们两个结合起来,")}
      {p("去做一个非常非常灵活的AI的应用。")}
    </div>
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 400 280" xmlns="http://www.w3.org/2000/svg">
        <rect x="60" y="100" width="120" height="80" rx="12" fill="rgba(56,189,248,0.15)" stroke="#38bdf8"/>
        <text x="120" y="148" text-anchor="middle" fill="#7dd3fc" font-size="14" font-weight="800">OpenClaw</text>
        <text x="200" y="145" text-anchor="middle" fill="#94a3b8" font-size="28">+</text>
        <rect x="220" y="100" width="120" height="80" rx="12" fill="rgba(52,211,153,0.15)" stroke="#34d399"/>
        <text x="280" y="148" text-anchor="middle" fill="#6ee7b7" font-size="14" font-weight="800">Hermes</text>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="part-row" style="justify-content:center;"><span class="part-tag">PART</span><span class="part-num">02</span></div>
    <div class="part-title" style="text-align:center;width:100%;">自动生成技能</div>
    <div class="title title-sm">门槛 · 复盘 · <span class="accent-w">模板</span></div>
    {p("咱们现在来聊一聊这个<strong>Hermes Agent</strong>,")}
    {p("他的这个最让人觉得神奇的地方,就是他的这个<strong>自动生成技能</strong>,")}
    {p("这个到底是怎么实现的?他背后的这个触发的机制是什么?")}
    {p("其实他是有一个门槛的,就是只有当你这个任务,")}
    {p("<strong>连续调用了五次工具以上</strong>,他才会认为说OK我要去自动生成一个技能,")}
    {p("就简单的一两个步骤的这种操作他是不会理的。")}
    {p("所以说他是专门针对这种比较复杂的重复性的流程。")}
    {p("没错,然后他还有一个就是<strong>每15次的工具调用</strong>,他会做一次自我的复盘,")}
    {p("就是他会把之前的这些任务的执行的轨迹都回放一遍,去优化他的这个技能库。")}
    {p("对,所以说就是复杂的任务,才值得他去自动的归纳出一个可以反复用的一个技能模板。")}
    <div class="stat-row" style="margin-top:20px;">
      <div class="stat"><div class="stat-num c1">5+</div><div class="stat-desc">工具调用门槛</div></div>
      <div class="stat"><div class="stat-num c2">15</div><div class="stat-desc">次调用复盘</div></div>
      <div class="stat"><div class="stat-num c3" style="font-size:88px;">规约</div><div class="stat-desc">行为与边界</div></div>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap wrap-split">
    <div class="txt">
      <div class="pill">LLM</div>
      <div class="title title-sm">值不值得变成<span class="hl">新技能</span></div>
      {p("那他是怎么去判断说,")}
      {p("哪些任务流程是值得被保存下来作为一个新的技能的呢?")}
      {p("他是这样就是每完成一个任务,")}
      {p("他会去用这个<strong>LLM</strong>去分析这整个的执行的轨迹,")}
      {p("然后把那些关键的步骤以及这个判断的点都给抽出来。")}
      {p("最后他会去根据这个结果,是不是稳定是不是可以被复用来决定要不要存成一个新的技能。")}
      {p("所以说其实他不只是在记录步骤,他其实还在判断这个东西到底有没有用?")}
    </div>
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
        <rect x="60" y="40" width="280" height="100" rx="14" fill="rgba(99,102,241,0.12)" stroke="#818cf8"/>
        <text x="200" y="100" text-anchor="middle" fill="#c4b5fd" font-size="18" font-weight="800">LLM 分析轨迹</text>
        <path d="M200,150 L200,200" stroke="#64748b" stroke-width="3"/>
        <rect x="80" y="210" width="240" height="60" rx="10" fill="rgba(52,211,153,0.12)" stroke="#34d399"/>
        <text x="200" y="248" text-anchor="middle" fill="#6ee7b7" font-size="16" font-weight="700">稳定 · 可复用 → 存技能</text>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="pill pill-ok">规范</div>
    <div class="title title-sm"><span class="hl">agentskills.io</span></div>
    {p("对,没错没错,而且他生成的这个技能文件,")}
    {p("他是有一个非常规范的一个结构的,")}
    {p("就是他是一个markdown的文件,")}
    {p("然后他里面有这个技能的名字,有这个触发的场景,有每一步的操作,")}
    {p("还有这个已知的一些注意事项。")}
    {p("就是他是一个完全符合这个<strong>agentskills.io</strong>的这个标准的一个东西,")}
    {p("所以他可以很方便的在不同的平台之间进行共享和迁移。")}
    <div class="viz-box viz-short" style="margin-top:16px;" aria-hidden="true">
      <svg viewBox="0 0 560 120" xmlns="http://www.w3.org/2000/svg">
        <rect x="20" y="20" width="120" height="80" rx="10" fill="rgba(56,189,248,0.15)" stroke="#38bdf8"/>
        <text x="80" y="68" text-anchor="middle" fill="#7dd3fc" font-size="14" font-weight="700">技能名</text>
        <text x="160" y="70" fill="#94a3b8" font-size="28">→</text>
        <rect x="200" y="20" width="120" height="80" rx="10" fill="rgba(129,140,246,0.12)" stroke="#a78bfa"/>
        <text x="260" y="68" text-anchor="middle" fill="#c4b5fd" font-size="14" font-weight="700">场景</text>
        <text x="340" y="70" fill="#94a3b8" font-size="28">→</text>
        <rect x="380" y="20" width="160" height="80" rx="10" fill="rgba(52,211,153,0.12)" stroke="#34d399"/>
        <text x="460" y="68" text-anchor="middle" fill="#6ee7b7" font-size="14" font-weight="700">步骤 · 注意</text>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="pill pill-warn">收益</div>
    <div class="title title-sm">重复工作 <span class="accent-w">快至少 40%</span></div>
    <div class="stat-row">
      <div class="stat"><div class="stat-num c2">40%</div><div class="stat-desc">提速（口播数据）</div></div>
      <div class="stat"><div class="stat-num c1">分层</div><div class="stat-desc">技能库智能加载</div></div>
      <div class="stat"><div class="stat-num c3">省</div><div class="stat-desc">内存与 token</div></div>
    </div>
    {p("就是说这个<strong>Hermes Agent</strong>他这个自动生成技能这个东西,到底在实际用起来的时候有什么明显的好处?")}
    {p("你想象一下,就是这个东西用了一段时间之后,")}
    {p("你就发现他处理那些重复性的工作的速度会<strong>快至少40%</strong>,")}
    {p("他直接就可以用他之前总结的那个经验,就不需要再重新摸索一遍。")}
    {p("对,这个确实很省力呀,然后他的那个技能库是<strong>分层的</strong>,")}
    {p("他会智能地去加载你需要的那一部分技能,所以他会很省你的内存和token,")}
    {p("而且他会随着你不断的使用他,遇到新的情况他会自动地去优化他的技能。")}
    {p("所以他这个就是完全不需要你人工地去插手,")}
    {p("他就是一个真正的可以<strong>自我进化</strong>的一个AI。")}
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="part-row" style="justify-content:center;"><span class="part-tag">PART</span><span class="part-num">03</span></div>
    <div class="part-title" style="text-align:center;width:100%;">前景与场景</div>
    <div class="title title-sm">谁适合用 <span class="hl">Hermes Agent</span></div>
    {p("然后咱们来到第三个部分,")}
    {p("咱们来聊一聊这个<strong>Hermes Agent</strong>他的这个广阔的前景。")}
    {p("OK,第一个问题,就是说哪些人或者说哪些群体最适合用<strong>Hermes Agent</strong>?")}
    {p("其实我觉得就是技术爱好者或者说独立开发者是特别适合的,")}
    {p("因为你可以用他来自动地去处理你的一些<strong>运维的任务</strong>,")}
    {p("然后或者是说帮你管理你的项目啊,甚至帮你生成一些文档啊,")}
    {p("就是你可以把它当成你的一个非常高效的<strong>数字助理</strong>。")}
    {p("听起来对个人用户非常友好。没错没错,")}
    {p("而且他其实也很适合那种跨境的团队或者说那种远程办公的人,")}
    {p("因为他可以多平台的消息聚合嘛,")}
    {p("然后你可以在不同的设备之间无缝地同步你的这个对话。")}
  </div>"""
    )

    add(
        f"""  <div class="wrap wrap-split">
    <div class="txt">
      <div class="pill pill-muted">场景</div>
      <div class="title title-sm">从创业到<span class="accent">学生</span></div>
      {p("所以就是说无论是你是一个小的创业公司,")}
      {p("还是说你是一个有这种私有化需求的企业,")}
      {p("甚至说你是一个科研人员或者说学生,")}
      {p("你想要做一些知识管理啊,或者是说文献的追踪啊,")}
      {p("都可以用他来提高你的效率。")}
      {p("就是说<strong>Hermes Agent</strong>到底可以在哪些实际的场景当中去发挥他的作用?")}
    </div>
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
        <circle cx="200" cy="120" r="50" fill="rgba(56,189,248,0.15)" stroke="#38bdf8"/>
        <text x="200" y="128" text-anchor="middle" fill="#e2e8f0" font-size="14" font-weight="800">数字助理</text>
        <rect x="80" y="200" width="240" height="56" rx="12" fill="rgba(15,23,42,0.8)" stroke="rgba(148,163,184,0.3)"/>
        <text x="200" y="235" text-anchor="middle" fill="#94a3b8" font-size="16" font-weight="600">日程 · 消息 · 定时任务</text>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="pill">管家</div>
    <div class="title title-sm">全职全能<span class="hl">管家</span></div>
    {p("比如说你可以把它变成你的一个专属的<strong>数字助理</strong>。")}
    {p("他可以帮你自动地去整理你的日程啊,")}
    {p("然后帮你去聚合你各个平台的消息啊,")}
    {p("包括你可以让他去定时的帮你执行一些任务啊。")}
    {p("你可以把它变成一个你的全职全能的这种管家。")}
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="pill pill-ok">团队</div>
    <div class="title title-sm">客服 · 运维 · <span class="hl">原型</span></div>
    {p("听起来他好像不只是可以管个人的事务。")}
    {p("没错没错没错,")}
    {p("而且他还可以做很多就是团队协作的事情,")}
    {p("比如说自动的帮你同步一些跨平台的信息啊,")}
    {p("然后帮你做一些<strong>客服的自动化</strong>啊,")}
    {p("或者说帮你监控一些数据啊,帮你运维一些东西啊,")}
    {p("甚至说帮你这个开发团队去快速的搭建一些<strong>原型</strong>啊,")}
    {p("或者说帮你这个研究团队去高效的梳理一些文献啊。")}
    {p("就是他其实是一个非常非常好的一个助力,在很多很多领域里面。")}
  </div>"""
    )

    add(
        f"""  <div class="wrap wrap-split">
    <div class="txt">
      <div class="pill pill-purple">优势</div>
      <div class="title title-sm">自动生成 · <span class="hl">本地闭环</span></div>
      {p("你觉得<strong>Hermes Agent</strong>跟其他的一些同类的AI框架相比,")}
      {p("他最突出的优势在哪里?")}
      {p("就是他的那个技能是可以<strong>自动生成</strong>并且不断的<strong>自我进化</strong>的。")}
      {p("就他的那个整个的学习的<strong>闭环</strong>都是在本地完成的,")}
      {p("所以他可以越用越聪明,")}
      {p("而且他的那个<strong>多层的记忆系统</strong>也非常的厉害,")}
      {p("就是他可以非常准确地去记住你这个<strong>跨会话</strong>的一些细节。")}
    </div>
    <div class="viz-box viz-tall" aria-hidden="true">
      <svg viewBox="0 0 400 320" xmlns="http://www.w3.org/2000/svg">
        <rect x="50" y="50" width="300" height="220" rx="16" fill="rgba(15,23,42,0.6)" stroke="rgba(52,211,153,0.35)"/>
        <text x="200" y="120" text-anchor="middle" fill="#6ee7b7" font-size="18" font-weight="800">本地闭环</text>
        <text x="200" y="170" text-anchor="middle" fill="#94a3b8" font-size="16">记忆 · 跨会话</text>
        <text x="200" y="220" text-anchor="middle" fill="#cbd5e1" font-size="15">越用越聪明</text>
      </svg>
    </div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="pill">工程力</div>
    <div class="title title-sm">工具 · 平台 · <span class="accent-w">沙盒</span> · MIT</div>
    {p("然后他的部署啊和他的这个兼容啊,是不是也特别灵活啊?")}
    {p("没错没错没错,")}
    {p("就是他支持<strong>几十种工具</strong>,")}
    {p("然后<strong>六大平台</strong>的消息接入主流的大模型,")}
    {p("他都是原生的兼容,")}
    {p("再加上他的那个<strong>一键迁移</strong>和他的那个<strong>安全沙盒</strong>,")}
    {p("就是你无论是个人还是团队还是企业,")}
    {p("你都可以非常快速地去上手并且保证你的数据的安全。")}
    {p("他的这个<strong>MIT的协议</strong>也非常的宽松,")}
    {p("就是你几乎可以为所欲为地使用他。")}
    <div class="badge-line" style="margin-top:20px;">一键迁移 · 安全沙盒 · MIT</div>
  </div>"""
    )

    add(
        f"""  <div class="wrap">
    <div class="title title-lg">感谢收听</div>
    <p class="lede">百闻不如一见 · 去试试 Hermes Agent</p>
    {p("对,今天我们把<strong>Hermes Agent</strong>这个自动生成技能啊,然后自我进化的这个能力给大家聊了一遍。")}
    {p("对,其实还是那句话,<strong>百闻不如一见</strong>,我觉得大家不如自己去试一试,")}
    {p("感受一下这个AI助手不一样的成长方式。")}
    {p("感谢大家的收听,然后咱们下期节目再见,")}
    {p("记得去体验一下<strong>Hermes Agent</strong>,")}
    {p("咱们下次聊点更酷的东西,拜拜,拜拜")}
  </div>"""
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920, initial-scale=1">
<title>Hermes Agent · 豆包AI播客</title>
<style>
{css}
</style>
</head>
<body>
<div id="progress" style="width:0%"></div>
<div id="presentation">
{chr(10).join(parts)}
</div>
<div id="pageNum"></div>
<script>
function resize(){{
  var p=document.getElementById('presentation');
  var s=Math.min(window.innerWidth/1920,window.innerHeight/1080);
  var ox=(window.innerWidth-1920*s)/2;
  var oy=(window.innerHeight-1080*s)/2;
  p.style.transform='scale('+s+')';
  p.style.left=ox+'px';
  p.style.top=oy+'px';
}}
window.addEventListener('resize',resize);
resize();
var slides=document.querySelectorAll('.slide');
var total=slides.length;
var cur=0;
function updateUI(){{
  document.getElementById('pageNum').textContent=(cur+1)+' / '+total;
  document.getElementById('progress').style.width=(total<=1?100:(cur/(total-1)*100))+'%';
}}
function goTo(i){{
  if(i<0||i>=total)return;
  slides[cur].classList.remove('active');
  cur=i;
  slides[cur].classList.add('active');
  updateUI();
}}
function go(n){{ goTo(n); }}
document.addEventListener('keydown',function(e){{
  if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '){{e.preventDefault();goTo(cur+1);}}
  else if(e.key==='ArrowLeft'||e.key==='ArrowUp'){{e.preventDefault();goTo(cur-1);}}
}});
document.addEventListener('click',function(e){{
  if(e.clientX>window.innerWidth*0.3)goTo(cur+1);
  else goTo(cur-1);
}});
updateUI();
</script>
</body>
</html>
"""

    OUT.write_text(html, encoding="utf-8")
    print("slides", len(parts), "->", OUT)


if __name__ == "__main__":
    main()
