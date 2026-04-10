# one-context (Python package)

This directory contains the **`onecxt` CLI** and the importable module **`one_context`**. Product overview and architecture are in the repository root [`README.md`](../../README.md).

## Install

From the one-context repository root (the checkout that contains `meta/repos.yaml`):

```bash
pip install -e ./packages/one-context
```

For development (tests), use:

```bash
pip install -e "./packages/one-context[dev]"
```

## Run

Portable on Windows, macOS, and Linux:

```bash
python -m one_context --help
```

If `onecxt` is on your `PATH` (depends on Python install), you can use the same subcommands without `python -m one_context`.

Use `ONECXT_ROOT` or `--root PATH` when your shell is not inside the workspace tree.

## Common commands

```bash
onecxt doctor
onecxt repo list
onecxt workspace list
onecxt workspace show WORKSPACE_ID
onecxt context export WORKSPACE_ID
onecxt context export WORKSPACE_ID --format markdown
onecxt context export WORKSPACE_ID --format markdown --compress --target-tokens 8000
onecxt profile list
onecxt sync
onecxt sync your-repo-id
onecxt adapt dev                    # generate all adapters
onecxt adapt dev --only hermes      # only Hermes
onecxt adapt dev --only hermes --dry-run
onecxt adapt-install                # install git hooks (auto-adapt on pull/checkout)
onecxt adapt-uninstall              # remove git hooks
```
