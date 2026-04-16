from __future__ import annotations

import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.ports.source_backends import SkillManagementProviderPort, SkillSourceProviderPort

_EXCLUDED_SKILL_DIRS = frozenset((".git", ".github", ".hub", "__pycache__"))
_PLATFORM_MAP = {
    "macos": "darwin",
    "linux": "linux",
    "windows": "win32",
}


def _yaml_load(content: str) -> Any:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - exercised through fallback
        raise RuntimeError("PyYAML is not installed") from exc

    loader = getattr(yaml, "CSafeLoader", None) or yaml.SafeLoader
    return yaml.load(content, Loader=loader)


def _parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    frontmatter: dict[str, Any] = {}
    body = content

    if not content.startswith("---"):
        return frontmatter, body

    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return frontmatter, body

    yaml_content = content[3 : end_match.start() + 3]
    body = content[end_match.end() + 3 :]

    try:
        parsed = _yaml_load(yaml_content)
        if isinstance(parsed, dict):
            frontmatter = parsed
    except Exception:
        for line in yaml_content.strip().splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip()
        prerequisite_env_match = re.search(
            r"^\s*env_vars:\s*\[(?P<values>[^\]]*)\]\s*$",
            yaml_content,
            re.MULTILINE,
        )
        if prerequisite_env_match:
            raw_values = prerequisite_env_match.group("values")
            frontmatter["prerequisites"] = {
                "env_vars": [
                    item.strip().strip("\"'")
                    for item in raw_values.split(",")
                    if item.strip()
                ]
            }

        collect_secret_matches = re.findall(
            r"^\s*-\s*env_var:\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*$|^\s*env_var:\s*(?P<alt>[A-Za-z_][A-Za-z0-9_]*)\s*$",
            yaml_content,
            re.MULTILINE,
        )
        if collect_secret_matches:
            frontmatter["setup"] = {
                "collect_secrets": [
                    {"env_var": env_var_name or alt_env_var_name}
                    for env_var_name, alt_env_var_name in collect_secret_matches
                ]
            }

    return frontmatter, body


def _skill_matches_platform(frontmatter: dict[str, Any]) -> bool:
    platforms = frontmatter.get("platforms")
    if not platforms:
        return True
    if not isinstance(platforms, list):
        platforms = [platforms]
    current_platform = sys.platform
    for platform_name in platforms:
        normalized = str(platform_name).lower().strip()
        mapped = _PLATFORM_MAP.get(normalized, normalized)
        if current_platform.startswith(mapped):
            return True
    return False


def _extract_summary(frontmatter: dict[str, Any], body: str) -> str:
    description = str(frontmatter.get("description") or "").strip()
    if description:
        return description

    for line in body.strip().splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return ""


def _extract_sections(body: str) -> tuple[str, ...]:
    sections = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            sections.append(stripped.lstrip("#").strip())
    return tuple(sections)


def _normalize_prerequisite_values(value: Any) -> tuple[str, ...]:
    if not value:
        return ()
    if isinstance(value, str):
        value = [value]
    return tuple(str(item).strip() for item in value if str(item).strip())


def _collect_prerequisite_env_vars(frontmatter: dict[str, Any]) -> tuple[str, ...]:
    prerequisites = frontmatter.get("prerequisites")
    if not isinstance(prerequisites, dict):
        return ()
    return _normalize_prerequisite_values(prerequisites.get("env_vars"))


def _collect_setup_secret_env_vars(frontmatter: dict[str, Any]) -> tuple[str, ...]:
    setup = frontmatter.get("setup")
    if not isinstance(setup, dict):
        return ()
    collect_secrets = setup.get("collect_secrets")
    if isinstance(collect_secrets, dict):
        collect_secrets = [collect_secrets]
    if not isinstance(collect_secrets, list):
        return ()

    env_vars: list[str] = []
    for item in collect_secrets:
        if not isinstance(item, dict):
            continue
        env_var = str(item.get("env_var") or "").strip()
        if env_var:
            env_vars.append(env_var)
    return tuple(env_vars)


