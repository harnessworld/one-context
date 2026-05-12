# 幻灯重做简报（action=0 新口播 vs 当前 deck）

> 真源口播：`production/subtitles/sub.srt`（约 8m40s，与 `01-script.md` 字句已不一致）。  
> 当前 HTML：`production/slides/presentation.html`（Open Design 简版 + `../media/wechat-article/img-*.jpg`）。

## 1. 叙事变了什么（对改 PPT 的影响）

| 维度 | 旧稿（`01-script.md`） | 新音频（字幕概括） |
|------|------------------------|---------------------|
| 开篇 | OpenAI 拉多家高管、三条结论点名 | 泛问「强模型为何不等于顺利用在日常」→ 再落到 capability gap |
| 结构 | 「今夜按五条顺序」目录感强 | 对话推进：gap → 三阶段+监督 → 文化先于工具 → … → checklist → 英文收束 → 感谢收听 |
| 收口 | 偏「自检一句英文」 | 同样保留 **redesign vs layering** + **PDF leadership checklist**，但前面多了一段「从文化到治理…每一步」总结 |

结论：**版式骨架可沿用**（封面 / gap / 5 pattern / checklist / 收口），但**每页大标题、要点、`.wa` 锚字**应改成与 **字幕里实际用词** 同向（否则 `wav-auto` 与观众读屏都会漂）。字幕里公司名多为 Whisper 误听（如 Philipus / Miracle / Jet Prince / Chris Kent），**画面上仍写正确专名**。

## 2. 建议的页面级改版方向（仍 10 页时）

| 页 | 当前角色 | 建议 |
|----|-----------|------|
| s0 封面 | 强调「企业规模化 AI 五条」+ 六家 logo 感 | 可改为**问题导向主标题**（与字幕 1–4 条一致）；右侧 `img-01`：若仍是微信头图且与「强模型≠落地」弱相关，**换官网/PDF 视觉或抽象主视觉**。 |
| s1 目录 | 「今夜目录」五条英文列 | 音频里**没有**完整念五条菜单式目录；可改成 **「本期会走过：gap → 文化 → 治理 → …」** 极简时间线，或**删目录页**改 9 页（改页数须同步 `wav-durations.json` 长度与重跑 `wav`）。 |
| s2 Reality | capability gap + 四格要点 | 字幕用较多时间讲 gap 根因与**三阶段+人不卸责**；四格文案建议**对齐 #20–#30 条**措辞。 |
| s3 Culture + Philips | `img-02` | 案例仍对；**口播是「7 万员工、高管培训、真实场景」**——数字与流程可提到卡上；Patrick「文化·好奇·敢试」仍适用。图**保留**。 |
| s4 Governance + BBVA | `img-03` | 秘鲁助手、7 分半→1 分、12 万 Enterprise 仍一致；**「治理作赋能者」**叙事对齐字幕「法务合规安全 IT 一开始参与」。图**保留**。 |
| s5 Ownership | 双栏 + 数字条，**无大图** | 口播 **Mirakl + Scania + 一串数字** 很重；若 `wechat-article` 有 **Mirakl/物流/制造** 类图可加一侧图，否则维持信息图但**加一条「Scania 嵌入工程到售后」**可见字。 |
| s6 Quality + Scout24 | `img-05` | Scout24、评测、不达标延期仍一致；字幕提 **OpenAI Evals 思路**——卡上可写「Evals 类评测」避免听成别词。图**保留**。 |
| s7 Protecting + JetBrains | `img-06` | 口播 **JetBrains + 判断质量 + 混合工作流 + Kris Kang 安全/可读/可维护**；注意字幕误听 **Jet Prince / Chris Kent**，画面写对即可。图**保留**。 |
| s8 Checklist | 四格 + 英文 | 与字幕 **重做流程 vs 贴补丁 / PDF checklist** 一致，**少改结构**。 |
| s9 收口 | 英文问句 | 与字幕 **redesign vs layering** 一致；可删「感谢收听」类字（口播已有）避免抢镜。 |

## 3. 配图资产核对（`../media/wechat-article/`）

| 文件 | 当前出现 | 与现口播是否仍匹配 | 备注 |
|------|-----------|---------------------|------|
| `img-01.jpg` | 封面右侧 | **待你肉眼定**：若仍是转载微信首图，可能偏「文章配图」而非本集问题陈述。 | 可换 PDF 封面风或纯色+logo。 |
| `img-02.jpg` | Philips | **匹配**（素养、高管、真实场景）。 | 确认版权/清晰度。 |
| `img-03.jpg` | BBVA | **匹配**（银行、治理、秘鲁助手）。 | 同上。 |
| `img-04.*` | **未在 deck 使用** | 若素材里有与 **Mirakl/Scania** 相关，可考虑给 s5。 | 无则维持无图栏。 |
| `img-05.jpg` | Scout24 | **匹配**（质量、评测、延期）。 | 同上。 |
| `img-06.jpg` | JetBrains | **匹配**（判断工作、代码与审查）。 | 同上。 |

## 4. 重做后的工程顺序（建议）

1. 改 `presentation.html`（或按 `skills/html-deck-layout` 重生）：**每页可见字 ≈ 字幕同段关键词**（不必逐字），并更新 `.wa`。  
2. `node cli.js timing-check --project production`（若手改 `wav-durations.json`）。  
3. `node cli.js wav --project production`（或 `wav-auto` 初稿再手修时长）。  
4. `skills/srt-proofread`：专名、数字与幻灯对齐。

## 5. 可选：`01-script.md` 怎么办

- 若以后还要 **action=0**：可把 **`01-script.md` 改成「给火山的长文素材」**（与播客允许改写一致），**另存**「定稿事实核对」在 `reference-*.md`。  
- 若改回 **action=3 念稿**：仍以 **`01-volc-dialogue.md`** 为合成输入，**`01-script.md`** 作人类讲稿与幻灯一致源。
