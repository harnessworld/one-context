# Oracle Parallel Debugging — Splitting Large Tasks with Known-Correct Implementations

> Source: Nicholas Carlini, "Building a C Compiler with a Team of Parallel Claudes", Anthropic Engineering Blog, 2026-02-05
> Link: https://www.anthropic.com/engineering/building-c-compiler

---

## Problem Scenario

Multi-agent parallelism works well on independent subtasks (e.g., each fixing a failing test), but stalls on **a single large task** — all agents hit the same bug, overwriting each other's fixes.

Compiling the Linux kernel is a classic example: not 1000 independent tests, but "one giant task". 16 agents all doing the same thing.

---

## Solution: Oracle Comparison

Use a **known-correct implementation (oracle)** as a reference to decompose large tasks into parallelizable small tasks.

### Steps

1. **Random allocation** — When compiling the kernel, most files are compiled with GCC (oracle), leaving only a few files for Claude's compiler.
2. **Bisection** — If the kernel build fails, the problem is in the files compiled by Claude. Switch some back to GCC, progressively narrowing the scope.
3. **Parallel fixing** — Different agents handle bugs in different files without conflict.
4. **Delta debugging** — When individual files pass but the combination fails, use delta debugging to find file pairs with interaction bugs.

### Illustration

```
Kernel 1000 source files
├── 990 → GCC compiled (known correct)
└── 10  → Claude compiled (to verify)
    ├── Agent A fixes bug in file_03.c
    ├── Agent B fixes bug in file_07.c
    └── Agent C fixes bug in file_09.c
```

---

## Generalized Pattern

This strategy is not limited to compilers. The core pattern is:

**When a task is too large to parallelize, use an oracle for controlled experiments to isolate variables.**

| Domain | Oracle | Under Test | Method |
|--------|--------|------------|--------|
| Compiler | GCC | Your compiler | Mixed compilation + bisection |
| API rewrite | Old service | New service | Random traffic split + response comparison |
| Translation system | Human translation | MT output | Sentence-by-sentence comparison + locate problem sentences |
| Data pipeline | Reference implementation | Optimized implementation | Compare outputs + find differences |
| Refactoring | Original code | Refactored code | Per-module replacement + testing |

---

## Requirements

This strategy requires:

1. **Oracle exists and is reliable** — must have a known-correct reference
2. **Composable** — oracle and test implementation outputs can be mixed
3. **Isolatable** — problems can be pinpointed to a subset of the test implementation
4. **Verifiable** — correctness of mixed results can be automatically judged

---

## Limitations

- Not all problems have an oracle (e.g., no reference exists when innovating from scratch)
- Oracle and test implementation interfaces must be compatible, otherwise mixing is impossible
- Interaction bugs (requiring multiple files/modules combined to appear) need delta debugging or other additional methods