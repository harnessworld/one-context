from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from one_context import __version__
from one_context.agents import load_agents
from one_context.context import build_workspace_context, render_workspace_context
from one_context.dotenv import load_dotenv
from one_context.errors import ManifestError
from one_context.log import setup_logging
from one_context.profiles import load_profiles
from one_context.repos import load_repos
from one_context.root import find_root
from one_context.sync import sync_repositories
from one_context.validate import doctor, workspace_context_summary
from one_context.workspaces import load_workspaces

logger = logging.getLogger("one_context.cli")


# ---------------------------------------------------------------------------
# Resolve helpers
# ---------------------------------------------------------------------------

def _resolve_root(path: Path | None) -> Path:
    if path is not None:
        root = path.expanduser().resolve()
        if not (root / "meta" / "repos.yaml").is_file():
            raise ManifestError(f"Not an one-context root (missing meta/repos.yaml): {root}")
        return root
    return find_root()


# ---------------------------------------------------------------------------
# Command handlers — each returns an int exit code
# ---------------------------------------------------------------------------

def _cmd_doctor(root: Path, _args: argparse.Namespace) -> int:
    load_dotenv(root / ".env")
    result = doctor(root)
    for msg in result.errors:
        print(f"error: {msg}", file=sys.stderr)
    for msg in result.warnings:
        print(f"warning: {msg}")
    return 1 if result.errors else 0


def _cmd_sync(root: Path, args: argparse.Namespace) -> int:
    load_dotenv(root / ".env")
    select = list(args.select) if args.select else None
    sync_repositories(root, select, workers=args.jobs)
    return 0


def _cmd_repo_list(root: Path, _args: argparse.Namespace) -> int:
    entries, _ = load_repos(root)
    for e in entries:
        desc = e.get("description") or ""
        line = f"{e['id']}\t{e['url']}\t{e['path']}"
        if desc:
            line += f"\t# {desc}"
        print(line)
    return 0


def _cmd_manifest_list(
    loader, label: str, root: Path, _args: argparse.Namespace,
) -> int:
    """Generic list handler for workspaces / profiles."""
    entries, _ = loader(root)
    if not entries:
        print(f"(no {label}.yaml or empty {label} list)")
        return 0
    for entry in entries:
        eid = entry.get("id", "")
        name = entry.get("name", "")
        print(f"{eid}\t{name}")
    return 0


def _cmd_workspace_list(root: Path, args: argparse.Namespace) -> int:
    return _cmd_manifest_list(load_workspaces, "workspaces", root, args)


def _cmd_workspace_show(root: Path, args: argparse.Namespace) -> int:
    try:
        data = workspace_context_summary(root, args.id)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    print(render_workspace_context(data, "json"), end="")
    return 0


def _cmd_context_export(root: Path, args: argparse.Namespace) -> int:
    try:
        data = build_workspace_context(root, args.id)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2

    rendered = render_workspace_context(data, args.format)
    if args.output is None:
        print(rendered, end="")
        return 0

    target = args.output.expanduser()
    if not target.is_absolute():
        target = root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")
    return 0


def _cmd_profile_list(root: Path, args: argparse.Namespace) -> int:
    return _cmd_manifest_list(load_profiles, "profiles", root, args)


def _print_dry_run_block(rel_path: str, description: str, body: str) -> None:
    """Print generated content in dry-run mode.

    On Windows, ``sys.stdout`` may use a legacy encoding (e.g. GBK) that
    cannot encode some UTF-8 characters from knowledge files; fall back to
    writing UTF-8 bytes so ``--dry-run`` does not crash.
    """
    block = f"--- {rel_path} ({description}) ---\n{body}\n"
    try:
        sys.stdout.write(block)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(block.encode("utf-8", errors="replace"))


