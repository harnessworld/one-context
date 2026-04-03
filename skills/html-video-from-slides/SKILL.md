---
name: html-video-from-slides
description: HTML 幻灯（presentation.html + go(n)）与口播合成 MP4。支持 Edge TTS（讲稿.md）、手动 WAV 时长（wav-durations.json）、或 wav-auto（仅 HTML+单个 WAV，本地 Whisper 自动对齐）。实现位于 one-context skills/html-video-from-slides/，跨 Cursor / Claude Code / OpenClaw 共用同一 CLI。
---

# HTML 幻灯 → 讲解视频（跨工具技能）

## 目的声明（与 one-context 一致）

- **工具无关**：同一 `SKILL.md` 与 **`cli.js`**，在 **Cursor、Claude Code、OpenClaw** 及任意能跑 **Node.js** 的终端中行为一致。
- **一处维护**：代码只在 `skills/html-video-from-slides/`；选题目录**只放素材**，不复制脚本。
- **自动发现**：各 IDE 对「技能」索引不同；未自动加载时，在规则里**链到本文件**或粘贴下方命令。

## 模式一览

| 模式 | 命令 | 输入 | 质量要点 |
|------|------|------|----------|
| **wav-auto**（推荐「只给 WAV+HTML」） | `node cli.js wav-auto --project <dir>` | `presentation.html`、目录内**恰好一个** `.wav`；可选 `video-input.json` | 口播内容与**各页幻灯可见文字**大致一致时，对齐最准；否则可能降级静音切分/均分；支持 `burnSubtitles: true` 自动烧录字幕 |
| **wav** | `node cli.js wav --project <dir>` | `presentation.html`、`wav-durations.json`、`.wav` | 时长由你精确指定 |
| **tts** | `node cli.js tts --project <dir>` | `presentation.html`、`讲稿.md`、可选 `config.json` | 机器念稿 + 自动字幕 |

幻灯按 **1920×1080** 视口截图。

## wav-auto：质量前提（必读）

1. **内容对齐**：录音应基本按幻灯顺序讲，且与 **HTML 里 `.slide` 的 innerText** 能对上字（允许少量口误；会尝试前缀匹配）。
2. **模型**：默认 Whisper **`medium`**（速度与精度折中）。更高精度可在 `video-input.json` 设 `whisperModel` 为 `large-v3`（更慢、更吃内存/显存）。
   - **CPU 环境注意**：`medium` / `large` 模型在纯 CPU 上可能卡死，建议用 **`small`** 或 **`base`** 模型。
3. **ffmpeg**：静音降级分支需要可执行 **`ffmpeg`**；未装时 Node 侧会通过 `ffmpeg-static` 注入 **`FFMPEG_PATH`** 给对齐脚本（与 `wav-auto` 主流程一致）。
4. **字幕**：
   - wav-auto 默认不烧录字幕；在 `video-input.json` 中设 `"burnSubtitles": true` 即可启用。
   - **SRT 生成后必须先 review 校对，再烧录视频**：这是强制流程，不能先烧后改。Whisper 转写常有错别字（如 Monoreport→Monorepo、G2→Jira、指→只、倉庫→仓库 等），生成 SRT 后先展示给用户校对，确认后再执行烧录步骤。
   - 也可设 `"subtitle": { "fontSize": 24, "marginV": 18, "fontName": "Microsoft YaHei", "bold": true }` 自定义样式。tts 模式始终烧录字幕。

## 代理与网络（下载失败时先看这里）

**Whisper 模型、Playwright 浏览器、`pip` / `npx` 走外网时，若未走代理，常表现为 `IncompleteRead`、`Connection reset`、`timed out`。**

与仓库根 [`README.md`](../../README.md) 一致：在**同一终端**里先导出代理，再执行安装与 `wav-auto`（子进程会继承环境变量）。

| 变量 | 作用 |
|------|------|
| **`HTTPS_PROXY`** / **`HTTP_PROXY`** | `pip`、`faster-whisper` 经 Hugging Face 拉模型；`requests`/`urllib3` 会读 |
| **`ALL_PROXY`** | 若你用的是 SOCKS 等统一代理，部分工具会认 |
| **国内镜像（可选）** | `HF_ENDPOINT=https://hf-mirror.com` 减轻直连 HF 失败 |

**PowerShell 示例（按你本机端口改）：**

```powershell
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
$env:HTTP_PROXY  = "http://127.0.0.1:7890"
# 可选：$env:HF_ENDPOINT = "https://hf-mirror.com"
```

然后再执行 `pip install …`、`npx playwright install chromium`、`node cli.js wav-auto …`。

## 一次性安装

```bash
cd skills/html-video-from-slides
npm install
npx playwright install chromium
pip install edge-tts
pip install -r requirements-whisper.txt
```

## 运行示例

