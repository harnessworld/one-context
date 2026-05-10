# 配图清单（短视频横屏 1920×1080）

把下列 **PNG** 放在 **`production/media/article-images/`**（与 `presentation.html` 中 `../media/article-images/` 引用一致）。文件可由下载目录里的 `.webp` 用 Pillow 转成 PNG，并按下列文件名保存。

| 建议文件名 | 用途（对应口播/幻灯） |
|-----------|----------------------|
| `tweet-thariq-html-open-in-browser-workflow.png` | 开场钩子：Thariq 原帖截图 |
| `infographic-html-eight-information-types.png` | 「信息类型」信息图，支撑 HTML 表达力 |
| `compare-markdown-vs-html-payments-spec.png` | Markdown vs HTML 并排对比 |
| `chart-html-more-readable-markdown.png` | 可读性/密度对比示意（**当前幻灯 `s6` 已内嵌 SVG**，此 PNG 可选替换） |
| `workflow-html-tune-copy-prompt-to-claude-code.png` | 写 HTML → 调参 → 复制 → Claude Code 工作流 |
| `tweet-gordon-excalidraw-svg-agent-question.png` | 生态位：Excalidraw / SVG / Agent |
| `article-snippet-html-blocks-readable-on-phone.png` | 可选：正文块在手机上的可读性 |

## 短视频屏摄要点

- **字少图大**：单屏一行结论 + 整屏配图，`object-fit: contain`，勿拉伸变形。
- **停留时间**：证据截图（推文、对比图）每页约 **4–8s** 口播；抽象流程页可稍短。
- **安全区**：标题与 `.wa` 锚字避开底部 **约 12%**（字幕条）。
- **426 规则**：图文页与纯排版页穿插，避免连续多页只有密密麻麻小字。
