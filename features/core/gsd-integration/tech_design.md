# Technical Design: GSD Integration

> **版本历史**
> - v1.0 (初始版本) — MCP Server 方案设计
> - v1.1 (当前) — 修复评审问题：CLI 入口设计、detect_workspace 实现、错误处理、安全边界、测试完整性

## 概述

本设计实现 GSD（Get Shit Done）自主编程系统与 one-context 多仓库上下文聚合器的集成，使 GSD 在执行任务时能自动获取和注入 one-context 生成的上下文。

---

## 架构分析

### GSD 关键机制

| 机制 | 说明 | 集成点 |
|------|------|--------|
| **MCP Client** | 原生支持 `.mcp.json` / `.gsd/mcp.json` 配置外部工具 | ⭐ 主要集成点 |
| **Skills** | Agent Skills 标准，`~/.agents/skills/` 或项目 `.agents/skills/` | 辅助集成点 |
| **Context Injection** | dispatch 前预置文件到 prompt | 输出消费方 |
| **PREFERENCES.md** | 支持技能发现和路由规则 | 配置层 |

### one-context 关键能力

| 能力 | CLI 命令 | 输出 |
|------|---------|------|
| 上下文导出 | `onecxt context export <workspace>` | JSON / Markdown |
| Token 压缩 | `--compress --target-tokens N` | 压缩后的上下文 |
| Workspace 管理 | `onecxt workspace list/show` | workspace 元数据 |

### 与现有代码的契合度

| 设计模块 | 现有代码位置 | 复用策略 |
|----------|-------------|----------|
| `export_context` | `one_context/context/__init__.py` | 直接调用 `build_workspace_context` / `render_workspace_context` |
| `workspace list/show` | `one_context/cli.py` `_cmd_workspace_list/show` | 直接复用，MCP tool 返回相同数据结构 |
| `apply_context_compression` | `one_context/context/__init__.py` | 复用，允许 GSD 特定参数 |
| Adapter 模式 | `one_context/adapters/*.py` | 参考 Hermes adapter 的生成模式 |

---

## 集成方案

### 方案对比

| 方案 | 实现成本 | 维护成本 | 用户体验 | 推荐度 |
|------|---------|---------|---------|--------|
| **A. MCP Server** | 中 | 低 | 优 | ⭐⭐⭐ 推荐 |
| B. GSD Skill | 低 | 中 | 良 | ⭐⭐ 备选 |
| C. CLI Hook | 低 | 低 | 差 | ⭐ 不推荐 |

**选择方案 A（MCP Server）**：GSD 原生支持 MCP，通过 MCP 暴露 one-context 功能最自然。

---

## 详细设计

### Phase 1: MCP Server 实现

#### 1.1 one-context MCP Server

在 one-context 包中添加 MCP server 模式：

