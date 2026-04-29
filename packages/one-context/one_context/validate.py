from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from one_context.agents import load_agents
from one_context.context import build_workspace_context
from one_context.profiles import load_mixins, load_profiles
from one_context.repos import load_repos
from one_context.workspaces import load_workspaces

# Pattern to match @path/to/file.md references inside .md files (Claude Code adapter style).
# Matches things like @knowledge/standards/agent-framework.md but not email addresses or CSS @rules.
AT_REF_PATTERN = re.compile(r"(?<!\w)@([a-zA-Z][\w/.-]*\.md)\b")

VALID_ROLES = {"pm", "architect", "dev", "qa", "sre", "reviewer", "knowledge-keeper"}


@dataclass
class DoctorResult:
    errors: list[str]
    warnings: list[str]
    info: list[str] = field(default_factory=list)


def doctor(root: Path) -> DoctorResult:
    """
    Cross-check meta/repos.yaml, meta/workspaces.yaml, and meta/profiles.yaml.

    Also emits warnings for expected local paths that are missing or not git repos.
    """
    errors: list[str] = []
    warnings: list[str] = []

    try:
        repo_entries, _ = load_repos(root)
    except Exception as e:
        return DoctorResult(errors=[str(e)], warnings=[])

    repo_ids: set[str] = {e["id"] for e in repo_entries}

    try:
        workspaces, _ = load_workspaces(root)
    except Exception as e:
        errors.append(str(e))
        workspaces = []

    try:
        profiles, profiles_by_id = load_profiles(root)
    except Exception as e:
        errors.append(str(e))
        profiles = []
        profiles_by_id = {}

    try:
        mixins, mixins_by_id = load_mixins(root)
    except Exception as e:
        errors.append(str(e))
        mixins = []
        mixins_by_id = {}

    profile_ids = {p["id"] for p in profiles}

    # --- Inheritance & mixin validation ---
    for p in profiles:
        pid = p["id"]
        parent_id = p.get("extends")
        if parent_id:
            plk = parent_id.casefold()
            if plk not in profiles_by_id:
                errors.append(
                    f"profile {pid!r}: extends unknown profile {parent_id!r}"
                )
            else:
                parent = profiles_by_id[plk]
                if parent.get("extends"):
                    errors.append(
                        f"profile {pid!r}: multi-layer inheritance not allowed "
                        f"(parent {parent_id!r} also has 'extends')"
                    )
                if parent.get("mixins"):
                    errors.append(
                        f"profile {pid!r}: parent {parent_id!r} must not have 'mixins'"
                    )

        mixin_refs = p.get("mixins") or []
        for mid in mixin_refs:
            mlk = mid.casefold()
            if mlk not in mixins_by_id:
                errors.append(
                    f"profile {pid!r}: references unknown mixin {mid!r}"
                )

    for m in mixins:
        mid = m["id"]
        if m.get("extends"):
            errors.append(f"mixin {mid!r}: mixins must not have 'extends'")
        if m.get("mixins"):
            errors.append(f"mixin {mid!r}: mixins must not have 'mixins'")

    for ws in workspaces:
        wid = ws.get("id", "?")
        raw_repos = ws.get("repos")
        if raw_repos is not None:
            if not isinstance(raw_repos, list):
                errors.append(f"workspace {wid!r}: 'repos' must be a list")
            else:
                for rid in raw_repos:
                    if not isinstance(rid, str) or not rid.strip():
                        errors.append(f"workspace {wid!r}: invalid repo id in repos list")
                        continue
                    rid = rid.strip()
                    if rid not in repo_ids:
                        errors.append(
                            f"workspace {wid!r}: unknown repo id {rid!r} "
                            f"(not in meta/repos.yaml)"
                        )

        raw_prof = ws.get("profiles")
        if raw_prof is None:
            continue
        if not isinstance(raw_prof, list):
            errors.append(f"workspace {wid!r}: 'profiles' must be a list")
            continue
        for pid in raw_prof:
            if not isinstance(pid, str) or not pid.strip():
                errors.append(f"workspace {wid!r}: invalid profile id in profiles list")
                continue
            pid = pid.strip()
            if pid not in profile_ids:
                errors.append(
                    f"workspace {wid!r}: unknown profile id {pid!r} "
                    f"(not in meta/profiles.yaml)"
                )

    # --- Agents validation ---
    try:
        agents, agents_by_id = load_agents(root)
    except Exception as e:
        errors.append(str(e))
        agents = []
        agents_by_id = {}

    for agent in agents:
        aid = agent.get("id", "?")

        # Validate role
        role = agent.get("role")
        if not role:
            errors.append(f"agent {aid!r}: missing required 'role' field")
        elif role not in VALID_ROLES:
            errors.append(
                f"agent {aid!r}: invalid role {role!r}. "
                f"Must be one of: {', '.join(sorted(VALID_ROLES))}"
            )

        # Validate profile reference
        profile_ref = agent.get("profile")
        if profile_ref:
            plk = profile_ref.casefold()
            if plk not in profiles_by_id:
                errors.append(
                    f"agent {aid!r}: references unknown profile {profile_ref!r}"
                )

        # Validate knowledge paths (warn only)
        knowledge_paths = agent.get("knowledge") or []
        for kp in knowledge_paths:
            if not isinstance(kp, str) or not kp.strip():
                continue
            target = (root / kp.strip()).resolve()
            if not target.exists():
                warnings.append(
                    f"agent {aid!r}: knowledge path not found: {kp}"
                )

        # Validate worktree config (dev agent)
        wt = agent.get("worktree")
        if wt:
            if role and role != "dev":
                warnings.append(
                    f"agent {aid!r}: 'worktree' config is intended for "
                    f"role=dev, but agent has role={role!r}"
                )
            if isinstance(wt, dict):
                for req_key in ("branch_pattern", "path_pattern"):
                    if not wt.get(req_key):
                        errors.append(
                            f"agent {aid!r}: worktree.{req_key} is required"
                        )
                bp = wt.get("branch_pattern", "")
                pp = wt.get("path_pattern", "")
                if bp and "{feature_id}" not in bp:
                    warnings.append(
                        f"agent {aid!r}: worktree.branch_pattern should "
                        "contain {{feature_id}} placeholder"
                    )
                if pp and ("{repo_id}" not in pp or "{feature_id}" not in pp):
                    warnings.append(
                        f"agent {aid!r}: worktree.path_pattern should "
                        "contain {{repo_id}} and {{feature_id}} placeholders"
                    )
            else:
                errors.append(
                    f"agent {aid!r}: 'worktree' must be a mapping"
                )

    # --- deploy.yaml validation (per-repo) ---
    sre_agent = next(
        (a for a in agents if a.get("role") == "sre"), None
    )
    deploy_filename = (
        sre_agent.get("deploy_manifest", "deploy.yaml") if sre_agent else None
    )
    if deploy_filename:
        for entry in repo_entries:
            repo_path = (root / entry["path"]).resolve()
            deploy_path = repo_path / deploy_filename
            if deploy_path.is_file():
                from one_context.deploy import validate_deploy_yaml

                d_errors, d_warnings = validate_deploy_yaml(deploy_path)
                for e in d_errors:
                    errors.append(
                        f"repo {entry['id']!r} {deploy_filename}: {e}"
                    )
                for w in d_warnings:
                    warnings.append(
                        f"repo {entry['id']!r} {deploy_filename}: {w}"
                    )

    for entry in repo_entries:
        target = (root / entry["path"]).resolve()
        label = entry["id"]
        if not target.exists():
            warnings.append(f"repo {label}: local path missing {target}")
        elif not (target / ".git").is_dir():
            warnings.append(
                f"repo {label}: path exists but is not a git repo: {target}"
            )

    # --- Knowledge reference integrity checks ---
    _check_knowledge_integrity(root, workspaces, agents, errors, warnings)

    return DoctorResult(errors=errors, warnings=warnings, info=[])


