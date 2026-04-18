# MarkItDown (Microsoft) — 开源文档转 Markdown 工具

> 来源：[microsoft/markitdown](https://github.com/microsoft/markitdown) · PyPI [`markitdown`](https://pypi.org/project/markitdown/)
> 作者：Microsoft AutoGen Team
> 发布日期：2024
> 收录日期：2026-04-12
>
> 口语或检索里常被说成「MakeItDown」；**正式项目名与 PyPI 包名为 [MarkItDown](https://github.com/microsoft/markitdown)**（mark-it-down）。

**权威入口**：[microsoft/markitdown](https://github.com/microsoft/markitdown) · 许可证 **MIT** · 维护方标注为 **AutoGen Team**（见仓库 README 徽章）。

**怎么用（分步操作）**：见 `knowledge/playbooks/use-microsoft-markitdown.md`（虚拟环境、安装选型、CLI、Python API、MCP、Docker、排障）。

---

## 1. 定位

轻量 **Python** 工具：把多种文件与 Office 文档转为 **Markdown**，供 LLM、RAG、文本分析管线使用。设计上类似 [textract](https://github.com/deanmalmgren/textract)，但强调保留标题、列表、表格、链接等结构。

**前置条件**：Python **3.10+**。

---

## 2. 支持格式（官方 README 列举）

包括但不限于：PDF、PowerPoint、Word、Excel、图片（EXIF / OCR）、音频（元数据与转写）、HTML、CSV / JSON / XML、ZIP（遍历内容）、YouTube URL、EPub 等。

---

## 3. 安装与最简用法

```bash
pip install 'markitdown[all]'
markitdown path-to-file.pdf -o document.md
```

可选依赖可按格式分包安装（如 `markitdown[pdf,docx,pptx]`）；完整列表见仓库 README（`[all]`、`[pdf]`、`[docx]`、`[pptx]`、`[xlsx]`、`[xls]`、`[outlook]`、`[az-doc-intel]`、`[audio-transcription]`、`[youtube-transcription]` 等）。

**源码安装**（节选）：

```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

---

## 4. 生态与集成

| 能力 | 说明 |
|------|------|
| **MCP** | 提供 **Model Context Protocol** 服务，便于接入 Claude Desktop 等；见仓库内 [`packages/markitdown-mcp`](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)。 |
| **插件** | 第三方插件默认关闭；`markitdown --list-plugins`、`--use-plugins`。社区插件可搜 GitHub 标签 `#markitdown-plugin`；示例与开发见 `packages/markitdown-sample-plugin`。 |
| **markitdown-ocr** | 独立包，为 PDF/DOCX/PPTX/XLSX 等增加基于 LLM Vision 的 OCR；见 `packages/markitdown-ocr`。 |
| **Azure** | 可选用 **Azure Document Intelligence** 做转换（CLI `-d`、endpoint 等；详见官方 README）。 |

---

## 5. 版本注意

0.0.1 → 0.1.0 起有 **破坏性变更**：依赖改为可选特性组、`DocumentConverter` 面向**二进制流**、`convert_stream()` 行为变更等。若只使用 `MarkItDown` 类或 CLI 按官方示例调用，通常不受影响；细节以 [README](https://github.com/microsoft/markitdown/blob/main/README.md) 为准。

---

## 6. 与本知识库的关系

- **概念与索引**：本文档。
- **落地使用**：`knowledge/playbooks/use-microsoft-markitdown.md`。
- **选项与边界情况**：始终以 [官方 README](https://github.com/microsoft/markitdown/blob/main/README.md) 为准（版本更新最快）。
