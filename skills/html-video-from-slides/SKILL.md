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
| **wav-auto**（推荐「只给 WAV+HTML」） | `node cli.js wav-auto --project <dir>`（可加 `--whisper-srt` 忽略 `srtFile`、强制 Whisper 字幕时间轴） | `presentation.html`、目录内**恰好一个** `.wav`；可选 `video-input.json` | 口播内容与**各页幻灯可见文字**大致一致时，对齐最准；否则可能降级静音切分/均分；**默认关闭 VAD** 以减少片头/轻声被裁导致的无字幕大段空白；支持 `burnSubtitles: true` 烧录；可选 `strictSubtitles` 在超长字幕缺口时中止成片 |
| **wav** | `node cli.js wav --project <dir>` | `presentation.html`、`wav-durations.json`、`.wav` | 时长由你精确指定 |
| **tts** | `node cli.js tts --project <dir>` | `presentation.html`、`讲稿.md`、可选 `config.json` | 机器念稿 + 自动字幕 |
| **srt-map** | `node cli.js srt-map --project <dir>`（可选 `--boundaries "0:0-0,1:1-2,..."`） | `sub.srt`、`presentation.html` | Whisper 对齐失败时，手动映射 SRT 条目→幻灯片，生成 `wav-durations.json` |
| **cover** | `node cli.js cover --project <dir>`（可选 `--horizontal`） | `cover.html` / `cover_h.html` | Playwright 截图 → `videos/cover.png` 或 `videos/cover_h.png` |

幻灯按 **1920×1080** 视口截图。

## 制作 presentation.html（视觉规范）

**先读以下两份文档，再开始写 HTML**：

| 文档 | 作用 |
|------|------|
| `DESIGN-STANDARD.md`（同目录） | 字号规范、信息密度、主题系统、反模式列表、新建流程 |
| `TEMPLATES.md`（同目录） | 5 种布局的可复制 HTML 模板 + Minimum Fill Table + AI 生成 Checklist |

**核心约束**（详见上述文档）：
- 每张 slide 画面覆盖率 ≥ 85%
- 卡片/大图布局用 `justify-content:space-between`（不用 `center`）
- 禁止 `<br>` 空行当间距，禁止内容区用 `position:absolute`
- 总字数 ≤ 120 汉字/张

---

## 一键生成成片（wav-auto）

在**已安装依赖**的前提下（见下文「一次性安装」），素材目录内放好 **`presentation.html`**、**单个 `.wav`**，可选 **`video-input.json`**，在仓库中执行：

```powershell
Set-Location "path\to\one-context\skills\html-video-from-slides"
node cli.js wav-auto --project "path\to\你的素材目录"
```

**Windows PowerShell 5.x** 请用 **`;`** 连接命令，不要用 **`&&`**。

**推荐 `video-input.json` 至少包含**：`burnSubtitles: true`、`whisperModel`（CPU 可用 `small`）、`outputFile`、`subtitle`（含 `charsPerLine`）。可选：`noSpeechThreshold`、`fillSrtGaps`、`whisperHotwords`、`srtReplacements`、`wrapSubtitles`（见下文「字幕与稳定性」）。一条命令即可：**对齐 →（缺口二次转写）→ 截图分段 → 拼接 → 字幕预处理 → 烧录 → 输出 MP4**。

## wav-auto：质量前提（必读）

1. **内容对齐**：录音应基本按幻灯顺序讲，且与 **HTML 里 `.slide` 的 innerText** 能对上字（允许少量口误；会尝试前缀匹配）。
2. **模型**：默认 Whisper **`medium`**（速度与精度折中）。更高精度可在 `video-input.json` 设 `whisperModel` 为 `large-v3`（更慢、更吃内存/显存）。
   - **CPU 环境注意**：`medium` / `large` 模型在纯 CPU 上可能卡死，建议用 **`small`** 或 **`base`** 模型。