```python
# packages/one-context/one_context/mcp_server.py

"""MCP Server for one-context — enables GSD and other MCP clients to query context."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from one_context.context import build_workspace_context, render_workspace_context
from one_context.errors import ManifestError
from one_context.repos import load_repos
from one_context.root import find_root
from one_context.workspaces import load_workspaces

logger = logging.getLogger("one_context.mcp")

# MCP SDK imports (optional dependency)
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    Server = None  # type: ignore


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    Tool(
        name="list_workspaces",
        description="List available one-context workspaces with their repo counts",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="export_context",
        description="Export one-context workspace context for AI agents. Returns markdown or JSON.",
        inputSchema={
            "type": "object",
            "properties": {
                "workspace_id": {
                    "type": "string",
                    "description": "Workspace ID (case-insensitive)",
                },
                "format": {
                    "type": "string",
                    "enum": ["json", "markdown"],
                    "default": "markdown",
                    "description": "Output format",
                },
                "compress": {
                    "type": "boolean",
                    "default": False,
                    "description": "Apply token-budget compression",
                },
                "target_tokens": {
                    "type": "integer",
                    "description": "Max tokens when compressing (default: 8000)",
                },
            },
            "required": ["workspace_id"],
        },
    ),
    Tool(
        name="detect_workspace",
        description="Detect which workspace(s) a path belongs to by matching against repo paths",
        inputSchema={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Absolute or relative file/directory path",
                },
            },
            "required": ["path"],
        },
    ),
    Tool(
        name="get_workspace_summary",
        description="Get a brief summary of a workspace (repos, profiles, knowledge count)",
        inputSchema={
            "type": "object",
            "properties": {
                "workspace_id": {
                    "type": "string",
                    "description": "Workspace ID (case-insensitive)",
                },
            },
            "required": ["workspace_id"],
        },
    ),
]


# ---------------------------------------------------------------------------
# Tool handlers — reuse existing CLI logic
# ---------------------------------------------------------------------------

def _find_root() -> Path | None:
    """Find one-context root, return None if not found (don't raise)."""
    try:
        return find_root()
    except ManifestError:
        return None


def _handle_list_workspaces(root: Path) -> dict[str, Any]:
    """List workspaces — reuses logic from _cmd_workspace_list."""
    entries, _ = load_workspaces(root)
    result = []
    for e in entries:
        result.append({
            "id": e.get("id", ""),
            "name": e.get("name", ""),
            "repo_count": len(e.get("repos") or []),
        })
    return {"workspaces": result, "count": len(result)}


def _handle_export_context(
    root: Path,
    workspace_id: str,
    fmt: str = "markdown",
    compress: bool = False,
    target_tokens: int | None = None,
) -> dict[str, Any]:
    """Export context — reuses build_workspace_context and render_workspace_context."""
    try:
        data = build_workspace_context(root, workspace_id)
    except ValueError as e:
        return {"success": False, "error": str(e), "error_code": "WORKSPACE_NOT_FOUND"}

    rendered = render_workspace_context(data, fmt)

    if compress or target_tokens is not None:
        from one_context.context import apply_context_compression
        rendered = apply_context_compression(
            rendered,
            compress=compress,
            target_tokens=target_tokens,
        )

    return {
        "success": True,
        "format": fmt,
        "workspace_id": data.get("workspace", {}).get("id", workspace_id),
        "content": rendered,
        "repo_count": data.get("summary", {}).get("repo_count", 0),
    }


def _handle_detect_workspace(root: Path, target_path: str) -> dict[str, Any]:
    """Detect workspace by path — matches against workspace repo paths."""
    target = Path(target_path).expanduser().resolve()
    repo_entries, _ = load_repos(root)
    workspaces, _ = load_workspaces(root)

    # Build repo_id -> path mapping
    repo_paths: dict[str, Path] = {}
    for entry in repo_entries:
        repo_id = entry.get("id", "")
        repo_path = (root / entry.get("path", "")).resolve()
        repo_paths[repo_id] = repo_path

    # Check which workspaces contain repos that match the target path
    matched_workspaces: list[dict[str, Any]] = []
    for ws in workspaces:
        ws_id = ws.get("id", "")
        ws_name = ws.get("name", "")
        ws_repos = ws.get("repos") or []

        for repo_id in ws_repos:
            if repo_id not in repo_paths:
                continue
            repo_path = repo_paths[repo_id]
            try:
                # Check if target is inside or exactly this repo
                target.relative_to(repo_path)
                matched_workspaces.append({
                    "id": ws_id,
                    "name": ws_name,
                    "matched_repo": repo_id,
                    "match_type": "inside" if target != repo_path else "exact",
                })
                break  # One match per workspace is enough
            except ValueError:
                continue  # target not under this repo

    return {
        "target_path": str(target),
        "matched_workspaces": matched_workspaces,
        "count": len(matched_workspaces),
        "suggestion": matched_workspaces[0]["id"] if matched_workspaces else None,
    }


def _handle_get_workspace_summary(root: Path, workspace_id: str) -> dict[str, Any]:
    """Get workspace summary — lightweight version of export_context."""
    try:
        data = build_workspace_context(root, workspace_id)
    except ValueError as e:
        return {"success": False, "error": str(e), "error_code": "WORKSPACE_NOT_FOUND"}

    ws = data.get("workspace", {})
    return {
        "success": True,
        "id": ws.get("id", ""),
        "name": ws.get("name", ""),
        "description": ws.get("description", ""),
        "repos": [r.get("id") for r in data.get("repos", [])],
        "profiles": [p.get("id") for p in data.get("profiles", [])],
        "knowledge_count": data.get("summary", {}).get("knowledge_count", 0),
    }


# ---------------------------------------------------------------------------
# MCP Server setup
# ---------------------------------------------------------------------------

def create_mcp_server() -> "Server":
    """Create and configure the MCP server instance."""
    if not MCP_AVAILABLE:
        raise RuntimeError("MCP SDK not installed. Install with: pip install 'one-context[mcp]'")

    app = Server("one-context")

    @app.list_tools()
    async def list_tools():
        return TOOLS

    @app.call_tool()
    async def call_tool(name: str, arguments: dict):
        root = _find_root()
        if root is None:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Not in a one-context project (no meta/repos.yaml found)", "success": False}),
            )]

        result: dict[str, Any]
        if name == "list_workspaces":
            result = _handle_list_workspaces(root)
        elif name == "export_context":
            result = _handle_export_context(
                root,
                workspace_id=arguments.get("workspace_id", ""),
                fmt=arguments.get("format", "markdown"),
                compress=arguments.get("compress", False),
                target_tokens=arguments.get("target_tokens"),
            )
        elif name == "detect_workspace":
            result = _handle_detect_workspace(root, arguments.get("path", ""))
        elif name == "get_workspace_summary":
            result = _handle_get_workspace_summary(root, arguments.get("workspace_id", ""))
        else:
            result = {"success": False, "error": f"Unknown tool: {name}", "error_code": "TOOL_ERROR"}

        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

    return app


async def run_mcp_server() -> None:
    """Run the MCP server using stdio transport."""
    if not MCP_AVAILABLE:
        print("Error: MCP SDK not installed.", file=sys.stderr)
        print("Install with: pip install 'one-context[mcp]'", file=sys.stderr)
        raise SystemExit(1)

    app = create_mcp_server()
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())
```

