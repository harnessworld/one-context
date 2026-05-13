# Design: Claude Code 沙箱与并发安全 — 双层色调方案

## Overview

为视频 `claudecode-sandbox-concurrency-mid-video` 制作两套 HTML 幻灯片（Open-Design 风格），用于视频分镜配图。每页一张内嵌精简源码的 SVG 技术流程图。

## Content (8 pages)

| Page | Topic | Key Visual |
|------|-------|-----------|
| 1 | Cover — 5 层安全架构概览 | 横向串联流水线 / 垂直堆叠滤网（Agent 自选） |
| 2 | Python REPL 沙箱 — 黑名单 | `__builtins__.__import__` 替换流程图 |
| 3 | 文件锁 — `O_CREAT\|O_EXCL` 原子锁 | 双进程竞争时序 + 死锁自愈触发器 |
| 4 | Session 锁 — PID 复用防御 | 双重验证流程 + `O_NOFOLLOW` 防 symlink 攻击 |
| 5 | 任务级并发 Claim | 预检 → 加锁 → 重读验证三步时序 |
| 6 | Bridge 生命周期 — 四层验证 | SIGINT→SIGTERM→SIGKILL 逐级升级链路 |
| 7 | 总结 — 4 个设计原则 | 四象限/矩阵式布局 |
| 8 | End page | Thanks |

## Code Embedding Rule

- 每个流程图节点只放 **1-3 行最关键的代码或伪代码**
- 例如：`open(lockPath, O_CREAT \| O_EXCL)` 或 `kill(pid, SIGINT)`
- 保持语法高亮但字号缩小到可读下限

## Two Color Schemes

### Scheme A: 全暗黑底层风 (pure-dark)

- **Background**: `#0a0a0b` pure black, WebGL holographic dispersion (rainbow ripple)
- **Text**: `#f1efea` warm white, IBM Plex Mono for code
- **Accent**: amber `#f59e0b` (danger/attack), cyan `#06b6d4` (security mechanism)
- **Node style**: frosted glass (`backdrop-filter: blur`), code blocks keep original syntax highlight
- **Lines**: glowing + `filter: drop-shadow`, animated arrow for data flow
- **Vibe**: kernel / low-level system, hacker aesthetic

### Scheme B: 深/浅交替 Guizang 风 (guizang-alt)

- **Background**: dark/light alternating pages, dual WebGL background switching
- **Text**: inverse to background, ink/paper restraint
- **Accent**: warm gold + deep gray, magazine feel
- **Node style**: geometric blocks, code box auto-switches bg with page
- **Lines**: clean thin lines, no glow, thickness/dashed for hierarchy
- **Vibe**: high-end tech magazine, calm analysis

## Common Layout per Slide

```
chrome (meta + page number)
frame:
  - kicker (mono, small)
  - h-xl / h-hero (serif, large)
  - ┌─ SVG 技术流程图 (55-65vh) ─┐
  - │  nodes = module + key code │
  - │  lines = data/ctrl/timing  │
  - └────────────────────────────┘
  - lead (≤2 sentences summary)
foot (chapter + subtopic)
wa (whisper anchor for video sync)
```

## Reference

- `presentation-open-design-guizang.html` — Guizang template base
- `features/content-pipeline/claudecode-prompt-caching-mid-video/production/content/02-design-notes.md` — iteration lessons
- `features/content-pipeline/claudecode-sandbox-concurrency-mid-video/production/content/01-script.md` — full narration script
