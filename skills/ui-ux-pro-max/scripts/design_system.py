#!/usr/bin/env python3
"""Return traceable UI design candidates; never select or write a final design."""

import json
import re
import uuid
from pathlib import Path

from core import search, search_stack


SEARCH_CONFIG = {"product": 3, "style": 3, "color": 2, "typography": 2}
PLATFORM_BY_STACK = {
    **dict.fromkeys(("react", "nextjs", "vue", "svelte", "astro", "nuxtjs", "nuxt-ui", "html-tailwind", "shadcn", "threejs", "angular", "laravel"), "web"),
    "swiftui": "apple", "jetpack-compose": "android",
    **dict.fromkeys(("javafx", "wpf", "winui", "uwp"), "desktop"),
}
CROSS_PLATFORM_STACKS = {"flutter", "react-native", "avalonia", "uno"}
PLATFORMS = {"web", "mini-program", "apple", "android", "desktop"}
IMPLEMENTATION_FIELDS = {
    "CSS Import", "GSAP Snippet", "Tailwind Config", "Import Code",
    "Code Example Good", "Code Example Bad", "Code Good", "Code Bad",
}
NATIVE_ONLY_EXCLUSIONS = IMPLEMENTATION_FIELDS | {
    "AI Prompt Keywords", "CSS/Technical Keywords", "Design System Variables",
    "Effects & Animation", "Framework Compatibility", "Implementation Checklist",
}


def safe_slug(name: str, fallback: str = "default") -> str:
    """Make one safe path segment."""
    slug = re.sub(r"[^a-z0-9_-]+", "-", str(name).lower()).strip("-")
    return slug or fallback


def _candidate_rows(result: dict, platform: str = None, include_implementation: bool = False) -> list:
    candidates = []
    for row in result.get("results", []):
        candidate = {key: value for key, value in row.items()
                     if key not in {"_source", "_match_basis"}
                     and (include_implementation or key not in IMPLEMENTATION_FIELDS)
                     and (platform in {None, "web"} or key not in NATIVE_ONLY_EXCLUSIONS)}
        candidate["source"] = row.get("_source", {"file": result.get("file", ""), "line": None})
        candidate["match_basis"] = row.get("_match_basis", "BM25 lexical match")
        candidates.append(candidate)
    return candidates


def _resolve_platform(stack: str = None, platform: str = None) -> tuple[str | None, list[str]]:
    inferred = PLATFORM_BY_STACK.get(stack)
    unresolved = []
    if stack in CROSS_PLATFORM_STACKS and platform == "mini-program":
        raise ValueError(f"platform '{platform}' conflicts with cross-platform stack '{stack}'; choose a host platform")
    if stack in CROSS_PLATFORM_STACKS and not platform:
        unresolved.append(f"stack '{stack}' is cross-platform; choose a platform explicitly")
    elif stack and stack not in CROSS_PLATFORM_STACKS and not inferred:
        unresolved.append(f"stack '{stack}' has no platform mapping")
    if platform and inferred and platform != inferred:
        raise ValueError(f"platform '{platform}' conflicts with stack '{stack}' ({inferred})")
    return platform or inferred, unresolved


