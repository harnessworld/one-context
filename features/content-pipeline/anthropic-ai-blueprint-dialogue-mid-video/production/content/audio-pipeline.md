# 口播音频约定

- **默认路径**：本期口播 WAV 使用 **豆包（火山引擎）语音 / TTS API** 合成（非 Edge TTS）。
- **实现参考**：仓库内 `skills/doubao-dialogue-tts/cli.py`（具体参数与鉴权以火山控制台文档为准）。
- **产出位置**：按内容生产惯例放在 `production/media/`（若目录尚未创建，成片流程前补齐）；文件名与 `timing/video-input.json` / `wav-durations.json` 中的 `wavFile` 保持一致。

## 互动播客（volc-podcast-tts · action=0）

- **输入稿（推荐）**：`production/content/01-input-podcast-action0.md` —— 纯叙述、无分镜，避免服务端总结时被制作标记带偏。
- **也可用**：`production/content/01-script.md`（含画面与「主播」标记，总结结果可能更飘）。
- **命令示例**（仓库根、`VOLCENGINE_PODCAST_API_KEY` 已配置）：

```bash
python skills/volc-podcast-tts/cli.py --action 0 -i features/content-pipeline/anthropic-ai-blueprint-dialogue-mid-video/production/content/01-input-podcast-action0.md -o features/content-pipeline/anthropic-ai-blueprint-dialogue-mid-video/production/media/podcast-action0.wav --format pcm
```

- **说明**：action=0 会由服务端 **重写结构与措辞**，不等于念稿；若要贴近原文对白用 action=3（见 `skills/volc-podcast-tts/SKILL.md`）。