#### 1.2 CLI 入口 — 子命令方式

**重要**：使用子命令 `onecxt mcp` 而非 `--mcp` 标志，避免与现有 argparse 冲突。

```python
# packages/one-context/one_context/cli.py 中添加子命令

def _cmd_mcp(root: Path, args: argparse.Namespace) -> int:
    """Start the MCP server for GSD and other MCP clients."""
    import asyncio
    import sys

    try:
        from one_context.mcp_server import run_mcp_server, MCP_AVAILABLE
    except ImportError:
        print("Error: MCP SDK not installed.", file=sys.stderr)
        print("Install with: pip install 'one-context[mcp]'", file=sys.stderr)
        return 1

    if not MCP_AVAILABLE:
        print("Error: MCP SDK not installed.", file=sys.stderr)
        print("Install with: pip install 'one-context[mcp]'", file=sys.stderr)
        return 1

    try:
        asyncio.run(run_mcp_server())
    except KeyboardInterrupt:
        pass
    return 0


# 在 build_parser() 中添加子命令
def build_parser() -> argparse.ArgumentParser:
    # ... existing code ...

    # MCP subcommand
    p_mcp = sub.add_parser(
        "mcp",
        help="Start MCP server for GSD and other MCP clients (stdio transport)",
    )
    p_mcp.set_defaults(func=_cmd_mcp)

    # ... rest of parser ...
```

运行方式：

```bash
onecxt mcp                    # 启动 MCP server (stdio transport)
```

MCP 配置文件 `.mcp.json`：

```json
{
  "mcpServers": {
    "one-context": {
      "command": "onecxt",
      "args": ["mcp"],
      "description": "one-context: multi-repo context aggregation for AI agents"
    }
  }
}
```

#### 1.3 错误处理规范

所有 MCP tool 返回统一的 JSON schema：

