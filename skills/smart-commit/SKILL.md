---
name: smart-commit
type: workflow
description: >
  智能提交：扫描本地变更，敏感词告警（ant/支付宝/蚂蚁等公司标识），按 one-context 定位评估文件归属，
  挪正错位文件，排除不属于仓库的内容（加入 gitignore 或移至 tmp/），将合规变更拆分为多个独立 commit
  并推送。触发关键词：提交、commit、smart-commit、智能提交。
triggers:
  - 提交
  - commit
  - smart-commit
  - 智能提交
  - 提交代码
author: 水猿
version: 1.1.0
tags:
  - git
  - workflow
  - commit
openclaw:
  requires:
    bins:
      - git
  install: []
---

# Smart Commit — one-context 智能提交流程

按 one-context 仓库定位，对本地变更进行分类、归位、排除，然后拆分为多个独立 commit 并推送。

---

## 触发条件

当用户提到以下场景时使用：
- "提交" / "commit" / "提交代码"
- "帮我提交" / "smart-commit"
- "把这些改动提交了"

---

## one-context 仓库定位速查

one-context 是**本地优先、跨仓库、AI 工具无关的协作层**——核心哲学是"一处定义，多处同步"。

### 应纳入版本控制的路径（合规）

| 类别 | 路径模式 | 说明 |
|------|---------|------|
| 注册表 | `meta/*.yaml` | repos / workspaces / profiles / agents |
| 知识库 | `knowledge/**` | standards / playbooks / prompts / references / tools |
| 特性文档 | `features/**/spec.md`, `features/**/tech_design.md`, `features/**/test_report.md`, `features/**/mr_report.md`, `features/**/deliver.md`, `features/INDEX.md` | 伞形需求文档 |
| 技能 | `skills/*/SKILL.md`, `skills/*/references/**`, `skills/*/assets/**`, `skills/*/lib/**`, `skills/*/templates/**` | 可复用自动化流程 |
| 工具适配输出 | `.claude/agents/**`, `.claude/adapters/**`, `.cursor/rules/**`, `CLAUDE.md` | onecxt adapt 生成，需跟踪以保持同步 |
| CLI | `packages/one-context/**` | 核心 Python CLI |
| 顶层配置 | `.gitignore`, `docs/**`, `AGENTS.md` | 仓级文件 |

### 不应纳入的路径（排除）

| 类别 | 路径模式 | 处理方式 |
|------|---------|---------|
| 临时 / 构建产物 | `tmp/**`, `features/**/production/**`, `features/**/temp_*`, `features/**/scratch/` | 移至 `tmp/` 或确认已在 .gitignore |
| 运行时产物 | `.skill-parallel-verify/**`, `memory/*`（除 .gitkeep / README.md） | 确认 .gitignore |
| 媒体文件 | `*.mp4`, `*.webm`, `*.wav` | 移至 `tmp/` 或确认 .gitignore |
| IDE / OS | `.idea/**`, `.vscode/**`, `.DS_Store`, `*.swp` | 确认 .gitignore |
| Node 依赖 | `**/node_modules/` | 确认 .gitignore |
| Python 产物 | `.venv/`, `__pycache__/`, `*.egg-info/` | 确认 .gitignore |
| 本地配置 | `.env` | 确认 .gitignore |
| 个人 Agent 配置 | `HEARTBEAT.md`, `IDENTITY.md`, `SOUL.md`, `USER.md`, `TOOLS.md`, `canvas-philosophy.md`, 根目录 `cover.*` | 移至 `tmp/` |
| ad-hoc 脚本 | `/_*.py`, `/_*.ps1`, `/_*_*.py`, `_*-*.txt`, `_search*.cjs`, `/_shots_*/` | 确认 .gitignore 或移至 `tmp/` |
| 业务资产 | `features/**/production/videos/**`, 大体积素材 | 移至 `tmp/` |
| 其他工具运行时 | `.openclaw/**`（除 `onecxt-project.json`）, `.opencli/`, `.playwright-mcp/**` | 确认 .gitignore |

### 可能错位的文件（需要挪正）

