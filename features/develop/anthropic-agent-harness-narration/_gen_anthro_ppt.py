# -*- coding: utf-8 -*-
"""Anthropic Agent Harness 播客 PPT - 竖屏短视频规格
    规格：1080×1920 | 零空白 | 字号加大 | 科技蓝黑风
"""
import os

# ============================================================
# 颜色主题（科技蓝黑）
# ============================================================
BG       = "#0a0e14"
BG2      = "#0d1420"
BG3      = "#111928"
CYAN     = "#00D4FF"
BLUE     = "#0066FF"
PURPLE   = "#7C3AED"
ORANGE   = "#FF6B35"
GOLD     = "#FFD700"
GREEN    = "#00E676"
RED      = "#FF5252"
WHITE    = "#FFFFFF"
MUTED    = "#6B7A8C"
MUTED2   = "#4A5568"
CARD_BG  = "rgba(0,212,255,0.07)"
CARD_BD  = "rgba(0,212,255,0.18)"
ACCENT_LINE = "#00D4FF"

# SVG 图标库（内联，不依赖外部）
SVG_ICONS = {
    "cloud":    '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M48 36a12 12 0 0 0-12-12 12 12 0 0 0-22.4-4A10 10 0 1 0 14 50h34a10 10 0 0 0 0-14z" fill="#00D4FF" opacity=".85"/></svg>',
    "layers":   '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M32 8L8 20v24l24 12 24-12V20L32 8z" fill="#7C3AED" opacity=".85"/><path d="M32 18L14 28v18l18 9 18-9V28L32 18z" fill="#00D4FF" opacity=".75"/></svg>',
    "shield":   '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M32 6L8 16v20c0 14.4 10.24 27.84 24 31 13.76-3.16 24-16.6 24-31V16L32 6z" fill="#00E676" opacity=".85"/></svg>',
    "bolt":     '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M36 4L14 36h16L24 60l28-34H34z" fill="#FFD700" opacity=".9"/></svg>',
    "chart":    '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><rect x="8" y="40" width="12" height="18" rx="3" fill="#00D4FF" opacity=".7"/><rect x="26" y="26" width="12" height="32" rx="3" fill="#00D4FF" opacity=".85"/><rect x="44" y="12" width="12" height="46" rx="3" fill="#00D4FF" opacity="1"/></svg>',
    "gear":     '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><circle cx="32" cy="32" r="10" fill="#FFD700" opacity=".9"/><path d="M32 4v8M32 52v8M4 32h8M52 32h8M10.8 10.8l5.66 5.66M47.54 47.54l5.66 5.66M53.2 10.8l-5.66 5.66M16.46 47.54l-5.66 5.66" stroke="#FFD700" stroke-width="4" stroke-linecap="round" opacity=".7"/></svg>',
    "brain":    '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><ellipse cx="32" cy="32" rx="22" ry="20" fill="#7C3AED" opacity=".8"/><path d="M20 26c4-4 8-4 12 0M32 26c4-4 8-4 12 0M18 38c4-4 8-4 14 0M32 38c4-4 8-4 12 0" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity=".6"/></svg>',
    "server":   '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><rect x="8" y="12" width="48" height="14" rx="4" fill="#0066FF" opacity=".8"/><rect x="8" y="32" width="48" height="14" rx="4" fill="#00D4FF" opacity=".8"/><rect x="8" y="52" width="48" height="14" rx="4" fill="#7C3AED" opacity=".8"/><circle cx="18" cy="19" r="3" fill="#00E676"/><circle cx="18" cy="39" r="3" fill="#00E676"/><circle cx="18" cy="59" r="3" fill="#FFD700"/></svg>',
    "warning":  '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M32 8L4 56h56L32 8z" fill="#FF6B35" opacity=".85"/><rect x="29" y="22" width="6" height="18" rx="3" fill="#FFFFFF" opacity=".9"/><circle cx="32" cy="46" r="3" fill="#FFFFFF" opacity=".9"/></svg>',
    "check":    '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><circle cx="32" cy="32" r="26" fill="#00E676" opacity=".15" stroke="#00E676" stroke-width="3"/><path d="M20 32l9 9 15-18" stroke="#00E676" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "arrow":    '<svg viewBox="0 0 64 64" width="32" height="32" fill="none"><path d="M12 32h40M40 20l12 12-12 12" stroke="#00D4FF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "clock":    '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><circle cx="32" cy="32" r="26" stroke="#00D4FF" stroke-width="4" opacity=".8"/><path d="M32 18v16l10 10" stroke="#00D4FF" stroke-width="4" stroke-linecap="round"/></svg>',
    "fingerprint": '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M32 8v12M32 44v12M8 32h12M44 32h12" stroke="#00D4FF" stroke-width="3" stroke-linecap="round" opacity=".6"/><circle cx="32" cy="32" r="12" stroke="#00D4FF" stroke-width="3" opacity=".8"/><circle cx="32" cy="32" r="20" stroke="#00D4FF" stroke-width="3" opacity=".5" stroke-dasharray="4 4"/></svg>',
    "puzzle":   '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M20 8h24a8 8 0 0 1 0 16H20V8z" fill="#7C3AED" opacity=".85"/><path d="M8 24h16v24H8V24z" fill="#00D4FF" opacity=".75"/><path d="M24 48h16a8 8 0 0 1 0 16H24V48z" fill="#FFD700" opacity=".75"/></svg>',
    "expand":   '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M8 24V8h16M56 24V8H40M8 40v16h16M56 40v16H40" stroke="#00D4FF" stroke-width="4" stroke-linecap="round" opacity=".8"/></svg>',
    "cpu":      '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><rect x="16" y="16" width="32" height="32" rx="6" fill="#7C3AED" opacity=".85"/><path d="M24 8v8M40 8v8M24 48v8M40 48v8M8 24h8M8 40h8M48 24h8M48 40h8" stroke="#00D4FF" stroke-width="3" stroke-linecap="round" opacity=".7"/><rect x="24" y="24" width="16" height="16" rx="2" fill="#00D4FF" opacity=".6"/></svg>',
    "lock":     '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><rect x="12" y="28" width="40" height="28" rx="6" fill="#FF5252" opacity=".85"/><path d="M20 28V20a12 12 0 0 1 24 0v8" stroke="#FF5252" stroke-width="4" stroke-linecap="round" fill="none"/><circle cx="32" cy="42" r="4" fill="#FFFFFF" opacity=".9"/></svg>',
    "trophy":   '<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M20 8h24v24c0 8.84-5.37 16-12 16s-12-7.16-12-16V8z" fill="#FFD700" opacity=".9"/><path d="M20 16H8v8c0 6 4 10 12 10M44 16h12v8c0 6-4 10-12 10" stroke="#FFD700" stroke-width="3" fill="none" opacity=".8"/><rect x="28" y="48" width="8" height="8" fill="#FFD700" opacity=".9"/><rect x="20" y="54" width="24" height="4" rx="2" fill="#FFD700" opacity=".8"/></svg>',
}