```python
# 成功响应
{
    "success": true,
    "workspace_id": "backend-api",
    "content": "...",
    "repo_count": 3
}

# 错误响应
{
    "success": false,
    "error": "Unknown workspace id: 'nonexistent'",
    "error_code": "WORKSPACE_NOT_FOUND"
}

# 错误码定义
ERROR_CODES = {
    "NOT_ONECONTEXT_ROOT": "Not in a one-context project",
    "WORKSPACE_NOT_FOUND": "Unknown workspace id",
    "INVALID_PATH": "Path does not exist or is not accessible",
    "TOOL_ERROR": "Internal tool execution error",
}
```

---

### Phase 2: GSD Skill 实现

作为 MCP 的补充，提供 research phase 的自动上下文获取：

#### 2.1 Skill 目录结构

```
~/.agents/skills/one-context/
  SKILL.md
  scripts/
    detect-and-export.sh
```

#### 2.2 SKILL.md 内容

```markdown
---
name: one-context
description: Auto-inject one-context workspace context during research phase
triggers:
  - when: starting research in a one-context umbrella project
  - when: working with multi-repo codebase
---

# one-context Integration

When working in a one-context umbrella project, automatically fetch and inject relevant context.

## Trigger Detection

Check if current directory has one-context markers:
- `meta/repos.yaml` exists
- `meta/workspaces.yaml` exists
- `.onecontext` marker file

## Workflow

1. Run `onecxt workspace list` to see available workspaces
2. If workspace_id is known or can be detected:
   - Run `onecxt context export <workspace_id> --compress --target-tokens 8000`
   - Inject the output into research context
3. If unclear, ask user which workspace to use

## MCP Tools Available

When the one-context MCP server is configured, use:
- `mcp_call(server="one-context", tool="list_workspaces", args={})`
- `mcp_call(server="one-context", tool="export_context", args={"workspace_id": "..."})`

## Token Budget

Default: 8000 tokens for context export
Adjust based on GSD token profile:
- minimal: 4000 tokens
- balanced: 8000 tokens
- comprehensive: 16000 tokens
```

#### 2.3 检测脚本

```bash
#!/bin/bash
# scripts/detect-and-export.sh

set -e

# 检测 one-context umbrella
if [ ! -f "meta/repos.yaml" ]; then
    echo "Not in a one-context umbrella project"
    exit 0
fi

# 获取 workspace 列表（使用 JSON 格式）
WORKSPACES=$(onecxt workspace list --format json 2>/dev/null || onecxt workspace list 2>/dev/null | awk -F'\t' '{print $1}')
COUNT=$(echo "$WORKSPACES" | wc -l | tr -d ' ')

if [ "$COUNT" -eq 0 ]; then
    echo "No workspaces defined"
    exit 0
elif [ "$COUNT" -eq 1 ]; then
    WORKSPACE_ID=$(echo "$WORKSPACES" | head -1)
else
    # 多个 workspace 时输出列表让用户选择
    echo "Multiple workspaces available:"
    echo "$WORKSPACES" | while read -r line; do
        echo "  - $line"
    done
    exit 1
fi

# 导出上下文
onecxt context export "$WORKSPACE_ID" --compress --target-tokens 8000
```

---

### Phase 3: 便捷 CLI 命令

#### 3.1 `onecxt gsd-init`

生成 GSD 集成所需配置：

