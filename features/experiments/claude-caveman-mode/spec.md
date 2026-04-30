---
id: claude-caveman-mode
title: 用穴居人模式让 Claude 省 Token
status: done
category: develop
primary_repo_id: one-context
owner: 
updated: 2026-04-05
---

# 概述

用穴居人模式让 Claude（Claude Code）节省 Token 的视频项目。

# 目标与非目标

## 目标

- 生成宣传视频（竖版 + 横版封面 + MP4）
- 音频已就位：`用穴居人模式让+Claude+省+Token.wav`（29MB，约 8 分钟）
- 使用 html-video-from-slides skill 生成视频

## 非目标

- 暂不涉及视频工厂的其他模式

# 验收标准

- [x] 竖版封面生成（1080×1920）→ `production/videos/cover.png`
- [x] 横版封面生成（1440×1080）→ `production/videos/cover_h.png`（由 `cover_h.html` + 视频工厂 `gen_cover_h.js` 导出）
- [x] Whisper 转写生成 SRT 字幕 → `production/sub.srt`（口播对齐阶段生成；`video-input.json` 指定 `srtFile` 供烧录）
- [x] 字幕校对后烧录（已修正明显错字如「摸尾→末尾」；首条文案与口播对齐；用 `tmp/merged.mp4` + 当前 `sub.srt` 重烧 `final_auto.mp4`）
- [x] final_auto.mp4 生成 → `production/final_auto.mp4`

# 实现落点

- **仓库 id**: one-context
- **分支**: superno
- **主要路径**: `features/experiments/claude-caveman-mode/`（历史成片路径可能仍为相对 `production/`）
- **音频**: `production/用穴居人模式让+Claude+省+Token.wav`

# 关联

- 视频生成 skill: `skills/html-video-from-slides/`
- 发布文案与检查清单: `production/05-publish-kit.md`