def _cmd_adapt(root: Path, args: argparse.Namespace) -> int:
    # Lazy import to avoid circular deps and keep startup fast
    from one_context.adapters import ADAPTERS, get_adapter, list_adapters
    # Trigger adapter registration via side-effect imports
    import one_context.adapters.claude_code  # noqa: F401
    import one_context.adapters.cursor  # noqa: F401
    import one_context.adapters.openclaw  # noqa: F401

    workspace_ids: list[str]
    if args.all:
        ws_list, _ = load_workspaces(root)
        workspace_ids = [w["id"] for w in ws_list]
    else:
        if not args.workspace_id:
            print("error: specify a WORKSPACE_ID or use --all", file=sys.stderr)
            return 2
        workspace_ids = [args.workspace_id]

    only = args.only
    if only and only not in ADAPTERS:
        print(
            f"error: unknown adapter {only!r}. "
            f"Available: {', '.join(list_adapters())}",
            file=sys.stderr,
        )
        return 2

    adapter_names = [only] if only else list_adapters()
    dry_run = args.dry_run

    # Load agents and profiles once — used for per-agent config generation
    agents, _ = load_agents(root)
    _, profiles_by_id = load_profiles(root)

    for ws_id in workspace_ids:
        try:
            ctx = build_workspace_context(root, ws_id)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2

        workspace = ctx["workspace"]
        for aname in adapter_names:
            adapter = get_adapter(aname)

            # Workspace-level config (existing behaviour)
            files = adapter.generate(root, workspace, ctx)
            for gf in files:
                if dry_run:
                    _print_dry_run_block(gf.rel_path, gf.description, gf.content)
                else:
                    target = root / gf.rel_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(gf.content, encoding="utf-8")
                    print(f"wrote: {gf.rel_path} ({gf.description})")

    # Agent files and project-root hooks — once per adapt run (not per workspace)
    for aname in adapter_names:
        adapter = get_adapter(aname)
        if agents:
            for gf in adapter.generate_agents(root, agents, profiles_by_id):
                if dry_run:
                    _print_dry_run_block(gf.rel_path, gf.description, gf.content)
                else:
                    target = root / gf.rel_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(gf.content, encoding="utf-8")
                    print(f"wrote: {gf.rel_path} ({gf.description})")

        for gf in adapter.generate_project_artifacts(root, workspace_ids, agents):
            if dry_run:
                _print_dry_run_block(gf.rel_path, gf.description, gf.content)
            else:
                target = root / gf.rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(gf.content, encoding="utf-8")
                print(f"wrote: {gf.rel_path} ({gf.description})")

    return 0


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="onecxt",
        description="one-context — multi-repository workspace CLI",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="one-context root (directory containing meta/repos.yaml). "
        "Default: walk parents from cwd or use ONECXT_ROOT.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Enable verbose (DEBUG) logging to stderr",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_doctor = sub.add_parser("doctor", help="Validate manifests and local clone state")
    p_doctor.set_defaults(func=_cmd_doctor)

    p_sync = sub.add_parser(
        "sync",
        help="Clone or fast-forward pull repositories from meta/repos.yaml",
    )
    p_sync.add_argument(
        "select",
        nargs="*",
        metavar="ID_OR_ALIAS",
        help="If set, only these repo ids or aliases (case-insensitive)",
    )
    p_sync.add_argument(
        "--jobs", "-j",
        type=int,
        default=4,
        metavar="N",
        help="Number of parallel workers (default: 4, use 1 for serial)",
    )
    p_sync.set_defaults(func=_cmd_sync)

    p_repo = sub.add_parser("repo", help="Repository commands")
    repo_sub = p_repo.add_subparsers(dest="repo_command", required=True)
    p_repo_list = repo_sub.add_parser("list", help="List registered repositories")
    p_repo_list.set_defaults(func=_cmd_repo_list)

    p_ws = sub.add_parser("workspace", help="Workspace commands")
    ws_sub = p_ws.add_subparsers(dest="ws_command", required=True)
    p_ws_list = ws_sub.add_parser("list", help="List workspaces from meta/workspaces.yaml")
    p_ws_list.set_defaults(func=_cmd_workspace_list)
    p_ws_show = ws_sub.add_parser(
        "show",
        help="Print workspace definition and resolved repo paths (JSON)",
    )
    p_ws_show.add_argument("id", metavar="WORKSPACE_ID", help="Workspace id")
    p_ws_show.set_defaults(func=_cmd_workspace_show)

    p_ctx = sub.add_parser("context", help="Context export commands")
    ctx_sub = p_ctx.add_subparsers(dest="context_command", required=True)
    p_ctx_export = ctx_sub.add_parser(
        "export",
        help="Export a minimal workspace context bundle",
    )
    p_ctx_export.add_argument("id", metavar="WORKSPACE_ID", help="Workspace id")
    p_ctx_export.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format (default: json)",
    )
    p_ctx_export.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write export to a file instead of stdout",
    )
    p_ctx_export.set_defaults(func=_cmd_context_export)

    p_prof = sub.add_parser("profile", help="Profile commands")
    prof_sub = p_prof.add_subparsers(dest="prof_command", required=True)
    p_prof_list = prof_sub.add_parser("list", help="List profiles from meta/profiles.yaml")
    p_prof_list.set_defaults(func=_cmd_profile_list)

    p_adapt = sub.add_parser(
        "adapt",
        help="Generate tool-specific config files from workspace + profile",
    )
    p_adapt.add_argument(
        "workspace_id",
        nargs="?",
        metavar="WORKSPACE_ID",
        default=None,
        help="Workspace id to generate configs for",
    )
    p_adapt.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="Generate configs for all workspaces",
    )
    p_adapt.add_argument(
        "--only",
        metavar="ADAPTER",
        default=None,
        help="Only run a specific adapter (e.g. cursor, claude_code, openclaw)",
    )
    p_adapt.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print generated content without writing files",
    )
    p_adapt.set_defaults(func=_cmd_adapt)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(verbose=args.verbose)

    try:
        root = _resolve_root(args.root)
    except ManifestError as e:
        print(e.message, file=sys.stderr)
        raise SystemExit(1) from e

    raise SystemExit(args.func(root, args))
