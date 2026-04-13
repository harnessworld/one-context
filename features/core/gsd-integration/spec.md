---
id: gsd-integration
title: GSD 集成 — one-context 上下文注入 GSD 工作流
status: draft
category: core
primary_repo_id: one-context
owner: ""
updated: "2026-04-13"
---

# 概述

GSD-2 (Get Shit Done) 是一个强大的 AI Agent 自主编程系统，5.5k stars，基于 Pi SDK 构建，具备：
- 上下文隔离与管理（session 级清空、按需注入）
- 自主编排（auto mode、崩溃恢复、stuck detection）
- 并行里程碑执行
- Git worktree 隔离
- 成本与 token 追踪

one-context 是多仓库上下文聚合器，生成 AGENTS.md、knowledge/、workspaces 等供 AI 使用。

**问题**：GSD 的 context injection 能力很强，但缺少多仓库协调视角；one-context 提供多仓库聚合，但没有执行引擎。两者互补。

**机会**：让 GSD 在 dispatch 任务时，自动使用 one-context 生成的上下文，实现「多仓库感知的自主编程」。

# 目标与非目标

## 目标

1. **GSD 能消费 one-context 输出**
   - `onecxt context export <workspace>` 输出可作为 GSD 的 context injection 输入
   - GSD skill 自动发现并注入相关 AGENTS.md / knowledge/

2. **GSD research phase 可调用 one-context**
   - 新增 GSD skill: `one-context-context`
   - 自动检测当前目录是否在 one-context umbrella 内
   - 生成适合注入的压缩上下文

3. **工作流集成**
   - 在 one-context umbrella 项目中启动 GSD 时，自动携带上下文
   - 支持按 workspace 选择性注入

## 非目标

- 不在 one-context 内实现 GSD 的执行引擎
- 不修改 GSD 核心架构（只做 skill / hook 级集成）
- 不依赖具体 LLM provider
- 不做 Windows 之外的适配（one-context 已跨平台，GSD 也是）

# 用户与场景

## 场景 1：在 umbrella repo 中用 GSD 开发子仓库功能

```bash
cd ~/one-context  # umbrella root
onecxt workspace show backend-api
onecxt context export backend-api --format markdown --compress --target-tokens 4000 > .gsd/context/backend-api.md
gsd new-feature --context .gsd/context/backend-api.md
```

AI 收到 backend-api 相关的多仓库上下文，自主完成 feature 开发。

## 场景 2：GSD skill 自动获取 one-context

在 GSD 的 research phase，skill 自动执行：
```bash
onecxt context export <detected-workspace> --compress --target-tokens 8000
```
将输出注入 dispatch prompt。

## 场景 3：CI/CD 中 one-context + GSD

```yaml
# .github/workflows/gsd-auto.yml
- name: Export one-context
  run: onecxt context export ${{ inputs.workspace }} --format markdown > context.md
  
- name: Run GSD auto
  run: gsd auto --context context.md
```

# 验收标准

- [ ] GSD skill `one-context-context` 实现并测试通过
- [ ] `onecxt context export` 输出格式与 GSD context injection 兼容
- [ ] 文档：如何在 one-context umbrella 中使用 GSD
- [ ] POC：在一个真实 workspace 中用 GSD 完成 feature
- [ ] 可选：`onecxt gsd-context <workspace>` 便捷命令

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: one-context
- **分支 / PR**: `feature/gsd-integration`（待创建）
- **主要路径或模块**:
  - `packages/one-context/one_context/adapters/gsd.py` — GSD 适配器
  - `packages/one-context/one_context/commands/gsd_context.py` — CLI 命令
  - `skills/gsd-one-context/SKILL.md` — GSD skill 定义
  - `docs/gsd-integration.md` — 使用文档

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）: —
- **其他需求目录**: 
  - `features/core/hermes-adapter/` — 类似的 adapter 模式
  - `features/core/agent-framework/` — 智能体框架扩展点

# 开放问题

1. ~~**GSD skill 部署方式**：是放到 one-context 仓库的 `skills/` 目录，还是单独仓库？GSD 如何发现 skill？~~
   - **已解决**：放到 `skills/one-context/` 目录，用户通过 `onecxt gsd init` 生成配置。

2. ~~**Token 预算分配**：one-context 压缩后的上下文应占 GSD 上下文预算的多少比例？需要可配置吗？~~
   - **已解决**：提供 `--token-profile` 参数（minimal: 4k / balanced: 8k / comprehensive: 16k）。

3. ~~**Workspace 自动检测**：如何让 GSD skill 知道当前任务属于哪个 workspace？依赖用户指定还是自动推断？~~
   - **已解决**：MCP tool `detect_workspace(path)` 根据路径匹配 repo，返回建议 workspace_id。

4. ~~**版本兼容**：GSD 更新频繁，skill API 是否稳定？需要版本锁定吗？~~
   - **已解决**：文档说明最低版本 GSD v2.67+，提供 CLI 备用方案降级。

5. **性能监控**：是否需要在 MCP server 中添加性能指标（请求耗时、上下文大小）？
   - **待定**：Phase 2 可选，先验证核心功能。

6. **多语言支持**：错误消息是否需要国际化？
   - **待定**：当前保持英文，后续按需添加。