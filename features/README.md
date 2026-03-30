# Features — 伞仓级需求与交付文档

本目录存放 **跨仓库或产品级** 的需求说明与过程产物。实现代码通常在 `repos/` 下的独立 Git 仓库中；此处文档必须与 **`meta/repos.yaml` 中的仓库 `id`** 对齐，避免「有文档找不到代码」。

工具无关：Cursor、OpenClaw、其他代理或人类协作时，**以本文件与 `features/INDEX.md` 为约定来源**。

## 目录结构

```text
features/
  README.md          # 本约定（权威）
  INDEX.md           # 需求索引表（人类维护）
  _template/         # 新建需求时复制其中的 Markdown 模板
  <category>/        # 类别（小写 kebab-case，例如 aips-personal-cli、content-pipeline）
    <feature-id>/    # 单个需求目录（kebab-case，全局唯一优先）
      spec.md
      tech_design.md
      test_report.md
      mr_report.md
      deliver.md
```

- **`<category>`**：按主题或产品线划分；跨类需求选一个 **主类别** 落目录，在 `spec.md` 里链接其他相关需求目录即可。
- **`<feature-id>`**：建议稳定、简短；可与 `INDEX.md` 中的 `id` 列一致。

## 各文件职责

| 文件 | 职责 |
|------|------|
| `spec.md` | 背景、目标、非目标、用户故事、验收标准、与 `meta/workspaces.yaml` 的关联（如有）。**必须**包含实现落点：相关 `repos.yaml` 的 `id`、分支或 PR 链接、关键路径。 |
| `tech_design.md` | 方案、接口、数据流、依赖、风险；按需创建，可与 spec 分阶段合并或拆分。 |
| `test_report.md` | 测试范围、用例、结果、已知问题；**勿写入密钥、token、未脱敏客户信息**。 |
| `mr_report.md` | 合并请求 / Code Review 过程：讨论摘要、决议、待办；侧重 **协作与评审**。 |
| `deliver.md` | 对外或业务视角的交付说明：范围、版本、上线与回滚要点；侧重 **交付与运营**。 |

`mr_report` 与 `deliver` 不要混写：前者偏工程协作，后者偏交付叙事。

## 新建一条需求的步骤

1. 在 `INDEX.md` 增加一行（`id`、标题、类别、`status`、`path`、可选 `primary_repo_id`）。
2. 创建 `features/<category>/<feature-id>/`。
3. 将 `features/_template/` 下各 `.md` 复制到该目录，按 frontmatter 与正文补全。
4. 在 `spec.md` 中填写 `repos.yaml` 中的仓库 `id` 与 PR/分支链接。

状态建议：`draft` → `in_progress` → `review` → `done` → `archived`（可按需增减）。

## 与 canonical 来源的关系

| 来源 | 作用 |
|------|------|
| `meta/repos.yaml` | 实现所在仓库的登记与本地路径；**链接代码时只引用这里的 id**。 |
| `meta/workspaces.yaml` | 任务视角；若需求对应某 workspace，在 `spec.md` 注明 workspace id。 |
| `knowledge/` | 工程标准与操作手册；与流程相关的步骤见 `knowledge/playbooks/add-umbrella-feature.md`。 |

## 代理速查

- 用户提到「伞仓需求、features、规格、跨仓功能」→ 先读本文件，再打开对应 `features/<category>/<feature-id>/spec.md`。
- 修改或新增需求文档后 → 同步更新 `features/INDEX.md` 的 `status` 与路径。
- 不要在 `test_report.md` / `mr_report.md` 中粘贴密钥；内部 URL 若仓库可能对外公开，需脱敏。

更完整的 aips-personal 约定见根目录 `README.md`、`knowledge/standards/aips-personal-conventions.md`。
