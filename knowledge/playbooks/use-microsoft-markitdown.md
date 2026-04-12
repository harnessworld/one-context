# Playbook: 使用 Microsoft MarkItDown 将文件转为 Markdown

适用于需要把 PDF、Office、图片、音频等批量转为 **Markdown**（供 LLM、RAG、笔记或版本管理）的场景。项目常被称为「MakeItDown」，**正式名称为 MarkItDown**。

**前置阅读（可选）**：`knowledge/references/microsoft-markitdown.md`（项目定位与索引）。

**权威文档**（选项最全、随版本更新）：[microsoft/markitdown README](https://github.com/microsoft/markitdown/blob/main/README.md)。

---

## 1. 环境准备

1. 确认本机有 **Python 3.10+**（`python --version` 或 `py -3 --version`）。
2. **建议**使用独立虚拟环境，避免与系统或其它项目依赖冲突：

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate
```

---

## 2. 安装方式（选一种）

### 2.1 全量能力（与官方「兼容旧行为」一致）

适合：不确定会碰到哪些格式，或希望一次装全。

```bash
pip install 'markitdown[all]'
```

### 2.2 按需安装（减小体积）

适合：只处理固定几类文件。示例：仅 PDF + Word + PPT：

```bash
pip install 'markitdown[pdf,docx,pptx]'
```

可选特性组完整列表以官方 README 为准（如 `[xlsx]`、`[xls]`、`[outlook]`、`[az-doc-intel]`、`[audio-transcription]`、`[youtube-transcription]` 等）。

### 2.3 从源码可编辑安装（参与开发或追 main）

```bash
git clone https://github.com/microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

---

## 3. 命令行用法（最常用）

### 3.1 单文件输出到文件

```bash
markitdown path\to\file.pdf -o output.md
```

### 3.2 重定向到标准输出

```bash
markitdown path\to\file.pdf > output.md
```

### 3.3 从管道读入

官方示例（类 Unix）：`cat path-to-file.pdf | markitdown`。在 **Windows** 上优先使用 **文件路径 + `-o`**，避免二进制管道与 shell 差异导致问题。

### 3.4 列出 / 启用插件

```bash
markitdown --list-plugins
markitdown --use-plugins path\to\file.pdf -o out.md
```

---

## 4. Python API（脚本内调用）

最小示例（与官方 README 一致）：

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)  # 需要插件时改为 True
result = md.convert("test.xlsx")
print(result.text_content)
```

需要 **图片说明** 或兼容 OpenAI API 的客户端时，传入 `llm_client` / `llm_model`（见官方 README 图片示例）。

使用 **Azure Document Intelligence** 时在构造 `MarkItDown` 时传入 `docintel_endpoint=`，或使用 CLI 的 `-d`、`-e`（见官方文档）。

---

## 5. 与编辑器 / Agent 集成（MCP）

若希望在 **Claude Desktop** 等支持 MCP 的环境里把「转 Markdown」当工具用：使用仓库内的 **markitdown-mcp** 包，按 [packages/markitdown-mcp](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp) 说明安装与配置。具体 JSON 配置随客户端而异，以该目录文档为准。

---

## 6. 可选：Docker

在项目根目录有 `Dockerfile` 时（以你克隆的仓库为准）：

```bash
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < your-file.pdf > output.md
```

适合：不想在宿主机装 Python 依赖、或需要可复现环境。

---

## 7. 进阶：OCR 插件

需要扫描版 PDF 等更强 OCR 时，可安装 **`markitdown-ocr`**，并按 `packages/markitdown-ocr/README.md` 配置 `llm_client` / `llm_model`。无客户端时插件可能静默回退到内置转换。

---

## 8. 常见问题

| 现象 | 建议 |
|------|------|
| 某格式转换失败或缺依赖 | 对照官方 README，为该格式安装对应 extras，或直接用 `[all]`。 |
| 升级后脚本报错 | 阅读 README 中 **0.0.1 → 0.1.0** 破坏性变更；插件作者需适配流式 API。 |
| 需要企业级版面/表格识别 | 评估 **Azure Document Intelligence** 路径（需 Azure 资源与 endpoint）。 |

---

## 检查

- [ ] Python 版本 ≥ 3.10，且在已激活的 venv 中执行 `pip` / `markitdown`
- [ ] 安装 extras 与待转换文件类型一致（或已使用 `[all]`）
- [ ] 输出 `output.md` 已检查编码与表格/列表是否符合预期；不满意时尝试插件、Azure 或 OCR 路径