| 文件特征 | 应挪至 | 原因 |
|---------|-------|------|
| 根目录下的 `prompt-*.md`（内容为知识性 prompt） | `knowledge/prompts/` | 属于知识层，不属于根目录 |
| 根目录下的设计素材（`.jpg`, `.png` 等非封面） | `knowledge/design-resources/` 或 `skills/<相关skill>/assets/` | 属于资源层 |
| 根目录下的架构 / 分析文档 | `docs/` 或 `knowledge/references/` | 属于文档或参考层 |
| 根目录下的工具说明 | `knowledge/tools/` | 属于知识层 |
| `.claude/` 下非 onecxt adapt 生成的个人文件 | 移除或移至 `tmp/` | .claude/ 仅保留 adapt 输出 |

---

## 执行流程

### Step 1: 扫描本地变更

```bash
git status --short
git diff --name-status HEAD
```

收集所有 **modified (M)**、**added (A)**、**untracked (?)**、**deleted (D)**、**renamed (R)** 的文件。

### Step 2: 敏感词扫描告警

对 Step 1 中所有**新增或修改**的文件内容进行敏感词扫描：

```bash
# 扫描已暂存和未暂存的变更内容
git diff HEAD --unified=0 -- $(git diff --name-only HEAD)
# 扫描未跟踪文件
for f in $(git ls-files --others --exclude-standard); do echo "=== $f ==="; cat "$f"; done
```

**敏感关键词来源**：`.onecxt/sensitive-words.yaml`

敏感词列表从项目本地配置文件 `.onecxt/sensitive-words.yaml` 读取，该文件不纳入版本控制（已在 `.gitignore` 中排除），每个团队/个人可自行维护。

**文件格式**：

```yaml
words:
  - keyword: example-敏感词
    category: 类别标签
    note: 简要说明
```

**缺省行为**：若 `.onecxt/sensitive-words.yaml` 不存在或 `words` 为空，Step 2 直接放行，不执行敏感词扫描。

**扫描规则**：
- 逐条读取 `words` 中的 `keyword`，对变更内容进行大小写不敏感匹配
- 匹配时需排除合理上下文（如路径中包含 `ant` 的 UI 属性名 `ant-design`、`.gitignore`、`package.json` 中的依赖声明等非敏感引用），排除规则参见各 `note` 字段
- 对每个命中，输出 **文件路径:行号:命中内容**

**告警流程**：
1. 输出命中清单表格：`文件 | 行号 | 命中关键词 | 上下文片段`
2. 如有命中，**暂停流程**，向用户发出告警并等待确认：
   - 列出所有命中项
   - 询问用户是否属于敏感信息泄露风险
   - 用户确认"继续"后才能进入 Step 3
3. 如无命中，直接进入 Step 3，无需额外提示

### Step 3: 分类每一行

对每个变更路径，判定为以下类别之一：

| 类别 | 标记 | 含义 |
|------|------|------|
| **合规** | `OK` | 文件在正确位置，属于 one-context 仓库 |
| **错位** | `MOVE` | 文件属于仓库但放错了位置，需挪到正确路径 |
| **排除** | `SKIP` | 文件不属于仓库，需加入 .gitignore 或移至 tmp/ |
| **灰区** | `ASK` | 不确定归属，需询问用户 |

输出 **Markdown 表格**：`路径 | 标记(OK/MOVE/SKIP/ASK) | 一行理由`。

### Step 4: 执行挪正（MOVE 类）

对标记为 `MOVE` 的文件：

1. 确定目标路径（参考上方"可能错位的文件"表）
2. 用 `git mv`（已跟踪文件）或 `mv` + `git add`（未跟踪文件）挪到正确位置
3. 若目标目录不存在，先 `mkdir -p` 创建
4. 记录挪正操作，在最终报告里展示

### Step 5: 执行排除（SKIP 类）

对标记为 `SKIP` 的文件，按系统性原则处理：

1. **已在 .gitignore 中有匹配规则** → 无需额外操作，确认跳过
2. **属于已有分类但缺规则** → 在 .gitignore 中添加**分类级规则**（如 `tmp/`、`.playwright-mcp/`），而非逐文件添加
3. **个人临时文件 / 业务资产** → `mkdir -p tmp && mv` 移至 `tmp/`，确认 `tmp/` 已在 .gitignore
4. 输出排除操作清单