# ============================================================
# 幻灯数据（竖屏 1080×1920 规格）
# ============================================================
SLIDES = [
    # ── 封面 ──────────────────────────────────────────────
    {
        "id": 0, "start": 0, "end": 7,
        "type": "cover",
        "tag": "豆包AI播客",
        "headline": "Agent\n是宠物\n还是牲口？",
        "sub": "Anthropic 把 AI 从精心呵护的宠物\n变成了随时可替换的打工仔",
        "theme": "gradient",
    },
    # ── PART I 架构的转变 ────────────────────────────────
    {
        "id": 1, "start": 7, "end": 15,
        "type": "section",
        "tag": "PART I",
        "title": "架构的转变",
        "icon": "layers",
        "body": "Anthropic 之前的 Agent\n所有东西都塞进了一个容器",
    },
    {
        "id": 2, "start": 15, "end": 36,
        "type": "icon_grid",
        "tag": "PART I · 旧架构",
        "title": "单体的困境",
        "icon": "warning",
        "items": [
            ("容器挂了", "所有状态全失\n任务重来"),
            ("调试困难", "排查问题\n牵一发而动全身"),
            ("扩展受限", "模型升级\n牵动 Harness 全局"),
            ("安全集中", "风险都集中在\n一个容器内"),
        ],
        "color": ORANGE,
    },
    {
        "id": 3, "start": 36, "end": 51,
        "type": "big_number",
        "tag": "PART I · 核心问题",
        "title": "这个架构\n就像养了一只宠物",
        "icon": "brain",
        "big": "🐶",
        "sub": "精心呵护 · 不可替换 · 全局耦合",
    },
    {
        "id": 4, "start": 51, "end": 67,
        "type": "triple_layers",
        "tag": "PART I · 新架构",
        "title": "三层分离",
        "subtitle": "Session · Harness · Sandbox",
        "layers": [
            ("Session", "日志层", "只追加事件记录\n不关业务逻辑\n支持 replay", CYAN),
            ("Harness", "大脑层", "无状态\n负责任务调度\n和工具选择", PURPLE),
            ("Sandbox", "执行层", "安全隔离\n执行命令\n返回结果", ORANGE),
        ],
    },
    {
        "id": 5, "start": 67, "end": 82,
        "type": "icon_list",
        "tag": "PART I · 优势",
        "title": "各层职责清晰",
        "icon": "check",
        "items": [
            ("Session", "可随时 replay\n任意步骤"),
            ("Harness", "多模型适配\n无状态扩容"),
            ("Sandbox", "沙箱隔离\n错误不外溢"),
            ("接口通信", "层间稳定接口\n系统灵活可靠"),
        ],
    },
    {
        "id": 6, "start": 82, "end": 96,
        "type": "contrast_center",
        "tag": "PART I · 小结",
        "before": "宠物",
        "after": "打工仔",
        "icon": "arrow",
        "body": "从精心呵护的宠物架构\n到随时可替换的打工仔架构",
    },
    # ── PART II 变革带来的成效 ─────────────────────────
    {
        "id": 7, "start": 96, "end": 113,
        "type": "section",
        "tag": "PART II",
        "title": "变革带来的成效",
        "icon": "trophy",
    },
    {
        "id": 8, "start": 113, "end": 148,
        "type": "numbers",
        "tag": "PART II · 延迟",
        "title": "推理提前启动",
        "body": "脑手分离之后\nAgent 不需要等沙箱完全起来\n才开始干活",
        "numbers": [
            ("P50", "↓60%", "首 Token 延迟"),
            ("P95", "↓90%+", "尾部延迟"),
        ],
    },
    {
        "id": 9, "start": 148, "end": 183,
        "type": "flow",
        "tag": "PART II · 弹性",
        "title": "故障自动恢复",
        "steps": [
            ("会话状态", "持久化存储", "📦"),
            ("沙箱挂了", "自动重启", "🔄"),
            ("新实例启动", "无缝恢复", "⚡"),
            ("业务层面", "零感知", "✅"),
        ],
    },
    {
        "id": 10, "start": 183, "end": 222,
        "type": "contrast",
        "tag": "PART II · 安全",
        "title": "安全边界重塑",
        "before_label": "旧：凭证藏沙箱",
        "after_label": "新：凭证移出沙箱",
        "before_items": ["风险集中", "被攻破即泄露"],
        "after_items": ["加密挂载", "代理访问", "隔离保护"],
    },
    {
        "id": 11, "start": 222, "end": 261,
        "type": "icon_list",
        "tag": "PART II · 可观测",
        "title": "中间件 + 多Agent",
        "icon": "server",
        "items": [
            ("中间件", "做观测和流控"),
            ("多 Agent 协作", "标准接口支撑"),
            ("管理平台", "权限控制和操作审计"),
            ("可维护", "组件可替换"),
        ],
    },
    # ── PART III 发展方向 ───────────────────────────────
    {
        "id": 12, "start": 261, "end": 333,
        "type": "section",
        "tag": "PART III",
        "title": "发展方向",
        "icon": "expand",
    },
    {
        "id": 13, "start": 333, "end": 370,
        "type": "pain",
        "tag": "PART III · 过去",
        "title": "各自造轮子",
        "icon": "warning",
        "items": [
            "自己搞编排",
            "自己搞沙箱",
            "自己搞会话管理",
        ],
        "sub": "什么都要自己来，非常费劲",
    },
    {
        "id": 14, "start": 370, "end": 410,
        "type": "timeline_horiz",
        "tag": "PART III · 现在",
        "title": "标准化与平台化",
        "steps": [
            ("初创公司", "标准 Agent 框架"),
            ("云厂商", "Managed Agent 服务"),
            ("主流趋势", "运行时 + 平台托管出去"),
        ],
    },
    {
        "id": 15, "start": 410, "end": 450,
        "type": "resources",
        "tag": "PART III · 平台化",
        "title": "一切皆为资源",
        "subtitle": "Cloud Managed Agents",
        "resources": [
            ("Agent", "可组合的\n能力单元", CYAN),
            ("Environment", "可替换的\n执行环境", PURPLE),
            ("Session", "可管理的\n会话状态", GOLD),
        ],
    },
    {
        "id": 16, "start": 450, "end": 485,
        "type": "metaphor",
        "tag": "PART III · 未来",
        "title": "模块化分层架构",
        "body": "模型只是大脑\n通过稳定接口连接各种\n可替换的执行环境和工具",
        "metaphor": "AI Native OS",
        "layers": ["模型 = CPU", "工具 = 外设", "平台 = 操作系统"],
    },
    {
        "id": 17, "start": 485, "end": 520,
        "type": "icon_list",
        "tag": "PART III · 趋势",
        "title": "多Agent协作",
        "icon": "puzzle",
        "items": [
            ("行业标准", "接口统一 · 生态繁荣"),
            ("工具生态", "专业分工 · 各司其职"),
            ("创新重心", "向应用层迁移"),
            ("未来展望", "AI Native 新范式"),
        ],
    },
    # ── 结尾 ─────────────────────────────────────────────
    {
        "id": 18, "start": 520, "end": 545,
        "type": "ending",
        "tag": "尾声",
        "title": "架构升级的必然结果",
        "body": "Agent 从宠物变成打工仔\n是 AI 行业逐渐走向成熟的标志",
    },
    {
        "id": 19, "start": 545, "end": 565,
        "type": "end",
        "headline": "感谢收听\n下期再见",
    },
]

