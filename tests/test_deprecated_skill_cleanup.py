from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_legacy_factory_scripts_are_removed() -> None:
    assert not list((REPO_ROOT / "scripts").glob("factory-*"))
    assert not (REPO_ROOT / "scripts" / "factory_core.py").exists()
    assert not (REPO_ROOT / "scripts" / "shanforge-cli").exists()
    assert not (REPO_ROOT / "src" / "access" / "cli").exists()
    assert not (REPO_ROOT / "config" / "action-registry.json").exists()
    assert not (REPO_ROOT / "skills" / "software-factory-cli").exists()
    removed_artifacts = (
        ".factory/agent-session.json",
        ".factory/chat-bootstrap.json",
        ".factory/process/chat-bootstrap.md",
        ".factory/process/intent-approvals.json",
        ".factory/process/intent-approvals.md",
        ".factory/process/multi-agent-board.md",
        ".factory/process/state-doctor-report.md",
        ".factory/memory/chat-bootstrap.generic.coordinator.md",
        ".factory/memory/chat-bootstrap.opencode.coordinator.md",
        ".factory/memory/chat-bootstrap.summary.md",
        ".factory/memory/multi-agent-board.summary.md",
        ".factory/memory/state-doctor.summary.md",
    )
    for path in removed_artifacts:
        assert not (REPO_ROOT / path).exists()


def test_legacy_factory_functional_tests_are_removed() -> None:
    removed_tests = (
        "tests/test_factory_relative_paths_and_docs_index.py",
        "tests/test_factory_skill_approval.py",
        "tests/test_factory_skill_delete_approval.py",
        "tests/test_factory_skill_draft.py",
        "tests/test_factory_skill_eval.py",
        "tests/test_factory_skill_promote.py",
        "tests/test_factory_skill_rollback.py",
        "tests/test_access_cli.py",
    )
    for path in removed_tests:
        assert not (REPO_ROOT / path).exists()

    for path in (REPO_ROOT / "tests").glob("test_*.py"):
        content = path.read_text(encoding="utf-8")
        assert "FACTORY_" + "DISPATCH" not in content
        assert "FACTORY_" + "INIT" not in content
        assert "FACTORY_" + "AGENT_SESSION" not in content


def test_current_entries_do_not_reference_legacy_factory_scripts() -> None:
    current_entry_files = (
        "AGENTS.md",
        "GEMINI.md",
        "README.md",
        ".factory/project.json",
        ".factory/memory/runtime-brief.md",
        ".factory/memory/agent-session.md",
        ".factory/memory/doc-map.md",
        "config/software-factory.defaults.json",
        "docs/01-getting-started/quick-start.md",
        "docs/02-user-guide/index.md",
        "docs/02-user-guide/user-guide.md",
        "docs/02-user-guide/prompt-templates.md",
        "docs/03-developer-guide/application-development.md",
        "docs/03-developer-guide/development-setup.md",
    )

    forbidden = (
        "software-" + "factory-cli",
        "factory-" + "dispatch",
        "factory-" + "agent-session",
        "factory-" + "init",
        "factory-" + "workflow-runner",
        "scripts/" + "factory-",
        "action-" + "registry",
    )
    for path in current_entry_files:
        content = read(path)
        for phrase in forbidden:
            assert phrase not in content


def test_document_templates_no_longer_recommends_factory_dispatch_onboarding() -> None:
    skill = read("skills/document-templates/SKILL.md")
    gates = read("skills/document-templates/references/traceability-and-gates.md")

    for content in (skill, gates):
        assert "factory-" + "dispatch historical-project-onboarding" not in content
        assert "先交给 `using-shanforge` 判断是否需要项目纳管" in content
        assert "factory-" + "init" not in content
        assert "factory-" + "requirements-upgrade" not in content


def test_unused_development_flow_skills_are_removed() -> None:
    removed_skill_dirs = (
        "skills/find-skills",
        "skills/web-artifacts-builder",
        "skills/backend-patterns",
    )
    for path in removed_skill_dirs:
        assert not (REPO_ROOT / path).exists()

    kept_skill_dirs = (
        "skills/ai-regression-testing",
        "skills/agent-harness-construction",
        "skills/ai-first-engineering",
    )
    for path in kept_skill_dirs:
        assert (REPO_ROOT / path / "SKILL.md").exists()

    active_flow_files = (
        "skills/using-shanforge/SKILL.md",
        "docs/05-design/workflow-execution-design.md",
        ".factory/project.json",
        "config/software-factory.defaults.json",
    )
    forbidden = ("find-skills", "web-artifacts-builder", "backend-patterns")
    for path in active_flow_files:
        content = read(path)
        for phrase in forbidden:
            assert phrase not in content
