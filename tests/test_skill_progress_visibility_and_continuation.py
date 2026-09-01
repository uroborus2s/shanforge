from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_controller_exposes_project_position_before_internal_routing() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "项目位置快照",
        "项目整体进度",
        "当前任务",
        "已完成",
        "正在执行",
        "停止原因",
        "唯一下一动作",
        "用户可见的下一动作必须描述项目动作",
        "不得只写调用某个 skill",
    ):
        assert phrase in controller


def test_controller_uses_three_part_human_response_without_stopping_internal_work() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    ordered_sections = (
        "1. **第一部分：直接回应**",
        "2. **第二部分：处理结果**",
        "3. **第三部分：需要用户回复**",
    )
    positions = [controller.index(section) for section in ordered_sections]
    assert positions == sorted(positions)

    for phrase in (
        "三段式人类响应合同",
        "`direct_answer`、`lightweight_analysis` 和项目化回复",
        "项目位置快照只作为第二部分",
        "“无需回复”表示不存在真实人工 Gate",
        "不得因为输出“无需回复”而停止",
        "必须继续既有授权范围内的执行",
        "不得结束当前 turn",
    ):
        assert phrase in controller

    final_response_boundary = next(
        line for line in controller.splitlines() if "才可以发送结束当前 turn 的最终回复" in line
    )
    for phrase in (
        "当前授权范围已经到达终态",
        "存在真实人工 Gate",
        "存在无法内部解决的 blocker",
        "继续需要新的权限",
    ):
        assert phrase in final_response_boundary


def test_project_responses_use_a_shared_header_and_work_type_body() -> None:
    controller = read("skills/using-shanforge/SKILL.md")
    contract = read("skills/using-shanforge/references/human-readable-status.md")

    assert "共享状态头 + 按工作类型正文" in controller
    for phrase in (
        "已批准 WBS、TaskCard 和 ledger",
        "已完成、进行中、未开始和阻塞",
        "可观察结果和验证状态",
        "无法计算",
        "不得猜测百分比或分母",
        "system、评审、提交等任务不得算作产品功能",
        "开发 / 计划",
        "测试",
        "Bug / 修复",
        "评审 / 交付",
        "内部 ID、Gate、路径和命令只作为末尾技术记录",
    ):
        assert phrase in contract


def test_controller_reconciles_worker_facts_before_advancing_wbs_progress() -> None:
    controller = read("skills/using-shanforge/SKILL.md")
    contract = read("skills/using-shanforge/references/human-readable-status.md")

    assert "所有展示的 WBS/产品进度变化必须先与已批准 WBS、TaskCard 和 ledger 对账" in controller
    boundary = contract.split("## 进度事实对账边界", maxsplit=1)[1].split("\n## ", maxsplit=1)[0]
    assert (
        "| 已批准 WBS、TaskCard 和 ledger 可匹配 | 映射为对应 WBS 项状态 | 可推进该项产品完成度 |"
        in boundary
    )
    assert (
        "| worker facts 无法匹配 | 仅作为本轮执行观察或技术记录 | 不得推进产品完成度 |"
        in boundary
    )


def test_controller_distinguishes_internal_actions_from_true_human_gates() -> None:
    controller = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "真实人工 Gate",
        "内部动作不是人工 Gate",
        "实现、验证、独立只读评审、同范围整改和 memory sync",
        "reviewer `approved` 不自动等于 `pending_human_confirmation`",
        "产品或需求取舍",
        "风险接受",
        "扩大授权范围",
        "破坏性或外部动作",
        "精确候选哈希批准或正式发布",
    ):
        assert phrase in controller

    assert "reviewer 已 approved | 无工作 skill | 必须进入人工确认" not in controller


def test_execution_skills_continue_only_inside_authorized_envelope() -> None:
    for path in (
        "skills/executing-plans/SKILL.md",
        "skills/subagent-driven-development/SKILL.md",
    ):
        skill = read(path)
        for phrase in (
            "授权执行包",
            "不要逐项请求继续",
            "普通 task checkpoint 不是人工 Gate",
            "授权范围不得扩大",
            "需要人类产品决策",
            "超出允许文件范围",
            "破坏性或外部动作",
        ):
            assert phrase in skill, f"{path} missing {phrase}"
        for project_field in (
            "project_position",
            "completion_level",
            "stop_reason",
            "scope_remaining",
        ):
            assert project_field not in skill, f"{path} still owns {project_field}"

    subagent = read("skills/subagent-driven-development/SKILL.md")
    assert "只有 `human_confirmation_required: true` 且有完整 `gate_reason` 时" in subagent
    assert "普通授权任务不得额外制造人工 Gate" in subagent
    assert "`approved` 和 `done` 由流程总控、独立评审、验证和人工确认共同决定" not in subagent


def test_readonly_review_and_same_scope_remediation_are_internal_actions() -> None:
    review = read("skills/requesting-code-review/SKILL.md")

    for phrase in (
        "只读独立评审是已授权任务的内部质量动作",
        "无需为只读派发单独请求人工授权",
        "同范围整改循环",
        "changes_requested",
        "不扩大原授权范围",
        "human_confirmation_required",
        "只有真实人工 Gate 才写 `pending_human_confirmation`",
    ):
        assert phrase in review

    assert "loop 结束必须进入 `pending_human_confirmation`" not in review
    assert "需要子 agent 但用户未授权时，必须停止并请求授权" not in review


def test_memory_recovery_prefers_current_header_over_historical_gates() -> None:
    memory = read("skills/project-memory/SKILL.md")

    for phrase in (
        "当前状态头部优先于历史条目",
        "历史条目中的“当前”“下一步”不得覆盖头部",
        "项目整体进度",
        "当前任务",
        "停止原因",
        "唯一下一动作",
        "不得恢复已撤销、已取代或已关闭的 Gate",
    ):
        assert phrase in memory


def test_completion_evidence_reports_claim_scope_without_owning_project_state() -> None:
    verification = read("skills/verification-before-completion/SKILL.md")
    controller = read("skills/using-shanforge/SKILL.md")

    for phrase in (
        "声明范围核对",
        "任务验证通过不等于阶段或项目完成",
        "只报告证据直接覆盖的声明和未验证项",
        "项目位置、完成层级、停止原因和剩余工作由 `using-shanforge`",
    ):
        assert phrase in verification
    for project_field in (
        "project_position",
        "completion_level",
        "stop_reason",
        "scope_remaining",
    ):
        assert project_field not in verification
        assert project_field in controller


def test_runtime_skill_management_is_not_reintroduced() -> None:
    assert not (REPO_ROOT / "src" / "runtime" / "skills").exists()
    assert not (REPO_ROOT / "src" / "settings" / "skills").exists()
