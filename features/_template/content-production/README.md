# Content Production — 短视频 Feature 模板

新建短视频 feature 时复制此目录到 `features/content-pipeline/<feature-id>/`，与标准 feature 模板（`spec.md` 等）合用。

## 命名规范

Feature-id 格式：`{主题}-{类型}`，类型后缀统一为：

| 后缀 | 含义 | 典型时长 |
|------|------|---------|
| `short-video` | 短视频口播 | ≤3min |
| `mid-video` | 中视频深度解析 | 3-15min |
| `narration` | 纯音频口播/播客 | 不限 |

**category 必须为 `content-pipeline`**，不要放在 `develop/` 或其他类别下。

## 目录结构

```
<feature-id>/
├── spec.md                         # Feature 规格
├── review_record.md                # 评审记录（不在 production/ 内）
├── issue_checklist.md              # 问题清单（不在 production/ 内）
│
└── production/
    ├── content/                    # 内容创作资产 ✅ 跟踪
    │   ├── 00-structure.md         #   话题大纲
    │   ├── 01-script.md            #   口播讲稿
    │   └── 05-publish-kit.md       #   发布素材（标题/简介/话题/检查清单）
    │
    ├── slides/                     # 幻灯片资产 ✅ 跟踪
    │   └── presentation.html       #   主幻灯（核心资产）
    │
    ├── subtitles/                  # 字幕资产 ✅ 跟踪
    │   └── sub.srt                 #   校对后字幕
    │
    ├── timing/                     # 时间轴与配置 ✅ 跟踪
    │   ├── wav-durations.json      #   精确翻页时长
    │   └── video-input.json        #   配置 + srtReplacements 积累
    │
    ├── media/                      # 媒体文件 ❌ 不跟踪
    │   ├── *.wav                   #   原始录音
    │   ├── *.mp4                   #   成片
    │   └── cover.png               #   封面截图（可从 HTML 重建）
    │
    └── tmp/                        # 构建中间物 ❌ 不跟踪
        └── ...                     #   帧图、分段音频等
```

## 分类原则

**如果这个文件消失了，需要人重新做创意决策或 AI 推理，那就是资产——要跟踪。**

| 分类 | 跟踪？ | 原因 |
|------|--------|------|
| 大纲、讲稿、发布素材 | ✅ | 人写的内容创作，不可无损重建 |
| presentation.html | ✅ | 布局+SVG+精炼文字，不可无损重建 |
| sub.srt（校对后） | ✅ | 校对是人工+推理过程，不可无损重建 |
| wav-durations.json | ✅ | 精确翻页时长，不可无损重建 |
| video-input.json | ✅ | 含 srtReplacements 积累，不可无损重建 |
| cover.html | ✅ | 封面设计，不可无损重建 |
| review_record / issue_checklist | ✅ | 评审产出，放 feature 根目录 |
| *.wav / *.mp4 / *.png | ❌ | 媒体文件，体积大；mp4/png 可从 HTML 重建 |
| tmp/ | ❌ | 构建中间物，可随时重建 |

## Skill 产出物路径映射

| Skill | 产出物 | 写入路径 |
|-------|--------|----------|
| srt-proofread | `sub.srt` | `production/subtitles/sub.srt` |
| srt-to-deck | `presentation.html` | `production/slides/presentation.html` |
| srt-to-deck | `wav-durations.json` | `production/timing/wav-durations.json` |
| html-deck-layout | `presentation.html` | `production/slides/presentation.html` |
| html-video-from-slides | `--project` 指向 | `production/`（读取各子目录） |

## 与标准 feature 模板的关系

此模板**补充而非替代** `features/_template/` 下的标准模板。短视频 feature 同时包含：

- 标准产物：`spec.md`（必选）、`review_record.md` / `issue_checklist.md`（按需）
- 内容产物：`production/` 下的全部创作资产

`tech_design.md` / `test_report.md` / `mr_report.md` / `deliver.md` 通常不适用于内容型 feature。

## 结构校验清单

对 `features/content-pipeline/` 下每个 feature 执行以下检查。`project-audit` skill 应内嵌此逻辑。

### 必须通过（FAIL = 阻塞）

| # | 检查项 | 判定规则 |
|---|--------|---------|
| 1 | spec.md 存在 | `<feature>/spec.md` 存在 |
| 2 | spec.md category 正确 | frontmatter `category: content-pipeline` |
| 3 | production/ 骨架完整 | 子目录 `content/`, `slides/`, `subtitles/`, `timing/`, `media/`, `tmp/` 均存在 |
| 4 | 无遗留临时脚本 | `<feature>/` 根目录不得有 `_gen_*.py` / `_fix_*.py` / `_*.py` 等文件 |
| 5 | 无旧 srt/ 目录 | 不得存在 `<feature>/srt/` 目录（字幕应在 `production/subtitles/`） |
| 6 | .DS_Store 未被跟踪 | `git ls-files` 不含 `<feature>/**/.DS_Store` |

### 应当通过（WARN = 提醒）

| # | 检查项 | 判定规则 |
|---|--------|---------|
| 7 | content/ 有大纲 | `production/content/00-structure.md` 存在 |
| 8 | content/ 有讲稿 | `production/content/01-script.md` 存在 |
| 9 | INDEX.md 一致 | `features/INDEX.md` 中该 feature 的 path 与实际目录一致 |
| 10 | spec.md 路径自洽 | spec.md 内引用的路径前缀与实际 `features/content-pipeline/<id>/` 一致 |