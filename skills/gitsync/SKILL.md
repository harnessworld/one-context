---
name: gitsync
description: >-
  Safely syncs the current Git repository with its remote: fetch, assess
  ahead/behind and dirty state, integrate with ff-only pull or user-chosen
  merge/rebase, detect and resolve conflicts without discarding local work.
  Use when the user says /gitsync, git sync, pull remote, sync with origin,
  or wants to update local from remote without losing uncommitted or unpushed work.
disable-model-invocation: true
---

# gitsync — Safe remote → local sync

**Goal:** Bring the local branch up to date with its upstream remote **without losing** uncommitted changes, unpushed commits, or stashes.

**Non-goals:** Push to remote, selective path merges, or rewriting shared history unless the user explicitly authorizes a named destructive command.

---

## When to use

- User invokes **`/gitsync`**, or asks to **sync / pull / update from remote**, **check conflicts**, or **avoid losing local work**.

## Hard rules (no local loss)

1. **Never** run `git reset --hard`, `git clean -fd`, `git checkout -- .`, or `git restore .` on the whole tree without **explicit user authorization** for that exact command.
2. **Never** `git push --force` (any branch) unless the user explicitly requests it after you state the risk.
3. **Never** drop or pop a stash until conflicts are resolved or the user confirms the stash is no longer needed.
4. **Prefer `git pull --ff-only`** when integrating; if fast-forward is impossible, **stop and ask** merge vs rebase (do not guess).
5. Before any operation that could overwrite tracked files (`pull`, `merge`, `rebase`, `stash pop`), create a **backup branch** (see Step 2).
6. **Uncommitted work:** default to **`git stash push -u`** with a descriptive message; only **`git commit`** WIP if the user prefers a commit over stash.

---

## Parameters (infer from context)

| Parameter | Default | Notes |
|-----------|---------|--------|
| Remote | `origin` | Use `git remote -v`; if multiple, ask |
| Branch | current branch | `git branch --show-current` |
| Upstream | `@{u}` | If no upstream, set or ask: `git branch -u origin/<branch>` |

---

## Workflow

Copy and track progress:

```
gitsync:
- [ ] Step 1: Preflight snapshot
- [ ] Step 2: Backup branch
- [ ] Step 3: Fetch remote
- [ ] Step 4: Divergence report
- [ ] Step 5: Integrate (ff-only / merge / rebase per user)
- [ ] Step 6: Conflicts (if any)
- [ ] Step 7: Restore stashed work (if any)
- [ ] Step 8: No-loss verification report
```

### Step 1: Preflight snapshot

Run in parallel where possible:

```bash
git rev-parse --is-inside-work-tree
git branch --show-current
git status -sb
git remote -v
git rev-parse --abbrev-ref @{u} 2>/dev/null || echo "NO_UPSTREAM"
git stash list
```

Record:

- Current `HEAD` short hash
- Count of modified / untracked files
- Whether upstream exists
- Any existing stashes (note top entry)

**Gate:** Not a git repo → stop with instructions. No upstream → ask user which remote branch to track before continuing.

### Step 2: Backup branch (mandatory before integrate)

```bash
git branch "gitsync-backup/$(date +%Y%m%d-%H%M%S)-$(git rev-parse --short HEAD)"
```

On **Windows PowerShell** (no `date` in PATH):

```powershell
$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$short = git rev-parse --short HEAD
git branch "gitsync-backup/${ts}-$short"
```

Tell the user the backup branch name. This preserves the pre-sync commit even if later steps go wrong.

### Step 3: Fetch remote

```bash
git fetch --prune origin
```

If the user named another remote, replace `origin`.

### Step 4: Divergence report

Assume upstream is `@{u}` (e.g. `origin/main`).

```bash
git status -sb
git log --oneline HEAD..@{u}
git log --oneline @{u}..HEAD
git merge-base HEAD @{u}
```

Present a short table:

| Signal | Meaning |
|--------|---------|
| `HEAD..@{u}` non-empty | Remote has commits you lack → need integrate |
| `@{u}..HEAD` non-empty | You have local commits not on remote → integrate may need merge/rebase |
| Both non-empty | **Diverged** — cannot ff-only; user must choose merge or rebase |
| Working tree dirty | Stash (or commit) before integrate |

