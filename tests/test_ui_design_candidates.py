import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock
from uuid import UUID

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SEARCH = REPO_ROOT / "skills/ui-ux-pro-max/scripts/search.py"
SCRIPTS = SEARCH.parent


def load_design_system():
    """Load the script with its sibling core module without keeping a generic import."""
    original_core = sys.modules.pop("core", None)
    sys.path.insert(0, str(SCRIPTS))
    try:
        spec = importlib.util.spec_from_file_location(
            "ui_design_candidates", SCRIPTS / "design_system.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)
        if original_core is None:
            sys.modules.pop("core", None)
        else:
            sys.modules["core"] = original_core


design_system = load_design_system()


def run_search(*args: str, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SEARCH), *args], cwd=cwd, text=True, capture_output=True
    )


def test_design_system_json_is_candidate_evidence_not_a_final_design() -> None:
    result = run_search(
        "healthcare dashboard calm accessible", "--design-system", "--stack", "swiftui",
        "--json", "--project-name", "Care Console", "--surface", "operate",
        "--variance", "8",
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == 1
    assert payload["kind"] == "design_candidates"
    assert payload["status"] == "candidate"
    assert payload["project_name"] == "Care Console"
    assert payload["context"]["platform"] == "apple"
    assert payload["context"]["stack"] == "swiftui"
    assert payload["context"]["dials"]["variance"] == 8
    assert "style" in payload["candidates"]
    assert "source" in payload["candidates"]["style"][0]
    assert "record" in payload["candidates"]["style"][0]["source"]
    match_basis = payload["candidates"]["style"][0]["match_basis"]
    assert match_basis["algorithm"] == "BM25 lexical match"
    assert match_basis["lexical_score"] > 0
    assert match_basis["matched_terms"]
    assert all(term in payload["query"].lower() for term in match_basis["matched_terms"])
    assert "colors" not in payload


def test_design_system_does_not_add_landing_unless_persuading() -> None:
    result = run_search("inventory dashboard", "--design-system", "--json", "--surface", "operate")
    assert result.returncode == 0, result.stderr
    assert "landing" not in json.loads(result.stdout)["candidates"]


@pytest.mark.parametrize(
    "stack,platform",
    [("swiftui", "apple"), ("jetpack-compose", "android")],
)
def test_native_candidates_exclude_web_implementation_and_certification_fields(
    stack: str, platform: str
) -> None:
    result = run_search(
        "healthcare dashboard", "--design-system", "--stack", stack, "--platform", platform,
        "--json",
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    excluded = {
        "Effects & Animation", "Framework Compatibility", "CSS/Technical Keywords",
        "Implementation Checklist", "Design System Variables", "AI Prompt Keywords",
    }
    for domain, rows in payload["candidates"].items():
        if domain != "stack":
            assert not any(excluded.intersection(row) for row in rows)
    assert "unverified candidate metadata" in " ".join(payload["warnings"])


def test_mini_program_candidates_exclude_web_implementation_fields() -> None:
    result = run_search(
        "healthcare dashboard", "--design-system", "--platform", "mini-program", "--json"
    )
    assert result.returncode == 0, result.stderr
    excluded = {"CSS/Technical Keywords", "Effects & Animation", "AI Prompt Keywords"}
    for rows in json.loads(result.stdout)["candidates"].values():
        assert not any(excluded.intersection(row) for row in rows)


def test_web_search_and_stack_guidance_remain_available() -> None:
    result = run_search("dashboard accessibility", "--design-system", "--stack", "react", "--json")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["candidates"]["stack"]


def test_landing_search_error_is_propagated_not_recast_as_no_match(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    search_results = [{"results": []}] * len(design_system.SEARCH_CONFIG)
    search_results.append({"error": "landing.csv missing"})
    monkeypatch.setattr(design_system, "search", Mock(side_effect=search_results))
    result = design_system.DesignSystemGenerator().generate("dashboard", surface="persuade")
    assert "landing.csv missing" in result["unresolved"]
    assert "landing: no BM25 matches for query" not in result["unresolved"]


def test_design_system_persist_creates_only_candidate_and_keeps_formal_files(
    tmp_path: Path,
) -> None:
    project_dir = tmp_path / "design-system" / "care-console"
    pages = project_dir / "pages"
    pages.mkdir(parents=True)
    master = project_dir / "MASTER.md"
    page = pages / "dashboard.md"
    master.write_bytes(b"formal-master")
    page.write_bytes(b"formal-page")

    result = run_search(
        "healthcare dashboard", "--design-system", "--json", "--persist", "--page", "dashboard",
        "--project-name", "Care Console", "--output-dir", str(tmp_path),
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    created = [Path(path) for path in payload["persistence"]["created_files"]]
    assert len(created) == 1
    assert created[0].parent == project_dir / "candidates"
    assert created[0].suffix == ".json"
    assert json.loads(created[0].read_text(encoding="utf-8"))["kind"] == "design_candidates"
    assert master.read_bytes() == b"formal-master"
    assert page.read_bytes() == b"formal-page"


def test_cli_rejects_incompatible_modes_without_stdout() -> None:
    for arguments in (
        ("dashboard", "--domain", "style", "--design-system"),
        ("dashboard", "--domain", "style", "--stack", "react"),
        ("dashboard", "--persist"),
        ("dashboard", "--page", "home"),
        ("dashboard", "--max-results", "0"),
    ):
        result = run_search(*arguments)
        assert result.returncode == 2
        assert not result.stdout


def test_stack_platform_conflict_is_reported() -> None:
    result = run_search("dashboard", "--design-system", "--stack", "swiftui", "--platform", "web")
    assert result.returncode == 2
    assert not result.stdout
    assert "conflicts" in result.stderr


def test_zero_matches_and_chinese_are_explicitly_unresolved() -> None:
    for query in ("qxzvnomatch", "完全没有匹配的中文词"):
        result = run_search(query, "--design-system", "--json")
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert all(not rows for rows in payload["candidates"].values())
        assert any("no BM25 matches" in item for item in payload["unresolved"])


@pytest.mark.parametrize("stack,platform", [
    ("react", "web"), ("nextjs", "web"), ("vue", "web"), ("svelte", "web"),
    ("astro", "web"), ("nuxtjs", "web"), ("nuxt-ui", "web"), ("html-tailwind", "web"),
    ("shadcn", "web"), ("threejs", "web"), ("angular", "web"), ("laravel", "web"),
    ("swiftui", "apple"), ("jetpack-compose", "android"), ("javafx", "desktop"),
    ("wpf", "desktop"), ("winui", "desktop"), ("uwp", "desktop"),
])
def test_single_platform_stacks_infer_and_reject_conflicts(stack: str, platform: str) -> None:
    result = run_search("dashboard", "--design-system", "--stack", stack, "--json")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["context"]["platform"] == platform
    conflict = "apple" if platform != "apple" else "web"
    rejected = run_search("dashboard", "--design-system", "--stack", stack, "--platform", conflict)
    assert rejected.returncode == 2
    assert not rejected.stdout


@pytest.mark.parametrize("stack", ["flutter", "react-native", "avalonia", "uno"])
def test_cross_platform_stacks_require_or_accept_a_real_host(stack: str) -> None:
    unresolved = run_search("dashboard", "--design-system", "--stack", stack, "--json")
    assert unresolved.returncode == 0, unresolved.stderr
    assert any("cross-platform" in item for item in json.loads(unresolved.stdout)["unresolved"])
    explicit = run_search(
        "dashboard", "--design-system", "--stack", stack, "--platform", "apple", "--json"
    )
    assert explicit.returncode == 0, explicit.stderr
    platform_unresolved = [
        item for item in json.loads(explicit.stdout)["unresolved"] if "platform" in item
    ]
    assert not platform_unresolved
    rejected = run_search(
        "dashboard", "--design-system", "--stack", stack, "--platform", "mini-program"
    )
    assert rejected.returncode == 2


def test_design_system_formats_have_the_same_candidate_semantics(tmp_path: Path) -> None:
    json_result = run_search(
        "healthcare dashboard", "--design-system", "--json", "--format", "markdown",
        "--persist", "--output-dir", str(tmp_path),
    )
    assert json_result.returncode == 0, json_result.stderr
    payload = json.loads(json_result.stdout)
    for output_format in ("ascii", "markdown"):
        result = run_search(
            "healthcare dashboard", "--design-system", "--format", output_format,
            "--persist", "--output-dir", str(tmp_path),
        )
        assert result.returncode == 0, result.stderr
        for value in (
            payload["status"], payload["advisory_reasoning"], "Context:", "Warnings", "Persistence"
        ):
            assert value in result.stdout
        assert "candidates/" in result.stdout


def test_dials_record_intent_without_changing_candidates_and_normal_query_writes_nothing(
    tmp_path: Path,
) -> None:
    plain = run_search("healthcare dashboard", "--design-system", "--json", cwd=tmp_path)
    dialed = run_search(
        "healthcare dashboard", "--design-system", "--json", "--variance", "9", "--motion", "8",
        "--density", "7", cwd=tmp_path,
    )
    assert plain.returncode == dialed.returncode == 0
    assert json.loads(plain.stdout)["candidates"] == json.loads(dialed.stdout)["candidates"]
    assert not (tmp_path / "design-system").exists()


def test_cli_parameter_matrix_and_io_failure_have_no_success_output(tmp_path: Path) -> None:
    for arguments in (
        ("dashboard", "--format", "markdown"), ("dashboard", "--project-name", "Care"),
        ("dashboard", "--output-dir", str(tmp_path)), ("   ", "--design-system"),
    ):
        result = run_search(*arguments)
        assert result.returncode == 2
        assert not result.stdout
    (tmp_path / "design-system").write_text("not-a-directory", encoding="utf-8")
    failed_write = run_search(
        "dashboard", "--design-system", "--persist", "--output-dir", str(tmp_path)
    )
    assert failed_write.returncode == 2
    assert not failed_write.stdout


def test_persist_is_unique_collision_safe_and_rejects_candidate_symlink(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    design = design_system.DesignSystemGenerator().generate("dashboard", "Care Console")
    first = design_system.persist_design_system(design, "home", tmp_path)
    second = design_system.persist_design_system(design, "home", tmp_path)
    assert first["created_files"] != second["created_files"]
    candidate = Path(first["created_files"][0])
    master = tmp_path / "design-system" / "care-console" / "MASTER.md"
    pages = tmp_path / "design-system" / "care-console" / "pages"
    pages.mkdir()
    master.write_bytes(b"master")
    page = pages / "home.md"
    page.write_bytes(b"page")
    fixed_uuid = UUID(hex=candidate.stem.split("-")[-1])
    monkeypatch.setattr(design_system.uuid, "uuid4", Mock(return_value=fixed_uuid))
    with pytest.raises(FileExistsError):
        design_system.persist_design_system(design, "home", tmp_path)
    assert candidate.read_bytes()
    assert master.read_bytes() == b"master"
    assert page.read_bytes() == b"page"
    escaped = tmp_path / "escaped" / "design-system" / "care-console"
    (escaped / "pages").mkdir(parents=True)
    (escaped / "candidates").symlink_to(escaped / "pages", target_is_directory=True)
    with pytest.raises(ValueError, match="escapes"):
        design_system.persist_design_system(design, "home", tmp_path / "escaped")
    outside = tmp_path / "outside"
    outside.mkdir()
    guarded = tmp_path / "guarded"
    guarded.mkdir()
    (guarded / "design-system").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="escapes"):
        design_system.persist_design_system(design, "home", guarded)
    assert not list(outside.iterdir())


def test_public_api_remains_positional_and_rejects_invalid_boundaries(tmp_path: Path) -> None:
    assert isinstance(design_system.generate_design_system("dashboard", "Care", "json"), str)
    with pytest.raises(ValueError, match="unknown output format"):
        design_system.generate_design_system("dashboard", output_format="xml")
    with pytest.raises(ValueError, match="output_dir"):
        design_system.generate_design_system("dashboard", output_dir=str(tmp_path))
    with pytest.raises(ValueError, match="max-results"):
        design_system.generate_design_system("dashboard", max_results="3")
    with pytest.raises(ValueError, match="variance"):
        design_system.generate_design_system("dashboard", variance=11)


@pytest.mark.parametrize(
    "encoding,arguments",
    [
        ("ascii", ("中文", "--design-system", "--platform", "apple", "--json")),
        ("cp1252", ("中文", "--domain", "style", "--json")),
    ],
)
def test_cli_forces_utf8_output_when_parent_stream_is_not_utf8(
    encoding: str, arguments: tuple[str, ...]
) -> None:
    environment = os.environ | {"PYTHONIOENCODING": encoding}
    result = subprocess.run(
        [sys.executable, str(SEARCH), *arguments], cwd=REPO_ROOT,
        capture_output=True, env=environment,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8")
    payload = json.loads(result.stdout.decode("utf-8"))
    assert payload["query"] == "中文"
    assert not result.stderr


def test_cli_error_stderr_remains_utf8_when_parent_stream_is_not_utf8() -> None:
    result = subprocess.run(
        [sys.executable, str(SEARCH), " ", "--design-system"], cwd=REPO_ROOT,
        capture_output=True, env=os.environ | {"PYTHONIOENCODING": "ascii"},
    )
    assert result.returncode == 2
    assert not result.stdout
    assert "query must not be blank" in result.stderr.decode("utf-8")