```bash
node path/to/one-context/skills/html-video-from-slides/cli.js wav-auto --project path/to/素材目录
```

## 输出与临时文件

| 模式 | 默认成片 | 临时目录 |
|------|----------|----------|
| tts | `final.mp4` | `<素材>/temp_video/` |
| wav | `wav-durations.json` 内 `outputFile` | `<素材>/temp_video_wav/` |
| wav-auto | `final_auto.mp4`（`video-input.json` 可改） | 同上 + 技能目录 `.cache/`（可删） |

## 故障排除

- **找不到 go**：`presentation.html` 需 `function go(n){...}`。
- **多个 wav**：只留一个，或写 `video-input.json` 的 `wavFile`。
- **align 失败 / faster-whisper**：`pip install faster-whisper`，首次运行会下载模型。
- **Playwright**：在**技能目录**执行 `npx playwright install chromium`（与项目里 `node_modules` 绑定）。
- **Hugging Face 下载中断**（`IncompleteRead` / `ChunkedEncodingError`）：多数是没走代理或链路不稳——先设 **`HTTPS_PROXY`/`HTTP_PROXY`**（见上文「代理与网络」），再重跑；仍失败可多跑几次续传；或把 `whisperModel` 改为 **`base`** / **`small`** 减小体积；国内可加 **`HF_ENDPOINT=https://hf-mirror.com`**。
- **TTS**：`pip install edge-tts` + 网络。

示例配置：`config.json.example`、`wav-durations.example.json`、`video-input.example.json`。

---

## 封面生成（竖版 + 横版）

使用 VideoFactory 的封面模板生成竖版（1080×1920）和横版（1440×1080）封面图。

### 前置依赖

确保 VideoFactory 环境可用（视频工厂的工具目录）：
```
D:\自媒体\视频工厂\_工具
```

### 竖版封面生成

1. 复制模板到项目目录：
```bash
copy "D:\自媒体\视频工厂\_模板\cover_template.html" "<项目>\cover.html"
```

2. 修改 CONFIG（参考 presentation 第一页配色）：
```javascript
const CONFIG = {
    headline:    "标题第一行\n标题第二行",
    accentLine:  1,          // 第几行高亮（1=第1行）
    subline:     "副标题",
    tag:         "2026 · 分类",
    bgImage:     "",
    avatarImage: "",
    footerItems: ["亮点1", "亮点2"],
    watermark:   "",
    theme:       "onecontext",
};
```

3. 生成封面（cd 到项目目录后执行）：
```bash
node "D:\自媒体\视频工厂\_工具\gen_cover.js"
# 输出：videos/cover.png (1080×1920)
```

### 横版封面生成

1. 复制横向模板并修改 CONFIG：
```bash
copy "D:\自媒体\视频工厂\_模板\cover_template_h.html" "<项目>\cover_h.html"
```

2. CONFIG 示例：
```javascript
const CONFIG = {
    headline:    "主标题",
    accentWord:  "要高亮的词",
    subline:     "副标题",
    tag:         "2026 · 分类",
    bgImage:     "",
    avatarImage: "",
    infoItems:   ["亮点1", "亮点2", "亮点3", "亮点4", "亮点5"],
    watermark:   "",
    theme:       "onecontext",
};
```

3. 生成横版：
```bash
node "D:\自媒体\视频工厂\_工具\gen_cover_h.js" cover_h.html
# 输出：videos/cover_h.png (1440×1080)
```

### 定制主题：onecontext

在模板中添加 onecontext 主题，沿用 presentation 第一页的渐变色（蓝→紫→绿→橙）：

```javascript
const THEMES = {
    onecontext: {
        accent:     "#60A5FA",
        accent2:    "#8B5CF6",
        tagBg:      "rgba(96,165,250,0.12)",
        tagBorder:  "rgba(96,165,250,0.5)",
        tagColor:   "#60A5FA",
        glowColor:  "rgba(96,165,250,0.25)",
        glowColor2: "rgba(139,92,246,0.15)",
        dotColor:   "#60A5FA",
        bar:        "linear-gradient(90deg, transparent 2%, #60A5FA 35%, #8B5CF6 70%, #34D399 85%, transparent 98%)",
        textGlow:   "0 0 80px rgba(96,165,250,0.35), 0 4px 30px rgba(0,0,0,0.9)",
        accentGrad: "linear-gradient(135deg, #60A5FA 0%, #818CF8 30%, #C084FC 55%, #34D399 78%, #FBBF24 100%)",
        fallbackBg: "radial-gradient(ellipse 120% 80% at 50% 30%, #0a1628 0%, #030712 40%, #050210 100%)",
    },
};
```

### 优化要点

- **横版字号**：标题建议 180px+，副标题 48px+，确保手机横屏可读
- **装饰光晕**：可添加 CSS 光晕增强视觉冲击
- **亮点数量**：竖版建议 2-3 个，横版可放 5 个
