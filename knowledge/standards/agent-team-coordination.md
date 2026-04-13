# Agent Team Coordination — Multi-Agent Parallel Coordination Patterns

> Source: Nicholas Carlini, "Building a C Compiler with a Team of Parallel Claudes", Anthropic Engineering Blog, 2026-02-05
> Link: https://www.anthropic.com/engineering/building-c-compiler

---

## Core Approach

When multiple AI agents work in parallel, no orchestrator, message queue, or central scheduler is needed. A **bare git repo + file locks** provides lightweight, effective coordination.

---

## Architecture

```
Host Machine
│
├── /upstream          ← bare git repo (shared codebase)
│   ├── src/           ← shared code
│   ├── tests/         ← test suite
│   └── current_tasks/ ← file lock directory
│
├── Agent 1 (Docker)   ← /workspace = clone of /upstream
├── Agent 2 (Docker)   ← /workspace = clone of /upstream
└── Agent N (Docker)   ← /workspace = clone of /upstream
```

Each agent clones a copy to `/workspace` in its own container, then pushes back to upstream when done.

## Coordination Protocol (3 Steps)

1. **Lock task** — Agent writes a file in `current_tasks/` (e.g., `parse_if_statement.txt`). If two agents compete for the same task, git push conflict forces the second one to switch.
2. **Work + Sync** — After completion: pull upstream → merge other agents' changes → push own changes → delete lock.
3. **Loop** — Outer harness loops infinitely: start new session, claim new task, repeat.

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Orchestration | No central orchestrator | Each agent judges "next most obvious task", reducing single point of failure |
| Task assignment | File locks + git conflicts | Zero extra infrastructure; git provides built-in conflict detection |
| Merge conflicts | Let agents resolve themselves | LLMs have sufficient context to understand and resolve most conflicts |
| Container isolation | Each agent in separate Docker | Avoid state pollution; failures can be restarted |

## Role Differentiation

Parallelism not only accelerates, it enables agent specialization:

- **Implementation agent** — writes core functionality
- **Deduplication agent** — finds and merges duplicate code
- **Performance agent** — optimizes compiler speed itself
- **Code quality agent** — refactors from a language expert perspective
- **Documentation agent** — maintains README and progress files

Each role has different prompts but shares the same coordination protocol.

## Applicable Scenarios

- ✅ Large projects decomposable into independent subtasks
- ✅ High-quality automated testing for validation
- ✅ Low coupling between tasks (or decouplable via oracle strategy)
- ⚠️ Not suitable for highly sequential task scenarios
- ⚠️ Not suitable for projects without test coverage (agents may persistently produce incorrect code)

## Limitations

- Efficiency drops when merge conflicts are frequent
- No cross-agent communication mechanism (currently only indirect info exchange via git commits)
- Agents may choose wrong task priorities (no global view)