---
name: doubao-dialogue-tts
description: 火山豆包 TTS V3 — 对口播脚本进行逐句合成，支持男女人声交替对话或单人朗读，输出 WAV 音频。
triggers:
  - 豆包语音
  - 火山 TTS
  - doubao tts
  - 对白合成
  - 口播合成
version: 0.1.0
---

# doubao-dialogue-tts

火山引擎 **豆包语音合成 API V3**（HTTP/WebSocket）：**逐句念稿**，文本即所读，适用于口播稿精确对齐画面或需要严格控制每句发音的场景。与仓库内 `volc-podcast-tts`（服务端总结+双人播客编排）不同。

## 前置条件

1. 控制台开通语音合成服务：<https://console.volcengine.com/speech/service>
2. 获取鉴权信息（二选一）：
   - **新版控制台**：**API Key** → 环境变量 `VOLCENGINE_TTS_API_KEY`
   - **旧版控制台**：**APP ID** + **Access Token** → `VOLCENGINE_TTS_APP_ID` / `VOLCENGINE_TTS_ACCESS_KEY`

## 安装

```bash
cd skills/doubao-dialogue-tts
# 确保 lib/volc_v3_tts.py 存在（从技能仓库获取或自行实现）
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `VOLCENGINE_TTS_API_KEY` | 新版控制台 API Key |
| `VOLCENGINE_TTS_APP_ID` | 旧版：APP ID |
| `VOLCENGINE_TTS_ACCESS_KEY` | 旧版：Access Token |
| `VOLCENGINE_TTS_RESOURCE_ID` | 可选，默认 `volc.service_type.10051` |

可将 `local.env.example` 复制为 `local.env`（勿提交）。

## 用法

### 双人对话模式（默认）

对白脚本格式（UTF-8）：

```
男：大家好，欢迎来到本期节目。
女：今天我们要聊聊 AI 工具的使用心得。
男：首先，谁能告诉我什么是 TTS？
```

执行：

```bash
python skills/doubao-dialogue-tts/cli.py -i 对白脚本.txt -o output.wav
```

### 单人朗读模式

```bash
python skills/doubao-dialogue-tts/cli.py -i 讲稿.txt -o output.wav --mono
```

### 指定音色

```bash
# 单人模式指定音色
python skills/doubao-dialogue-tts/cli.py -i 讲稿.txt -o output.wav --mono --speaker zh_female_xiaoyi

# 双人模式指定男女音色
python skills/doubao-dialogue-tts/cli.py -i 对白.txt -o output.wav \
  --voice-male zh_male_yuanfeng \
  --voice-female zh_female_xiaoyi
```

### 调整句间停顿

```bash
# 默认 280ms，可自行调整（单位：毫秒）
python skills/doubao-dialogue-tts/cli.py -i 对白.txt -o output.wav --pause-ms 150
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `-i, --input` | 输入文本文件路径（UTF-8 编码） |
| `-o, --output` | 输出 WAV 文件路径（必需） |
| `--mono` | 单人朗读模式（不使用男/女前缀识别） |
| `--speaker` | 单人模式音色，默认 `zh_female_xiaoyi` |
| `--voice-male` | 双人模式男声音色，默认 `zh_male_yuanfeng` |
| `--voice-female` | 双人模式女声音色，默认 `zh_female_xiaoyi` |
| `--sample-rate` | 采样率，默认 24000 |
| `--pause-ms` | 对白句间静音长度（毫秒），默认 280 |
| `--resource-id` | 资源 ID，默认 `volc.service_type.10051` |
| `--api-key` | 直接传入 API Key（不推荐） |
| `--app-id, --access-key` | 旧版鉴权方式 |

## 与 volc-podcast-tts 的区别

| | doubao-dialogue-tts | volc-podcast-tts |
|--|---------------------|------------------|
| 能力 | **逐句合成**，文本即所读 | 总结/联网/对白 → **双人播客**（模型编排） |
| 接口 | HTTP/WebSocket V3 合成 | WebSocket `podcasttts` |
| 典型用途 | 口播稿精确对齐画面 | 长文/链接听播客 |
| 控制粒度 | 逐句精确控制 | 服务端自主编排 |

## 故障排除

- **提示缺少模块**：确保 `lib/volc_v3_tts.py` 存在，或安装 `pip install volcengine`
- **401 鉴权失败**：检查 API Key 是否正确（不要用密钥显示名），或核对旧版 APP_ID + Access Token
- **音色无效**：在控制台核对发音人列表，确保已开通对应音色