# ============================================================
# CSS 样式
# ============================================================
def css():
    return f"""<style>
/* Google Fonts (可选增强，本地字体兜底) */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&family=Roboto+Mono:wght@400;700&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}

body {{
    /* 本地字体优先，Google Fonts 增强覆盖 */
    font-family: 'Microsoft YaHei UI', 'PingFang SC', 'Microsoft YaHei',
                 'Source Han Sans CN', sans-serif;
    background: {BG};
    color: {WHITE};
    overflow-x: hidden;
}}

.slides {{
    width: 100vw;
    height: 100vh;
    overflow-y: scroll;
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}}

.slide {{
    width: 100vw;
    height: 100vh;
    min-height: 100vh;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding: 72px 60px 60px;
    position: relative;
    overflow: hidden;
}}

/* 背景光效 */
.slide::before {{
    content: '';
    position: absolute;
    top: -200px;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 800px;
    background: radial-gradient(ellipse at center,
        rgba(0,212,255,0.08) 0%,
        rgba(124,58,237,0.04) 40%,
        transparent 70%);
    pointer-events: none;
    z-index: 0;
}}
.slide > * {{
    position: relative;
    z-index: 1;
}}

/* 顶部进度条 */
#progress {{
    position: fixed;
    top: 0; left: 0;
    height: 3px;
    background: linear-gradient(90deg, {CYAN}, {PURPLE});
    z-index: 999;
    transition: width 0.3s ease;
}}

/* 右侧导航点 */
#dots {{
    position: fixed;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 999;
}}
.dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: rgba(0,212,255,0.3);
    cursor: pointer;
    transition: all 0.3s;
}}
.dot.active {{
    background: {CYAN};
    box-shadow: 0 0 8px {CYAN};
    transform: scale(1.6);
}}

/* ─── 共用组件 ─── */
.tag {{
    font-family: 'Microsoft YaHei UI', 'PingFang SC', 'Noto Sans SC', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 6px;
    color: {CYAN};
    text-transform: uppercase;
    opacity: 0.9;
}}

.title {{
    font-family: 'Microsoft YaHei UI', 'PingFang SC', 'Noto Sans SC', sans-serif;
    font-size: clamp(44px, 6vw, 72px);
    font-weight: 900;
    line-height: 1.15;
    color: {WHITE};
    text-align: center;
    letter-spacing: 1px;
    text-shadow: 0 0 40px rgba(0,212,255,0.2);
    margin-top: 16px;
}}

.body-text {{
    font-family: 'Microsoft YaHei UI', 'PingFang SC', 'Noto Sans SC', sans-serif;
    font-size: clamp(24px, 3vw, 36px);
    line-height: 1.7;
    color: rgba(255,255,255,0.8);
    text-align: center;
    margin-top: 24px;
    white-space: pre-line;
}}

.divider {{
    width: 60px; height: 3px;
    background: linear-gradient(90deg, {CYAN}, {PURPLE});
    border-radius: 2px;
    margin: 20px auto;
}}

/* 顶部细线 */
.top-bar {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {CYAN} 30%, {PURPLE} 70%, transparent);
}}

/* 底部时间 */
.timestamp {{
    position: absolute;
    bottom: 24px;
    right: 36px;
    font-family: 'Consolas', 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    color: rgba(107,122,140,0.4);
    letter-spacing: 1px;
}}

/* 底部页码 */
.page-num {{
    position: absolute;
    bottom: 24px;
    left: 36px;
    font-family: 'Consolas', 'Consolas', 'Courier New', monospace;
    font-size: 11px;
    color: rgba(107,122,140,0.4);
    letter-spacing: 1px;
}}

/* ─── 封面 ─── */
.cover-bg {{
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 50% 30%,
            rgba(0,212,255,0.12) 0%,
            rgba(124,58,237,0.06) 40%,
            transparent 70%),
        radial-gradient(ellipse 60% 50% at 80% 80%,
            rgba(255,107,53,0.08) 0%,
            transparent 60%),
        {BG};
}}
.cover-glow {{
    position: absolute;
    width: 600px; height: 600px;
    top: 50%; left: 50%;
    transform: translate(-50%, -60%);
    background: radial-gradient(ellipse, rgba(0,212,255,0.15) 0%, transparent 70%);
    pointer-events: none;
}}
.cover-eyebrow {{
    font-size: 14px;
    letter-spacing: 8px;
    color: rgba(0,212,255,0.7);
    font-weight: 500;
    text-transform: uppercase;
    margin-bottom: 32px;
}}
.cover-headline {{
    font-size: clamp(72px, 10vw, 120px);
    font-weight: 900;
    line-height: 1.0;
    text-align: center;
    color: {WHITE};
    letter-spacing: 4px;
    text-shadow: 0 0 60px rgba(0,212,255,0.3);
    white-space: pre-line;
}}
.cover-sub {{
    font-size: clamp(18px, 2.2vw, 26px);
    color: rgba(255,255,255,0.65);
    text-align: center;
    margin-top: 28px;
    line-height: 1.8;
    white-space: pre-line;
}}
.cover-bottom {{
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, {CYAN}, {PURPLE}, {ORANGE});
}}

/* ─── 章节分隔页 ─── */
.section-icon {{
    width: 80px; height: 80px;
    margin-bottom: 24px;
}}
.section-title {{
    font-size: clamp(52px, 7vw, 88px);
    font-weight: 900;
    color: {WHITE};
    text-align: center;
    letter-spacing: 2px;
    text-shadow: 0 0 40px rgba(0,212,255,0.3);
    margin-top: 16px;
}}
.section-icon svg {{
    width: 80px; height: 80px;
}}

/* ─── 图标网格（四宫格）─── */
.grid-2x2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    width: 100%;
    margin-top: 28px;
}}
.grid-card {{
    padding: 28px 24px;
    border-radius: 20px;
    background: {CARD_BG};
    border: 1px solid {CARD_BD};
    text-align: center;
}}
.grid-card-icon {{
    width: 52px; height: 52px;
    margin: 0 auto 14px;
}}
.grid-card-icon svg {{
    width: 52px; height: 52px;
}}
.grid-card h3 {{
    font-size: clamp(22px, 2.5vw, 30px);
    font-weight: 700;
    margin-bottom: 8px;
}}
.grid-card p {{
    font-size: clamp(15px, 1.5vw, 18px);
    color: rgba(255,255,255,0.65);
    line-height: 1.5;
    white-space: pre-line;
}}

/* ─── 大数字 ─── */
.big-center {{
    text-align: center;
    margin-top: 20px;
}}
.big-emoji {{
    font-size: 120px;
    line-height: 1;
    margin-bottom: 20px;
}}
.big-sub {{
    font-size: clamp(18px, 2vw, 24px);
    color: rgba(255,255,255,0.5);
    letter-spacing: 4px;
    margin-top: 16px;
}}

/* ─── 三层架构 ─── */
.layers {{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin-top: 28px;
}}
.layer-row {{
    display: grid;
    grid-template-columns: 160px 1fr;
    align-items: center;
    gap: 20px;
    padding: 22px 28px;
    border-radius: 18px;
    border-left: 5px solid;
}}
.layer-name {{
    font-size: clamp(20px, 2.2vw, 26px);
    font-weight: 800;
    letter-spacing: 2px;
}}
.layer-role {{
    font-size: 13px;
    opacity: 0.65;
    letter-spacing: 2px;
    margin-top: 2px;
}}
.layer-desc {{
    font-size: clamp(16px, 1.6vw, 20px);
    color: rgba(255,255,255,0.85);
    line-height: 1.6;
    white-space: pre-line;
}}

/* ─── 对比中心 ─── */
.contrast-center {{
    text-align: center;
    margin-top: 24px;
    width: 100%;
}}
.contrast-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 32px;
    flex-wrap: wrap;
}}
.contrast-box {{
    padding: 28px 48px;
    border-radius: 20px;
    font-size: clamp(32px, 4vw, 52px);
    font-weight: 900;
    border: 2px solid;
}}
.contrast-arrow-icon {{
    width: 48px; height: 48px;
}}
.contrast-arrow-icon svg {{
    width: 48px; height: 48px;
}}

/* ─── 数字卡片 ─── */
.numbers-row {{
    display: flex;
    gap: 24px;
    justify-content: center;
    margin-top: 32px;
    width: 100%;
}}
.num-card {{
    flex: 1;
    max-width: 280px;
    padding: 32px 24px;
    border-radius: 24px;
    text-align: center;
    border: 2px solid;
}}
.num-value {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: clamp(52px, 6vw, 80px);
    font-weight: 900;
    line-height: 1;
}}
.num-label {{
    font-size: clamp(14px, 1.5vw, 18px);
    opacity: 0.7;
    margin-top: 10px;
    letter-spacing: 1px;
}}

/* ─── 流程 ─── */
.flow {{
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 100%;
    margin-top: 28px;
}}
.flow-step {{
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 22px 28px;
    border-radius: 16px;
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.15);
}}
.flow-emoji {{
    font-size: 36px;
    flex-shrink: 0;
    width: 56px;
    text-align: center;
}}
.flow-text {{
    flex: 1;
}}
.flow-step-title {{
    font-size: clamp(20px, 2.2vw, 26px);
    font-weight: 700;
    color: {CYAN};
    margin-bottom: 4px;
}}
.flow-step-desc {{
    font-size: clamp(15px, 1.5vw, 18px);
    color: rgba(255,255,255,0.7);
}}

/* ─── 左右对比 ─── */
.contrast-layout {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 20px;
    align-items: start;
    margin-top: 28px;
    width: 100%;
}}
.contrast-col {{
    padding: 24px 20px;
    border-radius: 20px;
    border: 1px solid;
}}
.contrast-col-title {{
    font-size: clamp(16px, 1.8vw, 22px);
    font-weight: 700;
    margin-bottom: 14px;
}}
.contrast-item {{
    font-size: clamp(15px, 1.5vw, 18px);
    padding: 6px 0;
    opacity: 0.85;
}}
.contrast-arrow-col {{
    display: flex;
    align-items: center;
    padding-top: 40px;
}}

/* ─── 图标列表 ─── */
.icon-list {{
    width: 100%;
    margin-top: 24px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}}
.icon-list-item {{
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px 24px;
    border-radius: 16px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
}}
.icon-list-icon {{
    width: 44px; height: 44px;
    flex-shrink: 0;
}}
.icon-list-icon svg {{
    width: 44px; height: 44px;
}}
.icon-list-text h4 {{
    font-size: clamp(18px, 2vw, 24px);
    font-weight: 700;
    color: {WHITE};
    margin-bottom: 4px;
}}
.icon-list-text p {{
    font-size: clamp(14px, 1.4vw, 17px);
    color: rgba(255,255,255,0.6);
    white-space: pre-line;
}}

/* ─── 痛点 ─── */
.pain-items {{
    width: 100%;
    margin-top: 28px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}}
.pain-item {{
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 22px 28px;
    border-radius: 16px;
    background: rgba(255,107,53,0.08);
    border: 1px solid rgba(255,107,53,0.25);
}}
.pain-item-icon {{
    font-size: 32px;
    flex-shrink: 0;
    width: 44px;
    text-align: center;
}}
.pain-item-text {{
    font-size: clamp(22px, 2.8vw, 34px);
    font-weight: 700;
    color: {ORANGE};
}}

/* ─── 水平时间线 ─── */
.timeline-horiz {{
    width: 100%;
    margin-top: 32px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}}
.timeline-step {{
    display: flex;
    align-items: center;
    gap: 24px;
}}
.timeline-num {{
    min-width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, {CYAN}, {PURPLE});
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 22px;
    font-weight: 700;
    flex-shrink: 0;
}}
.timeline-content {{
    flex: 1;
    padding: 20px 24px;
    border-radius: 16px;
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.15);
}}
.timeline-title {{
    font-size: clamp(18px, 2vw, 24px);
    font-weight: 700;
    color: {CYAN};
    margin-bottom: 6px;
}}
.timeline-desc {{
    font-size: clamp(15px, 1.5vw, 18px);
    color: rgba(255,255,255,0.7);
}}

/* ─── 资源 ─── */
.resources-grid {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
    margin-top: 28px;
}}
.resource-row {{
    display: grid;
    grid-template-columns: 180px 1fr;
    align-items: center;
    gap: 20px;
    padding: 24px 28px;
    border-radius: 18px;
    border-left: 5px solid;
}}
.resource-name {{
    font-size: clamp(22px, 2.5vw, 32px);
    font-weight: 800;
    letter-spacing: 2px;
}}
.resource-desc {{
    font-size: clamp(16px, 1.6vw, 20px);
    color: rgba(255,255,255,0.8);
    line-height: 1.6;
    white-space: pre-line;
}}

/* ─── 比喻 ─── */
.metaphor-badges {{
    display: flex;
    gap: 14px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 20px;
}}
.metaphor-badge {{
    padding: 12px 28px;
    border-radius: 100px;
    font-size: clamp(16px, 1.8vw, 22px);
    font-weight: 700;
    border: 2px solid;
}}

/* ─── 结尾 ─── */
.ending-text {{
    font-size: clamp(28px, 3.5vw, 48px);
    font-weight: 700;
    color: {WHITE};
    text-align: center;
    line-height: 1.8;
    margin-top: 24px;
    white-space: pre-line;
}}
.ending-emphasis {{
    font-size: clamp(22px, 2.5vw, 34px);
    font-weight: 700;
    color: {CYAN};
    text-align: center;
    margin-top: 20px;
    padding: 20px 40px;
    border: 2px solid {CYAN};
    border-radius: 16px;
    background: rgba(0,212,255,0.08);
    text-shadow: 0 0 24px rgba(0,212,255,0.5);
}}

/* ─── 最终页 ─── */
.end-title {{
    font-size: clamp(64px, 9vw, 120px);
    font-weight: 900;
    text-align: center;
    line-height: 1.1;
    background: linear-gradient(135deg, {CYAN}, {PURPLE});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 4px;
    white-space: pre-line;
    text-shadow: none;
    filter: drop-shadow(0 0 40px rgba(0,212,255,0.4));
}}

/* ─── 动画 ─── */
.slide > * {{
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.5s ease, transform 0.5s ease;
}}
.slide.visible > * {{
    opacity: 1;
    transform: translateY(0);
}}
.slide > *:nth-child(1) {{ transition-delay: 0.05s; }}
.slide > *:nth-child(2) {{ transition-delay: 0.12s; }}
.slide > *:nth-child(3) {{ transition-delay: 0.20s; }}
.slide > *:nth-child(4) {{ transition-delay: 0.28s; }}
.slide > *:nth-child(5) {{ transition-delay: 0.36s; }}
.slide > *:nth-child(6) {{ transition-delay: 0.44s; }}
</style>"""

