# video-pipeline.step.yaml — 视频制作混合编排流水线

WAV → 校对 SRT → 拆分话题 → 生成幻灯 → 渲染 MP4（带烧录字幕）的端到端 `/step` 流水线。

## 工作原理

将此流水线与 `/step` 命令配合使用（定义见 `.claude/commands/step.md`）。

- **确定性步骤**（script）：环境检查、Whisper 转写、繁简转换、格式校验、渲染、封面 — 全部自动执行，无需人工干预。
- **决策步骤**（reasoning）：SRT 校对、话题拆页、**内容板生成**、**视觉细化** — 由 Agent 执行语义推理，**关键节点需用户确认**后继续。

### 设计原则：能编码的固化，只留创意给推理

本流水线的分层逻辑遵循一条铁律：**凡是能用规则、脚本或配置表达的东西，就不应该放进 reasoning step 里消耗 token 和等待时间。**

| 层级 | 应该放在哪里 | 典型例子 |
|------|-------------|---------|
| 数据采集 / 格式转换 / 计算 | **script**（确定性脚本） | WAV 切片、SRT→ASS、时长校验、字段填充 |
| 语义理解、边界判定 | **reasoning**（AI 推理） | 话题拆页、错字校对、锚文字选取 |
| 视觉表现、创意排版 | **reasoning**（AI 推理） | 布局选择、SVG 图形、配色组合、装饰元素 |

具体含义：

1. **script 层负责"怎么跑"**：ffmpeg 命令、文件搬运、数值计算、格式校验。这部分一旦跑通就写入代码，后续不再变动。
2. **reasoning 层负责"做什么"和"怎么好看"**：拆页边界、文字精炼、视觉设计。这部分保留给 Agent，因为依赖语义理解和审美判断，无法简单规则化。
3. **`presentation.html` 是创意的保留地**：它不被硬编码进模板引擎，而是交由 Step 9 的视觉细化自由发挥。这是有意为之的设计——如果把它模板化，会牺牲每次生产的视觉差异性。

这条原则指导着流水线的演化方向：当某个 reasoning step 中的逻辑被发现是稳定可规则化的（例如"字幕超过 18 字则拆分"、"时长低于 0.8s 则标记警告"），就应该下沉到 script 工具中执行，只把真正需要智识的决策留给 AI。

## 快速开始

### 前提条件

确保 `html-video-from-slides` skill 已安装依赖：

```bash
cd skills/html-video-from-slides
npm install
npx playwright install chromium
pip install faster-whisper huggingface_hub opencc-python-reimplemented
```

### 目录结构要求

素材目录（`PROJECT_DIR`）至少包含一个 `.wav` 文件。可选配置 `video-input.json`：

```
my-video-project/
├── voiceover.wav          # 口播（必须有且仅有一个，除非 video-input.json 指定）
└── video-input.json       # 可选：模型、阈值、字幕样式、替换规则...
```

### 完整流程（从头开始）

```bash
# 1. 切换到仓库根目录
# 2. 指定素材目录
export PROJECT_DIR=/path/to/my-video-project

# 3. 运行完整流水线
/step --plan_file skills/html-video-from-slides/video-pipeline.step.yaml 端到端视频制作
```

或使用更简洁的方式（Claude Code 会自动解析 `--plan_file`）：

```
/step run --plan_file skills/html-video-from-slides/video-pipeline.step.yaml
```

## 断点恢复：从不同阶段开始

这是本流水线的核心价值 — 你可以任意步骤断点恢复，无需从头再来。

| 你的现状 | 入口命令 | 说明 |
|---------|---------|------|
| 刚录完 WAV，什么都没有 | `--from_step 1`（默认） | 完整流程 |
| 环境已确认，想跳过检查 | `--from_step 2` | 跳过 preflight，直接 Whisper |
| **已有校对后的 `sub.srt`** | `--from_step 5` | 跳过转写+校对，从拆页开始 |
| **已有拆页确认，想重新出内容** | `--from_step 8` | 从内容板生成开始 |
| **已有内容板，想重做视觉** | `--from_step 9` | 只跑视觉细化（Step 9 专门负责布局、SVG、配色、装饰） |
| **已有 HTML + `wav-durations.json`** | `--from_step 11` | 只做渲染+封面+检查 |
| 渲染失败，修正后重试 | `--from_step 11` | 同上 |

示例：

```
/step run --plan_file skills/html-video-from-slides/video-pipeline.step.yaml --from_step 9
```

## 步骤详解（13 步）

| Step | 类型 | 名称 | 产出物 | 用户交互 |
|------|------|------|--------|---------|
| 1 | script | 环境预检与目录解析 | `state.json` | 无 |
| 2 | script | Whisper 转写 | `sub.srt` | 无 |
| 3 | script | 繁简转换与预处理 | 简体 `sub.srt` | 无 |
| 4 | reasoning | SRT 错字分析与校对建议 | 变更清单 + `approval-4.json` | **审阅变更清单** |
| 5 | script | 确认校对状态 | — | 无（衔接） |
| 6 | reasoning | 话题拆页与时长计算 | 大纲表 + `wav-durations-preview.json` | **审阅拆页结果** |
| 7 | script | 确认拆页状态 | — | 无（衔接） |
| 8 | reasoning | **生成内容板** | `content-slabs.json` + `wav-durations.json` | 无（纯生成） |
| 9 | reasoning | **视觉细化 → HTML** | `presentation.html` | 无（纯生成） |
| 10 | script | 格式校验 | 校验报告 | 无 |
| 11 | script | 视频渲染 | `final.mp4` | 无 |
| 12 | script | 封面生成 | `cover.png` | 无 |
| 13 | script | 最终检查与汇总 | 产出清单 | 无 |