**Gate:** If diverged, **ask**: “Merge (preserves merge commit) or rebase (linear history)?” Do not proceed until answered.

### Step 5: Integrate

**5a — Dirty working tree (before pull/merge/rebase):**

```bash
git stash push -u -m "gitsync: pre-sync $(date +%Y-%m-%dT%H:%M:%S)"
```

PowerShell message example: `gitsync: pre-sync 2026-05-16T14:30:00`

**5b — Try fast-forward first (default):**

```bash
git pull --ff-only
```

- **Success** → skip to Step 7 (if stashed) or Step 8.
- **Fails** (not possible to ff-only) → follow user choice from Step 4:

**Merge:**

```bash
git merge @{u}
```

**Rebase:**

```bash
git rebase @{u}
```

Do **not** use `--autostash` unless the user explicitly wants it; prefer the explicit stash in 5a.

### Step 6: Conflicts

If merge/rebase/stash pop reports conflicts:

```bash
git status
git diff --name-only --diff-filter=U
```

For each conflicted file:

1. Show conflict hunks (`git diff` or read file).
2. Propose resolution strategy:
   - **Both sides needed** → edit markers manually.
   - **Keep local version** → only if user confirms for that file: `git checkout --ours -- <path>` (during merge; during rebase “ours” is inverted — use `git show :2:path` / `:3:path` or manual edit).
   - **Take remote** → only if user confirms **local committed work in that hunk can be discarded**: `git checkout --theirs -- <path>` (merge only; confirm semantics on rebase).
3. After edits: `git add <path>`
4. Continue:
   - Merge: `git merge --continue` or `git commit` if merge commit pending
   - Rebase: `git rebase --continue`
   - Stash pop: `git stash pop` only after index clean, or resolve then `git add` and continue

**Abort paths (user must request):**

- `git merge --abort`
- `git rebase --abort`
- Restore from backup: `git reset --hard gitsync-backup/<timestamp>-<hash>` — **only with explicit user authorization**

### Step 7: Restore stashed work

If Step 5a created a stash:

```bash
git stash list
git stash pop
```

If pop causes conflicts → return to Step 6; **do not** `stash drop` until resolved or user aborts.

### Step 8: No-loss verification report

Run:

```bash
git status -sb
git stash list
git log -3 --oneline
git branch --list "gitsync-backup/*" | tail -5
```

Output **gitsync report** to the user:

```markdown
## gitsync 报告

### 结果
- 分支: <branch> @ <short HEAD>
- 上游: <upstream>
- 同步方式: ff-only | merge | rebase
- 冲突: 无 | 已解决 N 个文件 | 中止（原因）

### 本地保护
- 备份分支: `gitsync-backup/...`（仍保留，可手动删除）
- Stash: <none | 已恢复 | 仍存在 `stash@{0}: ...`>
- 相对同步前: 未推送提交 <kept N | 0>；工作区变更 <restored | 无>

### 建议下一步
- [ ] 运行测试 / `onecxt doctor`（若适用）
- [ ] 确认无问题后删除旧备份分支: `git branch -d gitsync-backup/...`（可选，需用户同意）
```

**Gate:** User should confirm the working tree matches expectations before you delete backup branches or stashes.

---

## Quick reference

| Situation | Action |
|-----------|--------|
| Only behind remote, clean tree | `git pull --ff-only` |
| Behind + dirty tree | stash → `git pull --ff-only` → stash pop |
| Diverged | Ask merge vs rebase; backup branch first |
| Conflicts | List files, resolve with user, continue merge/rebase |
| Catastrophic mess | Point user to backup branch; **no** hard reset without consent |

## Anti-patterns

- `git pull` without `--ff-only` when user asked for safe sync (silent merge commit).
- Discarding stash after failed `stash pop`.
- Resolving conflicts by blindly taking `--theirs` on all files (drops local intent).
- Skipping backup branch to “save time”.
