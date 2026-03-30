# aips-personal conventions

These conventions keep `aips-personal` agent-agnostic and easy to extend.

## Canonical sources

- **`meta/repos.yaml`**: what repositories exist and where they live locally.
- **`meta/workspaces.yaml`**: task- or theme-oriented views that reference repo ids.
- **`meta/profiles.yaml`**: shared behavior and context policy hints for AI tooling.
- **`knowledge/`**: human- and AI-readable standards, playbooks, and prompt fragments.
- **`features/`**: umbrella-level requirements and delivery artifacts (`spec.md`, design, tests, MR notes, deliverables). Convention: `features/README.md`; index: `features/INDEX.md`. Link implementations using repo **`id`** values from `meta/repos.yaml`.

Do not duplicate the same intent in vendor-specific formats. If a tool needs a special file, add an **adapter** that derives it from the canonical sources.

## Tool adapters

Implementations belong under `aiws.adapters` (today: package stubs; later: concrete exporters). Adapters translate; they do not own the meaning of policies or playbooks.

## Validation

After editing manifests, run:

```bash
python -m aiws doctor
```

On some systems the `aiws` script is not on `PATH`; `python -m aiws` is the portable form.