# ============================================================
# 幻灯生成
# ============================================================

def icon(name):
    return SVG_ICONS.get(name, "")

def hex_alpha(hex_color, alpha):
    """rgba(rr,gg,bb,a) from hex + alpha float"""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"

def slide_html(s):
    t = s["type"]
    ts  = f'<div class="tag">{s["tag"]}</div>' if s.get("tag") else ""
    tt  = f'<div class="title">{s["title"]}</div>' if s.get("title") else ""
    pt  = f'<div class="page-num">{s["id"]+1}/{len(SLIDES)}</div>'
    tst = f'<div class="timestamp">{s["start"]}s–{s["end"]}s</div>'

    # ── 封面 ──────────────────────────────────────────────
    if t == "cover":
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  <div class="cover-bg"></div>
  <div class="cover-glow"></div>
  <div class="cover-eyebrow">{s.get('tag','')}</div>
  <div class="cover-headline">{s['headline']}</div>
  <div class="cover-sub">{s['sub']}</div>
  <div class="cover-bottom"></div>
  {pt}{tst}
</div>"""

    # ── 章节分隔页 ────────────────────────────────────────
    if t == "section":
        ic = icon(s.get("icon", "bolt"))
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  <div class="section-icon">{ic}</div>
  <div class="section-title">{s['title']}</div>
  <div class="divider"></div>
  {pt}{tst}
</div>"""

    # ── 图标四宫格 ─────────────────────────────────────────
    if t == "icon_grid":
        grid = ""
        for title, desc in s["items"]:
            grid += f'''<div class="grid-card" style="border-color:{hex_alpha(s['color'],0.3)};background:{hex_alpha(s['color'],0.08)}">
  <div class="grid-card-icon">{icon(s.get('icon','warning'))}</div>
  <h3 style="color:{s['color']}">{title}</h3>
  <p>{desc}</p>
</div>'''
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="grid-2x2">{grid}</div>
  {pt}{tst}
