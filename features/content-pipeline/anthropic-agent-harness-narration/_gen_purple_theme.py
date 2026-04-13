# -*- coding: utf-8 -*-
"""Anthropic Agent Harness 播客 PPT
    规格：1080×1920 | 零空白 | 字号加大
    主题：深紫黑 + 薰衣草紫 + 冰蓝（冷艳高级）
"""
import os

# ============================================================
# 颜色主题（深紫黑 + 薰衣草 + 冰蓝）
# ============================================================
BG        = "#0b0914"          # 深紫黑背景
BG2       = "#130f20"         # 浅一层紫黑
BG3       = "#1c1528"         # 卡片底色
BG4       = "#251d35"         # 更亮的卡片

TEXT      = "#e8e0f5"         # 薰衣草白（主文字）
TEXT_DIM  = "#9988b8"         # 淡紫灰（副文字）
TEXT_MID  = "#bba8d0"         # 中等灰紫

PURPLE    = "#a855f7"         # 主色：薰衣草紫
PURPLE2   = "#c084fc"         # 高亮紫
CYAN      = "#22d3ee"         # 冰蓝（数字/强调）
CYAN_DIM  = "#0891b2"         # 深冰蓝
PINK      = "#f472b6"         # 粉紫（对比/警示）
PINK_DIM  = "#be185d"         # 深粉
GHOST     = "rgba(168,85,247,0.12)"
GHOST_BD  = "rgba(168,85,247,0.25)"

