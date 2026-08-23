from __future__ import annotations

from test_remaining_skill_project_status_contract import REPO_ROOT, read_skill


def test_engineering_skill_resources_and_local_contracts_are_portable() -> None:
    crawler = read_skill("crawler4j-model-project")
    for resource in ("cli-workflow", "module-structure", "core-integration"):
        assert f"[{resource}](references/{resource}.md)" in crawler

    shadcn = read_skill("shadcn")
    assert "按任务读取最小相关资料" in shadcn.split("---", 2)[1]
    assert "`done`、`blocked` 或 `needs_user_input`" in shadcn

    webapp = read_skill("webapp-testing")
    assert "<skill-dir>/scripts/with_server.py" in webapp
    assert "python scripts/with_server.py" not in webapp
    assert "status: ready_for_review | partial | blocked | needs_user_input" in webapp
    assert "review | verification | test_environment_contract | user_input | none" in webapp


def test_content_tool_statuses_and_skill_local_scripts_are_portable() -> None:
    for name in ("algorithmic-art", "doc-coauthoring"):
        assert "`done`、`blocked` 或 `needs_user_input`" in read_skill(name)

    for name in ("docx", "humanizer", "pdf", "xlsx"):
        assert "status: ready_for_review | partial | blocked | needs_user_input" in read_skill(name)

    for name in ("docx", "pdf", "xlsx"):
        skill = read_skill(name)
        assert "<skill-dir>" in skill
        assert "python scripts/" not in skill

    uiux = read_skill("ui-ux-pro-max")
    assert "<skill-dir>/scripts/search.py" in uiux
    assert "python3 skills/ui-ux-pro-max/scripts/search.py" not in uiux


def test_git_human_gate_and_release_receipt_keep_their_true_boundaries() -> None:
    gitcommit = read_skill("gitcommitzh")
    assert "只有真实待确认人工 Gate 存在时，才要求 `human_approved`" in gitcommit
    assert "review / verification evidence / human_approved / memory sync" not in gitcommit

    release = read_skill("release-deployment")
    assert "发布回执是本 skill 的专业输出" in release
    assert "任务身份、`needs` 和 ledger 事件" in release


def test_bundled_visual_resources_are_neutral_and_honest_about_network_use() -> None:
    algorithm_dir = REPO_ROOT / "skills" / "algorithmic-art"
    viewer = (algorithm_dir / "templates" / "viewer.html").read_text(encoding="utf-8")
    generator = (algorithm_dir / "templates" / "generator_template.js").read_text(
        encoding="utf-8"
    )

    assert "anthropic" not in (viewer + generator).lower()
    assert "fonts.googleapis.com" not in viewer
    assert "requires network access for p5.js" in viewer
    assert "模板默认联网加载 p5.js" in read_skill("algorithmic-art")


def test_skill_resource_commands_resolve_from_the_skill_directory() -> None:
    brainstorming = (
        REPO_ROOT / "skills" / "brainstorming" / "visual-companion.md"
    ).read_text(encoding="utf-8")
    assert "`<skill-dir>`" in brainstorming
    assert "skills/brainstorming/scripts" not in brainstorming
    for resource in ("start-server.sh", "stop-server.sh", "frame-template.html", "helper.js"):
        assert f"<skill-dir>/scripts/{resource}" in brainstorming

    forms = (REPO_ROOT / "skills" / "pdf" / "forms.md").read_text(encoding="utf-8")
    assert "`<skill-dir>`" in forms
    assert "python scripts/" not in forms
    assert "<skill-dir>/scripts/check_fillable_fields.py" in forms

    for name in ("test-plan.md", "test-cases.md", "test-report.md"):
        template = (
            REPO_ROOT
            / "skills"
            / "document-templates"
            / "assets"
            / "templates"
            / "05-quality"
            / name
        ).read_text(encoding="utf-8")
        assert "`<skill-dir>`" in template
        assert "skills/document-templates/scripts" not in template
        assert "<skill-dir>/scripts/validate_test_documents.py" in template


def test_document_templates_keep_project_specific_profiles_conditional() -> None:
    references = REPO_ROOT / "skills" / "document-templates" / "references"
    catalog = (references / "document-catalog.md").read_text(encoding="utf-8")
    structure = (references / "repository-structure.md").read_text(encoding="utf-8")
    design = (references / "technical-design-template.md").read_text(encoding="utf-8")

    for text in (catalog, structure):
        lowered = text.lower()
        for project_specific in ("hermes", "agent-platform", "ai-drama"):
            assert project_specific not in lowered
    assert "access -> application -> domain -> runtime -> settings" not in design
    assert "## Shanforge Profile" in structure
    generic_structure = structure.split("## Shanforge Profile", 1)[0]
    assert ".factory" not in generic_structure
    assert "适用时" in design


def test_linked_component_workflow_and_codex_tool_map_exist() -> None:
    shadcn = read_skill("shadcn")
    assert "## Updating Components" in shadcn

    tool_map = (
        REPO_ROOT / "skills" / "using-shanforge" / "references" / "codex-tools.md"
    ).read_text(encoding="utf-8")
    for tool in (
        "spawn_agent",
        "send_message",
        "followup_task",
        "wait_agent",
        "list_agents",
        "interrupt_agent",
    ):
        assert f"`{tool}`" in tool_map
    assert "close_agent" not in tool_map
    assert "dispatching-parallel-agents" not in tool_map


def test_work_results_do_not_own_the_project_state_envelope() -> None:
    affected = (
        "project-memory",
        "executing-plans",
        "receiving-code-review",
        "release-deployment",
        "requesting-code-review",
        "requirements-engineering",
        "subagent-driven-development",
        "verification-before-completion",
        "writing-plans",
    )
    for name in affected:
        assert "next_required_action" not in read_skill(name), name

    for name in (
        "executing-plans",
        "subagent-driven-development",
        "verification-before-completion",
    ):
        skill = read_skill(name)
        for field in ("project_position", "completion_level", "stop_reason", "scope_remaining"):
            assert field not in skill, f"{name} still owns {field}"


def test_review_feedback_permissions_distinguish_triage_from_remediation() -> None:
    receiving = read_skill("receiving-code-review")
    assert "`state_or_gate_write` 时只" in receiving
    assert "`source_or_test_write` 时才" in receiving


def test_review_approval_only_creates_a_real_human_gate_conditionally() -> None:
    references = REPO_ROOT / "skills" / "requesting-code-review" / "references"
    independent = (references / "independent-review-task-template.md").read_text(
        encoding="utf-8"
    )
    assert "如果 approved，下一状态仍是 pending_human_confirmation" not in independent

    for name in (
        "independent-review-task-template.md",
        "task-review-template.md",
        "pr-review-template.md",
        "review-score-rubric.md",
    ):
        resource = (references / name).read_text(encoding="utf-8")
        assert "return_to_orchestrator" in resource, name
    rubric = (references / "review-score-rubric.md").read_text(encoding="utf-8")
    assert "但仍需人工确认" not in rubric