</div>"""

    # ── 大数字/emoji居中 ──────────────────────────────────
    if t == "big_number":
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="big-center">
    <div class="big-emoji">{s['big']}</div>
    <div class="big-sub">{s['sub']}</div>
  </div>
  {pt}{tst}
</div>"""

    # ── 三层架构 ───────────────────────────────────────────
    if t == "triple_layers":
        layers_html = ""
        for name, role, desc, color in s["layers"]:
            layers_html += f'''<div class="layer-row" style="background:{hex_alpha(color,0.1)};border-color:{hex_alpha(color,0.5)}">
  <div>
    <div class="layer-name" style="color:{color}">{name}</div>
    <div class="layer-role" style="color:{color}">{role}</div>
  </div>
  <div class="layer-desc">{desc}</div>
</div>'''
        subtitle = f'<div class="body-text" style="margin-top:8px;font-size:clamp(16px,1.8vw,22px);opacity:0.5">{s.get("subtitle","")}</div>' if s.get("subtitle") else ""
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  {subtitle}
  <div class="layers">{layers_html}</div>
  {pt}{tst}
</div>"""

    # ─── 图标列表 ─────────────────────────────────────────
    if t == "icon_list":
        items_html = ""
        for title, desc in s["items"]:
            items_html += f'''<div class="icon-list-item">
  <div class="icon-list-icon">{icon(s.get('icon','check'))}</div>
  <div class="icon-list-text"><h4>{title}</h4><p>{desc}</p></div>
</div>'''
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="icon-list">{items_html}</div>
  {pt}{tst}
</div>"""

    # ── 对比中心 ──────────────────────────────────────────
    if t == "contrast_center":
        before_color = ORANGE
        after_color = CYAN
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="contrast-center">
    <div class="contrast-row">
      <div class="contrast-box" style="color:{before_color};border-color:{hex_alpha(before_color,0.6)};background:{hex_alpha(before_color,0.1)}">{s['before']}</div>
      <div class="contrast-arrow-icon">{icon(s.get('icon','arrow'))}</div>
      <div class="contrast-box" style="color:{after_color};border-color:{hex_alpha(after_color,0.6)};background:{hex_alpha(after_color,0.1)}">{s['after']}</div>
    </div>
    <div class="body-text" style="margin-top:28px">{s.get('body','')}</div>
  </div>
  {pt}{tst}
