# CLI

The command-line interface is provided by the `aips-personal` Python package.

From the aips-personal root directory (the checkout that contains `meta/repos.yaml`):

```bash
pip install -e ./packages/aips-personal
```

Run the CLI (portable on Windows, macOS, and Linux):

```bash
python -m aiws --help
```

If `aiws` is on your `PATH` (depends on Python install), you can use the same subcommands without `python -m aiws`.

Common commands:

```bash
aiws doctor
aiws repo list
aiws workspace list
aiws workspace show WORKSPACE_ID
aiws context export WORKSPACE_ID
aiws context export WORKSPACE_ID --format markdown
aiws profile list
aiws sync
aiws sync your-repo-id
```

Use `AIWS_ROOT` or `--root PATH` when your shell is not inside the workspace tree.
