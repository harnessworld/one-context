# 从 PPT（HTML）+ 口播出片

权威实现：**`skills/html-video-from-slides/cli.js`**（勿在项目里再复制 Node 脚本）。

## 一次性安装（全仓库一次）

```bash
cd skills/html-video-from-slides
npm install
npx playwright install chromium
pip install edge-tts
pip install -r requirements-whisper.txt
```

## 路线 0：只要 HTML + 单个 WAV（自动对齐，推荐）

**前提**：口播顺序与内容尽量和 **各页幻灯上的字**一致（允许少量口误）。

1. 在 **`production/`** 下放好 `presentation.html` 与**唯一**一个 `.wav`。
2. 执行（在 `production/` 内）：

```powershell
node ../../../../skills/html-video-from-slides/cli.js wav-auto --project .
```

3. 默认得到 **`final_auto.mp4`**。可选：复制 `skills/html-video-from-slides/video-input.example.json` 为 **`video-input.json`**，改 `whisperModel`（如 `large-v3`）、`outputFile`、`wavFile`（多 wav 时）。

详见 [`skills/html-video-from-slides/SKILL.md`](../../../../skills/html-video-from-slides/SKILL.md)。

---

## 路线 A：手动每页时长（WAV）

1. `wav-durations.example.json` → **`wav-durations.json`**，填 `wavFile`、`slideDurationsSec`（7 个数与 `.slide` 数量一致）。
2. `node ../../../../skills/html-video-from-slides/cli.js wav --project .`

---

## 路线 B：讲稿 + Edge TTS

1. 准备 **`讲稿.md`**（`# 【第N页 · …】`）。
2. 可选 **`config.json`**（从技能目录 `config.json.example` 复制）。
3. `node ../../../../skills/html-video-from-slides/cli.js tts --project .` → **`final.mp4`**（含烧录字幕）。

---

## HTML 约定

须全局 **`go(n)`** 切页（本目录 `presentation.html` 已具备）。

## 字幕

- **tts**：自动烧录。
- **wav / wav-auto**：成片无内嵌字幕；后处理用剪映等。