</div>"""

    # ── 数字 ──────────────────────────────────────────────
    if t == "numbers":
        nums = ""
        for label, val, desc in s.get("numbers", []):
            color = CYAN if "%" in val else PURPLE
            nums += f'''<div class="num-card" style="border-color:{hex_alpha(color,0.5)};background:{hex_alpha(color,0.08)}">
  <div class="num-value" style="background:linear-gradient(135deg,{CYAN},{PURPLE});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">{val}</div>
  <div class="num-label">{label} · {desc}</div>
</div>'''
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="body-text">{s.get('body','')}</div>
  <div class="numbers-row">{nums}</div>
  {pt}{tst}
</div>"""

    # ── 流程 ──────────────────────────────────────────────
    if t == "flow":
        steps_html = ""
        for step_title, step_desc, step_emoji in s["steps"]:
            steps_html += f'''<div class="flow-step">
  <div class="flow-emoji">{step_emoji}</div>
  <div class="flow-text">
    <div class="flow-step-title">{step_title}</div>
    <div class="flow-step-desc">{step_desc}</div>
  </div>
</div>'''
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="flow">{steps_html}</div>
  {pt}{tst}
</div>"""

    # ── 左右对比 ───────────────────────────────────────────
    if t == "contrast":
        before_items = "".join(f'<div class="contrast-item">• {it}</div>' for it in s.get("before_items",[]))
        after_items  = "".join(f'<div class="contrast-item">✓ {it}</div>' for it in s.get("after_items",[]))
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="contrast-layout">
    <div class="contrast-col" style="background:rgba(255,82,82,0.07);border-color:rgba(255,82,82,0.25)">
      <div class="contrast-col-title" style="color:{RED}">{s['before_label']}</div>
      {before_items}
    </div>
    <div class="contrast-arrow-col">
      <div style="width:48px;height:48px;">{icon('arrow')}</div>
    </div>
    <div class="contrast-col" style="background:rgba(0,230,118,0.07);border-color:rgba(0,230,118,0.25)">
      <div class="contrast-col-title" style="color:{GREEN}">{s['after_label']}</div>
      {after_items}
    </div>
  </div>
  {pt}{tst}
</div>"""

    # ── 痛点 ──────────────────────────────────────────────
    if t == "pain":
        items_html = ""
        for item in s.get("items", []):
            items_html += f'''<div class="pain-item">
  <div class="pain-item-icon">✗</div>
  <div class="pain-item-text">{item}</div>
</div>'''
        sub = f'<div class="body-text" style="margin-top:20px;font-size:clamp(18px,2vw,24px);color:rgba(255,107,53,0.7)">{s["sub"]}</div>' if s.get("sub") else ""
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="pain-items">{items_html}</div>
  {sub}
  {pt}{tst}