def workspace_context_summary(root: Path, workspace_id: str) -> dict[str, Any]:
    """Return resolved workspace entry plus repo paths for tooling."""
    data = build_workspace_context(root, workspace_id)
    repos_out = [
        {
            "id": repo["id"],
            "path": repo["path"],
            "url": repo["url"],
        }
        for repo in data["repos"]
    ]
    return {"workspace": data["workspace"], "repos": repos_out}


# ---------------------------------------------------------------------------
# Knowledge integrity checks
# ---------------------------------------------------------------------------

def _collect_all_knowledge_references(
    workspaces: list[dict[str, Any]],
    agents: list[dict[str, Any]],
) -> set[str]:
    """Collect all knowledge paths referenced by workspaces and agents.

    Returns a set of relative paths (forward-slash, as declared in yaml).
    Directory references (ending with /) are included as-is — callers must
    expand them separately.
    """
    refs: set[str] = set()
    for ws in workspaces:
        context = ws.get("context")
        if not isinstance(context, dict):
            continue
        for kp in context.get("knowledge") or []:
            if isinstance(kp, str) and kp.strip():
                refs.add(kp.strip())
    for agent in agents:
        for kp in agent.get("knowledge") or []:
            if isinstance(kp, str) and kp.strip():
                refs.add(kp.strip())
    return refs