### Step 6: 处理灰区（ASK 类）

对标记为 `ASK` 的文件，向用户提问：
- 该文件属于 one-context 仓库吗？
- 如果属于，应该放在哪里？
- 如果不属于，加入 .gitignore 还是移至 tmp/？

等用户确认后再继续。

### Step 7: 拆分 commit

将所有合规变更（包括挪正后的文件）按逻辑拆分为多个独立 commit。**推荐拆分维度**：

| commit 维度 | 包含路径模式 | commit message 前缀 |
|-------------|-------------|-------------------|
| 知识层 | `knowledge/**` | `feat(knowledge):` 或 `docs(knowledge):` |
| 注册表 / 框架 | `meta/**` | `feat(meta):` |
| 特性文档 | `features/**` | `feat(features):` |
| 技能 | `skills/**` | `feat(skills):` |
| 工具适配 | `.claude/agents/**`, `.claude/adapters/**`, `.cursor/rules/**`, `CLAUDE.md` | `chore(adapt):` |
| CLI | `packages/one-context/**` | `feat(cli):` 或 `fix(cli):` |
| 顶层配置 | `.gitignore`, `AGENTS.md`, `docs/**` | `chore:` |
| 文件挪正 | 跨目录移动的文件 | `refactor: relocate misplaced files` |

**规则**：
- 如果某个维度没有变更，跳过该 commit
- 如果只有 1-2 个维度有变更，可以合并为一个 commit
- commit message 参考项目最近提交风格（使用中文或英文均可，但同一批 commit 风格一致）
- 每个 commit 末尾附加 `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`

### Step 8: 推送

所有 commit 完成后，执行：

```bash
git push origin HEAD
```

若当前分支没有设置 upstream，使用 `git push -u origin HEAD`。

### Step 9: 输出报告

生成简短报告：

```
## Smart Commit 报告

### 挪正
- <old_path> → <new_path>（理由）

### 排除
- <path>：加入 .gitignore（规则）
- <path>：移至 tmp/（理由）

### Commits
1. <commit-hash> <message>
2. <commit-hash> <message>
...

### 推送
- 分支：<branch>
- 远程：<remote>
- 状态：成功/失败
```

---

## 硬规则

1. **不提交敏感信息**：`.env`、含 token/密钥的文件绝不提交
2. **敏感词扫描门控**：Step 2 扫描到敏感词命中时必须暂停并告警，用户确认后才能继续；不得跳过此步骤
3. **必须经用户确认**：Step 3 的分类表和 Step 6 的灰区问题须等用户确认后才能继续执行
4. **不 force push**：除非用户用原话明确要求
5. **系统性 .gitignore**：添加忽略规则时按分类级添加（如 `tmp/`、`.playwright-mcp/`），不逐文件添加
6. **保留 .gitkeep 和 README.md**：`memory/.gitkeep`、`memory/README.md`、`repos/**/.gitkeep` 等占位文件不被排除
7. **不修改 adapt 生成文件内容**：`.claude/agents/`、`.claude/adapters/`、`.cursor/rules/` 下的文件由 `onecxt adapt` 生成，仅跟踪同步，不手动编辑

---

## Quick Reference

| 步骤 | 操作 | 门控条件 |
|------|------|---------|
| 1 | 扫描 git status / diff | 变更清单获取完成 |
| 2 | 敏感词扫描告警 | 无命中 → 直接继续；有命中 → 用户确认 |
| 3 | 分类 (OK/MOVE/SKIP/ASK) | 分类表输出 |
| 4 | 挪正 MOVE 类文件 | 文件到位 |
| 5 | 排除 SKIP 类文件 | .gitignore 更新 + tmp/ 移动 |
| 6 | 处理 ASK 类文件 | 用户确认 |
| 7 | 拆分 commit | 所有 commit 完成 |
| 8 | git push | 推送成功 |
| 9 | 输出报告 | 报告展示完毕 |