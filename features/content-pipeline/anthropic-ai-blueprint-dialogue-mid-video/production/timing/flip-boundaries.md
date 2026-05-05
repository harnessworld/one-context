# 翻页时刻 — 零模糊约定

**音轨**：`production/media/podcast-action0.wav`（实测时长 **730.143167 s**，ffprobe）  
**字幕**：`production/subtitles/sub.srt`  
**规则**：第 **n→n+1** 页翻页发生的瞬间 = 下列「进入第 n+1 页」的 **wall-clock 秒数**（从音频 **0:00** 起算）。等价于：`slideDurationsSec` 前缀和在该时刻抵达下一页。

以下时间为 **`sub.srt` 条目中打印的时间码**（与烧录字幕一致）。

| 页码 | `data-title` | 进入该页的音频时刻 | 锚点（SRT 序号 / 时间码 / 该行起始文本） |
|-----|----------------|---------------------|------------------------------------------|
| 1 | Cover | **0.000 s** | （音轨起点） |
| 2 | Trap | **42.140 s** | **#18** `00:00:42,140` → 「很多标题党啊」— 与旧版一致 |
| 3 | TrapStory | **88.920 s** | **#41** `00:01:28,920` → 「那最近 Vaibhav…」— 叙事转入推文线前，**拆 Trap 后段** 以均衡停留 |
| 4 | AgendaFour | **126.360 s** | **#55 结束瞬间**：紧随「…蓝图真正想描绘的…」— **合并原 Agenda+Four**（#56「我们来谈谈」— #58 末仍在同一认知节拍，避免 &lt;2s 闪页） |
| 5 | Managed | **130.400 s** | **#59** `00:02:10,400` → 「managed agents」 |
| 6 | WF-Agent | **215.660 s** | **#95** `00:03:35,660` → 「Agent 和 Workflow 在决策逻辑上面」 |
| 7 | Vertex | **291.260 s** | **#131** `00:04:51,260` → 「那 Cloud 和 Google Cloud…」 |
| 8 | Platform | **359.440 s** | **#164** `00:05:59,440` → 「他们最近的口号都变成了」 |
| 9 | Cold | **396.060 s** | **#186** `00:06:36,060` → 「开发者的冷静的质疑」 |
| 10 | Memory | **555.040 s** | **#293** `00:09:15,040` → 「长期记忆」 |
| 11 | Shift | **591.040 s** | **#319** `00:09:51,040` → 「好我们接着就要聚焦」 |
| 12 | Timeline | **689.000 s** | **#379** `00:11:29,000` → 「2023年」 |
| 13 | CTA | **711.040 s** | **#396** `00:11:51,040` → 「那我们来总结一下」 |

**闭合**：第 13 页持续到音轨结束 **730.143167 s**（最后一项 `slideDurationsSec` = **19.103167**）。

---

## 特别说明

1. **Trap / TrapStory**  
   旧版单页 Trap 锚点跨度约 **84 s**，观感失衡；现以 **#41** 为界拆成两页：**Trap** = 标题党 vs 图层读本（含蓝图对照）；**TrapStory** = Demo→商用 / 非无人工厂 / Vaibhav 翻译层收束。

2. **AgendaFour**  
   口播上 **#56—#58** 极短，单独「目录」+「四块拼图」两页会导致 **~1.5s + ~2.5s** 闪页；合并为一页后 **~4.04s** 仍偏短（由口播密度决定），但消除了无意义翻页。

3. **均匀时长**  
   `timing-check` 与 SRT 语义锚点**不保证**每页时长均匀；优先话题边界。若需更均匀，只能 **改口播密度** 或 **接受合并/拆分页**（见 `skills/html-video-from-slides/references/flip-boundaries.template.md` 规则 4）。

4. **与 `wav-durations.json`**  
   `slideDurationsSec[i]` = 上表「进入第 i+1 页」与「进入第 i+2 页」之差；最后一项 = 音轨尾 − 进入第 13 页时刻。

---

## 合成命令

在仓库根：

```bash
node skills/html-video-from-slides/cli.js wav --project "features/content-pipeline/anthropic-ai-blueprint-dialogue-mid-video/production"
```

先自检：

```bash
node skills/html-video-from-slides/cli.js timing-check --project "features/content-pipeline/anthropic-ai-blueprint-dialogue-mid-video/production"
```

若 `timing-check` 报 **FLIP_AT_NEXT_WA_SENTENCE_START**，再按 skill 说明调整累计边界。