3. **ffmpeg**：静音降级分支需要可执行 **`ffmpeg`**；未装时 Node 侧会通过 `ffmpeg-static` 注入 **`FFMPEG_PATH`** 给对齐脚本（与 `wav-auto` 主流程一致）。
4. **字幕与稳定性（wav-auto）**：
   - **Whisper 初稿始终落盘**：只要未指定外部 `srtFile`，每次对齐都会在项目根生成 **`sub.srt`**（与 `burnSubtitles` 无关），便于先校对再决定是否烧录。
   - **超长无字幕 → 自动二次转写**：整段 Whisper 仍可能在时间轴上留下大片无字幕区间（与 30s chunk、解码策略有关，未必仅靠调高 `noSpeechThreshold` 即可消除）。`align_wav_slides.py` 默认对**超过 `maxSubtitleGapSec`** 的缺口 **用 ffmpeg 切出对应 WAV 片段再跑一遍 Whisper** 并合并回 `seg_list`（可用 `fillSrtGaps: false` 或 `--no-fill-srt-gaps` 关闭；`maxGapFillSec` 对应 `--max-gap-fill-sec` 限制超长静音不切）。
   - **no_speech 过滤（易漏清晰人声）**：faster-whisper 与 OpenAI Whisper 一致：若某音频块的 **`no_speech_prob` 大于 `no_speech_threshold`，会整段跳过不输出字幕**（不是 VAD）。库默认阈值为 **0.6**，片头/垫乐旁白常被误判，出现「第 8 秒起明明很清晰却整段无字」。本 skill **默认改为 `noSpeechThreshold`: 0.85**（仅在 `video-input.json` 未显式传 `--no-speech-threshold` 时由 `align_wav_slides.py` 生效）：**阈值越高，越不容易误跳过**。仍漏时可继续提高到 **0.9**，或设 **`"noSpeechThreshold": null`** 关闭此项过滤（静音段可能多出幻听字幕，需自行审校）。若需与旧行为一致可设 **`0.6`**。
   - **VAD 默认关闭**：`video-input.json` 中 **`"vadFilter": true`** 才启用 faster-whisper 内置 VAD。此前默认开启时，容易把**轻声、气口、片头口播**判成非语音，造成 **SRT 中间出现十几秒～几十秒无字幕**，而音频仍在播放。环境噪声极大且口播很清晰时，可试开 `vadFilter`，否则保持 **false**（默认）。
   - **字幕缺口告警**：对齐结束会检测「无字幕区间」；超过 **`maxSubtitleGapSec`**（默认 **2.5**）会写入日志/`warnings`。需要「宁可不导出也不能烧残缺字幕」时，设 **`"strictSubtitles": true`**：存在超长缺口则 **中止成片**（退出码 4），先补 `sub.srt` 或换更大 `whisperModel` 再跑。
   - wav-auto **默认不烧录**；在 `video-input.json` 中设 `"burnSubtitles": true` 才会把字幕烧进 MP4。
   - **与口播时间轴一致**：SRT 时间码来自 Whisper 对 WAV 的分段（`align_wav_slides.py` 的 `--srt-out`）。若在 `video-input.json` 里写了 **`srtFile`** 指向已有文件，则会**跳过** Whisper 写 SRT，烧录沿用该文件的时间码——若该文件是手改/旧版，就会**和语音对不上**。需要重新对齐时任选其一：**去掉 `srtFile` 字段**后重跑 `wav-auto`；或保留配置但本次强制用 Whisper 时间轴：`node cli.js wav-auto --project <dir> --whisper-srt`。跑完后项目里的 `sub.srt` 会与口播同源；之后**只改错别字、不要改时间轴**（除非再跑一次上述命令）。
   - **简体中文**：`language="zh"` 的 Whisper 仍常输出**繁体或繁简混用**。`align_wav_slides.py` 在写出 SRT、以及用词级时间轴与幻灯对齐前，会**尽量**做繁体→简体（依赖 **`opencc-python-reimplemented`**，见上文 pip）；并对转写加了 `initial_prompt` 引导简体。未装 OpenCC 时会在日志里提示，字幕可能仍带繁体。已有 `sub.srt` 可事后统一简体：`python skills/html-video-from-slides/t2s_srt.py path/to/sub.srt`（在仓库根下执行时按实际路径调整）。
   - **错别字没有自动「审稿」**：流水线**不会**用 LLM 或词典替你纠错；**SRT 生成后仍建议人工 spot-check**（尤其专名、数字）。Whisper 常把 **Claude 听成 Cloud** 等，可二选一减轻：① **`whisperHotwords`**（空格分隔）交给 faster-whisper 的 **hotwords** 偏向正确拼写；② **`srtReplacements`** 在**烧录前**对文案做批量替换（如 `Cloud`→`Claude`，**长词组写在短词前面**）。二者均在 `video-input.json` 配置，见 `video-input.example.json`。
   - **对 AI 代理（强制）**：`wav-auto` 或任何步骤**一旦写出/更新了项目根 `sub.srt`**，代理在交付成片前**必须**完成一轮**字幕校对**（不得只跑完流水线就结束）：通读或按段检索 `sub.srt`，对照 `presentation.html` 各页主题与口播专名，修正明显同音错字（如专名、产品名、数字）；把可复现的纠正补进 `video-input.json` 的 **`srtReplacements`**（长词在前），再按需重烧。若**仅改字、不改时间轴**，可保留 `wav-durations.json` 中的 `slideDurationsSec`，在 `wav-durations.json` 中写好 **`burnSubtitles`** / **`srtFile`** / **`subtitle`** 与 **`srtReplacements`** 后执行 **`node cli.js wav --project <dir>`** 快速重烧，**无需**重跑 Whisper。
   - **单行字幕过长超出画面**：烧录阶段默认 **`wrapSubtitles: true`**，按 **`subtitle.charsPerLine`**（默认 28，口播密可改为 **22～24**）对每条字幕**折成多行**再交给 libass（实现于 `lib/srt_postprocess.js`）。若关闭 `wrapSubtitles` 则只做替换不折行。
   - 也可设 `"subtitle": { "fontSize": 18, "marginV": 18, "fontName": "Microsoft YaHei", "bold": true, "primaryColour": "#FFFF00", "primaryAlpha": 108, "charsPerLine": 24 }` 自定义样式（默认即黄字偏小字号；`primaryAlpha` 为 ASS 透明度：**0** 不透明，**255** 全透明）。tts 模式始终烧录字幕。

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

