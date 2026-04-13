# -*- coding: utf-8 -*-
"""Anthropic Agent Harness PPT v2 - 竖屏 · 高密度 · 动物主题
    规格：1080×1920 | 整页撑满 | 图形丰富 | 无空白
"""
import os

# ============================================================
# 暖土动物色板
# ============================================================
BG      = "#120c08"
BGCARD  = "#1e1209"
BGCARD2 = "#2a1a10"
BONE    = "#f5e6d3"
CREAM   = "#e8d5b7"
TERRA   = "#c2714f"
AMBER   = "#d4a843"
SAGE    = "#7d9c6c"
BURNT   = "#e85d3a"
MOSS    = "#4a6741"
GOLD    = "#f0c040"
MUTED   = "#8c7a6a"
DIVIDER = "#d4a843"
CARD_BG = "rgba(194,113,79,0.12)"
CARD_BD = "rgba(194,113,79,0.22)"

# ============================================================
# 丰富的 SVG 插图库（大尺寸，填充页面）
# ============================================================

def illust(name, color=None):
    c = color or AMBER
    D = "none"   # fill="none" shorthand

    LIB = {

        # ── 大狗插图（封面/宠物页）────────────────────────
        "dog_main": f'''<svg viewBox="0 0 400 340" width="380" height="320" xmlns="http://www.w3.org/2000/svg">
  <!-- 身体 -->
  <ellipse cx="200" cy="230" rx="120" ry="80" fill="{c}" opacity=".25"/>
  <ellipse cx="200" cy="220" rx="100" ry="65" fill="{c}" opacity=".35"/>
  <!-- 头 -->
  <ellipse cx="200" cy="110" rx="72" ry="65" fill="{c}" opacity=".45"/>
  <!-- 耳朵左 -->
  <ellipse cx="135" cy="75" rx="28" ry="42" fill="{c}" opacity=".6" transform="rotate(-20 135 75)"/>
  <!-- 耳朵右 -->
  <ellipse cx="265" cy="75" rx="28" ry="42" fill="{c}" opacity=".6" transform="rotate(20 265 75)"/>
  <!-- 脸部加深 -->
  <ellipse cx="200" cy="115" rx="58" ry="48" fill="#1e1209" opacity=".25"/>
  <!-- 眼睛 -->
  <circle cx="168" cy="105" r="14" fill="#1e1209" opacity=".8"/>
  <circle cx="232" cy="105" r="14" fill="#1e1209" opacity=".8"/>
  <circle cx="172" cy="101" r="5" fill="{BONE}" opacity=".9"/>
  <circle cx="236" cy="101" r="5" fill="{BONE}" opacity=".9"/>
  <!-- 鼻子 -->
  <ellipse cx="200" cy="135" rx="16" ry="11" fill="#1e1209" opacity=".85"/>
  <ellipse cx="200" cy="133" rx="6" ry="4" fill="{c}" opacity=".4"/>
  <!-- 嘴巴 -->
  <path d="M185 148 Q200 158 215 148" stroke="#1e1209" stroke-width="3" fill="none" opacity=".7" stroke-linecap="round"/>
  <!-- 舌头 -->
  <ellipse cx="200" cy="156" rx="9" ry="12" fill="{TERRA}" opacity=".7"/>
  <!-- 身体轮廓加深 -->
  <ellipse cx="200" cy="218" rx="95" ry="60" fill="#1e1209" opacity=".15"/>
  <!-- 腿 -->
  <ellipse cx="140" cy="305" rx="28" ry="18" fill="{c}" opacity=".3"/>
  <ellipse cx="260" cy="305" rx="28" ry="18" fill="{c}" opacity=".3"/>
  <!-- 尾巴 -->
  <path d="M310 210 Q360 180 340 140 Q330 160 315 175" fill="{c}" opacity=".4"/>
  <!-- 爪印装饰 -->
  <circle cx="80" cy="60" r="18" fill="{c}" opacity=".12"/>
  <circle cx="95" cy="40" r="8" fill="{c}" opacity=".12"/>
  <circle cx="65" cy="40" r="8" fill="{c}" opacity=".12"/>
  <circle cx="108" cy="52" r="8" fill="{c}" opacity=".12"/>
  <circle cx="70" cy="52" r="8" fill="{c}" opacity=".12"/>
</svg>''',

        # ── 牛群插图（牲口页）──────────────────────────────
        "cattle_main": f'''<svg viewBox="0 0 400 300" width="380" height="280" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景草 -->
  <rect x="0" y="230" width="400" height="70" fill="{SAGE}" opacity=".15" rx="0"/>
  <!-- 牛1 前景 -->
  <ellipse cx="100" cy="190" rx="60" ry="42" fill="{c}" opacity=".5"/>
  <ellipse cx="100" cy="165" rx="38" ry="30" fill="{c}" opacity=".6"/>
  <ellipse cx="75" cy="140" rx="14" ry="22" fill="{c}" opacity=".55" transform="rotate(-15 75 140)"/>
  <ellipse cx="125" cy="140" rx="14" ry="22" fill="{c}" opacity=".55" transform="rotate(15 125 140)"/>
  <circle cx="85" cy="158" r="6" fill="#1e1209" opacity=".8"/>
  <circle cx="115" cy="158" r="6" fill="#1e1209" opacity=".8"/>
  <ellipse cx="100" cy="175" rx="10" ry="7" fill="#1e1209" opacity=".7"/>
  <!-- 斑点 -->
  <ellipse cx="90" cy="200" rx="18" ry="12" fill="#1e1209" opacity=".2"/>
  <ellipse cx="120" cy="185" rx="12" ry="8" fill="#1e1209" opacity=".15"/>
  <!-- 牛2 中景 -->
  <ellipse cx="230" cy="200" rx="55" ry="38" fill="{c}" opacity=".35"/>
  <ellipse cx="230" cy="178" rx="34" ry="26" fill="{c}" opacity=".4"/>
  <ellipse cx="208" cy="155" rx="12" ry="18" fill="{c}" opacity=".38" transform="rotate(-12 208 155)"/>
  <ellipse cx="252" cy="155" rx="12" ry="18" fill="{c}" opacity=".38" transform="rotate(12 252 155)"/>
  <circle cx="218" cy="172" r="5" fill="#1e1209" opacity=".7"/>
  <circle cx="242" cy="172" r="5" fill="#1e1209" opacity=".7"/>
  <!-- 牛3 远景 -->
  <ellipse cx="340" cy="210" rx="48" ry="32" fill="{c}" opacity=".22"/>
  <ellipse cx="340" cy="190" rx="28" ry="22" fill="{c}" opacity=".28"/>
  <!-- 角 (牛1) -->
  <path d="M72 135 Q60 110 68 100" stroke="{c}" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/>
  <path d="M128 135 Q140 110 132 100" stroke="{c}" stroke-width="5" fill="none" opacity=".6" stroke-linecap="round"/>
  <!-- 脚 -->
  <rect x="70" y="228" width="16" height="18" rx="6" fill="{c}" opacity=".35"/>
  <rect x="108" y="228" width="16" height="18" rx="6" fill="{c}" opacity=".35"/>
  <!-- 尾巴 -->
  <path d="M155 190 Q185 200 180 230" stroke="{c}" stroke-width="5" fill="none" opacity=".4" stroke-linecap="round"/>
  <!-- 地面草线 -->
  <path d="M0 252 Q50 245 100 252 Q150 259 200 252 Q250 245 300 252 Q350 259 400 252" stroke="{SAGE}" stroke-width="3" fill="none" opacity=".4"/>
</svg>''',

        # ── 架构三层大插图 ──────────────────────────────────
        "arch_3layer": f'''<svg viewBox="0 0 480 360" width="460" height="340" xmlns="http://www.w3.org/2000/svg">
  <!-- 连接线 -->
  <path d="M240 90 L240 150" stroke="{c}" stroke-width="4" stroke-dasharray="8 6" opacity=".5"/>
  <path d="M240 210 L240 270" stroke="{c}" stroke-width="4" stroke-dasharray="8 6" opacity=".5"/>
  <!-- Session 层 -->
  <rect x="60" y="20" width="360" height="70" rx="16" fill="{TERRA}" opacity=".25"/>
  <rect x="60" y="20" width="360" height="70" rx="16" stroke="{TERRA}" stroke-width="2.5" opacity=".7"/>
  <text x="90" y="58" font-family="Consolas" font-size="22" font-weight="bold" fill="{TERRA}" opacity=".9">SESS</text>
  <rect x="180" y="30" width="120" height="10" rx="5" fill="{TERRA}" opacity=".4"/>
  <rect x="180" y="50" width="80" height="8" rx="4" fill="{TERRA}" opacity=".3"/>
  <rect x="180" y="65" width="100" height="8" rx="4" fill="{TERRA}" opacity=".25"/>
  <!-- 箭头1 -->
  <polygon points="235,95 245,95 240,105" fill="{c}" opacity=".6"/>
  <!-- Harness 层 -->
  <rect x="60" y="145" width="360" height="70" rx="16" fill="{AMBER}" opacity=".25"/>
  <rect x="60" y="145" width="360" height="70" rx="16" stroke="{AMBER}" stroke-width="2.5" opacity=".7"/>
  <text x="90" y="183" font-family="Consolas" font-size="22" font-weight="bold" fill="{AMBER}" opacity=".9">HARNESS</text>
  <circle cx="250" cy="180" r="22" fill="{AMBER}" opacity=".25" stroke="{AMBER}" stroke-width="2"/>
  <circle cx="250" cy="180" r="10" fill="{AMBER}" opacity=".5"/>
  <circle cx="320" cy="180" r="18" fill="{AMBER}" opacity=".2" stroke="{AMBER}" stroke-width="2"/>
  <circle cx="320" cy="180" r="8" fill="{AMBER}" opacity=".4"/>
  <circle cx="380" cy="180" r="16" fill="{AMBER}" opacity=".2" stroke="{AMBER}" stroke-width="2"/>
  <circle cx="380" cy="180" r="7" fill="{AMBER}" opacity=".4"/>
  <!-- 箭头2 -->
  <polygon points="235,220 245,220 240,230" fill="{c}" opacity=".6"/>
  <!-- Sandbox 层 -->
  <rect x="60" y="270" width="360" height="70" rx="16" fill="{SAGE}" opacity=".25"/>
  <rect x="60" y="270" width="360" height="70" rx="16" stroke="{SAGE}" stroke-width="2.5" opacity=".7"/>
  <text x="90" y="308" font-family="Consolas" font-size="22" font-weight="bold" fill="{SAGE}" opacity=".9">SANDBOX</text>
  <!-- 沙箱内部格子 -->
  <rect x="200" y="280" width="55" height="50" rx="8" fill="{SAGE}" opacity=".2" stroke="{SAGE}" stroke-width="1.5"/>
  <rect x="265" y="280" width="55" height="50" rx="8" fill="{SAGE}" opacity=".2" stroke="{SAGE}" stroke-width="1.5"/>
  <rect x="330" y="280" width="55" height="50" rx="8" fill="{SAGE}" opacity=".2" stroke="{SAGE}" stroke-width="1.5"/>
  <!-- 沙箱内图标 -->
  <circle cx="227" cy="305" r="12" fill="{SAGE}" opacity=".4"/>
  <circle cx="292" cy="305" r="12" fill="{SAGE}" opacity=".4"/>
  <circle cx="357" cy="305" r="12" fill="{SAGE}" opacity=".4"/>
</svg>''',

        # ── 爪印装饰（大型）────────────────────────────────
        "paw_hero": f'''<svg viewBox="0 0 200 180" width="200" height="180" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="100" cy="120" rx="50" ry="38" fill="{c}" opacity=".18"/>
  <circle cx="55" cy="70" r="22" fill="{c}" opacity=".15"/>
  <circle cx="145" cy="70" r="22" fill="{c}" opacity=".15"/>
  <circle cx="80" cy="42" r="17" fill="{c}" opacity=".13"/>
  <circle cx="120" cy="42" r="17" fill="{c}" opacity=".13"/>
  <!-- 中心爪垫 -->
  <ellipse cx="100" cy="118" rx="35" ry="26" fill="{c}" opacity=".22"/>
</svg>''',

        # ── 大爪印（空白装饰）───────────────────────────────
        "paw_bg": f'''<svg viewBox="0 0 100 90" width="80" height="72" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="50" cy="60" rx="28" ry="20" fill="{c}" opacity=".10"/>
  <circle cx="25" cy="32" r="12" fill="{c}" opacity=".08"/>
  <circle cx="75" cy="32" r="12" fill="{c}" opacity=".08"/>
  <circle cx="38" cy="18" r="9" fill="{c}" opacity=".07"/>
  <circle cx="62" cy="18" r="9" fill="{c}" opacity=".07"/>
</svg>''',

        # ── 对比图：容器内外 ─────────────────────────────────
        "container": f'''<svg viewBox="0 0 300 240" width="280" height="224" xmlns="http://www.w3.org/2000/svg">
  <!-- 容器边框 -->
  <rect x="20" y="20" width="260" height="200" rx="20" fill="rgba(194,113,79,0.08)" stroke="{c}" stroke-width="3" opacity=".6"/>
  <!-- 内部连接线 -->
  <path d="M80 120 L130 80" stroke="{c}" stroke-width="2" stroke-dasharray="6 4" opacity=".4"/>
  <path d="M80 120 L130 160" stroke="{c}" stroke-width="2" stroke-dasharray="6 4" opacity=".4"/>
  <path d="M170 80 L200 120" stroke="{c}" stroke-width="2" stroke-dasharray="6 4" opacity=".4"/>
  <!-- AI 大脑 -->
  <circle cx="80" cy="120" r="40" fill="{c}" opacity=".2" stroke="{c}" stroke-width="2.5"/>
  <circle cx="80" cy="120" r="28" fill="{c}" opacity=".3"/>
  <circle cx="80" cy="120" r="14" fill="{c}" opacity=".6"/>
  <!-- Harness -->
  <circle cx="130" cy="80" r="28" fill="{AMBER}" opacity=".2" stroke="{AMBER}" stroke-width="2"/>
  <circle cx="130" cy="80" r="16" fill="{AMBER}" opacity=".4"/>
  <!-- Sandbox -->
  <circle cx="130" cy="160" r="28" fill="{SAGE}" opacity=".2" stroke="{SAGE}" stroke-width="2"/>
  <rect x="118" y="148" width="24" height="24" rx="4" fill="{SAGE}" opacity=".35"/>
  <!-- Session -->
  <circle cx="200" cy="120" r="35" fill="{c}" opacity=".18" stroke="{c}" stroke-width="2"/>
  <rect x="182" y="108" width="36" height="8" rx="4" fill="{c}" opacity=".4"/>
  <rect x="182" y="120" width="28" height="8" rx="4" fill="{c}" opacity=".3"/>
  <rect x="182" y="132" width="32" height="8" rx="4" fill="{c}" opacity=".25"/>
</svg>''',

        # ── 延迟下降大图 ─────────────────────────────────────
        "latency_chart": f'''<svg viewBox="0 0 320 200" width="300" height="188" xmlns="http://www.w3.org/2000/svg">
  <!-- 基准线 -->
  <line x1="40" y1="160" x2="300" y2="160" stroke="{MUTED}" stroke-width="2" opacity=".4"/>
  <line x1="40" y1="100" x2="300" y2="100" stroke="{MUTED}" stroke-width="1" stroke-dasharray="6 4" opacity=".3"/>
  <line x1="40" y1="40" x2="300" y2="40" stroke="{MUTED}" stroke-width="1" stroke-dasharray="6 4" opacity=".3"/>
  <!-- P50 柱 -->
  <rect x="60" y="72" width="70" height="88" rx="8" fill="{TERRA}" opacity=".5"/>
  <rect x="60" y="72" width="70" height="88" rx="8" stroke="{TERRA}" stroke-width="2.5" fill="none" opacity=".8"/>
  <rect x="60" y="88" width="70" height="72" rx="8" fill="{TERRA}" opacity=".85"/>
  <!-- P95 柱 -->
  <rect x="175" y="28" width="70" height="132" rx="8" fill="{AMBER}" opacity=".5"/>
  <rect x="175" y="28" width="70" height="132" rx="8" stroke="{AMBER}" stroke-width="2.5" fill="none" opacity=".8"/>
  <rect x="175" y="50" width="70" height="110" rx="8" fill="{AMBER}" opacity=".85"/>
  <!-- 下降箭头 -->
  <path d="M200 50 L230 90" stroke="{BURNT}" stroke-width="4" stroke-linecap="round"/>
  <polygon points="230,85 238,95 222,93" fill="{BURNT}"/>
  <!-- 数字标注 -->
  <text x="95" y="65" font-family="Consolas" font-size="20" font-weight="bold" fill="{BONE}" text-anchor="middle" opacity=".95">↓60%</text>
  <text x="210" y="22" font-family="Consolas" font-size="20" font-weight="bold" fill="{BONE}" text-anchor="middle" opacity=".95">↓90%+</text>
  <!-- 标签 -->
  <text x="95" y="182" font-family="Consolas" font-size="14" fill="{MUTED}" text-anchor="middle">P50</text>
  <text x="210" y="182" font-family="Consolas" font-size="14" fill="{MUTED}" text-anchor="middle">P95</text>
</svg>''',

        # ── 流程图 ─────────────────────────────────────────
        "flow_steps": f'''<svg viewBox="0 0 360 260" width="340" height="245" xmlns="http://www.w3.org/2000/svg">
  <!-- 4个步骤框 -->
  <!-- 步骤1 -->
  <rect x="10" y="20" width="75" height="75" rx="14" fill="{c}" opacity=".12" stroke="{c}" stroke-width="2"/>
  <rect x="25" y="30" width="45" height="14" rx="4" fill="{c}" opacity=".4"/>
  <rect x="25" y="50" width="35" height="10" rx="4" fill="{c}" opacity=".25"/>
  <rect x="25" y="65" width="40" height="10" rx="4" fill="{c}" opacity=".2"/>
  <text x="47" y="112" font-family="Consolas" font-size="13" fill="{c}" text-anchor="middle" opacity=".8">持久化</text>
  <!-- 连接箭头1 -->
  <path d="M90 57 L110 57" stroke="{c}" stroke-width="3" stroke-dasharray="5 4" opacity=".5"/>
  <polygon points="108,52 118,57 108,62" fill="{c}" opacity=".5"/>
  <!-- 步骤2 -->
  <rect x="120" y="20" width="75" height="75" rx="14" fill="{TERRA}" opacity=".12" stroke="{TERRA}" stroke-width="2"/>
  <path d="M145 40 L165 40 M155 30 L155 50 M145 50 L165 50" stroke="{TERRA}" stroke-width="3" stroke-linecap="round" opacity=".7"/>
  <text x="157" y="112" font-family="Consolas" font-size="13" fill="{TERRA}" text-anchor="middle" opacity=".8">沙箱挂</text>
  <!-- 连接箭头2 -->
  <path d="M200 57 L220 57" stroke="{c}" stroke-width="3" stroke-dasharray="5 4" opacity=".5"/>
  <polygon points="218,52 228,57 218,62" fill="{c}" opacity=".5"/>
  <!-- 步骤3 -->
  <rect x="230" y="20" width="75" height="75" rx="14" fill="{AMBER}" opacity=".12" stroke="{AMBER}" stroke-width="2"/>
  <circle cx="267" cy="58" r="22" fill="{AMBER}" opacity=".2"/>
  <path d="M267 42 L267 58 L280 58" stroke="{AMBER}" stroke-width="3" stroke-linecap="round" opacity=".7"/>
  <circle cx="267" cy="58" r="5" fill="{AMBER}" opacity=".7"/>
  <text x="267" y="112" font-family="Consolas" font-size="13" fill="{AMBER}" text-anchor="middle" opacity=".8">重启</text>
  <!-- 连接箭头3 -->
  <path d="M90 155 L110 155" stroke="{c}" stroke-width="3" stroke-dasharray="5 4" opacity=".5"/>
  <polygon points="108,150 118,155 108,160" fill="{c}" opacity=".5"/>
  <!-- 步骤4 -->
  <rect x="120" y="118" width="75" height="75" rx="14" fill="{SAGE}" opacity=".12" stroke="{SAGE}" stroke-width="2"/>
  <path d="M145 138 Q157 130 170 138 Q182 146 195 138" stroke="{SAGE}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>
  <path d="M145 152 Q157 144 170 152 Q182 160 195 152" stroke="{SAGE}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".55"/>
  <text x="157" y="210" font-family="Consolas" font-size="13" fill="{SAGE}" text-anchor="middle" opacity=".8">零感知</text>
  <!-- 垂直连接 -->
  <path d="M157 98 L157 115" stroke="{c}" stroke-width="3" stroke-dasharray="5 4" opacity=".5"/>
  <polygon points="152,113 162,113 157,123" fill="{c}" opacity=".5"/>
</svg>''',

        # ── 进度时间线 ─────────────────────────────────────
        "timeline": f'''<svg viewBox="0 0 360 200" width="340" height="188" xmlns="http://www.w3.org/2000/svg">
  <!-- 主线 -->
  <line x1="30" y1="60" x2="330" y2="60" stroke="{c}" stroke-width="4" opacity=".5" stroke-linecap="round"/>
  <!-- 节点1 -->
  <circle cx="60" cy="60" r="18" fill="{c}" opacity=".3" stroke="{c}" stroke-width="2.5"/>
  <circle cx="60" cy="60" r="10" fill="{c}" opacity=".7"/>
  <text x="60" y="98" font-family="Consolas" font-size="14" fill="{c}" text-anchor="middle" opacity=".85">初创公司</text>
  <rect x="30" y="110" width="60" height="28" rx="8" fill="{c}" opacity=".12"/>
  <rect x="35" y="117" width="50" height="6" rx="3" fill="{c}" opacity=".4"/>
  <rect x="35" y="127" width="35" height="6" rx="3" fill="{c}" opacity=".25"/>
  <!-- 节点2 -->
  <circle cx="180" cy="60" r="18" fill="{AMBER}" opacity=".3" stroke="{AMBER}" stroke-width="2.5"/>
  <circle cx="180" cy="60" r="10" fill="{AMBER}" opacity=".7"/>
  <text x="180" y="98" font-family="Consolas" font-size="14" fill="{AMBER}" text-anchor="middle" opacity=".85">云厂商</text>
  <rect x="150" y="110" width="60" height="28" rx="8" fill="{AMBER}" opacity=".12"/>
  <rect x="155" y="117" width="50" height="6" rx="3" fill="{AMBER}" opacity=".4"/>
  <rect x="155" y="127" width="38" height="6" rx="3" fill="{AMBER}" opacity=".25"/>
  <!-- 节点3 -->
  <circle cx="300" cy="60" r="18" fill="{SAGE}" opacity=".3" stroke="{SAGE}" stroke-width="2.5"/>
  <circle cx="300" cy="60" r="10" fill="{SAGE}" opacity=".7"/>
  <text x="300" y="98" font-family="Consolas" font-size="14" fill="{SAGE}" text-anchor="middle" opacity=".85">平台托管</text>
  <rect x="270" y="110" width="60" height="28" rx="8" fill="{SAGE}" opacity=".12"/>
  <rect x="275" y="117" width="50" height="6" rx="3" fill="{SAGE}" opacity=".4"/>
  <rect x="275" y="127" width="42" height="6" rx="3" fill="{SAGE}" opacity=".25"/>
  <!-- 阶段箭头 -->
  <path d="M78 60 L162 60" stroke="{c}" stroke-width="3" stroke-dasharray="6 4" opacity=".4"/>
  <path d="M198 60 L282 60" stroke="{c}" stroke-width="3" stroke-dasharray="6 4" opacity=".4"/>
</svg>''',

        # ── 分层饼图（OS比喻）───────────────────────────────
        "os_layers": f'''<svg viewBox="0 0 280 280" width="260" height="260" xmlns="http://www.w3.org/2000/svg">
  <!-- 外圈：工具/外设 -->
  <circle cx="140" cy="140" r="130" fill="{SAGE}" opacity=".10" stroke="{SAGE}" stroke-width="2"/>
  <!-- 中圈：平台 -->
  <circle cx="140" cy="140" r="95" fill="{AMBER}" opacity=".12" stroke="{AMBER}" stroke-width="2"/>
  <!-- 内圈：模型 -->
  <circle cx="140" cy="140" r="60" fill="{c}" opacity=".18" stroke="{c}" stroke-width="2.5"/>
  <circle cx="140" cy="140" r="36" fill="{c}" opacity=".3"/>
  <circle cx="140" cy="140" r="18" fill="{c}" opacity=".6"/>
  <!-- 标签 -->
  <text x="140" y="136" font-family="Consolas" font-size="13" font-weight="bold" fill="{BONE}" text-anchor="middle" opacity=".9">CPU</text>
  <text x="140" y="152" font-family="Consolas" font-size="11" fill="{BONE}" text-anchor="middle" opacity=".7">模型</text>
  <text x="240" y="140" font-family="Consolas" font-size="13" fill="{AMBER}" opacity=".85">平台</text>
  <text x="45" y="230" font-family="Consolas" font-size="13" fill="{SAGE}" opacity=".85">工具</text>
  <!-- 连接线 -->
  <line x1="200" y1="140" x2="238" y2="140" stroke="{AMBER}" stroke-width="2" stroke-dasharray="5 4" opacity=".5"/>
  <line x1="140" y1="200" x2="80" y2="228" stroke="{SAGE}" stroke-width="2" stroke-dasharray="5 4" opacity=".5"/>
</svg>''',

        # ── 小图标：警告 ────────────────────────────────────
        "icon_warn": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <path d="M32 8L4 56h56L32 8z" fill="{TERRA}" opacity=".75"/>
  <rect x="29" y="22" width="6" height="18" rx="3" fill="{BG}" opacity=".8"/>
  <circle cx="32" cy="46" r="3.5" fill="{BG}" opacity=".8"/>
</svg>''',

        # ── 小图标：勾选 ────────────────────────────────────
        "icon_check": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="32" r="26" fill="{SAGE}" opacity=".15" stroke="{SAGE}" stroke-width="3"/>
  <path d="M20 32l9 9 15-18" stroke="{SAGE}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',

        # ── 小图标：箭头 ────────────────────────────────────
        "icon_arrow": f'''<svg viewBox="0 0 64 64" width="36" height="36" xmlns="http://www.w3.org/2000/svg">
  <path d="M10 32h44M42 18l14 14-14 14" stroke="{c}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>''',

        # ── 小图标：服务器 ─────────────────────────────────
        "icon_server": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <rect x="8" y="10" width="48" height="14" rx="4" fill="{AMBER}" opacity=".7"/>
  <rect x="8" y="30" width="48" height="14" rx="4" fill="{AMBER}" opacity=".85"/>
  <rect x="8" y="50" width="48" height="14" rx="4" fill="{AMBER}" opacity=".55"/>
  <circle cx="20" cy="17" r="3.5" fill="{BG}" opacity=".7"/>
  <circle cx="20" cy="37" r="3.5" fill="{BG}" opacity=".7"/>
  <circle cx="20" cy="57" r="3.5" fill="{BG}" opacity=".7"/>
</svg>''',

        # ── 小图标：拼图 ────────────────────────────────────
        "icon_puzzle": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <path d="M20 6h24a9 9 0 0 1 0 18H20V6z" fill="{c}" opacity=".85"/>
  <path d="M6 22h16v24H6V22z" fill="{c}" opacity=".7"/>
  <path d="M24 52h16a9 9 0 0 1 0 18H24V52z" fill="{c}" opacity=".7"/>
</svg>''',

        # ── 小图标：锁 ──────────────────────────────────────
        "icon_lock": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <rect x="12" y="28" width="40" height="28" rx="6" fill="{c}" opacity=".85"/>
  <path d="M20 28V20a12 12 0 0 1 24 0v8" stroke="{c}" stroke-width="4" fill="none" stroke-linecap="round"/>
  <circle cx="32" cy="42" r="5" fill="{BG}" opacity=".8"/>
</svg>''',

        # ── 小图标：护盾 ────────────────────────────────────
        "icon_shield": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <path d="M32 6L8 16v20c0 14.4 10.24 27.84 24 31 13.76-3.16 24-16.6 24-31V16L32 6z" fill="{SAGE}" opacity=".8"/>
  <path d="M22 32l7 7 13-14" stroke="{BG}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>''',

        # ── 小图标：扩展 ────────────────────────────────────
        "icon_expand": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <path d="M8 22V8h14M56 22V8H42M8 42v14h14M56 42v14H42" stroke="{c}" stroke-width="4.5" stroke-linecap="round"/>
</svg>''',

        # ── 小图标：奖杯 ────────────────────────────────────
        "icon_trophy": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <path d="M20 8h24v24c0 8.84-5.37 16-12 16s-12-7.16-12-16V8z" fill="{GOLD}" opacity=".9"/>
  <path d="M20 16H8v8c0 6 4 10 12 10M44 16h12v8c0 6-4 10-12 10" stroke="{GOLD}" stroke-width="3" fill="none" opacity=".75"/>
  <rect x="28" y="48" width="8" height="8" fill="{GOLD}" opacity=".9"/>
  <rect x="20" y="54" width="24" height="4" rx="2" fill="{GOLD}" opacity=".8"/>
</svg>''',

        # ── 小图标：CPU ─────────────────────────────────────
        "icon_cpu": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="16" width="32" height="32" rx="6" fill="{c}" opacity=".8"/>
  <path d="M24 8v8M40 8v8M24 48v8M40 48v8M8 24h8M8 40h8M48 24h8M48 40h8" stroke="{c}" stroke-width="3" stroke-linecap="round" opacity=".6"/>
  <rect x="24" y="24" width="16" height="16" rx="2" fill="{BG}" opacity=".5"/>
</svg>''',

        # ── 小图标：链 ──────────────────────────────────────
        "icon_chain": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <path d="M20 14h-4V10a12 12 0 0 1 24 0v4h-4" stroke="{c}" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M20 50h-4v4a12 12 0 0 1 24 0v-4h-4" stroke="{c}" stroke-width="4" fill="none" stroke-linecap="round"/>
  <line x1="20" y1="18" x2="20" y2="46" stroke="{c}" stroke-width="4" stroke-linecap="round"/>
</svg>''',

        # ── 小图标：钟 ──────────────────────────────────────
        "icon_clock": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="32" r="26" stroke="{c}" stroke-width="4" opacity=".8"/>
  <path d="M32 18v16l10 10" stroke="{c}" stroke-width="4" stroke-linecap="round"/>
</svg>''',

        # ── 小图标：爪印 ────────────────────────────────────
        "icon_paw": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="32" cy="42" rx="14" ry="10" fill="{c}" opacity=".75"/>
  <circle cx="18" cy="26" r="7" fill="{c}" opacity=".65"/>
  <circle cx="46" cy="26" r="7" fill="{c}" opacity=".65"/>
  <circle cx="26" cy="16" r="5.5" fill="{c}" opacity=".58"/>
  <circle cx="38" cy="16" r="5.5" fill="{c}" opacity=".58"/>
</svg>''',

        # ── 小图标：云 ──────────────────────────────────────
        "icon_cloud": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <path d="M48 36a12 12 0 0 0-12-12 12 12 0 0 0-22.4-4A10 10 0 1 0 14 50h34a10 10 0 0 0 0-14z" fill="{c}" opacity=".8"/>
</svg>''',

        # ── 小图标：齿轮 ────────────────────────────────────
        "icon_gear": f'''<svg viewBox="0 0 64 64" width="44" height="44" xmlns="http://www.w3.org/2000/svg">
  <circle cx="32" cy="32" r="12" fill="{c}" opacity=".9"/>
  <path d="M32 4v7M32 53v7M4 32h7M53 32h7M10.8 10.8l5 5M48.2 48.2l5 5M53.2 10.8l-5 5M15.8 48.2l-5 5" stroke="{c}" stroke-width="5" stroke-linecap="round" opacity=".65"/>
</svg>''',

    }
    return LIB.get(name, LIB.get("paw_bg"))


# ============================================================
# 幻灯数据
# ============================================================
SLIDES = [
    # ── 0 封面 ─────────────────────────────────────────────
    {
        "id": 0, "start": 0, "end": 7,
        "type": "cover",
        "tag": "豆包AI播客",
        "headline": "Agent\n是宠物\n还是牲口？",
        "sub": "Anthropic 把 AI 从精心呵护的宠物\n变成了随时可替换的打工仔",
    },
    # ── 1 PART I ──────────────────────────────────────────
    {
        "id": 1, "start": 7, "end": 15,
        "type": "section",
        "tag": "PART I",
        "title": "架构的转变",
        "icon": "icon_paw",
    },
    # ── 2 单体困境（大图+网格）──────────────────────────────
    {
        "id": 2, "start": 15, "end": 36,
        "type": "dense_grid",
        "tag": "PART I · 旧架构",
        "title": "单体的困境",
        "icon": "icon_warn",
        "icon_svg": "container",
        "items": [
            ("容器挂了", "所有状态全失\n任务重来", TERRA),
            ("调试困难", "排查问题\n牵一发而动全身", TERRA),
            ("扩展受限", "模型升级\n牵动 Harness 全局", TERRA),
            ("安全集中", "风险都集中在\n一个容器内", TERRA),
        ],
    },
    # ── 3 养宠物（大狗插图）────────────────────────────────
    {
        "id": 3, "start": 36, "end": 51,
        "type": "hero_illustration",
        "tag": "PART I · 核心问题",
        "title": "这个架构\n就像养了一只宠物",
        "icon_svg": "dog_main",
        "accent_color": AMBER,
        "sub": "精心呵护 · 不可替换 · 全局耦合",
        "badge": "🐶 PET",
    },
    # ── 4 三层分离（大架构图）───────────────────────────────
    {
        "id": 4, "start": 51, "end": 67,
        "type": "arch_hero",
        "tag": "PART I · 新架构",
        "title": "三层分离",
        "icon_svg": "arch_3layer",
    },
    # ── 5 各层职责（图标+描述）─────────────────────────────
    {
        "id": 5, "start": 67, "end": 82,
        "type": "dense_grid",
        "tag": "PART I · 优势",
        "title": "各层职责清晰",
        "icon": "icon_check",
        "icon_svg": None,
        "items": [
            ("Session", "可随时 replay\n任意步骤", SAGE),
            ("Harness", "多模型适配\n无状态扩容", AMBER),
            ("Sandbox", "沙箱隔离\n错误不外溢", TERRA),
            ("接口通信", "层间稳定接口\n系统灵活可靠", MUTED),
        ],
    },
    # ── 6 宠物→牲口（对比图）───────────────────────────────
    {
        "id": 6, "start": 82, "end": 96,
        "type": "contrast_animals",
        "tag": "PART I · 小结",
        "title": "从宠物变打工仔",
        "left_svg": "dog_main",
        "right_svg": "cattle_main",
    },
    # ── 7 PART II ─────────────────────────────────────────
    {
        "id": 7, "start": 96, "end": 113,
        "type": "section",
        "tag": "PART II",
        "title": "变革带来的成效",
        "icon": "icon_trophy",
    },
    # ── 8 延迟下降（柱状图）───────────────────────────────
    {
        "id": 8, "start": 113, "end": 148,
        "type": "stats_chart",
        "tag": "PART II · 延迟",
        "title": "推理提前启动",
        "body": "脑手分离之后\nAgent 不需要等沙箱完全起来\n才开始干活",
        "icon_svg": "latency_chart",
        "numbers": [
            ("P50", "↓60%", "首 Token 延迟"),
            ("P95", "↓90%+", "尾部延迟"),
        ],
    },
    # ── 9 故障恢复（流程图）───────────────────────────────
    {
        "id": 9, "start": 148, "end": 183,
        "type": "flow_diagram",
        "tag": "PART II · 弹性",
        "title": "故障自动恢复",
        "icon_svg": "flow_steps",
        "steps": [
            ("会话状态", "持久化存储", SAGE),
            ("沙箱挂了", "自动重启", TERRA),
            ("新实例启动", "无缝恢复", AMBER),
            ("业务层面", "零感知", MUTED),
        ],
    },
    # ── 10 安全 ──────────────────────────────────────────
    {
        "id": 10, "start": 183, "end": 222,
        "type": "security_split",
        "tag": "PART II · 安全",
        "title": "安全边界重塑",
        "left_color": TERRA,
        "right_color": SAGE,
        "left_items": [
            ("风险集中", "被攻破即泄露"),
            ("凭证内置", "沙箱内明文"),
        ],
        "right_items": [
            ("加密挂载", "凭证移出沙箱"),
            ("代理访问", "隔离保护"),
        ],
    },
    # ── 11 可观测 ────────────────────────────────────────
    {
        "id": 11, "start": 222, "end": 261,
        "type": "dense_grid",
        "tag": "PART II · 可观测",
        "title": "中间件 + 多Agent",
        "icon": "icon_server",
        "icon_svg": None,
        "items": [
            ("中间件", "做观测和流控", AMBER),
            ("多 Agent 协作", "标准接口支撑", SAGE),
            ("管理平台", "权限控制和审计", MUTED),
            ("可维护", "组件可替换", TERRA),
        ],
    },
    # ── 12 PART III ───────────────────────────────────────
    {
        "id": 12, "start": 261, "end": 333,
        "type": "section",
        "tag": "PART III",
        "title": "发展方向",
        "icon": "icon_expand",
    },
    # ── 13 各自造轮子（痛点）──────────────────────────────
    {
        "id": 13, "start": 333, "end": 370,
        "type": "pain_points",
        "tag": "PART III · 过去",
        "title": "各自造轮子",
        "icon": "icon_warn",
        "items": [
            ("自己搞编排", TERRA),
            ("自己搞沙箱", TERRA),
            ("自己搞会话管理", TERRA),
        ],
        "sub": "什么都要自己来，非常费劲",
    },
    # ── 14 时间线（标准化）───────────────────────────────
    {
        "id": 14, "start": 370, "end": 410,
        "type": "timeline_viz",
        "tag": "PART III · 现在",
        "title": "标准化与平台化",
        "icon_svg": "timeline",
    },
    # ── 15 资源 ─────────────────────────────────────────
    {
        "id": 15, "start": 410, "end": 450,
        "type": "resources_hero",
        "tag": "PART III · 平台化",
        "title": "一切皆为资源",
        "subtitle": "Cloud Managed Agents",
        "icon_svg": "os_layers",
        "resources": [
            ("Agent", "可组合的\n能力单元", TERRA),
            ("Environment", "可替换的\n执行环境", AMBER),
            ("Session", "可管理的\n会话状态", SAGE),
        ],
    },
    # ── 16 AI Native OS 比喻 ────────────────────────────
    {
        "id": 16, "start": 450, "end": 485,
        "type": "metaphor_viz",
        "tag": "PART III · 未来",
        "title": "模块化分层架构",
        "body": "模型只是大脑\n通过稳定接口连接各种\n可替换的执行环境和工具",
        "icon_svg": "os_layers",
        "metaphor": "🐾 AI Native OS",
        "layers": ["模型 = CPU", "工具 = 外设", "平台 = 操作系统"],
    },
    # ── 17 多Agent协作 ─────────────────────────────────
    {
        "id": 17, "start": 485, "end": 520,
        "type": "dense_grid",
        "tag": "PART III · 趋势",
        "title": "多Agent协作",
        "icon": "icon_puzzle",
        "icon_svg": None,
        "items": [
            ("行业标准", "接口统一 · 生态繁荣", SAGE),
            ("工具生态", "专业分工 · 各司其职", AMBER),
            ("创新重心", "向应用层迁移", MUTED),
            ("未来展望", "AI Native 新范式", TERRA),
        ],
    },
    # ── 18 结尾 ─────────────────────────────────────────
    {
        "id": 18, "start": 520, "end": 545,
        "type": "ending",
        "tag": "尾声",
        "title": "架构升级的必然结果",
        "body": "Agent 从宠物变成打工仔\n是 AI 行业逐渐走向成熟的标志",
        "icon_svg": "paw_hero",
    },
    # ── 19 最终页 ────────────────────────────────────────
    {
        "id": 19, "start": 545, "end": 565,
        "type": "end",
        "headline": "感谢收听\n下期再见",
    },
]

# ============================================================
# CSS
# ============================================================
def css():
    return """<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
    font-family: 'Microsoft YaHei UI', 'PingFang SC', 'Microsoft YaHei',
                 'Source Han Sans CN', sans-serif;
    background: #120c08; color: #f5e6d3; overflow-x: hidden;
}
.slides {
    width: 100vw; height: 100vh;
    overflow-y: scroll; scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}
.slide {
    width: 100vw; height: 100vh; min-height: 100vh;
    scroll-snap-align: start;
    display: flex; flex-direction: column;
    justify-content: flex-start; align-items: center;
    padding: 0; position: relative; overflow: hidden;
}
.slide-inner {
    width: 100%; height: 100%;
    display: flex; flex-direction: column;
    padding: 64px 52px 52px;
    position: relative; z-index: 1;
}
.slide::before {
    content: ''; position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 50% 20%,
            rgba(212,168,67,0.12) 0%,
            rgba(194,113,79,0.07) 40%,
            transparent 70%),
        radial-gradient(ellipse 50% 40% at 85% 85%,
            rgba(212,168,67,0.06) 0%,
            transparent 60%);
    pointer-events: none; z-index: 0;
}
.slide-inner { position: relative; z-index: 1; }

#progress { position: fixed; top: 0; left: 0; height: 3px; width: 0%;
    background: linear-gradient(90deg, #c2714f, #d4a843); z-index: 999; transition: width .3s; }
#dots { position: fixed; right: 18px; top: 50%; transform: translateY(-50%);
    display: flex; flex-direction: column; gap: 7px; z-index: 999; }
.dot { width: 5px; height: 5px; border-radius: 50%;
    background: rgba(212,168,67,.28); cursor: pointer; transition: all .3s; }
.dot.active { background: #d4a843; box-shadow: 0 0 8px rgba(212,168,67,.8); transform: scale(1.7); }

.tag { font-size: 12px; font-weight: 700; letter-spacing: 6px;
    color: #d4a843; text-transform: uppercase; opacity: .85;
    margin-bottom: 10px; }
.title { font-size: clamp(36px, 5vw, 60px); font-weight: 900;
    line-height: 1.15; color: #f5e6d3; letter-spacing: 1px;
    text-shadow: 0 0 30px rgba(212,168,67,.18);
    margin-bottom: 0; }
.body-text { font-size: clamp(20px, 2.5vw, 30px); line-height: 1.7;
    color: rgba(245,230,211,.72); text-align: center;
    margin-top: 18px; white-space: pre-line; }
.top-bar { position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #d4a843 30%, #c2714f 70%, transparent); }
.timestamp { position: absolute; bottom: 20px; right: 32px;
    font-family: 'Consolas','Courier New',monospace; font-size: 10px;
    color: rgba(140,122,106,.35); letter-spacing: 1px; }
.page-num { position: absolute; bottom: 20px; left: 32px;
    font-family: 'Consolas','Courier New',monospace; font-size: 10px;
    color: rgba(140,122,106,.35); letter-spacing: 1px; }

/* ─── 封面 ─── */
.cover-bg { position: absolute; inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 25%,
        rgba(212,168,67,.14) 0%, rgba(194,113,79,.07) 40%, transparent 70%),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(194,113,79,.08) 0%, transparent 60%), #120c08; }
.cover-glow { position: absolute; width: 600px; height: 600px; top: 45%; left: 50%;
    transform: translate(-50%, -55%);
    background: radial-gradient(ellipse, rgba(212,168,67,.18) 0%, transparent 70%); pointer-events: none; }
.cover-paw { position: absolute; right: -20px; bottom: 40px;
    opacity: .12; transform: rotate(-20deg); }
.cover-eyebrow { font-size: 13px; letter-spacing: 8px;
    color: rgba(212,168,67,.65); font-weight: 500; text-transform: uppercase; margin-bottom: 20px; }
.cover-headline { font-size: clamp(64px, 9.5vw, 108px); font-weight: 900;
    line-height: 1.0; text-align: center; color: #f5e6d3; letter-spacing: 4px;
    text-shadow: 0 0 70px rgba(212,168,67,.28); white-space: pre-line; }
.cover-sub { font-size: clamp(17px, 2vw, 24px);
    color: rgba(245,230,211,.58); text-align: center; margin-top: 24px;
    line-height: 1.85; white-space: pre-line; }
.cover-bottom { position: absolute; bottom: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #c2714f, #d4a843, #7d9c6c); }

/* ─── 章节页 ─── */
.section-icon { width: 80px; height: 80px; margin-bottom: 16px; }
.section-icon svg { width: 80px; height: 80px; }
.section-title { font-size: clamp(48px, 6.5vw, 80px); font-weight: 900;
    color: #f5e6d3; text-align: center; letter-spacing: 2px;
    text-shadow: 0 0 40px rgba(212,168,67,.22); margin-top: 12px; }

/* ─── 密集网格 ─── */
.dense-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; flex: 1; margin-top: 18px; }
.grid-card { padding: 22px 18px; border-radius: 16px;
    background: rgba(245,230,211,.04); border: 1px solid rgba(245,230,211,.08);
    display: flex; flex-direction: column; gap: 8px; }
.grid-card-icon { width: 42px; height: 42px; }
.grid-card-icon svg { width: 42px; height: 42px; }
.grid-card h3 { font-size: clamp(18px, 2vw, 24px); font-weight: 700; }
.grid-card p { font-size: clamp(13px, 1.3vw, 16px);
    color: rgba(245,230,211,.6); line-height: 1.55; white-space: pre-line; flex: 1; }

/* ─── 英雄插图页 ─── */
.hero-wrap { display: flex; align-items: center; gap: 24px; flex: 1; margin-top: 16px; }
.hero-illust { flex-shrink: 0; max-width: 42%; }
.hero-illust svg { max-width: 100%; height: auto; }
.hero-text { flex: 1; display: flex; flex-direction: column; gap: 14px; }
.hero-badge { display: inline-block; padding: 6px 18px; border-radius: 100px;
    font-size: 13px; font-weight: 700; letter-spacing: 3px;
    border: 1.5px solid; opacity: .85; }
.hero-sub { font-size: clamp(16px, 1.8vw, 22px); color: rgba(245,230,211,.55);
    letter-spacing: 3px; margin-top: 6px; }
.hero-stats { display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }
.hero-stat { display: flex; align-items: center; gap: 14px; padding: 14px 18px;
    border-radius: 12px; background: rgba(245,230,211,.04);
    border-left: 4px solid; }
.hero-stat-label { font-size: clamp(13px,1.3vw,16px); font-weight: 700; }
.hero-stat-desc { font-size: clamp(12px,1.2vw,15px); color: rgba(245,230,211,.6); margin-top: 2px; }

/* ─── 架构英雄 ─── */
.arch-wrap { flex: 1; display: flex; flex-direction: column; gap: 16px; margin-top: 14px; }
.arch-svg { text-align: center; }
.arch-svg svg { max-width: 100%; height: auto; }
.arch-layers { display: flex; flex-direction: column; gap: 12px; }
.arch-layer { display: grid; grid-template-columns: 140px 1fr; align-items: center; gap: 18px;
    padding: 18px 22px; border-radius: 14px; border-left: 5px solid; }
.arch-layer-name { font-size: clamp(18px,2vw,24px); font-weight: 800; letter-spacing: 2px; }
.arch-layer-role { font-size: 12px; opacity: .6; letter-spacing: 2px; margin-top: 2px; }
.arch-layer-desc { font-size: clamp(14px,1.4vw,17px);
    color: rgba(245,230,211,.8); line-height: 1.6; white-space: pre-line; }

/* ─── 动物对比 ─── */
.contrast-animals { display: grid; grid-template-columns: 1fr auto 1fr;
    gap: 20px; align-items: center; flex: 1; margin-top: 14px; }
.animal-col { text-align: center; }
.animal-svg { max-width: 100%; height: auto; margin: 0 auto; }
.animal-label { font-size: clamp(24px,3vw,38px); font-weight: 900; margin-top: 10px; }
.animal-desc { font-size: clamp(14px,1.4vw,17px); color: rgba(245,230,211,.55); margin-top: 6px; }
.contrast-arrow { width: 48px; height: 48px; flex-shrink: 0; }
.contrast-arrow svg { width: 48px; height: 48px; }

/* ─── 图表统计 ─── */
.stats-wrap { display: flex; align-items: center; gap: 24px; flex: 1; margin-top: 14px; }
.stats-chart { flex: 1; }
.stats-chart svg { max-width: 100%; height: auto; }
.stats-nums { display: flex; flex-direction: column; gap: 14px; flex: 1; }
.stat-card { padding: 20px 22px; border-radius: 16px; border: 1.5px solid; text-align: center; }
.stat-val { font-family: 'Consolas','Courier New',monospace;
    font-size: clamp(40px,5vw,64px); font-weight: 900; line-height: 1; }
.stat-label { font-size: clamp(12px,1.3vw,16px); opacity: .7; margin-top: 8px; letter-spacing: 1px; }

/* ─── 流程图 ─── */
.flow-wrap { display: flex; align-items: center; gap: 24px; flex: 1; margin-top: 14px; }
.flow-svg { flex: 1.2; }
.flow-svg svg { max-width: 100%; height: auto; }
.flow-items { display: flex; flex-direction: column; gap: 12px; flex: 0.8; }
.flow-item { display: flex; align-items: center; gap: 14px;
    padding: 14px 18px; border-radius: 12px; border: 1.5px solid; }
.flow-dot { min-width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.flow-item-title { font-size: clamp(15px,1.6vw,19px); font-weight: 700; }
.flow-item-desc { font-size: clamp(12px,1.2vw,15px); color: rgba(245,230,211,.6); margin-top: 2px; }

/* ─── 安全分割 ─── */
.security-wrap { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; flex: 1; margin-top: 18px; }
.sec-col { padding: 24px 20px; border-radius: 18px; border: 1.5px solid; }
.sec-col-title { font-size: clamp(16px,1.8vw,22px); font-weight: 700; margin-bottom: 16px; }
.sec-item { font-size: clamp(14px,1.4vw,17px); padding: 7px 0; opacity: .85; display: flex; align-items: center; gap: 8px; }
.sec-arrow { text-align: center; display: flex; align-items: center; justify-content: center; }

/* ─── 痛点 ─── */
.pain-wrap { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; flex: 1; margin-top: 18px; }
.pain-items-col { display: flex; flex-direction: column; gap: 12px; }
.pain-item { display: flex; align-items: center; gap: 14px;
    padding: 16px 20px; border-radius: 14px;
    background: rgba(194,113,79,.08); border: 1px solid rgba(194,113,79,.2); }
.pain-num { font-family: 'Consolas','Courier New',monospace;
    font-size: 28px; font-weight: 900; color: rgba(194,113,79,.5);
    min-width: 40px; }
.pain-text { font-size: clamp(17px,1.9vw,24px); font-weight: 700; color: #c2714f; }
.pain-illust { display: flex; align-items: center; justify-content: center; }
.pain-illust svg { max-width: 100%; height: auto; }

/* ─── 时间线可视化 ─── */
.timeline-wrap { flex: 1; margin-top: 14px; display: flex; flex-direction: column; gap: 20px; }
.timeline-svg { text-align: center; }
.timeline-svg svg { max-width: 100%; height: auto; }
.timeline-captions { display: flex; gap: 12px; }
.timeline-cap { flex: 1; text-align: center; padding: 12px 14px;
    border-radius: 12px; border: 1px solid rgba(212,168,67,.15);
    background: rgba(212,168,67,.05); }
.cap-title { font-size: clamp(13px,1.4vw,17px); font-weight: 700; margin-bottom: 4px; }
.cap-desc { font-size: clamp(11px,1.1vw,14px); color: rgba(245,230,211,.55); }

/* ─── 资源英雄 ─── */
.resources-wrap { display: flex; align-items: center; gap: 24px; flex: 1; margin-top: 14px; }
.resources-svg { flex: 1; }
.resources-svg svg { max-width: 100%; height: auto; }
.resources-list { flex: 1; display: flex; flex-direction: column; gap: 14px; }
.res-item { padding: 16px 20px; border-radius: 14px; border-left: 5px solid;
    background: rgba(245,230,211,.04); border-top: 1px solid rgba(245,230,211,.06);
    border-right: 1px solid rgba(245,230,211,.06); border-bottom: 1px solid rgba(245,230,211,.06); }
.res-name { font-size: clamp(18px,2vw,24px); font-weight: 800; margin-bottom: 4px; }
.res-desc { font-size: clamp(13px,1.3vw,16px); color: rgba(245,230,211,.6); white-space: pre-line; }

/* ─── OS 比喻可视化 ─── */
.metaphor-wrap { display: flex; align-items: center; gap: 24px; flex: 1; margin-top: 14px; }
.metaphor-svg { flex: 1; }
.metaphor-svg svg { max-width: 100%; height: auto; }
.metaphor-text { flex: 1; display: flex; flex-direction: column; gap: 14px; }
.met-badge { display: inline-block; padding: 8px 20px; border-radius: 100px;
    font-size: clamp(18px,2vw,26px); font-weight: 900;
    background: rgba(212,168,67,.12); border: 1.5px solid rgba(212,168,67,.4);
    color: #d4a843; text-align: center; }
.met-layers { display: flex; flex-direction: column; gap: 10px; }
.met-layer { padding: 12px 18px; border-radius: 12px; font-size: clamp(15px,1.6vw,19px);
    font-weight: 700; text-align: center; border: 1px solid; opacity: .85; }

/* ─── 结尾 ─── */
.ending-wrap { text-align: center; flex: 1; display: flex;
    flex-direction: column; align-items: center; justify-content: center; gap: 20px; margin-top: 14px; }
.ending-title { font-size: clamp(32px,4vw,54px); font-weight: 900;
    color: #f5e6d3; text-shadow: 0 0 40px rgba(212,168,67,.25); }
.ending-body { font-size: clamp(22px,2.8vw,38px); font-weight: 700;
    color: #d4a843; line-height: 1.7; white-space: pre-line; }
.ending-paw { margin-top: 8px; opacity: .18; }

/* ─── 最终页 ─── */
.end-title { font-size: clamp(60px,8.5vw,110px); font-weight: 900;
    text-align: center; line-height: 1.1;
    background: linear-gradient(135deg, #c2714f, #d4a843);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: 4px; white-space: pre-line;
    filter: drop-shadow(0 0 40px rgba(212,168,67,.4)); }

/* ─── 动画 ─── */
.slide-inner > * { opacity: 0; transform: translateY(16px);
    transition: opacity .45s ease, transform .45s ease; }
.slide.visible .slide-inner > * { opacity: 1; transform: translateY(0); }
.slide-inner > *:nth-child(1) { transition-delay: .04s; }
.slide-inner > *:nth-child(2) { transition-delay: .10s; }
.slide-inner > *:nth-child(3) { transition-delay: .16s; }
.slide-inner > *:nth-child(4) { transition-delay: .22s; }
.slide-inner > *:nth-child(5) { transition-delay: .28s; }
</style>"""


# ============================================================
# 幻灯 HTML 生成
# ============================================================
def ha(tag, cls, content=""):
    return f'<div class="{cls}">{content}</div>'

def ha_svg(name):
    return illust(name)

def slide_html(s):
    t = s["type"]
    sid = s["id"]
    total = len(SLIDES)
    ts = ha("tag", "tag", s.get("tag",""))
    tt = ha("title", "title", s.get("title",""))
    pt = f'<div class="page-num">{sid+1}/{total}</div>'
    tst = f'<div class="timestamp">{s["start"]}s–{s["end"]}s</div>'
    inner = "".join([x for x in [ts, tt] if x])

    # ── 封面 ──────────────────────────────────────────────
    if t == "cover":
        return f'''<div class="slide" id="s{sid}">
  <div class="top-bar"></div>
  <div class="cover-bg"></div>
  <div class="cover-glow"></div>
  <div class="cover-paw">{ha_svg("paw_bg")}</div>
  <div class="slide-inner" style="justify-content:center;align-items:center;text-align:center">
    <div class="cover-eyebrow">{s["tag"]}</div>
    <div class="cover-headline">{s["headline"]}</div>
    <div class="cover-sub">{s["sub"]}</div>
  </div>
  <div class="cover-bottom"></div>
  {pt}{tst}
</div>'''

    # ── 章节 ──────────────────────────────────────────────
    if t == "section":
        return f'''<div class="slide" id="s{sid}">
  <div class="top-bar"></div>
  <div class="slide-inner" style="justify-content:center;align-items:center;text-align:center">
    {ts}
    <div class="section-icon">{ha_svg(s.get("icon","icon_paw"))}</div>
    <div class="section-title">{s["title"]}</div>
  </div>
  {pt}{tst}
</div>'''

    # ── 密集网格 ───────────────────────────────────────────
    if t == "dense_grid":
        icon_svg = ha_svg(s.get("icon","icon_check")) if not s.get("icon_svg") else ""
        cards = ""
        for i, item in enumerate(s["items"]):
            title, desc, color = item
            cards += f'''<div class="grid-card">
  <div class="grid-card-icon" style="color:{color}">{icon_svg}</div>
  <h3 style="color:{color}">{title}</h3>
  <p>{desc}</p>
</div>'''
        # 左图右网格或全网格
        extra = ""
        if s.get("icon_svg"):
            extra = f'<div style="grid-column:1/-1;display:flex;justify-content:center;margin-bottom:8px">{ha_svg(s["icon_svg"])}</div>'
        return f'''<div class="slide" id="s{sid}">
  <div class="top-bar"></div>
  <div class="slide-inner">
    {ts}{tt}
    <div class="dense-grid">{extra}{cards}</div>
  </div>
  {pt}{tst}
</div>'''

    # ── 英雄插图页 ─────────────────────────────────────────
    if t == "hero_illustration":
        color = s.get("accent_color", AMBER)
        badge = ha("badge", "hero-badge", s.get("badge",""))
        badge_html = f