```python
# packages/one-context/one_context/commands/gsd.py

import json
from datetime import datetime
from pathlib import Path


def gsd_init(root: Path, args) -> int:
    """Generate GSD integration files."""
    mcp_config = {
        "mcpServers": {
            "one-context": {
                "command": "onecxt",
                "args": ["mcp"],
                "description": "one-context: multi-repo context aggregation"
            }
        }
    }

    # 检查 .mcp.json 是否存在
    mcp_path = root / ".mcp.json"
    if mcp_path.exists():
        existing = json.loads(mcp_path.read_text())
        if "one-context" in existing.get("mcpServers", {}):
            print("MCP config for one-context already exists in .mcp.json")
        else:
            existing.setdefault("mcpServers", {})["one-context"] = mcp_config["mcpServers"]["one-context"]
            mcp_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n")
            print("Updated .mcp.json with one-context MCP server")
    else:
        mcp_path.write_text(json.dumps(mcp_config, indent=2, ensure_ascii=False) + "\n")
        print("Created .mcp.json with one-context MCP server")

    # 生成 .gsd/PREFERENCES.md 片段（如果 .gsd 目录存在）
    gsd_dir = root / ".gsd"
    if gsd_dir.exists():
        prefs_path = gsd_dir / "PREFERENCES.md"
        prefs_content = f"""\
# GSD Preferences

---
version: 1
skill_discovery: auto
always_use_skills:
  - one-context
token_profile: balanced
---

## one-context Integration

This project uses one-context for multi-repo context aggregation.

### Available MCP Tools

- `mcp_call(server="one-context", tool="list_workspaces")`
- `mcp_call(server="one-context", tool="export_context", args={{"workspace_id": "..."}})`
- `mcp_call(server="one-context", tool="detect_workspace", args={{"path": "..."}})`

### Token Budget Profiles

| Profile | Tokens | Use Case |
|---------|--------|----------|
| minimal | 4000 | Quick tasks, limited context |
| balanced | 8000 | Default, most tasks |
| comprehensive | 16000 | Complex multi-repo work |

### Refresh Context

Run `onecxt context export <workspace> --compress --target-tokens 8000` to regenerate.
"""
        if not prefs_path.exists():
            prefs_path.write_text(prefs_content)
            print("Created .gsd/PREFERENCES.md with one-context integration")
        else:
            print(".gsd/PREFERENCES.md already exists, skipping")

    print("\nNext steps:")
    print("  1. Restart GSD to load the MCP server")
    print("  2. Run `mcp_servers` in GSD to verify connection")
    print("  3. Start a task and one-context will auto-inject context")
    return 0


def gsd_export(root: Path, args) -> int:
    """Export context optimized for GSD injection."""
    from one_context.context import build_workspace_context, render_workspace_context, apply_context_compression

    workspace_id = args.workspace_id
    token_profile = args.token_profile

    TOKEN_BUDGETS = {
        "minimal": 4000,
        "balanced": 8000,
        "comprehensive": 16000,
    }

    target_tokens = TOKEN_BUDGETS.get(token_profile, 8000)

    try:
        data = build_workspace_context(root, workspace_id)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    rendered = render_workspace_context(data, "markdown")
    compressed = apply_context_compression(rendered, compress=True, target_tokens=target_tokens)

    # GSD-friendly header
    header = f"""\
<!--
GSD Context Injection
Workspace: {data.get('workspace', {}).get('id', workspace_id)}
Token Budget: {target_tokens}
Generated: {datetime.now().isoformat()}
To refresh: onecxt gsd-export {workspace_id} --token-profile {token_profile}
-->

"""
    print(header + compressed, end="")
    return 0
```

CLI 命令注册：

```python
# 在 cli.py 的 build_parser() 中添加

# gsd 子命令
p_gsd = sub.add_parser("gsd", help="GSD integration commands")
gsd_sub = p_gsd.add_subparsers(dest="gsd_command", required=True)

# gsd init
p_gsd_init = gsd_sub.add_parser("init", help="Initialize GSD integration (create .mcp.json)")
p_gsd_init.set_defaults(func=_cmd_gsd_init)

# gsd export
p_gsd_export = gsd_sub.add_parser(
    "export",
    help="Export workspace context for GSD (markdown, compressed)",
)
p_gsd_export.add_argument("workspace_id", metavar="WORKSPACE_ID", help="Workspace id")
p_gsd_export.add_argument(
    "--token-profile",
    choices=["minimal", "balanced", "comprehensive"],
    default="balanced",
    help="Token budget profile (default: balanced = 8000 tokens)",
)
p_gsd_export.set_defaults(func=_cmd_gsd_export)
```

使用示例：