### 为什么 Step 8 和 9 要拆开？

原来的单一 Step 8 同时做「内容精炼 + 视觉设计 + HTML 生成」，Agent 在一个 prompt 里需要同时处理语义理解（从 SRT 提取关键信息）和审美设计（选 SVG、配色、布局），容易顾此失彼。

拆开后：

| 步骤 | 关注点 | 重跑成本 |
|------|--------|---------|
| **Step 8** | 内容正确性：标题/正文精炼、.wa 锚文字、时长确认 | 低（只改文字，不改视觉） |
| **Step 9** | 视觉表达：布局结构、SVG 图形、配色组合、装饰元素 | 中（只改 HTML 结构，不改内容） |

**典型场景**：如果内容对了但视觉不好看（比如布局太单调、SVG 选得不合适），直接 `--from_step 9` 重跑视觉细化，内容板保持不变。

## 人工确认机制

Step 4 和 Step 6 是**强制确认断点**：

1. Agent 分析并产出建议后，会在 `.step/video-pipeline/approval-{N}.json` 写入 `pending` 状态
2. 你审阅 Agent 的分析结果，确认无误后，可以：
   - **直接修改文件**：例如直接 Edit `sub.srt`，然后删除 approval 文件，再 `--from_step 5`
   - **认可无需修改**：直接删除 approval 文件，再 `--from_step 5`
   - **认可变更**：如果 Agent 产出了需要采纳的变更，由 Agent 或直接手动应用后，再 `--from_step 5`

这种设计的用意：确认动作本身不可编码（它依赖语义判断），但确认前后的衔接步骤全部自动化。

## 新增中间产物：`content-slabs.json`

Step 8 产出，Step 9 消费。它是**内容层和视觉层之间的契约**：

```json
{
  "pageCount": 12,
  "theme": "mobile-tech",
  "pages": [
    {
      "id": 0,
      "role": "cover",
      "layout": "Cover",
      "title": "...",
      "body": "...",
      "wa": "锚文字",
      "srtRange": [1, 2],
      "durationSec": 7.0,
      "accentColor": "g-hi"
    }
  ],
  "layoutStats": {"Cover": 1, "Grid 2×2": 2, ...}
}
```

Step 9 只需要读取此文件 + 模板/CSS/SVG 参考，即可独立完成视觉组装，不再回头读 SRT。

## 配置注入

所有 Whisper 参数、字幕样式、替换规则统一从素材目录的 `video-input.json` 读取。step 1 会读取该文件并持久化到 `state.json`，后续步骤共用同一配置，避免重复传参。

如需中途修改配置（例如换 whisperModel），直接修改 `video-input.json`，然后 `--from_step 2` 重跑转写。

## 故障排查

| 问题 | 处理 |
|------|------|
| strictSubtitles 触发中止 | 修改 `video-input.json`：增大 `maxSubtitleGapSec`、提高 `noSpeechThreshold`、换更大模型，然后 `--from_step 2` |
| 格式校验失败（时长不匹配） | 回到 Step 8 修正内容板，或回到 Step 6 重新拆页 |
| 渲染失败 | 检查 `presentation.html` 是否有 `go(n)`、CSS 路径是否正确，修正后 `--from_step 11` |
| 封面缺失 | 在 `PROJECT_DIR` 下放 `cover.html` 或 `cover_h.html`，再 `--from_step 12` |
| 内容对但视觉不好看 | `--from_step 9` 重跑视觉细化，内容板保持不变 |
| 视觉对但内容有错 | `--from_step 8` 重跑内容板，视觉会跟着重做 |

## 与单个 skill 的区别

| | 单独跑 skill | `/step` 流水线 |
|---|---|---|
| 状态管理 | 无，靠记忆 | 每步状态落盘到 `state.json` |
| 断点恢复 | 需手动记做到哪了 | `--from_step N` 任意恢复 |
| 自动降级 | 无 | script 步骤自动捕获 exit code，给出提示 |
| 用户确认 | implicit（Agent 自己判断） | explicit（approval-N.json 强制 gate） |
| 重跑成本 | 容易从头再来 | 精确恢复，只跑变化的步骤 |
| 内容/视觉解耦 | 混在一起 | Step 8 内容板锁定后，Step 9 可独立重跑 |

## 自定义扩展

如需增加一个 step（例如 Step 10.5：Agent 视觉检查画面覆盖率），在 YAML 中插入一个 `reasoning` 类型步骤即可。脚本步骤和推理步骤的数据传递通过 `output_file` 自动完成。