# ============================================================
# SVG 图标库（简约几何风，冷色调）
# ============================================================
def svg(name, color=None):
    c = color or "#a855f7"
    icons = {
        "paw":       f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><ellipse cx="32" cy="44" rx="12" ry="9" fill="{c}" opacity=".8"/><circle cx="18" cy="30" r="6" fill="{c}" opacity=".7"/><circle cx="46" cy="30" r="6" fill="{c}" opacity=".7"/><circle cx="24" cy="20" r="5" fill="{c}" opacity=".65"/><circle cx="40" cy="20" r="5" fill="{c}" opacity=".65"/></svg>',
        "layers":    f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M32 8L8 20v24l24 12 24-12V20L32 8z" fill="{c}" opacity=".8"/><path d="M32 20L14 30v18l18 9 18-9V30L32 20z" fill="{c}" opacity=".5"/></svg>',
        "warning":   f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M32 8L4 56h56L32 8z" fill="{c}" opacity=".85"/><rect x="29" y="22" width="6" height="18" rx="3" fill="#0b0914" opacity=".85"/><circle cx="32" cy="46" r="3" fill="#0b0914" opacity=".85"/></svg>',
        "check":     f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><circle cx="32" cy="32" r="26" fill="{c}" opacity=".15" stroke="{c}" stroke-width="3"/><path d="M20 32l9 9 15-18" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        "arrow":     f'<svg viewBox="0 0 64 64" width="32" height="32" fill="none"><path d="M12 32h40M40 20l12 12-12 12" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        "server":    f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><rect x="8" y="12" width="48" height="14" rx="4" fill="{c}" opacity=".7"/><rect x="8" y="32" width="48" height="14" rx="4" fill="{c}" opacity=".85"/><rect x="8" y="52" width="48" height="14" rx="4" fill="{c}" opacity=".6"/><circle cx="18" cy="19" r="3" fill="#0b0914" opacity=".7"/><circle cx="18" cy="39" r="3" fill="#0b0914" opacity=".7"/><circle cx="18" cy="59" r="3" fill="#0b0914" opacity=".7"/></svg>',
        "bolt":      f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M36 4L14 36h16L24 60l28-34H34z" fill="{c}" opacity=".9"/></svg>',
        "trophy":    f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M20 8h24v24c0 8.84-5.37 16-12 16s-12-7.16-12-16V8z" fill="{c}" opacity=".9"/><path d="M20 16H8v8c0 6 4 10 12 10M44 16h12v8c0 6-4 10-12 10" stroke="{c}" stroke-width="3" fill="none" opacity=".8"/><rect x="28" y="48" width="8" height="8" fill="{c}" opacity=".9"/><rect x="20" y="54" width="24" height="4" rx="2" fill="{c}" opacity=".8"/></svg>',
        "puzzle":    f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M20 8h24a8 8 0 0 1 0 16H20V8z" fill="{c}" opacity=".85"/><path d="M8 24h16v24H8V24z" fill="{c}" opacity=".7"/><path d="M24 48h16a8 8 0 0 1 0 16H24V48z" fill="{c}" opacity=".7"/></svg>',
        "expand":    f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M8 24V8h16M56 24V8H40M8 40v16h16M56 40v16H40" stroke="{c}" stroke-width="4" stroke-linecap="round" opacity=".8"/></svg>',
        "cpu":       f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><rect x="16" y="16" width="32" height="32" rx="6" fill="{c}" opacity=".8"/><path d="M24 8v8M40 8v8M24 48v8M40 48v8M8 24h8M8 40h8M48 24h8M48 40h8" stroke="{c}" stroke-width="3" stroke-linecap="round" opacity=".6"/><rect x="24" y="24" width="16" height="16" rx="2" fill="#0b0914" opacity=".5"/></svg>',
        "lock":      f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><rect x="12" y="28" width="40" height="28" rx="6" fill="{c}" opacity=".85"/><path d="M20 28V20a12 12 0 0 1 24 0v8" stroke="{c}" stroke-width="4" stroke-linecap="round" fill="none"/></svg>',
        "gear":      f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><circle cx="32" cy="32" r="10" fill="{c}" opacity=".9"/><path d="M32 4v8M32 52v8M4 32h8M52 32h8M10.8 10.8l5.66 5.66M47.54 47.54l5.66 5.66M53.2 10.8l-5.66 5.66M16.46 47.54l-5.66 5.66" stroke="{c}" stroke-width="4" stroke-linecap="round" opacity=".65"/></svg>',
        "shield":    f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M32 6L8 16v20c0 14.4 10.24 27.84 24 31 13.76-3.16 24-16.6 24-31V16L32 6z" fill="{c}" opacity=".8"/></svg>',
        "chain":     f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><path d="M20 16h-4v-4a12 12 0 0 1 24 0v4h-4" stroke="{c}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M20 48h-4v4a12 12 0 0 1 24 0v-4h-4" stroke="{c}" stroke-width="4" fill="none" stroke-linecap="round"/><line x1="20" y1="20" x2="20" y2="44" stroke="{c}" stroke-width="4" stroke-linecap="round"/></svg>',
        "chart":     f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><rect x="8" y="40" width="12" height="18" rx="3" fill="{c}" opacity=".6"/><rect x="26" y="26" width="12" height="32" rx="3" fill="{c}" opacity=".8"/><rect x="44" y="12" width="12" height="46" rx="3" fill="{c}" opacity="1"/></svg>',
        "brain":     f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><ellipse cx="32" cy="32" rx="22" ry="20" fill="{c}" opacity=".75"/><path d="M20 26c4-4 8-4 12 0M32 26c4-4 8-4 12 0M18 38c4-4 8-4 14 0M32 38c4-4 8-4 12 0" stroke="#0b0914" stroke-width="2.5" stroke-linecap="round" opacity=".7"/></svg>',
        "clock":     f'<svg viewBox="0 0 64 64" width="48" height="48" fill="none"><circle cx="32" cy="32" r="26" stroke="{c}" stroke-width="4" opacity=".8"/><path d="M32 18v16l10 10" stroke="{c}" stroke-width="4" stroke-linecap="round"/></svg>',
    }
    return icons.get(name, icons["layers"])