def _expand_directory_refs(root: Path, refs: set[str]) -> set[str]:
    """Expand directory references to individual .md file paths.

    For each ref that resolves to a directory on disk, replace it with all
    ``.md`` files found recursively under that directory.  Non-directory refs
    pass through unchanged.
    """
    expanded: set[str] = set()
    for ref in refs:
        target = root / ref
        if target.is_dir():
            for md_file in sorted(target.rglob("*.md")):
                rel = md_file.relative_to(root).as_posix()
                expanded.add(rel)
        else:
            expanded.add(ref)
    return expanded


def _check_knowledge_integrity(
    root: Path,
    workspaces: list[dict[str, Any]],
    agents: list[dict[str, Any]],
    errors: list[str],
    warnings: list[str],
) -> None:
    """Run all knowledge-layer integrity checks and append to *errors*/*warnings*."""
    raw_refs = _collect_all_knowledge_references(workspaces, agents)

    # -- Check 1: workspace knowledge paths exist --
    for ws in workspaces:
        wid = ws.get("id", "?")
        context = ws.get("context")
        if not isinstance(context, dict):
            continue
        for kp in context.get("knowledge") or []:
            if not isinstance(kp, str) or not kp.strip():
                continue
            target = (root / kp.strip()).resolve()
            if not target.exists():
                warnings.append(
                    f"workspace {wid!r}: knowledge path not found: {kp.strip()}"
                )

    # -- Check 2: orphan knowledge files --
    knowledge_dir = root / "knowledge"
    if knowledge_dir.is_dir():
        expanded_refs = _expand_directory_refs(root, raw_refs)
        # Collect all .md files under knowledge/
        all_knowledge_files: set[str] = set()
        for md_file in knowledge_dir.rglob("*.md"):
            rel = md_file.relative_to(root).as_posix()
            all_knowledge_files.add(rel)
        orphans = sorted(all_knowledge_files - expanded_refs)
        for orphan in orphans:
            warnings.append(
                f"knowledge: orphan file not referenced by any agent/workspace: "
                f"{orphan}"
            )

    # -- Check 3: dangling @-references inside .md files --
    # Scan knowledge/, docs/, and features/ for @path/to/file.md patterns.
    _check_at_references(root, warnings)


def _check_at_references(root: Path, warnings: list[str]) -> None:
    """Scan .md files for @path.md references and warn if targets don't exist."""
    scan_dirs = ["knowledge", "docs", "features"]
    seen: dict[str, list[str]] = {}  # ref -> [source_file, ...]

    for dir_name in scan_dirs:
        scan_root = root / dir_name
        if not scan_root.is_dir():
            continue
        for md_file in sorted(scan_root.rglob("*.md")):
            try:
                content = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            rel_source = md_file.relative_to(root).as_posix()
            for match in AT_REF_PATTERN.finditer(content):
                ref_path = match.group(1)
                # Skip if the target is inside node_modules or similar
                if "node_modules" in ref_path:
                    continue
                abs_target = root / ref_path
                if not abs_target.exists():
                    if ref_path not in seen:
                        seen[ref_path] = []
                    seen[ref_path].append(rel_source)

    for ref_path in sorted(seen):
        sources = seen[ref_path]
        source_list = ", ".join(sources)
        warnings.append(
            f"knowledge: dangling @-reference: @{ref_path} "
            f"(referenced in {source_list})"
        )


# ---------------------------------------------------------------------------
# Knowledge graph generation
# ---------------------------------------------------------------------------

def _safe_mermaid_node_id(path: str) -> str:
    """Convert a file path to a safe Mermaid node ID (alphanumeric + underscores)."""
    return path.replace("/", "_").replace(".", "_").replace("-", "_")


def _classify_knowledge_path(path: str) -> str:
    """Return the subcategory of a knowledge/ path (standards, playbooks, etc.)."""
    parts = path.split("/")
    if len(parts) >= 2 and parts[0] == "knowledge":
        return parts[1]  # e.g. "standards", "playbooks", "references", "prompts"
    return "other"


