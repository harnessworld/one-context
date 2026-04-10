# Playbook: Git Worktree 隔离开发 Feature

> 来源：通用 Git 工作流最佳实践

用 `git worktree` 为每个 feature 创建独立工作目录，避免频繁 stash/checkout，支持多分支并行。

## 适用场景

- 同时开发多个 feature / hotfix
- AI agent 需要各自独立工作目录，互不干扰
- 代码审查期间需要继续其他开发

## 步骤

1. **创建 worktree**
   ```bash
   # 从主分支新建分支并关联 worktree
   git worktree add ../feature-xyz feature-xyz
   # 或从已有分支
   git worktree add ../hotfix-123 hotfix/fix-123
   ```

2. **在 worktree 中开发**
   ```bash
   cd ../feature-xyz
   # 正常 commit / push
   ```

3. **完成后合并回主仓库**
   ```bash
   cd /path/to/main-repo
   git merge feature-xyz
   ```

4. **清理 worktree**
   ```bash
   git worktree remove ../feature-xyz
   # 或强制清理已删除目录
   git worktree prune
   ```

## 多 agent 场景

为每个 agent 分配独立 worktree：

```bash
# agent-1
git worktree add ../agent-1-work feat/agent-1-task

# agent-2
git worktree add ../agent-2-work feat/agent-2-task
```

每个 agent 在自己的 worktree 中 write/build/test，互不冲突。合并时按顺序 rebase 或 merge。

## 注意事项

- 同一分支不能同时被多个 worktree 检出
- worktree 共享 `.git` 对象，`git gc` 在任一目录执行即全局生效
- 删除 worktree 目录后必须 `git worktree prune`，否则 Git 仍记录该 worktree
- 子模块需在每个 worktree 中单独 `git submodule update --init`

## 检查

- [ ] worktree 分支名称与任务对应，避免无名分支
- [ ] 合并前已通过 CI / 本地测试
- [ ] 合并后及时清理 worktree，避免残留