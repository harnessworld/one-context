---
name: volc-podcast-tts
description: 火山引擎「播客语音合成」WebSocket v3 — 长文本/URL/对白脚本生成双人播客流式音频（PCM/WAV/MP3 等）。
triggers:
  - 火山播客
  - podcasttts
  - 双人播客合成
  - volc podcast
version: 0.1.0
---

# volc-podcast-tts

基于官方 **播客 API · WebSocket v3**（`wss://openspeech.bytedance.com/api/v3/sami/podcasttts`）：服务端可做 **内容总结 + 双人对话式播客**，与仓库内 `doubao-dialogue-tts`（逐句念稿 V3 TTS）不同。

权威文档：<https://www.volcengine.com/docs/6561/1668014?lang=zh>（以控制台最新说明为准）。

## 前置条件

1. 控制台开通播客试用：<https://console.volcengine.com/speech/service/10028>
2. 鉴权（二选一，与豆包语音 V3 说明一致）：
   - **新版控制台**：互动播客页「快速 API 接入」里 **复制 API Key** → 环境变量 `VOLCENGINE_PODCAST_API_KEY`（请求头 `X-Api-Key`）。**不要把列表里的密钥「名称」当成 APP ID。**
   - **旧版控制台**：**APP ID** + **Access Token**（文档称 Access Key）→ `VOLCENGINE_PODCAST_APP_ID` / `VOLCENGINE_PODCAST_ACCESS_KEY`
3. 默认请求头资源：`X-Api-Resource-Id: volc.service_type.10050`，`X-Api-App-Key: aGjiRDfUWi`（若文档变更以控制台为准）

## 安装

```bash
cd skills/volc-podcast-tts
pip install -r requirements.txt
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `VOLCENGINE_PODCAST_API_KEY` | **推荐**：控制台复制的 API Key（`X-Api-Key`） |
| `VOLCENGINE_PODCAST_APP_ID` | 旧版：APP ID |
| `VOLCENGINE_PODCAST_ACCESS_KEY` | 旧版：Access Token |
| `VOLCENGINE_PODCAST_RESOURCE_ID` | 可选，默认 `volc.service_type.10050` |

可将 `local.env.example` 复制为 `local.env`（勿提交）。

**写入 Windows 用户级永久变量**（从新终端生效）：

```powershell
powershell -ExecutionPolicy Bypass -File skills/volc-podcast-tts/scripts/sync-user-env-from-local.ps1
```

## 用法

在仓库根或本目录执行：

```bash
# action=0：长文本总结 → 播客（输出 WAV，内部为 PCM s16le）
python skills/volc-podcast-tts/cli.py --action 0 -i 讲稿.txt -o out.wav --format pcm

# action=0：URL / 可下载文件链接
python skills/volc-podcast-tts/cli.py --action 0 --input-url "https://..." -o out.wav --format pcm

# action=3：口播体「女：/男：」每行一条（空行可忽略，自动识别；与空行分段轮换格式二选一）
python skills/volc-podcast-tts/cli.py --action 3 -i 对白.md -o out.wav --format pcm

# action=3：无行首标记时，空行分段，奇数段男、偶数段女（`--dialogue-format paragraph` 可强制）
python skills/volc-podcast-tts/cli.py --action 3 -i 段落体.md -o out.wav --format pcm --dialogue-format paragraph

# action=3：精确轮次：nlp_texts JSON 文件
python skills/volc-podcast-tts/cli.py --action 3 --nlp-json rounds.json -o out.wav --format pcm

# action=4：prompt 联网总结（需服务端支持）
python skills/volc-podcast-tts/cli.py --action 4 --prompt "火山引擎" -o out.mp3 --format mp3

# 调试：写出服务端事件摘要
python skills/volc-podcast-tts/cli.py --action 0 -i 讲稿.txt -o out.wav -v --meta-out meta.json
```

### action 说明

| action | 含义 |
|--------|------|
| 0 | `input_text` 或 `input_info.input_url` 总结生成播客 |
| 3 | `nlp_texts` 对话文本直接生成播客（单轮 ≤300 字，总长限制见文档） |
| 4 | `prompt_text` 联网生成播客 |

### 断点重试

首次请求的 `session_id` 即任务 id；若中断，可按文档携带：

```bash
python skills/volc-podcast-tts/cli.py ... \
  --retry-task-id "<上次 session_id>" \
  --last-finished-round-id 5
```

## 听感（减轻「男女硬切 / 拼接感」）

互动播客 **action=3** 本质是服务端 **按轮合成**，轮与轮之间不会像真人对话那样自然，这是产品形态限制。

本 CLI 可做三件事（仍不改文案含义）：

1. **action=3 默认 `speaker_info.random_order=false`**，避免与稿子顺序不一致；action 0/4 仍为 `true`（可用 `--random-speaker-order` / `--fixed-speaker-order` 覆盖）。
2. **`--merge-same-speaker-lines`**：相邻同一发音人合并为一轮（≤300 字），减少无谓切换（例如连续两段「男：」）。
3. **`--inter-speaker-silence-ms 80`**（可自行试 60–150）：仅在 **发音人切换** 时插入极短静音，减轻两端 PCM 硬贴带来的「蹦」一下。

官方亦建议 **同一系列发音人成对**（默认 dayi / mizai）；换一对需在控制台核对列表。

## 与 doubao-dialogue-tts 的区别

| | volc-podcast-tts | doubao-dialogue-tts |
|--|------------------|---------------------|
| 能力 | 总结/联网/对白 → **双人播客**（模型编排） | **逐句合成**，文本即所读 |
| 接口 | WebSocket `podcasttts` | HTTP/WebSocket V3 合成 |
| 典型用途 | 长文/链接听播客 | 口播稿精确对齐画面 |

## 故障排除

- **401 `requested grant not found`**：常见是把控制台里 API Key 的 **显示名**（如 `api-key-202605…`）误填成 `VOLCENGINE_PODCAST_APP_ID`。应使用 **`VOLCENGINE_PODCAST_API_KEY=`「复制」出来的密钥**（常为 UUID）；改完后对 Windows 建议执行 `sync-user-env-from-local.ps1 -ResetFirst` 清掉 User 里残留的错误 APP_ID。自检：`python skills/volc-podcast-tts/scripts/handshake_check.py` 应打印 `OK handshake`。
- **401（其它）**：再核对旧版 **数字 APP ID + Access Token** 是否与 FAQ 一致。
- **建连非 200**：检查鉴权方式是否与新/旧控制台一致、播客是否开通、`X-Api-Resource-Id`。
- **收不到音频 / 长时间卡住**：文档写明 **363 PodcastEnd 可不返回**，不能只靠单一事件收尾。客户端行为：**合成阶段**用「墙钟 `max_stream_sec`（默认 `--timeout`）」与 **`recv_idle_sec`** 合成单次 `recv` 超时（取二者剩余较短），避免永久阻塞；**action=3** 在收到与 `nlp_texts` 条数一致的 `ROUND_END` 后即 `FinishSession`；**FinishSession / FinishConnection** 各有 **`finish_phase_sec`** 上限，`finish_connection` 遇提前断连仅告警不写 fatal。**调试**：`--meta-out meta.json` 看 `completed_via`（如 `nlp_round_ends`、`podcast_end`、`recv_idle`、`wall_clock`）与 `warnings`。
- **安全审核 50302102**：换素材或缩短输入，见文档错误码节。

## 实现说明

本 skill 用最小 Python 依赖实现二进制帧打包/解析；若官方后续调整 event 布局，优先以控制台提供的 **Python 示例** 为准做对齐。