```bash
# 初始化 GSD 集成
onecxt gsd init

# 导出上下文（不同 token 预算）
onecxt gsd export backend-api                    # 8000 tokens
onecxt gsd export backend-api --token-profile minimal      # 4000 tokens
onecxt gsd export backend-api --token-profile comprehensive  # 16000 tokens
```

---

## 安全边界设计

### MCP 访问范围

MCP Server 只暴露以下功能，**不提供**任意文件访问：

| 功能 | 访问范围 | 风险等级 |
|------|----------|----------|
| `list_workspaces` | 仅读取 `meta/workspaces.yaml` | 低 |
| `export_context` | 仅聚合已注册的 knowledge 路径 | 低 |
| `detect_workspace` | 仅匹配 `meta/repos.yaml` 中的路径 | 低 |
| `get_workspace_summary` | 仅读取元数据 | 低 |

### 路径安全

```python
# mcp_server.py 中的路径校验
def _validate_path(root: Path, target: Path) -> bool:
    """Ensure target path is within one-context root or registered repos."""
    try:
        target.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        # Check if it's under a registered repo
        repo_entries, _ = load_repos(root)
        for entry in repo_entries:
            repo_path = (root / entry.get("path", "")).resolve()
            try:
                target.resolve().relative_to(repo_path)
                return True
            except ValueError:
                continue
        return False
```

### 敏感信息过滤

MCP Server **不会**暴露：
- `.env` 文件内容
- `repos/*/` 中非 `.md` 文件的内容
- 任何包含 `secret`、`token`、`password` 的字段

---

## 性能考量

### 上下文导出性能

| 场景 | 预期耗时 | 缓解措施 |
|------|----------|----------|
| 小型 workspace (1-3 repos, <50 files) | <100ms | 无需优化 |
| 中型 workspace (3-10 repos, 50-200 files) | 100ms-500ms | 可接受 |
| 大型 workspace (10+ repos, 200+ files) | 500ms-2s | 压缩时使用流式处理 |

### 未来优化方向（Phase 1 不实现）

```python
# 可选：异步导出支持（保留接口）
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "export_context" and arguments.get("async"):
        # 返回 task_id，客户端轮询结果
        return {"task_id": "xxx", "status": "pending"}
```

### Token 压缩性能

当前 `apply_context_compression` 使用简单字符截断，开销可忽略。如需智能压缩：

- 可替换为 LLM-based 压缩（需额外 token 成本）
- 可缓存最近导出结果（需考虑时效性）

---

## GSD 版本兼容策略

### 版本检测

GSD 更新频繁，MCP 协议可能变化。推荐策略：

```bash
# 用户文档中说明
gsd --version  # 确认 >= 2.67.0
```

### 兼容性矩阵

| one-context 版本 | GSD 版本 | 状态 |
|------------------|----------|------|
| 0.5.0+ | >= 2.67.0 | ✅ 支持 MCP |
| 0.5.0+ | < 2.67.0 | ❌ 不支持（无 MCP，需用 CLI 备用方案） |

### 降级方案

如果 MCP 不可用，用户仍可使用 CLI 方式：

```bash
# 备用：直接导出到文件
onecxt context export backend-api --format markdown > .gsd/context.md

# GSD 手动加载上下文
gsd new-feature --context .gsd/context.md
```

---

## 数据流

