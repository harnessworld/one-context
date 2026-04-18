# Playbook: 新增伞仓级需求（`features/`）

适用于在 one-context 根目录记录跨仓库或产品级需求，而非仅在某一子仓库内写 issue 的场景。

## 前置阅读

- `features/README.md` — 目录与文件职责的权威约定
- `meta/repos.yaml` — 实现仓库的 `id` 与路径

## 步骤

1. 打开 `features/INDEX.md`，新增一行：`id`、标题、`category`、`status`（如 `draft`）、`path`、`primary_repo_id`（可选）。
2. 创建目录 `features/<category>/<feature-id>/`，名称与索引一致。
3. 复制 `features/_template/*.md` 到该目录。
4. 编辑 `spec.md`：填写 YAML frontmatter，并 **必须** 完成「实现落点」一节（`repos.yaml` 的仓库 id、分支或 PR）。
5. 随进度补充 `tech_design.md`、`test_report.md`、`mr_report.md`、`deliver.md`；不需要时可暂不创建非 `spec` 文件，但索引与 spec 应保持同步。
6. 需求结束或搁置时，更新 `INDEX.md` 的 `status`，必要时在 `spec.md` 中注明归档原因。

## 常见错误

- 忘记更新 `INDEX.md`，导致 feature 目录存在但索引缺失。
- `spec.md` 未填写「实现落点」一节，后续 Dev agent 无法定位实现仓库。
- 直接在子仓库内创建 issue，而非在 `features/` 下记录跨仓需求。

## 检查

- [ ] `spec.md` 含有效 `primary_repo_id` 或明确说明为何暂无仓库
- [ ] `INDEX.md` 与目录路径一致
- [ ] 敏感信息未写入 `test_report.md` / `mr_report.md`
- [ ] feature 目录名与 `INDEX.md` 中的 `id` 一致