**Windows PowerShell 5.x** 不支持 `cd … && npm install` 这种 **`&&` 链式**写法，请拆成多条命令，或改用 **`;`** 分隔。

## 一次性安装

```bash
cd skills/html-video-from-slides
npm install
npx playwright install chromium
pip install edge-tts
pip install faster-whisper huggingface_hub
pip install opencc-python-reimplemented
```

## 运行示例

```bash
node path/to/one-context/skills/html-video-from-slides/cli.js wav-auto --project path/to/素材目录
```

## 输出与临时文件

| 模式 | 默认成片 | 临时目录 |
|------|----------|----------|
| tts | `final.mp4` | `<素材>/tmp/` |
| wav | `wav-durations.json` 内 `outputFile` | `<素材>/tmp/` |
| wav-auto | `final_auto.mp4`（`video-input.json` 可改） | 同上 + 技能目录 `.cache/`（可删） |

说明：`<素材>` 一般为 `…/production/`。中间帧、分段音视频、`concat.txt` 等均写入 **`tmp/`**，可整夹删除；勿把成片唯一信源只放在 `tmp/`。

## 故障排除

- **日志出现「全文无匹配，均分音频」或 `whisper_align_partial` 且各页 `slideDurationsSec` 几乎完全相等**：说明 Whisper 转写**没能**把口播和 HTML 里 `.slide` 的可见文字对上，成片会按**平均时长**切页，画面与讲解往往**不同步**。处理：让每页幻灯上的字尽量接近该段**真实口播用语**（不必逐字相同，但要能前缀/关键词匹配）；或把 `video-input.json` 里 `whisperModel` 改为 **`medium`**（机器吃得消时）；或放弃自动对齐，改用 **`wav` 模式** + 手写 `wav-durations.json` 的 `slideDurationsSec`。若日志已提示 **`whisper_align_partial`**，CLI 也会打出额外说明，请优先检查幻灯文案与口播是否同源。
- **SRT 出现大片段无字幕、但 WAV 里明明有清晰说话**：先检查 **`noSpeechThreshold`**（默认已提高到 **0.85**，高于库默认 **0.6**）。若仍漏，可提到 **0.9** 或 **`null`** 关闭该过滤。另可排查是否误开 **VAD**（`vadFilter: true`）、或换更大 **`whisperModel`**，或手动补 `sub.srt`。
- **`strict-subtitles` / `strictSubtitles` 中止**：表示存在超过 **`maxSubtitleGapSec`** 的无字幕区间。补全 `sub.srt`、关 **`vadFilter`**、或放宽 **`maxSubtitleGapSec`** / 关闭 **`strictSubtitles`** 后再跑。
- **字幕和口播对不上**：几乎总是用了外部 `srtFile` 或手改了时间轴。按上文「与口播时间轴一致」处理：去掉 `srtFile` 或加 `--whisper-srt` 后重跑 `wav-auto`。
- **找不到 go**：`presentation.html` 需 `function go(n){...}`。
- **多个 wav**：只留一个，或写 `video-input.json` 的 `wavFile`。
- **align 失败 / faster-whisper**：`pip install faster-whisper huggingface_hub`，首次运行会从 hf-mirror.com 下载模型（已默认禁用不稳定的 Xet Storage，不会写坏缓存）。**字幕要统一简体**时再装：`pip install opencc-python-reimplemented`。
- **Playwright**：在**技能目录**执行 `npx playwright install chromium`（与项目里 `node_modules` 绑定）。
- **Hugging Face 下载中断**（`IncompleteRead` / `ChunkedEncodingError`）：多数是没走代理或链路不稳——先设 **`HTTPS_PROXY`/`HTTP_PROXY`**（见上文「代理与网络」），再重跑；仍失败可多跑几次续传；或把 `whisperModel` 改为 **`base`** / **`small`** 减小体积；国内可加 **`HF_ENDPOINT=https://hf-mirror.com`**。
- **TTS**：`pip install edge-tts` + 网络。

