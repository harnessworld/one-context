# Contributing to aips-personal

Thank you for your interest in contributing to aips-personal!

## Development Setup

1. Clone the repository:

```bash
git clone https://github.com/superaistation/aips-personal.git
cd aips-personal
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
pip install -e ./packages/aips-personal[dev]
```

3. Verify the setup:

```bash
python -m aiws doctor
python -m pytest packages/aips-personal/tests/ -v
```

## Project Structure

- `packages/aips-personal/` — the core Python package (`aiws` CLI)
- `meta/` — YAML manifests (repos, workspaces, profiles)
- `knowledge/` — tool-neutral standards, playbooks, and prompts
- `docs/` — architecture and contributor documentation
- `scripts/` — utility scripts

## Making Changes

1. Create a feature branch from `main`.
2. Make your changes. Follow existing code style and conventions.
3. Add or update tests if applicable.
4. Run the test suite:

```bash
python -m aiws doctor
python -m pytest packages/aips-personal/tests/ -v
```

5. Commit with a clear, descriptive message following Conventional Commits:

```
feat: add workspace switching command
fix: correct path resolution on Windows
docs: update CLI usage examples
```

## Pull Request Process

1. Ensure all tests pass.
2. Update documentation if your change affects user-facing behavior.
3. Keep PRs focused — one logical change per PR.
4. Describe what your PR does and why in the PR description.

## Code Style

- Python 3.10+ with type hints where practical.
- Use `from __future__ import annotations` in all modules.
- Follow PEP 8. Keep lines under 100 characters.
- Prefer simple, readable code over clever abstractions.

## Reporting Issues

Use GitHub Issues for bugs and feature requests. For **security vulnerabilities**, use the process in [SECURITY.md](SECURITY.md) instead of a public issue.

Include:

- What you expected to happen
- What actually happened
- Steps to reproduce
- Python version and OS

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