def generate_knowledge_graph(root: Path) -> str:
    """Generate a Mermaid knowledge graph from meta/ and knowledge/ references.

    Produces a graph showing:
    - Agents as nodes grouped by role
    - Knowledge subcategories as subgraph clusters
    - Agent → knowledge edges from meta/agents.yaml
    - Workspace → knowledge edges from meta/workspaces.yaml
    - Internal @-reference edges between .md files

    Returns a Markdown code block containing the Mermaid source.
    """
    workspaces, _ = load_workspaces(root)
    agents, _ = load_agents(root)

    lines = ["```mermaid", "graph TD"]

    # Collect references
    raw_refs = _collect_all_knowledge_references(workspaces, agents)
    expanded_refs = _expand_directory_refs(root, raw_refs)

    # Track all rendered node IDs and category subgraph IDs
    rendered_node_ids: set[str] = set()
    category_ids: set[str] = set()

    # --- Subgraphs for knowledge categories ---
    knowledge_dir = root / "knowledge"
    categories: dict[str, list[str]] = {}  # category -> [rel_paths]
    if knowledge_dir.is_dir():
        for md_file in sorted(knowledge_dir.rglob("*.md")):
            rel = md_file.relative_to(root).as_posix()
            cat = _classify_knowledge_path(rel)
            categories.setdefault(cat, []).append(rel)

    # Also include docs/ and features/ as categories
    for extra_dir in ["docs", "features"]:
        extra_path = root / extra_dir
        if extra_path.is_dir():
            for md_file in sorted(extra_path.rglob("*.md")):
                rel = md_file.relative_to(root).as_posix()
                categories.setdefault(extra_dir, []).append(rel)

    for cat in sorted(categories):
        cat_files = [f for f in categories[cat] if f in expanded_refs]
        if not cat_files:
            continue
        lines.append(f"    subgraph {cat}")
        for f in cat_files[:15]:  # Limit to 15 nodes per subgraph for readability
            node_id = _safe_mermaid_node_id(f)
            label = Path(f).stem
            lines.append(f"        {node_id}[{label}]")
            rendered_node_ids.add(node_id)
        remaining = len(cat_files) - 15
        if remaining > 0:
            lines.append(f"        {cat}_more[... +{remaining} more]")
        lines.append("    end")
        category_ids.add(cat)

    # --- Agent nodes grouped as subgraph ---
    agent_node_ids: set[str] = set()
    if agents:
        lines.append("    subgraph agents[Agents]")
        for agent in sorted(agents, key=lambda a: str(a.get("id", ""))):
            aid = agent.get("id", "unknown")
            role = agent.get("role", "")
            node_id = f"agent_{aid}"
            lines.append(f"        {node_id}[{aid} · {role}]")
            agent_node_ids.add(node_id)
        lines.append("    end")

    # --- Workspace nodes ---
    ws_node_ids: set[str] = set()
    if workspaces:
        lines.append("    subgraph workspaces[Workspaces]")
        for ws in sorted(workspaces, key=lambda w: str(w.get("id", ""))):
            wid = ws.get("id", "unknown")
            node_id = f"ws_{wid}"
            lines.append(f"        {node_id}[{wid}]")
            ws_node_ids.add(node_id)
        lines.append("    end")

    # --- Edges: agent → knowledge ---
    for agent in agents:
        aid = agent.get("id", "unknown")
        agent_node = f"agent_{aid}"
        knowledge_paths = agent.get("knowledge") or []
        for kp in knowledge_paths:
            if not isinstance(kp, str) or not kp.strip():
                continue
            kp_stripped = kp.strip()
            target = (root / kp_stripped).resolve()
            if target.is_dir():
                cat = _classify_knowledge_path(kp_stripped)
                if cat in category_ids:
                    lines.append(f"    {agent_node} -->|reads| {cat}")
            else:
                node_id = _safe_mermaid_node_id(kp_stripped)
                if node_id in rendered_node_ids:
                    lines.append(f"    {agent_node} -->|reads| {node_id}")

    # --- Edges: workspace → knowledge ---
    for ws in workspaces:
        wid = ws.get("id", "unknown")
        ws_node = f"ws_{wid}"
        context = ws.get("context")
        if not isinstance(context, dict):
            continue
        for kp in context.get("knowledge") or []:
            if not isinstance(kp, str) or not kp.strip():
                continue
            kp_stripped = kp.strip()
            target = (root / kp_stripped).resolve()
            if target.is_dir():
                cat = _classify_knowledge_path(kp_stripped)
                if cat in category_ids:
                    lines.append(f"    {ws_node} -->|loads| {cat}")
            else:
                node_id = _safe_mermaid_node_id(kp_stripped)
                if node_id in rendered_node_ids:
                    lines.append(f"    {ws_node} -->|loads| {node_id}")

    # --- Edges: internal @-references (limit to valid ones) ---
    scan_dirs = ["knowledge", "docs", "features"]
    for dir_name in scan_dirs:
        scan_root = root / dir_name
        if not scan_root.is_dir():
            continue
        for md_file in sorted(scan_root.rglob("*.md")):
            try:
                content = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            source_rel = md_file.relative_to(root).as_posix()
            source_id = _safe_mermaid_node_id(source_rel)
            if source_id not in rendered_node_ids:
                continue
            for match in AT_REF_PATTERN.finditer(content):
                ref_path = match.group(1)
                if "node_modules" in ref_path:
                    continue
                abs_target = root / ref_path
                if abs_target.exists():
                    target_id = _safe_mermaid_node_id(ref_path)
                    if target_id in rendered_node_ids and source_id != target_id:
                        lines.append(f"    {source_id} -->|@ref| {target_id}")

    lines.append("```")
    return "\n".join(lines)