```
┌─────────────────────────────────────────────────────────────────┐
│                         GSD Auto Mode                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Research Phase                                                 │
│  ┌─────────────────┐                                           │
│  │ one-context     │ (if .mcp.json configured)                 │
│  │ MCP Tool        │─────────────────────┐                     │
│  └─────────────────┘                     │                     │
│                                          ▼                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ mcp_call("one-context", "export_context",              │   │
│  │          {"workspace_id": "backend-api",               │   │
│  │           "compress": true,                            │   │
│  │           "target_tokens": 8000})                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Markdown context (~8000 tokens)                        │   │
│  │ - repos overview                                        │   │
│  │ - workspace tasks                                       │   │
│  │ - relevant knowledge                                    │   │
│  │ - profile rules                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  Context Injection → Dispatch Prompt                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Token 预算分配

GSD 总上下文预算通常为 200k tokens（Claude），分配策略：

| 场景 | one-context 占用 | 剩余给代码/指令 |
|------|-----------------|---------------|
| minimal | 4000 (2%) | 196k |
| balanced | 8000 (4%) | 192k |
| comprehensive | 16000 (8%) | 184k |

建议默认使用 `balanced` (8000 tokens)，用户可通过 `.gsd/PREFERENCES.md` 调整。

---

## 文件清单

| 文件 | 作用 | 优先级 | 状态 |
|------|------|--------|------|
| `one_context/mcp_server.py` | MCP server 实现（新建） | P0 | 待实现 |
| `one_context/commands/gsd.py` | GSD 便捷命令（新建） | P1 | 待实现 |
| `one_context/cli.py` | 添加 `mcp` 和 `gsd` 子命令 | P0 | 待修改 |
| `pyproject.toml` | 添加 `mcp` 可选依赖 | P0 | 待修改 |
| `skills/one-context/SKILL.md` | GSD skill 定义（新建） | P1 | 待实现 |
| `skills/one-context/scripts/detect-and-export.sh` | 检测脚本（新建） | P2 | 待实现 |
| `docs/gsd-integration.md` | 使用文档（新建） | P1 | 待实现 |
| `tests/test_mcp_server.py` | MCP server 单元测试（新建） | P0 | 待实现 |

---

## 依赖

### Python 依赖

```toml
# pyproject.toml
[project.optional-dependencies]
mcp = [
    "mcp>=1.0.0",
]
```

安装方式：

```bash
pip install "one-context[mcp]"
```

### 外部依赖

- **GSD v2.67+** (支持 MCP client) — 验证方式：`gsd --version`
- **Node.js 22+** (GSD 运行时)

---

## 风险与缓解

| 风险 | 影响 | 缓解措施 | 实现阶段 |
|------|------|----------|----------|
| GSD API 变更 | Skill/MCP 调用失效 | 版本检测 + 文档说明降级方案 | Phase 1 |
| Token 超支 | 上下文被截断 | 严格压缩 + `--token-profile` 配置 | Phase 1 |
| MCP 连接失败 | 功能不可用 | CLI 备用方案 (`onecxt gsd export`) | Phase 1 |
| 多 workspace 混淆 | 注入错误上下文 | `detect_workspace` + 明确 `workspace_id` 参数 | Phase 1 |
| MCP SDK 不兼容 | Server 无法启动 | 使用稳定版 `mcp>=1.0.0`，锁定版本范围 | Phase 1 |
| 性能瓶颈（大 workspace） | 响应超时 | 流式处理 + 性能测试验证 | Phase 2（可选） |
| 路径遍历攻击 | 安全漏洞 | `_validate_path` 校验 + 限制访问范围 | Phase 1 |

---

## 时间估算

| 阶段 | 工作量 | 时间 | 备注 |
|------|--------|------|------|
| Phase 1: MCP Server | 中 | 2-3 天 | 核心：mcp_server.py + CLI 集成 |
| Phase 2: GSD Skill | 低 | 0.5 天 | SKILL.md + 脚本 |
| Phase 3: CLI 命令 | 低 | 0.5 天 | gsd init/export |
| 测试 | 中 | 1 天 | 单元 + 集成 + E2E |
| 文档 | 低 | 0.5 天 | gsd-integration.md |
| **总计** | | **4-5 天** | |

---

## 后续扩展

1. **增量上下文更新** —— 检测文件变更，只更新受影响部分
2. **Workspace 智能推荐** —— 根据任务描述推荐合适的 workspace
3. **跨 workspace 合并** —— 任务涉及多个 workspace 时合并上下文
4. **GSD Dashboard 集成** —— 在 GSD visualizer 中显示 one-context 状态
5. **HTTP Transport** —— 支持 `onecxt mcp --transport http` 模式（远程访问）