# ============================================================
# 幻灯数据（20页，竖屏 1080×1920）
# ============================================================
SLIDES = [
    # ── 封面 ──────────────────────────────────────────────
    {
        "id": 0, "start": 0, "end": 7,
        "type": "cover",
        "tag": "豆包AI播客",
        "headline": "Agent\n是宠物\n还是牲口？",
        "sub": "Anthropic 把 AI 从精心呵护的宠物\n变成了随时可替换的打工仔",
    },
    # ── PART I 架构的转变 ────────────────────────────────
    {
        "id": 1, "start": 7, "end": 15,
        "type": "section",
        "tag": "PART I",
        "title": "架构的转变",
        "icon": "layers",
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
        "color": "#f472b6",
    },
    {
        "id": 3, "start": 36, "end": 51,
        "type": "big_center",
        "tag": "PART I · 核心问题",
        "title": "这个架构\n就像养了一只宠物",
        "icon": "paw",
        "accent_color": "#c084fc",
        "sub": "精心呵护 · 不可替换 · 全局耦合",
    },
    {
        "id": 4, "start": 51, "end": 67,
        "type": "triple_layers",
        "tag": "PART I · 新架构",
        "title": "三层分离",
        "subtitle": "Session · Harness · Sandbox",
        "layers": [
            ("Session", "日志层", "只追加事件记录\n不关业务逻辑\n支持 replay", "#a855f7"),
            ("Harness", "大脑层", "无状态\n负责任务调度\n和工具选择", "#22d3ee"),
            ("Sandbox", "执行层", "安全隔离\n执行命令\n返回结果", "#34d399"),
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
        "title": "从宠物变打工仔",
        "before": "🐾 宠物",
        "after": "⚙️ 打工仔",
        "icon": "arrow",
        "accent_color": "#22d3ee",
    },
    # ── PART II 变革带来的成效 ─────────────────────────────
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
            ("Agent", "可组合的\n能力单元", "#a855f7"),
            ("Environment", "可替换的\n执行环境", "#22d3ee"),
            ("Session", "可管理的\n会话状态", "#34d399"),
        ],
    },
    {
        "id": 16, "start": 450, "end": 485,
        "type": "metaphor",
        "tag": "PART III · 未来",
        "title": "模块化分层架构",
        "body": "模型只是大脑\n通过稳定接口连接各种\n可替换的执行环境和工具",
        "metaphor": "🤖 AI Native OS",
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
    # ── 结尾 ──────────────────────────────────────────────
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
# CSS 样式（深紫黑 + 薰衣草 + 冰蓝）
# ============================================================
def css():
    return """<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
    font-family: 'Microsoft YaHei UI', 'PingFang SC', 'Microsoft YaHei',
                 'Source Han Sans CN', sans-serif;
    background: #0b0914;
    color: #e8e0f5;
    overflow-x: hidden;
}

.slides {
    width: 100vw;
    height: 100vh;
    overflow-y: scroll;
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

.slide {
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
}

/* 紫色光晕 */
.slide::before {
    content: '';
    position: absolute;
    top: -300px; left: 50%;
    transform: translateX(-50%);
    width: 1000px; height: 1000px;
    background: radial-gradient(ellipse at center,
        rgba(168,85,247,0.12) 0%,
        rgba(34,211,238,0.04) 50%,
        transparent 70%);
    pointer-events: none;
    z-index: 0;
}
.slide > * { position: relative; z-index: 1; }

/* 进度条 */
#progress {
    position: fixed; top: 0; left: 0;
    height: 3px;
    background: linear-gradient(90deg, #a855f7, #22d3ee);
    z-index: 999;
    transition: width 0.3s ease;
}

/* 右侧导航点 */
#dots {
    position: fixed; right: 20px; top: 50%;
    transform: translateY(-50%);
    display: flex; flex-direction: column; gap: 8px;
    z-index: 999;
}
.dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: rgba(168,85,247,0.3);
    cursor: pointer; transition: all 0.3s;
}
.dot.active {
    background: #a855f7;
    box-shadow: 0 0 8px rgba(168,85,247,0.8);
    transform: scale(1.6);
}

/* ─── 共用组件 ─── */
.tag {
    font-size: 13px; font-weight: 700;
    letter-spacing: 6px;
    color: #22d3ee;
    text-transform: uppercase; opacity: 0.9;
}
.title {
    font-size: clamp(44px, 6vw, 72px); font-weight: 900;
    line-height: 1.15; color: #e8e0f5;
    text-align: center; letter-spacing: 1px;
    text-shadow: 0 0 40px rgba(168,85,247,0.2);
    margin-top: 16px;
}
.body-text {
    font-size: clamp(24px, 3vw, 36px); line-height: 1.7;
    color: rgba(232,224,245,0.65);
    text-align: center; margin-top: 24px; white-space: pre-line;
}
.divider {
    width: 60px; height: 3px;
    background: linear-gradient(90deg, #a855f7, #22d3ee);
    border-radius: 2px; margin: 20px auto;
}
.top-bar {
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #a855f7 30%, #22d3ee 70%, transparent);
}
.timestamp {
    position: absolute; bottom: 24px; right: 36px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 11px; color: rgba(153,136,184,0.4); letter-spacing: 1px;
}
.page-num {
    position: absolute; bottom: 24px; left: 36px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 11px; color: rgba(153,136,184,0.4); letter-spacing: 1px;
}

/* ─── 封面 ─── */
.cover-bg {
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 50% 30%,
            rgba(168,85,247,0.18) 0%,
            rgba(34,211,238,0.07) 40%,
            transparent 70%),
        radial-gradient(ellipse 60% 50% at 80% 80%,
            rgba(168,85,247,0.10) 0%,
            transparent 60%),
        #0b0914;
}
.cover-glow {
    position: absolute;
    width: 700px; height: 700px;
    top: 50%; left: 50%;
    transform: translate(-50%, -60%);
    background: radial-gradient(ellipse, rgba(168,85,247,0.20) 0%, transparent 70%);
    pointer-events: none;
}
.cover-eyebrow {
    font-size: 14px; letter-spacing: 8px;
    color: rgba(34,211,238,0.7); font-weight: 500;
    text-transform: uppercase; margin-bottom: 32px;
}
.cover-headline {
    font-size: clamp(72px, 10vw, 120px); font-weight: 900;
    line-height: 1.0; text-align: center;
    color: #e8e0f5; letter-spacing: 4px;
    text-shadow: 0 0 60px rgba(168,85,247,0.35);
    white-space: pre-line;
}
.cover-sub {
    font-size: clamp(18px, 2.2vw, 26px);
    color: rgba(232,224,245,0.55);
    text-align: center; margin-top: 28px; line-height: 1.8; white-space: pre-line;
}
.cover-bottom {
    position: absolute; bottom: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #a855f7, #c084fc, #22d3ee);
}

/* ─── 章节分隔页 ─── */
.section-icon { width: 80px; height: 80px; margin-bottom: 24px; }
.section-icon svg { width: 80px; height: 80px; }
.section-title {
    font-size: clamp(52px, 7vw, 88px); font-weight: 900;
    color: #e8e0f5; text-align: center; letter-spacing: 2px;
    text-shadow: 0 0 40px rgba(168,85,247,0.25);
    margin-top: 16px;
}

/* ─── 图标网格（四宫格）─── */
.grid-2x2 {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 16px; width: 100%; margin-top: 28px;
}
.grid-card {
    padding: 28px 20px; border-radius: 20px;
    background: rgba(244,114,182,0.06);
    border: 1px solid rgba(244,114,182,0.18);
    text-align: center;
}
.grid-card-icon { width: 52px; height: 52px; margin: 0 auto 14px; }
.grid-card-icon svg { width: 52px; height: 52px; }
.grid-card h3 {
    font-size: clamp(22px, 2.5vw, 30px); font-weight: 700; margin-bottom: 8px;
}
.grid-card p {
    font-size: clamp(15px, 1.5vw, 18px);
    color: rgba(232,224,245,0.55); line-height: 1.5; white-space: pre-line;
}

/* ─── 大居中 ─── */
.big-center { text-align: center; margin-top: 24px; }
.big-icon { width: 96px; height: 96px; margin: 0 auto 20px; }
.big-icon svg { width: 96px; height: 96px; }
.big-sub {
    font-size: clamp(18px, 2vw, 24px);
    color: rgba(192,132,252,0.7); letter-spacing: 4px; margin-top: 16px;
}

/* ─── 三层架构 ─── */
.layers { width: 100%; display: flex; flex-direction: column; gap: 14px; margin-top: 28px; }
.layer-row {
    display: grid; grid-template-columns: 160px 1fr;
    align-items: center; gap: 20px; padding: 22px 28px; border-radius: 18px; border-left: 5px solid;
}
.layer-name { font-size: clamp(20px, 2.2vw, 26px); font-weight: 800; letter-spacing: 2px; }
.layer-role { font-size: 13px; opacity: 0.65; letter-spacing: 2px; margin-top: 2px; }
.layer-desc { font-size: clamp(16px, 1.6vw, 20px); color: rgba(232,224,245,0.82); line-height: 1.6; white-space: pre-line; }

/* ─── 对比中心 ─── */
.contrast-center { text-align: center; margin-top: 24px; width: 100%; }
.contrast-row { display: flex; align-items: center; justify-content: center; gap: 32px; flex-wrap: wrap; }
.contrast-box { padding: 28px 48px; border-radius: 20px; font-size: clamp(32px, 4vw, 52px); font-weight: 900; border: 2px solid; }
.contrast-arrow-icon { width: 48px; height: 48px; }
.contrast-arrow-icon svg { width: 48px; height: 48px; }

/* ─── 数字卡片 ─── */
.numbers-row { display: flex; gap: 24px; justify-content: center; margin-top: 32px; width: 100%; }
.num-card { flex: 1; max-width: 280px; padding: 32px 24px; border-radius: 24px; text-align: center; border: 2px solid; }
.num-value { font-family: 'Consolas', 'Courier New', monospace; font-size: clamp(52px, 6vw, 80px); font-weight: 900; line-height: 1; }
.num-label { font-size: clamp(14px, 1.5vw, 18px); opacity: 0.65; margin-top: 10px; letter-spacing: 1px; }

/* ─── 流程 ─── */
.flow { display: flex; flex-direction: column; gap: 14px; width: 100%; margin-top: 28px; }
.flow-step { display: flex; align-items: center; gap: 20px; padding: 22px 28px; border-radius: 16px; background: rgba(168,85,247,0.06); border: 1px solid rgba(168,85,247,0.15); }
.flow-emoji { font-size: 36px; flex-shrink: 0; width: 56px; text-align: center; }
.flow-step-title { font-size: clamp(20px, 2.2vw, 26px); font-weight: 700; color: #a855f7; margin-bottom: 4px; }
.flow-step-desc { font-size: clamp(15px, 1.5vw, 18px); color: rgba(232,224,245,0.65); }

/* ─── 左右对比 ─── */
.contrast-layout { display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; align-items: start; margin-top: 28px; width: 100%; }
.contrast-col { padding: 24px 20px; border-radius: 20px; border: 1px solid; }
.contrast-col-title { font-size: clamp(16px, 1.8vw, 22px); font-weight: 700; margin-bottom: 14px; }
.contrast-item { font-size: clamp(15px, 1.5vw, 18px); padding: 6px 0; opacity: 0.82; }
.contrast-arrow-col { display: flex; align-items: center; padding-top: 40px; }

/* ─── 图标列表 ─── */
.icon-list { width: 100%; margin-top: 24px; display: flex; flex-direction: column; gap: 14px; }
.icon-list-item { display: flex; align-items: center; gap: 20px; padding: 20px 24px; border-radius: 16px; background: rgba(232,224,245,0.03); border: 1px solid rgba(232,224,245,0.08); }
.icon-list-icon { width: 44px; height: 44px; flex-shrink: 0; }
.icon-list-icon svg { width: 44px; height: 44px; }
.icon-list-text h4 { font-size: clamp(18px, 2vw, 24px); font-weight: 700; color: #e8e0f5; margin-bottom: 4px; }
.icon-list-text p { font-size: clamp(14px, 1.4vw, 17px); color: rgba(232,224,245,0.55); white-space: pre-line; }

/* ─── 痛点 ─── */
.pain-items { width: 100%; margin-top: 28px; display: flex; flex-direction: column; gap: 14px; }
.pain-item { display: flex; align-items: center; gap: 20px; padding: 22px 28px; border-radius: 16px; background: rgba(244,114,182,0.07); border: 1px solid rgba(244,114,182,0.20); }
.pain-item-icon { font-size: 32px; flex-shrink: 0; width: 44px; text-align: center; }
.pain-item-text { font-size: clamp(22px, 2.8vw, 34px); font-weight: 700; color: #f472b6; }

/* ─── 水平时间线 ─── */
.timeline-horiz { width: 100%; margin-top: 32px; display: flex; flex-direction: column; gap: 20px; }
.timeline-step { display: flex; align-items: center; gap: 24px; }
.timeline-num { min-width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #a855f7, #22d3ee); display: flex; align-items: center; justify-content: center; font-family: 'Consolas', 'Courier New', monospace; font-size: 22px; font-weight: 700; flex-shrink: 0; color: #0b0914; }
.timeline-content { flex: 1; padding: 20px 24px; border-radius: 16px; background: rgba(168,85,247,0.06); border: 1px solid rgba(168,85,247,0.15); }
.timeline-title { font-size: clamp(18px, 2vw, 24px); font-weight: 700; color: #a855f7; margin-bottom: 6px; }
.timeline-desc { font-size: clamp(15px, 1.5vw, 18px); color: rgba(232,224,245,0.65); }

/* ─── 资源 ─── */
.resources-grid { display: flex; flex-direction: column; gap: 16px; width: 100%; margin-top: 28px; }
.resource-row { display: grid; grid-template-columns: 180px 1fr; align-items: center; gap: 20px; padding: 24px 28px; border-radius: 18px; border-left: 5px solid; }
.resource-name { font-size: clamp(22px, 2.5vw, 32px); font-weight: 800; letter-spacing: 2px; }
.resource-desc { font-size: clamp(16px, 1.6vw, 20px); color: rgba(232,224,245,0.82); line-height: 1.6; white-space: pre-line; }

/* ─── 比喻 ─── */
.metaphor-badges { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; margin-top: 20px; }
.metaphor-badge { padding: 12px 28px; border-radius: 100px; font-size: clamp(16px, 1.8vw, 22px); font-weight: 700; border: 2px solid rgba(34,211,238,0.4); color: #22d3ee; background: rgba(34,211,238,0.06); }

/* ─── 结尾 ─── */
.ending-emphasis { font-size: clamp(28px, 3.5vw, 48px); font-weight: 700; color: #e8e0f5; text-align: center; margin-top: 20px; }
.ending-sub { font-size: clamp(22px, 2.5vw, 30px); font-weight: 700; color: #a855f7; text-align: center; margin-top: 20px; padding: 20px 40px; border: 2px solid rgba(168,85,247,0.4); border-radius: 16px; background: rgba(168,85,247,0.08); }

/* ─── 最终页 ─── */
.end-title {
    font-size: clamp(64px, 9vw, 120px); font-weight: 900;
    text-align: center; line-height: 1.1;
    background: linear-gradient(135deg, #a855f7, #22d3ee);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: 4px; white-space: pre-line;
    filter: drop-shadow(0 0 40px rgba(168,85,247,0.4));
}
</style>"""

# ============================================================
# 辅助函数
# ============================================================
def ha(hex_color, alpha):
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

    if t == "section":
        ic = svg(s.get("icon", "layers"))
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  <div class="section-icon">{ic}</div>
  <div class="section-title">{s['title']}</div>
  <div class="divider"></div>
  {pt}{tst}
</div>"""

    if t == "icon_grid":
        color = s.get("color", "#a855f7")
        grid = ""
        for title, desc in s["items"]:
            grid += f'<div class="grid-card">\n  <div class="grid-card-icon">{svg(s.get("icon","warning"), color)}</div>\n  <h3 style="color:{color}">{title}</h3>\n  <p>{desc}</p>\n</div>'
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="grid-2x2">{grid}</div>
  {pt}{tst}
</div>"""

    if t == "big_center":
        color = s.get("accent_color", "#c084fc")
        ic = svg(s.get("icon", "paw"), color)
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="big-center">
    <div class="big-icon">{ic}</div>
    <div class="big-sub">{s.get('sub','')}</div>
  </div>
  {pt}{tst}
</div>"""

    if t == "triple_layers":
        layers_html = ""
        for name, role, desc, color in s["layers"]:
            layers_html += f'<div class="layer-row" style="background:{ha(color,0.1)};border-color:{ha(color,0.5)}">\n  <div>\n    <div class="layer-name" style="color:{color}">{name}</div>\n    <div class="layer-role" style="color:{color}">{role}</div>\n  </div>\n  <div class="layer-desc">{desc}</div>\n</div>'
        subtitle = f'<div class="body-text" style="margin-top:8px;font-size:clamp(16px,1.8vw,22px);opacity:0.45;color:#9988b8">{s.get("subtitle","")}</div>' if s.get("subtitle") else ""
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}{subtitle}
  <div class="layers">{layers_html}</div>
  {pt}{tst}
</div>"""

    if t == "icon_list":
        items_html = ""
        for title, desc in s["items"]:
            items_html += f'<div class="icon-list-item">\n  <div class="icon-list-icon">{svg(s.get("icon","check"))}</div>\n  <div class="icon-list-text"><h4>{title}</h4><p>{desc}</p></div>\n</div>'
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="icon-list">{items_html}</div>
  {pt}{tst}
</div>"""

    if t == "contrast_center":
        color = s.get("accent_color", "#22d3ee")
        ic = svg(s.get("icon", "arrow"), color)
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="contrast-center">
    <div class="contrast-row">
      <div class="contrast-box" style="color:#f472b6;border-color:rgba(244,114,182,0.6);background:rgba(244,114,182,0.1)">{s['before']}</div>
      <div class="contrast-arrow-icon">{ic}</div>
      <div class="contrast-box" style="color:{color};border-color:{ha(color,0.6)};background:{ha(color,0.1)}">{s['after']}</div>
    </div>
  </div>
  {pt}{tst}
</div>"""

    if t == "numbers":
        nums = ""
        for label, val, desc in s.get("numbers", []):
            nums += f'<div class="num-card" style="border-color:rgba(34,211,238,0.5);background:rgba(34,211,238,0.06)">\n  <div class="num-value" style="background:linear-gradient(135deg,#a855f7,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">{val}</div>\n  <div class="num-label">{label} · {desc}</div>\n</div>'
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="body-text">{s.get('body','')}</div>
  <div class="numbers-row">{nums}</div>
  {pt}{tst}
</div>"""

    if t == "flow":
        steps_html = ""
        for step_title, step_desc, step_emoji in s["steps"]:
            steps_html += f'<div class="flow-step">\n  <div class="flow-emoji">{step_emoji}</div>\n  <div>\n    <div class="flow-step-title">{step_title}</div>\n    <div class="flow-step-desc">{step_desc}</div>\n  </div>\n</div>'
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="flow">{steps_html}</div>
  {pt}{tst}
</div>"""

    if t == "contrast":
        before_items = "".join(f'<div class="contrast-item">• {it}</div>' for it in s.get("before_items",[]))
        after_items  = "".join(f'<div class="contrast-item">✓ {it}</div>' for it in s.get("after_items",[]))
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="contrast-layout">
    <div class="contrast-col" style="background:rgba(244,114,182,0.06);border-color:rgba(244,114,182,0.20)">
      <div class="contrast-col-title" style="color:#f472b6">{s['before_label']}</div>
      {before_items}
    </div>
    <div class="contrast-arrow-col">
      <div style="width:48px;height:48px;">{svg('arrow')}</div>
    </div>
    <div class="contrast-col" style="background:rgba(168,85,247,0.06);border-color:rgba(168,85,247,0.20)">
      <div class="contrast-col-title" style="color:#a855f7">{s['after_label']}</div>
      {after_items}
    </div>
  </div>
  {pt}{tst}
</div>"""

    if t == "pain":
        items_html = ""
        for item in s.get("items", []):
            items_html += f'<div class="pain-item">\n  <div class="pain-item-icon">✗</div>\n  <div class="pain-item-text">{item}</div>\n</div>'
        sub = f'<div class="body-text" style="margin-top:20px;font-size:clamp(18px,2vw,24px);color:rgba(244,114,182,0.7)">{s["sub"]}</div>' if s.get("sub") else ""
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="pain-items">{items_html}</div>
  {sub}
  {pt}{tst}
</div>"""

    if t == "timeline_horiz":
        steps_html = ""
        for i, (step_title, step_desc) in enumerate(s["steps"]):
            steps_html += f'<div class="timeline-step">\n  <div class="timeline-num">{i+1}</div>\n  <div class="timeline-content">\n    <div class="timeline-title">{step_title}</div>\n    <div class="timeline-desc">{step_desc}</div>\n  </div>\n</div>'
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="timeline-horiz">{steps_html}</div>
  {pt}{tst}
</div>"""

    if t == "resources":
        resources_html = ""
        for name, desc, color in s["resources"]:
            resources_html += f'<div class="resource-row" style="background:{ha(color,0.08)};border-color:{ha(color,0.4)}">\n  <div class="resource-name" style="color:{color}">{name}</div>\n  <div class="resource-desc">{desc}</div>\n</div>'
        subtitle = f'<div class="body-text" style="margin-top:8px;font-size:clamp(14px,1.5vw,18px);opacity:0.45;color:#9988b8">{s.get("subtitle","")}</div>' if s.get("subtitle") else ""
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}{subtitle}
  <div class="resources-grid">{resources_html}</div>
  {pt}{tst}
</div>"""

    if t == "metaphor":
        badges = ""
        for layer in s.get("layers", []):
            badges += f'<div class="metaphor-badge">{layer}</div>'
        metaphor = f'<div style="margin-top:28px;font-size:clamp(28px,3vw,40px);color:#22d3ee;font-weight:900">{s["metaphor"]}</div>' if s.get("metaphor") else ""
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}{tt}
  <div class="body-text">{s.get('body','')}</div>
  <div class="metaphor-badges">{badges}</div>
  {metaphor}
  {pt}{tst}
</div>"""

    if t == "ending":
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  {ts}
  <div class="ending-sub">{s.get('title','')}</div>
  <div class="ending-emphasis">{s.get('body','')}</div>
  {pt}{tst}
</div>"""

    if t == "end":
        return f"""<div class="slide" id="s{s['id']}">
  <div class="top-bar"></div>
  <div class="cover-bg"></div>
  <div class="cover-glow"></div>
  <div class="end-title">{s['headline']}</div>
  <div class="cover-bottom"></div>
  {pt}{tst}
</div>"""

    return f'<div class="slide" id="s{s["id"]}">{ts}{tt}{pt}{tst}</div>'

def build():
    slides_html = "\n".join(slide_html(s) for s in SLIDES)
    dots_html = "\n".join(
        f'<div class="dot" onclick="document.getElementById(\'s{s["id"]}\').scrollIntoView()"></div>'
        for s in SLIDES
    )

    script = r"""<script>
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

// 立即显示第一页
slides[0].classList.add('visible');

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
<meta name="viewport" content="width=device-width, initial-scale=1.0">
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
