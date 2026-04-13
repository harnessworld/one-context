# Agent-Friendly Testing — Design Principles for AI Agent Tests

> Source: Nicholas Carlini, "Building a C Compiler with a Team of Parallel Claudes", Anthropic Engineering Blog, 2026-02-05
> Link: https://www.anthropic.com/engineering/building-c-compiler

---

## Core Insight

Writing tests for AI agents ≠ writing tests for humans. Agents have two fundamental constraints: **context window pollution** and **time blindness**. Test design must optimize around these constraints, or agents waste tokens and time on irrelevant information.

---

## Principle 1: Minimal Output, Avoid Context Pollution

An agent's context window is a scarce resource. Thousands of lines of useless log output = wasted context.

**Practices:**
- Test output should be at most a few lines of key information
- Write detailed information to log files for on-demand review
- Pre-compute aggregate statistics; don't make the agent compute them

**Anti-pattern:** Running 1000 test cases and printing all pass/fail details.
**Good practice:** `PASS: 990/1000 | FAIL: 10 | See /tmp/test_failures.log`

---

## Principle 2: Grep-Friendly Logs

Agents use `grep`/search to locate problems. Log format must be optimized for this.

**Practices:**
- Error lines start with `ERROR:`, reason on the same line
- Use consistent markers (`ERROR`, `WARN`, `FAIL`) for quick filtering
- Key status in uppercase markers, not buried in long sentences

**Anti-pattern:** `It seems like there was an issue with the parser on line 42 where the token was unexpected`
**Good practice:** `ERROR: parse_fail file=main.c line=42 token=unexpected`

---

## Principle 3: Fast Sampling Mode

Agents cannot perceive time passing and will naively run full test suites. Provide a fast path.

**Practices:**
- Provide a `--fast` option, running 1%–10% random sampling
- Sampling should be **per-agent deterministic** (same agent gets same result twice), **cross-agent random** (different agents cover different subsets)
- Determinism can use agent ID as random seed
- Each agent pinpoints regressions precisely, while multiple agents together cover the full suite

---

## Principle 4: Help Agents Self-Orient

Each agent starts in a "zero-context" state — new container, no history. The test environment must help it orient quickly.

**Practices:**
- Maintain a progress file (e.g., `PROGRESS.md`) recording current state and TODOs
- README should be comprehensive and kept up to date
- Test output should tell the agent "what to do next", not just "FAIL"
- On failure, attach fix hints or relevant file paths

---

## Principle 5: CI Protects Passed Functionality

When agents implement new features, they can easily break existing ones. Automated guardrails are needed.

**Practices:**
- Establish a CI pipeline that runs core tests on every commit
- Emphasize in agent prompts: new commits must not break existing tests
- Tighten test gates when pass rate reaches a high level

---

## Quick Reference

| Problem | Solution |
|---------|----------|
| Agent context overwhelmed by logs | Minimal output + detailed logs to file |
| Agent can't locate errors | Grep-friendly format: `ERROR: reason` same line |
| Agent wastes time on full suite | `--fast` random sampling |
| Agent disoriented after startup | Progress file + README + test-attached hints |
| Agent breaks old features with new ones | CI gates + strict regression tests |
| Agent can't interpret test results | Pre-computed statistics, direct conclusions |

---

## Scope

Not limited to compiler projects. Applicable to any scenario where LLM agents run autonomously and read test output, including:
- Automated bug-fixing CI bots
- Long-running coding agents
- Multi-agent collaborative development