</div>"""

    # ── 水平时间线 ────────────────────────────────────────
    if t == "timeline_horiz":
        steps_html = ""
        for i, (step_title, step_desc) in enumerate(s["steps"]):
            steps_html += f'''<div class="timeline-step">
  <div class="timeline-num">{i+1}</div>
  <div class="timeline-content">
    <div class="timeline-title">{step_title}</div>
    <div class="timeline-desc">{step_desc}</div>
  </div>
</div>'''
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="timeline-horiz">{steps_html}</div>
  {pt}{tst}
</div>"""

    # ── 资源 ──────────────────────────────────────────────
    if t == "resources":
        resources_html = ""
        for name, desc, color in s["resources"]:
            resources_html += f'''<div class="resource-row" style="background:{hex_alpha(color,0.08)};border-color:{hex_alpha(color,0.4)}">
  <div class="resource-name" style="color:{color}">{name}</div>
  <div class="resource-desc">{desc}</div>
</div>'''
        subtitle = f'<div class="body-text" style="margin-top:8px;font-size:clamp(14px,1.5vw,18px);opacity:0.5">{s.get("subtitle","")}</div>' if s.get("subtitle") else ""
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  {subtitle}
  <div class="resources-grid">{resources_html}</div>
  {pt}{tst}
</div>"""

    # ── 比喻/未来 ──────────────────────────────────────────
    if t == "metaphor":
        badges = ""
        for layer in s.get("layers", []):
            badges += f'<div class="metaphor-badge" style="border-color:{hex_alpha(CYAN,0.4)};color:{CYAN};background:{hex_alpha(CYAN,0.06)}">{layer}</div>'
        metaphor = f'<div class="ending-emphasis" style="margin-top:28px;font-size:clamp(28px,3vw,40px)">{s["metaphor"]}</div>' if s.get("metaphor") else ""
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {tt}
  <div class="body-text">{s.get('body','')}</div>
  <div class="metaphor-badges">{badges}</div>
  {metaphor}
  {pt}{tst}
</div>"""

    # ── 结尾 ──────────────────────────────────────────────
    if t == "ending":
        body = f'<div class="body-text" style="margin-top:20px">{s["body"]}</div>' if s.get("body") else ""
        emp  = f'<div class="ending-emphasis">{s["emphasis"]}</div>' if s.get("emphasis") else ""
        emp2 = f'<div class="ending-emphasis">{s["title"]}</div>' if not s.get("emphasis") else emp
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  {emp2}
  {body}
  {pt}{tst}
