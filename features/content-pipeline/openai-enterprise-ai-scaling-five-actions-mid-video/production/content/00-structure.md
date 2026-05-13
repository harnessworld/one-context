# 话题大纲

**口播稿与 `node cli.js tts`：** `production/content/01-script.md` 已按 **`# 【页题】`** 分页，与 `presentation.html` 的 `s0`–`s9` 一一对应；块内勿写单独一行的 `---`（会截断该页 TTS 正文）。出处与引用只放在本大纲或 `reference-*.md`，勿写进讲稿块尾以免被念出。

**火山引擎播客 WAV（当前定版：action=0）**

- **`timing/video-input.json` → `podcastTts`**：`action: 0`，`scriptPath: content/01-script.md`（整份作**长文输入**，服务端**总结后再双人播**，口播与讲稿字句**不完全一致**）。`forceRegenerate: true` 可强制重下 WAV。
- **鉴权**：`VOLCENGINE_PODCAST_API_KEY` 或 `skills/volc-podcast-tts/local.env`。流水线 Step 1 或本机手跑示例：

```powershell
New-Item -ItemType Directory -Force -Path "features/content-pipeline/openai-enterprise-ai-scaling-five-actions-mid-video/production/media" | Out-Null
py -3 skills/volc-podcast-tts/cli.py --action 0 -i features/content-pipeline/openai-enterprise-ai-scaling-five-actions-mid-video/production/content/01-script.md -o features/content-pipeline/openai-enterprise-ai-scaling-five-actions-mid-video/production/media/voiceover.wav --format pcm --speakers zh_male_dayixiansheng_v2_saturn_bigtts,zh_female_mizaitongxue_v2_saturn_bigtts --timeout 1200 --fixed-speaker-order
```

- **若仍要「念稿不总结」**：改回 **`action: 3`**，输入 **`content/01-volc-dialogue.md`**（仅 `男：`/`女：`），并可加 `--merge-same-speaker-lines --inter-speaker-silence-ms 80`（见该文件头注释）。

**字幕（识别）**：新 WAV 落盘后，在仓库根用 Whisper **只出 SRT**（不跑幻灯对齐）：

```powershell
py -3 skills/html-video-from-slides/scripts/align_wav_slides.py --wav features/content-pipeline/openai-enterprise-ai-scaling-five-actions-mid-video/production/media/voiceover.wav --srt-out features/content-pipeline/openai-enterprise-ai-scaling-five-actions-mid-video/production/subtitles/sub.srt --srt-only --model small
```

成片（含自动估翻页 + 烧录）：`cd skills/html-video-from-slides` 后 **`node cli.js wav-auto --project …/production`**；定版翻页仍以 **`sub.srt` + `wav-durations.json` + `wav`** 为准（见下节）。

**翻页＝内容 ↔ 字幕/语音（成片真源）**

- 本选题是**播客口播 + 幻灯精炼字**，与 `wav-auto` 依赖的「口播 ≈ 页上可见字」不一致，**定版成片不要只靠 `wav-auto` 猜翻页**（易均分、与话题脱节）。
- **真源**：`production/subtitles/sub.srt` 的时间轴 + 与口播一致的讲稿分段（**action=0 时以字幕为准**，不必强绑旧 `01-script.md` 的 `# 【】`）。维护 **`timing/wav-durations.json`** 的 `slideDurationsSec`（10 项与 `s0`–`s9` 同序）：第 *i* 页时长 =「进入第 *i+1* 页首句」的首条字幕 **`start`** 减去「本页首句」的首条字幕 **`start`**；最后一页 = `voiceover.wav` 总长 − 末页首条 `start`。间隙自然归上一页。
- **成片命令**（不重跑 Whisper 时）：在 `skills/html-video-from-slides` 下执行 **`node cli.js wav --project …/production`**。需要初稿字幕时可 **`wav-auto` 一次**写出 `sub.srt`，再按上条改 `wav-durations.json`，然后一律 **`wav`** 出 `final_auto.mp4`。
- **自检**：`node cli.js timing-check --project …/production`；若报 `FLIP_AT_NEXT_WA_SENTENCE_START`，微调累计边界（见 `skills/html-video-from-slides/SKILL.md`「翻页边界语义」）。

**一手入口（优先级）**

0. **口播已换、幻灯待对齐时**：先看 **`content/02-slide-redesign-brief.md`**（新字幕 vs 当前配图与每页改版建议）。

1. 官网页：[How enterprises are scaling AI](https://openai.com/business/guides-and-resources/how-enterprises-are-scaling-ai/) — 论点与五条 pattern 的**英文原句**见 `reference-openai-guide-page.md`。  
2. PDF：[Frontiers of AI Executive Guide](https://cdn.openai.com/pdf/025ecc00-e528-48dc-95f7-90a96c7be449/frontiers-of-ai-leadership-lessons-guide.pdf) — **案例细节、指标、领导自检问题**；写口播事实层以前应先扫一遍。

**二手参考**：微信转载仅作选题线索，事实与数字以官网 + PDF 为准。

---

## 建议口播设计流程（先原文，再双人）

| 步骤 | 做什么 | 产出 |
|------|--------|------|
| 1 | 逐条对照五条 pattern，把官网**一句定义**读透（必要时中英写在侧栏） | 每条约 1–2 句「不可曲解」的核心意思 |
| 2 | 在 PDF 里为每条 pattern **认领 1 个案例 + 最多 1 个数字**（没有就不硬编） | 案例卡片（公司 / 行为 / 证据） |
| 3 | 定双人分工：**阿哲**锚定官网框架与因果关系；**小夏**负责落地案例与反差句 | 角色边界清楚，避免俩人都在讲大道理 |
| 4 | 最后一遍才做口语化、气口、钩子；钩子优先来自 **PDF diagnostic / pressure-test 问题**，而不是新造金句 | `01-script.md` 终稿 |

---

## 分段大纲（与官网五条对齐）

建议总时长 **8–12 分钟**（可按密度增减）。

| 段 | 官网锚点 | 阿哲（框架） | 小夏（证据） | 时长 |
|----|-----------|--------------|--------------|------|
| 0 | 开篇：capability gap；信任 / 自主权 / 质量 | 总论点、文档用语 | 三件事、运营层 | ~45–60s |
| 1 | Culture before tooling | 定义句 | Philips 等 | ~90–120s |
| 2 | Governance as enabler | 设计伙伴、反转 | BBVA 等 | ~90–120s |
| 3 | Ownership over consumption | 改流程 vs 消费 | Mirakl + Scania 数字 | ~90–120s |
| 4 | Quality before scale | 评测与延期 | Scout24 等 | ~90–120s |
| 5 | Protecting judgment work | 判断工作 | JetBrains + 混合工作流 | ~90–120s |
| 6 | Closing | 方向一句收束 | PDF 自检问句 | ~60–90s |

---

定稿检查：**每条口语声称**，能否在官网页或 PDF 中找到对应依据；找不到则改成泛化表述或删掉。