示例配置：`config.json.example`、`wav-durations.example.json`、`video-input.example.json`。

---

## 封面生成（竖版 + 横版）

竖版 **1080×1920** → `videos/cover.png`；横版 **1440×1080** → `videos/cover_h.png`。文案与配色在对应 HTML 的 **`CONFIG`** 里改。

### 优先：项目自带脚本（本仓 feature 推荐）

在**素材目录**（多为 `…/production/`）放置 `cover.html`、`cover_h.html`、`gen_cover.js`、`gen_cover_h.js`、`package.json`（`devDependencies` 含 `playwright`）。与口播项目同目录维护，不依赖本机固定盘符。

```bash
cd <素材目录>   # 例如 features/develop/claude-caveman-mode/production
npm install
npx playwright install chromium   # 首次
node gen_cover.js                 # → videos/cover.png
node gen_cover_h.js               # → videos/cover_h.png
```

参考实现：

- `features/develop/claude-caveman-mode/production/`（竖横一体、`theme: "wenyan"` 等与 `presentation.html` 纸墨色一致时可加 `body.theme-wenyan`）
- `features/develop/one-context-intro-short-video/production/`（竖版 + `theme: "onecontext"`）

**竖版 CONFIG 要点：**

```javascript
const CONFIG = {
    headline:    "主标题\n可选第二行",  // 每行 ≤6 字为宜，共 ≤2 行
    accentLine:  1,
    subline:     "副标题",
    tag:         "2026 · 分类",
    bgImage:     "",
    avatarImage: "",
    footerItems: ["亮点1", "亮点2"],
    watermark:   "",
    theme:       "tech",   // 或项目内定义的 wenyan / onecontext 等
};
```