</div>"""

    # ── 最终感谢页 ─────────────────────────────────────────
    if t == "end":
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  <div class="cover-bg"></div>
  <div class="cover-glow"></div>
  <div class="end-title">{s['headline']}</div>
  <div class="cover-bottom"></div>
  {pt}{tst}
</div>"""

    return f'<div class="slide" id="s{s["id"]}">{ts}{tt}</div>'

def build():
    slides_html = "\n".join(slide_html(s) for s in SLIDES)
    dots_html = "\n".join(
        f'<div class="dot" onclick="document.getElementById(\'s{s["id"]}\').scrollIntoView()"></div>'
        for s in SLIDES
    )

    script = """<script>
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
const progress = document.getElementById('progress');

function updateProgress() {
    const total = slides.length;
    const idx = Array.from(slides).findIndex(s => s.classList.contains('visible'));
    if (idx >= 0) {
        progress.style.width = ((idx + 1) / total * 100) + '%';
        dots.forEach((d, i) => d.classList.toggle('active', i === idx));
    }
}

const obs = new IntersectionObserver(entries => {
    entries.forEach(e => e.target.classList.toggle('visible', e.isIntersecting));
    updateProgress();
}, { threshold: 0.5 });
slides.forEach(s => obs.observe(s));

document.addEventListener('keydown', e => {
    const cur = Array.from(slides).findIndex(s => s.classList.contains('visible'));
    if ((e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === ' ') && cur < slides.length - 1) {
        e.preventDefault(); slides[cur + 1].scrollIntoView();
    }
    if ((e.key === 'ArrowUp' || e.key === 'ArrowLeft') && cur > 0) {
        e.preventDefault(); slides[cur - 1].scrollIntoView();
    }
});
<\/script>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Anthropic Agent Harness · 豆包AI播客</title>
{css()}
</head>
<body>
<div id="progress"></div>
<div id="dots">{dots_html}</div>
<div class="slides">
{slides_html}
</div>
{script}
</body>
</html>"""
    return html

if __name__ == "__main__":
    out_dir = r"D:\harnessworld\one-context\features\develop\anthropic-agent-harness-narration\production"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "presentation.html")
    content = build()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    size = os.path.getsize(out_path)
    print(f"Written: {out_path}")
    print(f"Slides: {len(SLIDES)}")
    print(f"Size: {size/1024:.1f} KB")