class DesignSystemGenerator:
    """Collect independently reviewable BM25 candidates."""

    def generate(self, query: str, project_name: str = None, *, stack: str = None,
                 platform: str = None, surface: str = None, locale: str = None,
                 max_results: int = 3, variance: int = None, motion: int = None,
                 density: int = None, page: str = None) -> dict:
        if not query or not query.strip():
            raise ValueError("query must not be blank")
        if not isinstance(max_results, int) or isinstance(max_results, bool) or max_results < 1:
            raise ValueError("max-results must be a positive integer")
        if platform and platform not in PLATFORMS:
            raise ValueError(f"unknown platform '{platform}'")
        if surface and surface not in {"persuade", "operate", "read", "experience"}:
            raise ValueError(f"unknown surface '{surface}'")
        for dial_name, dial_value in {"variance": variance, "motion": motion, "density": density}.items():
            if dial_value is not None and (not isinstance(dial_value, int) or isinstance(dial_value, bool) or not 1 <= dial_value <= 10):
                raise ValueError(f"{dial_name} must be an integer from 1 to 10")
        resolved_platform, unresolved = _resolve_platform(stack, platform)
        candidates = {}
        for domain, limit in SEARCH_CONFIG.items():
            result = search(query, domain, min(limit, max_results))
            if "error" in result:
                unresolved.append(result["error"])
                candidates[domain] = []
            else:
                candidates[domain] = _candidate_rows(result, resolved_platform)
                if not candidates[domain]:
                    unresolved.append(f"{domain}: no BM25 matches for query")
        if surface == "persuade":
            landing_result = search(query, "landing", min(2, max_results))
            if "error" in landing_result:
                candidates["landing"] = []
                unresolved.append(landing_result["error"])
            else:
                candidates["landing"] = _candidate_rows(landing_result, resolved_platform)
            if not candidates["landing"] and "error" not in landing_result:
                unresolved.append("landing: no BM25 matches for query")
        if stack:
            stack_result = search_stack(query, stack, max_results)
            if "error" in stack_result:
                unresolved.append(stack_result["error"])
                candidates["stack"] = []
            else:
                candidates["stack"] = _candidate_rows(
                    stack_result, resolved_platform, include_implementation=True
                )
                if not candidates["stack"]:
                    unresolved.append(f"stack: no BM25 matches for query")
        if not resolved_platform:
            unresolved.append("platform is unresolved; verify host-platform conventions before implementation")
        if locale and locale.lower().startswith(("zh", "cn")):
            unresolved.append("CJK font coverage requires verified font evidence; database labels are not verification")
        return {
            "schema_version": 1,
            "kind": "design_candidates",
            "status": "candidate",
            "query": query,
            "project_name": project_name or query,
            "context": {"stack": stack, "platform": resolved_platform, "surface": surface,
                        "locale": locale, "page": page, "dials": {key: value for key, value in {
                            "variance": variance, "motion": motion, "density": density
                        }.items() if value is not None}},
            "candidates": candidates,
            "advisory_reasoning": "Ranks represent BM25 lexical matches, not aesthetic or accessibility scores. Review candidates independently.",
            "unresolved": unresolved,
            "warnings": [
                "Platform conventions and existing project components take precedence over candidates.",
                "CSV accessibility and performance labels are unverified candidate metadata, not page verification.",
            ],
        }


def format_markdown(candidates: dict) -> str:
    lines = [
        f"# Design candidates: {candidates['project_name']}", "",
        f"Status: {candidates['status']}", f"Query: {candidates['query']}",
        f"Context: {json.dumps(candidates['context'], ensure_ascii=False, sort_keys=True)}",
        f"Advisory: {candidates['advisory_reasoning']}",
    ]
    for domain, rows in candidates["candidates"].items():
        lines.extend(("", f"## {domain}"))
        for row in rows:
            lines.append(f"- {json.dumps(row, ensure_ascii=False, sort_keys=True)}")
    if candidates["unresolved"]:
        lines.extend(("", "## Unresolved", *[f"- {item}" for item in candidates["unresolved"]]))
    lines.extend(("", "## Warnings", *[f"- {item}" for item in candidates["warnings"]]))
    if candidates.get("persistence"):
        lines.extend(("", "## Persistence", *[f"- {path}" for path in candidates["persistence"]["created_files"]]))
    return "\n".join(lines)


def persist_design_system(design_system: dict, page: str = None, output_dir: str = None,
                          page_query: str = None) -> dict:
    """Create one candidate JSON file without touching formal design files."""
    base_dir = Path(output_dir) if output_dir else Path.cwd()
    project = safe_slug(design_system.get("project_name") or "default")
    filename = f"{safe_slug(page or 'candidate', 'candidate')}-{uuid.uuid4().hex}.json"
    candidate_file = base_dir / "design-system" / project / "candidates" / filename
    probe = base_dir
    for part in ("design-system", project, "candidates"):
        probe /= part
        if probe.is_symlink():
            raise ValueError("candidate path escapes design-system/<project>/candidates")
    candidate_file.parent.mkdir(parents=True, exist_ok=True)
    with candidate_file.open("x", encoding="utf-8") as handle:
        json.dump(design_system, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return {"status": "created", "created_files": [str(candidate_file)]}


def generate_design_system(query: str, project_name: str = None, output_format: str = "ascii",
                           persist: bool = False, page: str = None, output_dir: str = None,
                           variance: int = None, motion: int = None, density: int = None, *,
                           stack: str = None, platform: str = None, surface: str = None,
                           locale: str = None, max_results: int = 3) -> str:
    """Return candidate JSON or text while preserving the original positional API."""
    if output_format not in {"ascii", "markdown", "json"}:
        raise ValueError(f"unknown output format '{output_format}'")
    if output_dir is not None and not persist:
        raise ValueError("output_dir requires persist=True")
    design_system = DesignSystemGenerator().generate(
        query, project_name, stack=stack, platform=platform, surface=surface, locale=locale,
        max_results=max_results, variance=variance, motion=motion, density=density, page=page,
    )
    if persist:
        design_system["persistence"] = persist_design_system(design_system, page, output_dir, query)
    if output_format == "json":
        return json.dumps(design_system, ensure_ascii=False, indent=2)
    return format_markdown(design_system)