@dataclass(slots=True)
class LocalSkillCatalogProvider(SkillSourceProviderPort, SkillManagementProviderPort):
    """Filesystem-backed provider for project, global, and managed skills."""

    project_root: Path | None = None
    global_root: Path | None = None
    managed_root: Path | None = None
    state_path: Path | None = None

    def list_skills(self) -> tuple[dict[str, Any], ...]:
        records: list[dict[str, Any]] = []
        state = self._load_state()
        seen_ids: set[str] = set()

        for scope, root in self._iter_roots():
            if not root.exists():
                continue
            for skill_md in root.rglob("SKILL.md"):
                if any(part in _EXCLUDED_SKILL_DIRS for part in skill_md.parts):
                    continue

                skill_dir = skill_md.parent
                try:
                    content = skill_md.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    continue

                frontmatter, body = _parse_frontmatter(content)
                if not _skill_matches_platform(frontmatter):
                    continue

                name = str(frontmatter.get("name") or skill_dir.name).strip() or skill_dir.name
                skill_id = self._build_skill_id(scope, name)
                if skill_id in seen_ids:
                    continue

                seen_ids.add(skill_id)
                relative_dir = str(skill_dir.relative_to(root))
                required_env = self._get_required_env(frontmatter)
                missing_required_env = tuple(
                    name for name in required_env if not os.getenv(name)
                )
                records.append(
                    {
                        "skill_id": skill_id,
                        "name": name,
                        "summary": _extract_summary(frontmatter, body),
                        "scope": scope,
                        "enabled": state.get(skill_id, True),
                        "path": str(skill_md),
                        "skill_dir": str(skill_dir),
                        "sections": _extract_sections(body),
                        "frontmatter": frontmatter,
                        "relative_dir": relative_dir,
                        "setup_needed": bool(missing_required_env),
                        "required_environment_variables": required_env,
                        "missing_required_environment_variables": missing_required_env,
                    }
                )

        records.sort(key=lambda item: (item["scope"], item["name"]))
        return tuple(records)

    def load_skill(self, skill_id: str) -> dict[str, Any] | None:
        records = self.list_skills()
        exact_match = next((record for record in records if record["skill_id"] == skill_id), None)
        if exact_match is not None:
            return self._load_skill_document(exact_match)

        matching_names = [record for record in records if record["name"] == skill_id]
        if len(matching_names) == 1:
            return self._load_skill_document(matching_names[0])
        return None

    def install_skill(self, source: str, scope: str | None = None) -> dict[str, Any]:
        source_path = Path(os.path.expanduser(source))
        if source_path.is_dir():
            source_skill_md = source_path / "SKILL.md"
            source_dir = source_path
        else:
            source_skill_md = source_path
            source_dir = source_path.parent

        if not source_skill_md.exists():
            raise FileNotFoundError(f"Skill source not found: {source}")

        content = source_skill_md.read_text(encoding="utf-8")
        frontmatter, body = _parse_frontmatter(content)
        name = str(frontmatter.get("name") or source_dir.name).strip() or source_dir.name
        target_scope = scope or "managed"
        target_root = self._resolve_target_root(target_scope)
        target_dir = target_root / name
        if target_dir.exists():
            raise FileExistsError(f"Skill already installed: {name}")

        target_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_dir, target_dir)
        skill_id = self._build_skill_id(target_scope, name)

        return {
            "action": "install",
            "skill_id": skill_id,
            "status": "installed",
            "summary": _extract_summary(frontmatter, body),
            "scope": target_scope,
            "path": str(target_dir / "SKILL.md"),
        }

    def set_skill_enabled(self, skill_id: str, enabled: bool) -> dict[str, Any]:
        record = self._resolve_skill_record(skill_id)
        if record is None:
            raise KeyError(f"Unknown skill: {skill_id}")

        state = self._load_state()
        state[record["skill_id"]] = enabled
        self._save_state(state)
        return {
            "action": "enable" if enabled else "disable",
            "skill_id": record["skill_id"],
            "status": "enabled" if enabled else "disabled",
            "scope": record["scope"],
        }

    def remove_skill(self, skill_id: str) -> dict[str, Any]:
        record = self._resolve_skill_record(skill_id)
        if record is None:
            raise KeyError(f"Unknown skill: {skill_id}")

        managed_root = self._resolve_target_root("managed")
        skill_dir = Path(record["skill_dir"]).resolve()
        try:
            skill_dir.relative_to(managed_root.resolve())
        except ValueError as exc:
            raise ValueError(f"Only managed skills can be removed: {skill_id}") from exc

        shutil.rmtree(skill_dir)
        state = self._load_state()
        state.pop(record["skill_id"], None)
        self._save_state(state)
        return {
            "action": "remove",
            "skill_id": record["skill_id"],
            "status": "removed",
            "scope": record["scope"],
        }

    def _iter_roots(self) -> tuple[tuple[str, Path], ...]:
        roots: list[tuple[str, Path]] = []
        if self.project_root is not None:
            roots.append(("project", self.project_root.expanduser().resolve()))
        if self.managed_root is not None:
            roots.append(("managed", self.managed_root.expanduser().resolve()))
        if self.global_root is not None:
            roots.append(("global", self.global_root.expanduser().resolve()))
        return tuple(roots)

    def _resolve_target_root(self, scope: str) -> Path:
        if scope == "project":
            if self.project_root is None:
                raise ValueError("Project skills root is not configured.")
            return self.project_root.expanduser().resolve()
        if scope == "global":
            if self.global_root is None:
                raise ValueError("Global skills root is not configured.")
            return self.global_root.expanduser().resolve()
        if self.managed_root is None:
            raise ValueError("Managed skills root is not configured.")
        return self.managed_root.expanduser().resolve()

    def _resolve_skill_record(self, skill_id: str) -> dict[str, Any] | None:
        records = self.list_skills()
        for record in records:
            if record["skill_id"] == skill_id:
                return record
        matching_names = [record for record in records if record["name"] == skill_id]
        if len(matching_names) == 1:
            return matching_names[0]
        return None

    def _load_skill_document(self, record: dict[str, Any]) -> dict[str, Any]:
        skill_path = Path(record["path"])
        content = skill_path.read_text(encoding="utf-8")
        frontmatter, body = _parse_frontmatter(content)
        return {
            **record,
            "body": body.strip(),
            "raw_content": content,
            "frontmatter": frontmatter,
            "sections": _extract_sections(body),
            "linked_files": self._list_linked_files(skill_path.parent),
        }

    def _list_linked_files(self, skill_dir: Path) -> tuple[str, ...]:
        linked_files = []
        for relative_root in ("references", "templates", "assets", "scripts"):
            base = skill_dir / relative_root
            if not base.exists():
                continue
            for child in base.rglob("*"):
                if child.is_file():
                    linked_files.append(str(child.relative_to(skill_dir)))
        return tuple(sorted(linked_files))

    def _build_skill_id(self, scope: str, name: str) -> str:
        return f"{scope}:{name}"

    def _load_state(self) -> dict[str, bool]:
        if self.state_path is None or not self.state_path.exists():
            return {}
        try:
            payload = json.loads(self.state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        if not isinstance(payload, dict):
            return {}
        return {str(key): bool(value) for key, value in payload.items()}

    def _save_state(self, state: dict[str, bool]) -> None:
        if self.state_path is None:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps(state, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _get_required_env(self, frontmatter: dict[str, Any]) -> tuple[str, ...]:
        env_vars: list[str] = []
        raw = frontmatter.get("required_environment_variables")
        if isinstance(raw, list):
            env_vars.extend(str(item).strip() for item in raw if str(item).strip())
        elif isinstance(raw, dict):
            env_vars.extend(str(key).strip() for key in raw if str(key).strip())
        env_vars.extend(_collect_prerequisite_env_vars(frontmatter))
        env_vars.extend(_collect_setup_secret_env_vars(frontmatter))

        unique_env_vars: list[str] = []
        for env_var in env_vars:
            if env_var not in unique_env_vars:
                unique_env_vars.append(env_var)
        return tuple(unique_env_vars)
