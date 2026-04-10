from __future__ import annotations

import argparse
import difflib
import logging
import sys
from pathlib import Path

from one_context import __version__
from one_context.agents import load_agents
from one_context.context import build_workspace_context, render_workspace_context
from one_context.dotenv import load_dotenv
from one_context.errors import ManifestError
from one_context.log import setup_logging
from one_context.profiles import load_mixins, load_profiles, resolve_profile
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
    if getattr(args, "compress", False) or getattr(args, "target_tokens", None) is not None:
        from one_context.context import apply_context_compression

        rendered = apply_context_compression(
            rendered,
            compress=bool(getattr(args, "compress", False)),
            target_tokens=getattr(args, "target_tokens", None),
        )
    if args.output is None:
        print(rendered, end="")
        return 0

    target = args.output.expanduser()
    if not target.is_absolute():
        target = root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")
    return 0


def _cmd_profile_list(root: Path, _args: argparse.Namespace) -> int:
    profiles, _ = load_profiles(root)
    mixins, _ = load_mixins(root)
    if not profiles and not mixins:
        print("(no profiles.yaml or empty)")
        return 0
    for p in profiles:
        pid = p.get("id", "")
        name = p.get("name", "")
        extends = p.get("extends", "")
        tag = f"[extends {extends}]" if extends else ""
        mxs = p.get("mixins")
        if mxs:
            tag += f" [mixins: {', '.join(mxs)}]"
        print(f"{pid}\t{name}\tprofile\t{tag}".rstrip())
    for m in mixins:
        mid = m.get("id", "")
        name = m.get("name", "")
        print(f"{mid}\t{name}\tmixin")
    return 0


def _cmd_profile_show(root: Path, args: argparse.Namespace) -> int:
    profiles, profiles_by_id = load_profiles(root)
    mixins, mixins_by_id = load_mixins(root)

    lk = args.id.casefold()
    # Look in profiles first, then mixins
    entry = profiles_by_id.get(lk) or mixins_by_id.get(lk)
    if entry is None:
        print(f"error: unknown profile or mixin id {args.id!r}", file=sys.stderr)
        return 2

    if args.resolved and lk in profiles_by_id:
        import json
        resolved = resolve_profile(args.id, profiles_by_id, mixins_by_id)
        print(json.dumps(resolved, indent=2, ensure_ascii=False))
    else:
        import json
        print(json.dumps(entry, indent=2, ensure_ascii=False))
    return 0


def _cmd_agent_list(root: Path, _args: argparse.Namespace) -> int:
    agents, _ = load_agents(root)
    if not agents:
        print("(no agents.yaml or empty agents list)")
        return 0
    for a in agents:
        aid = a.get("id", "")
        name = a.get("name", "")
        role = a.get("role", "")
        print(f"{aid}\t{name}\t{role}")
    return 0


def _cmd_agent_show(root: Path, args: argparse.Namespace) -> int:
    agents, agents_by_id = load_agents(root)

    lk = args.id.casefold()
    entry = agents_by_id.get(lk)
    if entry is None:
        print(f"error: unknown agent id {args.id!r}", file=sys.stderr)
        return 2

    import json
    print(json.dumps(entry, indent=2, ensure_ascii=False))
    return 0


# ---------------------------------------------------------------------------
# Worktree commands
# ---------------------------------------------------------------------------

