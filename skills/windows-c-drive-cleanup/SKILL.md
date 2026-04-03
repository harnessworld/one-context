---
name: windows-c-drive-cleanup
description: Windows C 盘空间紧张时的安全清理流程。代理须先只读统计与建议；任何删除、prune、清空回收站均须在对话中获得用户明确授权后方可执行。实现位于 one-context skills/windows-c-drive-cleanup/。
---

# Windows C 盘空间清理（Agent Skill）

## 删除授权（全局硬约束）

任何 **删除文件或目录**、**清空回收站**、以及卸载以外的「清缓存」等 **实质移除数据** 的操作（含 `Remove-Item`、`Clear-RecycleBin`、各工具的 prune / 批量清理等），**必须**在对话中取得 **用户明确授权**（逐条确认、明确同意某路径/某步骤，或用户本人亲自执行命令）后，代理方可代为执行。

**未获授权前**，代理 **仅** 允许：枚举与体积估算、展示建议命令、引导 **设置 → 系统 → 存储 → 临时文件 / 存储感知**、运行本目录下 **只读** 脚本 `survey-disk-hints.ps1`。

**不得**默认、推测或静默删除或清空回收站。说明风险后 **仍须** 用户明确同意，严于「先说明再执行」。

---

## 何时使用（触发词）

用户提到 **清理 C 盘、腾空间、磁盘满了、Docker/npm 占 C 盘、WSL 太大** 等，且环境为 **Windows** 时，加载本 Skill 并按下方顺序执行。

---

## 推荐流程（先只读，后执行）

| 阶段 | 内容 | 默认是否需要授权 |
|------|------|------------------|
| **0** | 建议用户优先使用 **设置 → 系统 → 存储 → 临时文件**，勾选后由系统清理 | 用户在本机 UI 操作 |
| **1** | 记录 C 盘可用空间；运行或等价执行「只读统计」命令（见下） | 否 |
| **2** | 按「开发者 / 包管理 / Docker / 系统」分类展示可清理项与 **建议命令** | 否 |
| **3** | 仅在用户 **对每一条** 明确同意后，执行删除类命令 | **是** |

清理 **前后** 各记录一次 C 盘空闲（不要求字节级精确）：

```powershell
Get-PSDrive -Name C | Select-Object Used,Free
# 或
fsutil volume diskfree c:
```

---

## 1. 只读统计（无需授权）

本仓库脚本（**无删除逻辑**）。在 **one-context 仓库根** 下执行：

```powershell
.\skills\windows-c-drive-cleanup\survey-disk-hints.ps1
# 仅检查路径是否存在、不做递归体积（秒级）：
.\skills\windows-c-drive-cleanup\survey-disk-hints.ps1 -Quick
```

或使用本机的绝对路径（将根目录换成你的克隆位置）：

```powershell
& "D:\harnessworld\one-context\skills\windows-c-drive-cleanup\survey-disk-hints.ps1"
```

手动抽查单目录体积（大目录可能较慢，可提醒用户）：

```powershell
$p = $env:TEMP
(Get-ChildItem -LiteralPath $p -Recurse -Force -ErrorAction SilentlyContinue |
  Measure-Object -Property Length -Sum).Sum / 1GB
```

---

## 2. 无需管理员（常见 / 用户态）

下列 **仅** 在用户明确授权后执行；执行前再次口头确认路径。

| 类别 | 说明 | 示例（执行前须授权） |
|------|------|----------------------|
| 用户临时目录 | `%TEMP%`、`%LOCALAPPDATA%\Temp` | `Remove-Item -LiteralPath $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue`（**危险**：会删临时文件；须用户同意） |
| npm | 全局缓存 | `npm cache verify`（只读）；清理：`npm cache clean --force` |
| yarn | 全局缓存 | `yarn cache clean` |
| pnpm | store | `pnpm store prune`（须理解会删未引用包） |
| pip | 缓存目录 | `pip cache dir`（只读）；`pip cache purge` |
| conda | 本机包缓存与索引 | `conda info`（只读）；`conda clean --dry-run --all`（只读预览）；**授权后** `conda clean -a`（会删 tarballs/缓存等，需确认无在进行中的 env 操作） |
| 浏览器缓存 | 各浏览器设置内清理更安全 | 优先引导用户用浏览器或存储设置 |