**横版 CONFIG 要点：** 用 `accentWord` 高亮标题中的词；`infoItems` 为右侧条列。

```javascript
const CONFIG = {
    headline:    "主标题",
    accentWord:  "要高亮的词",
    subline:     "副标题",
    tag:         "2026 · 分类",
    bgImage:     "",
    avatarImage: "",
    infoItems:   ["亮点1", "亮点2", "…"],
    watermark:   "",
    theme:       "wenyan",
};
```

### 备选：VideoFactory 固定路径（旧环境）

若本机仍有 `D:\自媒体\视频工厂\_工具`，可从 `_模板` 复制 `cover_template.html` / `cover_template_h.html` 为 `cover.html` / `cover_h.html`，再执行：

```bash
node "D:\自媒体\视频工厂\_工具\gen_cover.js"
node "D:\自媒体\视频工厂\_工具\gen_cover_h.js" cover_h.html
```

### 定制主题示例：onecontext（与某期幻灯蓝紫渐变一致）

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

### 发布素材（全平台通用格式）

**不按抖音 / B 站 / 小红书等分块**；对外粘贴用同一套字段即可。

建议在素材目录增加 **`05-publish-kit.md`**，文首用**纯文本代码块**（无 Markdown 加粗）便于整段复制，格式为：

```
标题：……

简介：……

话题：#话题1 #话题2 …
```

示例：`features/develop/claude-caveman-mode/production/05-publish-kit.md`。下文可接标题备选、封面定稿说明、置顶评论、章节轴、素材路径、发布前检查等备忘。

### SRT→Slide 手动映射（Whisper 对齐失败时）

当 `wav-auto` 日志出现 **`whisper_align_partial`** 或所有幻灯片时长几乎相等时，说明 Whisper 无法将口播与 HTML 幻灯文字对齐（通常因为 PPT 文案是提炼要点而非逐字对应口播）。此时：

**Step 1** — 分析 SRT 与幻灯片：

```bash
node cli.js srt-map --project <素材目录>
```

输出：全部 SRT 条目（序号、时间、内容预览）+ 全部幻灯片文本。AI 阅读后判断每页幻灯片对应的 SRT 条目范围。

**Step 2** — 提供边界，生成时长配置：

```bash
node cli.js srt-map --project <素材目录> --boundaries "0:0-0,1:1-2,2:3-5,..."
```

格式：`slide_idx:first_entry-last_entry`，逗号分隔。脚本自动计算每页时长、找 .wav 文件，写入 `wav-durations.json`。

**Step 3** — 用精确时长渲染：

```bash
node cli.js wav --project <素材目录>
```

### 封面一键截图

```bash
node cli.js cover --project <素材目录>              # → videos/cover.png (1080×1920)
node cli.js cover --project <素材目录> --horizontal # → videos/cover_h.png (1440×1080)
```

在素材目录放 `cover.html`（竖版）和/或 `cover_h.html`（横版），内含 `CONFIG` 对象控制文案与配色（见上文 CONFIG 要点）。命令使用 Playwright 截图输出到 `videos/` 子目录。

### 优化要点

- **字号**：竖版主标题宜 **140px～220px**（按字数 class 调整）；横版标题建议 **140px 级及以上**，副标题 **36px+**，保证小图可读。
- **装饰**：背景服务于文字；与 `presentation.html` 同系列时可用纸墨 / 渐变主题（如 `wenyan`），避免与成片气质冲突。
- **亮点数量**：竖版底部 **2～3** 条；横版右侧 **5** 条左右。
