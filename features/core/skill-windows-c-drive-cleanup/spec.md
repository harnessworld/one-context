---
id: skill-windows-c-drive-cleanup
title: Windows C 盘空间清理 — 仓库内 Agent Skill
status: done
category: core
primary_repo_id: one-context
owner: ""
updated: "2026-04-04"
---

# 概述

在 **Windows** 环境下，C 盘空间不足是常见痛点。本需求在 one-context 的 **`skills/`** 目录新增一条 **可复用 Agent Skill**（`SKILL.md` + 必要时配套脚本），使 Cursor / 其他代理在收到「清理 C 盘」「腾空间」等意图时，按统一、可审计的步骤操作，而不是随意删文件。

**删除授权（全局硬约束）**：任何 **删除文件或目录**、**清空回收站**、以及卸载以外的「清缓存」等 **实质移除数据** 的操作（含 `Remove-Item`、`Clear-RecycleBin`、各工具的 prune / 批量清理等），**必须**在对话中取得 **用户明确授权**（用户逐条确认、明确回复同意某路径/某一步骤，或用户本人亲自执行命令）后，代理方可代为执行。**未获授权前**，代理仅可做枚举、体积估算、展示建议命令、引导用户使用系统自带能力；**不得**默认、推测或静默删除或清空回收站。

# 目标与非目标

## 目标

- 新增独立技能目录（建议 `skills/windows-c-drive-cleanup/`，名称以最终实现为准），根文件 **`SKILL.md`** 为单一入口，符合仓库内既有 skill 约定（见 `skills/README.md`）。
- 文档中明确 **安全边界**：默认优先 **可逆 / 低风险** 项（如用户级临时目录、包管理器缓存、可再生的构建产物），对 **系统目录、注册表、BitLocker、其他盘数据** 等给出禁止或需 **用户明确授权 + 单独确认** 的规则。
- **提权分层**：`SKILL.md` 须区分 **无需管理员** 的步骤（如 `%TEMP%`、`%LOCALAPPDATA%` 下各工具缓存）与 **需要 UAC/管理员** 的步骤（如 `DISM` 组件清理、部分系统临时目录、服务相关日志）；避免代理默认假设「整段都要提权」。
- **开发者相关路径**（与场景呼应）：Skill 须覆盖或引用 **npm/yarn/pnpm、pip/conda、Docker Desktop、Visual Studio / Build Tools** 等常见占用来源；删除 **`node_modules` 或项目构建产物** 时须 **用户指定项目路径并授权**，禁止全盘猜测删除。
- **Docker / WSL**：优先通过 **Docker 自带清理**（如 `docker system prune` 等，仍须用户授权后再由代理执行）；**WSL 虚拟磁盘压缩** 与镜像清理分开叙述；高风险操作单独成章并重复 **授权** 要求。
- **系统更新与存储**：涉及 `SoftwareDistribution` 等可能影响 Windows Update 的路径时，须写明 **风险与前置条件**（如是否在更新中），且删除前 **必须用户授权**。
- **推荐系统自带能力**：明确建议 **设置 → 系统 → 存储 → 临时文件 / 存储感知** 作为低风险首选（不替代该产品，但与 Skill 互补）。
- 提供 **可观测性**：清理前展示将影响的路径类别与大致体量（如 `Get-ChildItem` / `Measure-Object` 等只读方式）；清理前后各记录一次 C 盘可用空间（如 `Get-PSDrive C` 或 `fsutil volume diskfree c:`），不要求精确到字节级。
- **`SKILL.md` 须区分** **「仅展示 / 建议 / 只读统计」** 与 **「执行删除或服务变更」**；后者仅在 **用户明确授权** 后进行。
- 与 **用户规则** 对齐：不默认静默删除用户文档、下载、桌面内容；**所有删除与清空回收站均以本节「删除授权」为准，严于「先说明再执行」——说明后仍须用户明确同意。**

## 非目标

- 不实现「一键万能清理」闭源 GUI 或常驻服务；本需求以 **文档化流程 + 可选轻量脚本** 为主。
- 不在本需求内承诺具体释放容量数值或适配所有 OEM 预装路径。
- 不替代 Windows 自带的「存储感知」产品化体验；Skill 面向 **开发者 / 代理驱动** 的自动化场景。
- **不作为默认步骤**：调整 **pagefile.sys / hiberfil.sys**、禁用休眠等系统策略级变更（若文档提及，须单独警示且 **须用户明确授权**）。

# 用户与场景

- 本地 C 盘告警、Docker/WSL/npm 缓存膨胀、旧 SDK 与临时文件堆积。
- 用户在对话中说「帮我清一下 C 盘」「skills 里加个清理磁盘」等，代理应加载本 Skill 并按流程执行；**任何实际删除或清空回收站前须取得用户授权**。

# 验收标准

- [x] `skills/windows-c-drive-cleanup/SKILL.md` 存在，含：触发词、前置条件（管理员权限场景说明）、分步清单、PowerShell / 常用命令示例、**禁止清单**与回滚提示。
- [x] **`SKILL.md` 正文显著位置写明「删除授权」硬约束**：与本文 `# 概述` 中 **删除授权（全局硬约束）** 一致或更严；并说明代理在未授权时 **仅** 可做只读枚举与建议。
- [x] **禁止清单**至少包含：**禁止手工删除 `C:\Windows\WinSxS` 内容**（仅允许 `DISM` 等官方文档路径）；禁止在未授权下改动 `C:\Program Files` / `Program Files (x86)` 中非缓存、非日志类内容；默认不触碰用户 **文档 / 桌面 / 下载**（除非用户点名路径并授权）。
- [x] `features/INDEX.md` 已登记本需求；本 `spec.md` 中实现落点与实际目录一致。
- [x] 在至少一台 Windows 10/11 上 **手工或代理按文档走通** 一轮低风险清理路径，并在 `test_report.md`（可选）或本 spec 的「开放问题」中记录已知限制。（已在本机跑通 `survey-disk-hints.ps1` 只读路径；未执行任何删除。）

# 实现落点（必填）

- **仓库 id**（`meta/repos.yaml`）: `one-context`（伞仓本体；技能落在 umbrella 的 `skills/` 下，与 `meta/repos.yaml` 子仓条目无强制绑定）。
- **分支 / PR**: —
- **主要路径或模块**: `skills/windows-c-drive-cleanup/`（建议名，实现时可调整为 kebab-case 一致命名）；根目录 `skills/README.md` 在技能落地后 **增加一行索引**（与既有表格风格一致）。

# 关联

- **Workspace**（`meta/workspaces.yaml` id，如有）: —
- **其他需求目录**: 与 `features/core/agent-framework/` 同属「代理可执行产物」；不依赖 `packages/one-context` CLI 变更，除非后续决定将清理封装为 `onecxt` 子命令（当前 **不在** 本需求范围内）。

# 开放问题

- **脚本**：`survey-c-drive-report.ps1`（只读；五-A/五-B 交付）；`survey-disk-hints.ps1`（只读）；`invoke-c-drive-cleanup.ps1`（用户授权 + `-ChatAuthorizationNote` 后白名单清理；支持 `-DryRun`）。若后续要加重试/超时/浅层扫描，可在 `tech_design.md` 扩展。
- **WSL**：`SKILL.md` 已设「高风险附录」；VHD 压缩等具体命令仍以微软文档为准，避免在 skill 内写死易过期路径。