**Visual Studio / Build Tools**（易占数 GB，优先走官方入口）：

- **推荐（低风险）**：打开 **Visual Studio Installer** → 对应版本 → **修改 / 更多** → 移除不工作负载或按微软文档使用 **清理安装缓存** 类选项（以当前 Installer 界面为准）。
- **只读探查**：若已装 VS，可用 `vswhere`（通常位于 `%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe`）列出安装路径；`survey-disk-hints.ps1` 会尝试统计常见 **Installer 包缓存**目录（可能需管理员才能测准）。
- **目录级删除（须用户明确授权 + 单独说明风险）**：`C:\ProgramData\Microsoft\VisualStudio\Packages` 等处存放安装包缓存，删掉可腾空间但 **以后修复/增装组件可能要重新下载**；禁止在未说明风险并取得授权前代为删除。

**`node_modules` / `dist` / `build`**：仅当用户 **给出具体项目路径并授权** 时可删；禁止全盘搜索后批量删除。

---

## 3. 需要管理员（UAC）

下列通常需 **提升权限**；执行前 **授权 + 说明风险**。

| 操作 | 说明 |
|------|------|
| **磁盘清理** | `cleanmgr /d C:` 或存储设置中的临时文件 |
| **DISM 组件清理** | 例如 `DISM /Online /Cleanup-Image /StartComponentCleanup`（官方文档路径；可能耗时；勿与正在进行的更新冲突） |
| **WinSxS** | **禁止手工删除** `C:\Windows\WinSxS` 内文件；仅使用 **DISM** 等微软文档记载的方式 |

---

## 4. Docker（须单独授权）

- 先 `docker system df`（只读）。
- 清理类：**必须用户授权** 后再执行，例如：
  - `docker system prune`
  - `docker system prune -a`（更激进，会删未使用镜像）

说明：删除镜像/容器后需重新 pull / build。

---

## 5. WSL（高风险附录，须单独授权）

与 **WSL 发行版内文件清理**、**导出/导入发行版**、**虚拟磁盘压缩**（`wsl --shutdown` 后 `diskpart` / `Optimize-VHD` 等）相关步骤 **权限高、易误伤**，须：

1. 单独成章告知风险；
2. 确认用户无未保存工作、WSL 已关闭；
3. **用户明确授权** 后再提供逐步命令。

不确定时优先建议用户用 **Docker Desktop / WSL 设置** 或微软文档自行操作。

---

## 6. Windows Update 缓存（`SoftwareDistribution` 等）

- **风险**：若 Windows 正在下载/安装更新，动 `C:\Windows\SoftwareDistribution` 可能导致更新失败。
- **要求**：确认无进行中更新；**用户明确授权**；通常需停 **wuauserv** 等步骤（管理员），仅在有经验或按可信文档时协助。

---

## 7. 禁止与默认不触碰

- **禁止**手工删除 **`C:\Windows\WinSxS`** 下内容（仅 DISM 等官方路径）。
- **禁止**在未授权下改动 **`C:\Program Files`** / **`Program Files (x86)`** 中非用户可再生的缓存/日志以外的内容。
- **默认不碰** **文档 / 桌面 / 下载**（除非用户 **点名路径并授权**）。
- **不作为默认步骤**：调整 **pagefile.sys / hiberfil.sys**、禁用休眠等；若用户坚持，须 **单独警示 + 明确授权**。

---

## 8. 回滚说明

- 删除 **缓存、临时文件、未用 Docker 镜像** 后，一般可通过重新安装/下载恢复；**不保证**离线仍可运行。
- 清空回收站后 **不可**通过本 Skill「撤销」；须强调给用户。

---

## 实现落点

- **Spec**：`features/core/skill-windows-c-drive-cleanup/spec.md`
- **本 Skill**：`skills/windows-c-drive-cleanup/SKILL.md`
- **只读脚本**：`skills/windows-c-drive-cleanup/survey-disk-hints.ps1`（**不得**加入无确认批量删除）