def _cmd_worktree_setup(root: Path, args: argparse.Namespace) -> int:
    from one_context.worktree import setup_worktrees

    repo_ids = args.repos.split(",") if args.repos else None
    try:
        manifest = setup_worktrees(root, args.feature_id, repo_ids)
    except (ManifestError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    for wt in manifest.get("worktrees", []):
        print(f"  {wt['repo_id']}\t{wt['path']}\t(branch: {wt['branch']})")
    print(f"worktrees.yaml written for feature {args.feature_id}")
    return 0


def _cmd_worktree_status(root: Path, args: argparse.Namespace) -> int:
    from one_context.worktree import status_worktrees

    try:
        manifest = status_worktrees(root, args.feature_id)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2

    for wt in manifest.get("worktrees", []):
        print(f"  {wt.get('repo_id')}\t{wt.get('status')}\t{wt.get('path')}\t{wt.get('branch')}")
    return 0


def _cmd_worktree_teardown(root: Path, args: argparse.Namespace) -> int:
    from one_context.worktree import teardown_worktrees

    final_status = args.status if args.status else "merged"
    try:
        manifest = teardown_worktrees(root, args.feature_id, final_status)
    except (ManifestError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    for wt in manifest.get("worktrees", []):
        print(f"  {wt.get('repo_id')}\t{wt.get('status')}")
    print(f"worktrees.yaml updated for feature {args.feature_id}")
    return 0


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


def _emit_file(root: Path, gf, dry_run: bool) -> None:
    """Write a generated file to disk, or print in dry-run mode."""
    if dry_run:
        _print_dry_run_block(gf.rel_path, gf.description, gf.content)
    else:
        target = root / gf.rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(gf.content, encoding="utf-8")
        print(f"wrote: {gf.rel_path} ({gf.description})")


def _check_generated(root: Path, files: list) -> int:
    """Compare generated content to disk. Return 0 if all match, 1 if any differ."""
    mismatched: list[str] = []
    for gf in files:
        target = root / gf.rel_path
        if not target.is_file():
            mismatched.append(f"  missing: {gf.rel_path}")
            continue
        existing = target.read_text(encoding="utf-8")
        if existing != gf.content:
            mismatched.append(f"  stale:   {gf.rel_path}")

    if mismatched:
        print("adapt --check: generated files are NOT up-to-date:", file=sys.stderr)
        for line in mismatched:
            print(line, file=sys.stderr)
        print(f"\nRun `onecxt adapt --all` to regenerate.", file=sys.stderr)
        return 1

    print("adapt --check: all generated files are up-to-date.")
    return 0


def _report_dirty_files(root: Path, files: list) -> None:
    """Detect and report files that were modified externally since last adapt."""
    dirty_count = 0
    for gf in files:
        target = root / gf.rel_path
        if not target.is_file():
            continue
        existing = target.read_text(encoding="utf-8")
        if existing != gf.content:
            dirty_count += 1
            diff_lines = list(difflib.unified_diff(
                existing.splitlines(keepends=True),
                gf.content.splitlines(keepends=True),
                fromfile=f"disk:{gf.rel_path}",
                tofile=f"generated:{gf.rel_path}",
                n=1,
            ))
            add_count = sum(1 for l in diff_lines if l.startswith("+") and not l.startswith("+++"))
            del_count = sum(1 for l in diff_lines if l.startswith("-") and not l.startswith("---"))
            print(f"  dirty: {gf.rel_path} (+{add_count}/-{del_count} lines)")

    if dirty_count:
        print(f"warning: {dirty_count} generated file(s) differ from expected output; overwriting.")


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
    check_mode = getattr(args, "check", False)

    if dry_run and check_mode:
        print("error: --dry-run and --check are mutually exclusive", file=sys.stderr)
        return 2

    # Load agents and profiles once — used for per-agent config generation
    agents, _ = load_agents(root)
    _, profiles_by_id = load_profiles(root)

    # Resolve profile inheritance so adapters see fully merged profiles
    _, mixins_by_id = load_mixins(root)
    resolved_profiles: dict = {}
    for pid in profiles_by_id:
        try:
            resolved_profiles[pid] = resolve_profile(pid, profiles_by_id, mixins_by_id)
        except Exception:
            resolved_profiles[pid] = profiles_by_id[pid]  # fallback to raw

    # Collect all generated files first
    from one_context.adapters import GeneratedFile
    all_generated: list[GeneratedFile] = []

    for ws_id in workspace_ids:
        try:
            ctx = build_workspace_context(root, ws_id)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2

        workspace = ctx["workspace"]
        for aname in adapter_names:
            adapter = get_adapter(aname)
            all_generated.extend(adapter.generate(root, workspace, ctx))

    # Agent files and project-root hooks — once per adapt run (not per workspace)
    for aname in adapter_names:
        adapter = get_adapter(aname)
        if agents:
            all_generated.extend(adapter.generate_agents(root, agents, resolved_profiles))
        all_generated.extend(adapter.generate_project_artifacts(root, workspace_ids, agents))

    # --check mode: compare only, do not write
    if check_mode:
        return _check_generated(root, all_generated)

    # Normal mode: report dirty files, then emit
    _report_dirty_files(root, all_generated)
    for gf in all_generated:
        _emit_file(root, gf, dry_run)

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
    p_ctx_export.add_argument(
        "--compress",
        action="store_true",
        default=False,
        help="Apply automatic token-budget compression to the export (approximate)",
    )
    p_ctx_export.add_argument(
        "--target-tokens",
        type=int,
        default=None,
        metavar="N",
        help="Approximate max tokens when compressing (implies compression if set)",
    )
    p_ctx_export.set_defaults(func=_cmd_context_export)

    p_prof = sub.add_parser("profile", help="Profile commands")
    prof_sub = p_prof.add_subparsers(dest="prof_command", required=True)
    p_prof_list = prof_sub.add_parser(
        "list", help="List profiles and mixins from meta/profiles.yaml",
    )
    p_prof_list.set_defaults(func=_cmd_profile_list)

    p_prof_show = prof_sub.add_parser(
        "show", help="Show a profile or mixin definition",
    )
    p_prof_show.add_argument("id", metavar="PROFILE_ID", help="Profile or mixin id")
    p_prof_show.add_argument(
        "--resolved",
        action="store_true",
        default=False,
        help="Output the fully-resolved profile after inheritance and mixin merge",
    )
    p_prof_show.set_defaults(func=_cmd_profile_show)

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
    p_adapt.add_argument(
        "--check",
        action="store_true",
        default=False,
        help="Check that generated files are up-to-date (exit 1 if not). Does not write.",
    )
    p_adapt.set_defaults(func=_cmd_adapt)

    p_agent = sub.add_parser("agent", help="Agent commands")
    agent_sub = p_agent.add_subparsers(dest="agent_command", required=True)
    p_agent_list = agent_sub.add_parser(
        "list", help="List agents from meta/agents.yaml",
    )
    p_agent_list.set_defaults(func=_cmd_agent_list)

    p_agent_show = agent_sub.add_parser(
        "show", help="Show an agent definition",
    )
    p_agent_show.add_argument("id", metavar="AGENT_ID", help="Agent id")
    p_agent_show.set_defaults(func=_cmd_agent_show)

    p_wt = sub.add_parser("worktree", help="Git worktree commands")
    wt_sub = p_wt.add_subparsers(dest="wt_command", required=True)

    p_wt_setup = wt_sub.add_parser("setup", help="Create worktrees for a feature")
    p_wt_setup.add_argument("feature_id", metavar="FEATURE_ID", help="Feature id (kebab-case)")
    p_wt_setup.add_argument(
        "--repos", default=None,
        help="Comma-separated repo ids (default: all repos)",
    )
    p_wt_setup.set_defaults(func=_cmd_worktree_setup)

    p_wt_status = wt_sub.add_parser("status", help="Show worktree status for a feature")
    p_wt_status.add_argument("feature_id", metavar="FEATURE_ID", help="Feature id")
    p_wt_status.set_defaults(func=_cmd_worktree_status)

    p_wt_teardown = wt_sub.add_parser("teardown", help="Remove worktrees for a feature")
    p_wt_teardown.add_argument("feature_id", metavar="FEATURE_ID", help="Feature id")
    p_wt_teardown.add_argument(
        "--status", choices=("merged", "abandoned"), default="merged",
        help="Status to set for removed worktrees (default: merged)",
    )
    p_wt_teardown.set_defaults(func=_cmd_worktree_teardown)

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
