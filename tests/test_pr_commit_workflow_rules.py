from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_gitcommitzh_requires_pr_closure_preflight() -> None:
    skill = read("skills/gitcommitzh/SKILL.md")

    for phrase in (
        "PR 闭环与提交前置检查",
        "work item ledger",
        "review 结论",
        "verification evidence",
        "memory sync",
        "human_approved",
        "重读当前 work item ledger 最新事件",
        "next_required_action",
        "同一 `.factory/memory/` 文件混有其他任务条目时",
        "pending_human_confirmation",
        "禁止把未确认的 reviewer approved 当作提交闭环依据",
        "gitcommitzh 不负责创建、推送或合并 PR",
    ):
        assert phrase in skill

    assert "references/pr-closure-checklist.md" in skill


def test_pr_closure_checklist_links_review_evidence_memory_and_git_scope() -> None:
    checklist = read("skills/gitcommitzh/references/pr-closure-checklist.md")

    for phrase in (
        "PR 闭环与提交检查清单",
        ".factory/workitems/<WORKITEM-ID>/ledger.jsonl",
        ".factory/memory/review-ledger.jsonl",
        "review package",
        "verification evidence",
        "代码、文档、测试和 `.factory/memory/` 已同步",
        "git diff --cached --name-only",
        "重读当前 work item ledger 最新事件",
        "next_required_action",
        "同一 `.factory/memory/` 文件混有其他任务条目时",
        "git diff -- <files>",
        "排除无关脏改动",
        "提交后回写",
    ):
        assert phrase in checklist

    assert "git add ." not in checklist


def test_flow_controller_routes_commit_only_after_confirmation_and_sync() -> None:
    skill = read("skills/using-shanforge/SKILL.md")
    codex_tools = read("skills/using-shanforge/references/codex-tools.md")

    assert "人工已确认且有可提交改动" in skill
    assert "review / evidence / memory sync 已齐备" in skill
    assert "不得再要求用户额外说“提交”" in skill
    assert "重读当前 work item ledger 最新事件" in skill
    assert "next_required_action" in skill
    assert "当前任务范围" in skill
    assert "禁止把提交作为 review 或人工确认的替代品" in skill

    assert "任务完成且有可提交改动" in codex_tools
    assert "提交当前任务范围" in codex_tools
    assert "提交全部工作" not in codex_tools
    assert "work item、review、evidence 和 memory sync 记录" in codex_tools


def test_pr_commit_rules_do_not_reintroduce_script_gate() -> None:
    dispatch_gate = "factory-dispatch " + "loop" + "-gate"
    script_gate = "factory-workitem" + "-" + "loop" + "-" + "gate"
    paths = [
        "skills/using-shanforge/SKILL.md",
        "skills/gitcommitzh/SKILL.md",
        "skills/gitcommitzh/references/pr-closure-checklist.md",
        "scripts/factory-dispatch",
    ]
    combined = "\n".join(read(path) for path in paths)

    assert dispatch_gate not in combined
    assert script_gate not in combined
    assert not (REPO_ROOT / "scripts" / script_gate).exists()


def test_workflow_plan_tracks_sf_sp_008_commit_closure_rules() -> None:
    plan = read(
        "docs/04-project-development/05-development-process/"
        "superpowers-workflow-integration-plan.md"
    )

    for phrase in (
        "| `SF-SP-008` | PR 闭环与提交规则 |",
        "提交必须使用 `gitcommitzh`",
        "`gitcommitzh` 只做本地提交，不创建、不推送、不合并 PR",
        "代码类 work item 已进入 PR 闭环",
        "本地提交不能冒充 push、PR 或 merge",
    ):
        assert phrase in plan
