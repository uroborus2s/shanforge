from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_verification_before_completion_skill_requires_fresh_evidence() -> None:
    skill = read("skills/verification-before-completion/SKILL.md")

    assert "name: verification-before-completion" in skill
    assert "没有新鲜验证证据，不得声明完成" in skill
    assert "先识别能证明声明的命令" in skill
    assert "运行完整命令" in skill
    assert "读取完整输出" in skill
    assert "检查 exit code" in skill
    assert "统计失败数量" in skill
    assert ".factory/workitems/<WORKITEM-ID>/evidence/" in skill
    assert ".factory/workitems/<WORKITEM-ID>/ledger.jsonl" in skill
    assert "status" in skill
    assert "needs" in skill
    assert "与其他 skill 的关系" not in skill
    assert "requesting-code-review" not in skill
    assert "gitcommitzh" not in skill
    assert "docs/superpowers" not in skill


def test_verification_blocks_closure_without_fresh_command_output_and_evidence() -> None:
    skill = read("skills/verification-before-completion/SKILL.md")

    for phrase in (
        "关闭前必须检查新鲜命令、exit code、输出和 evidence",
        "无批次级 evidence 不能关闭批次、阶段或项目",
        "review 不能替代 verification",
        "verification 不能替代 human confirmation",
    ):
        assert phrase in skill


def test_verification_references_define_completion_evidence_package() -> None:
    expected = {
        "skills/verification-before-completion/references/completion-evidence-template.md": (
            "Completion Evidence",
            "Work item",
            "验证声明",
            "验证命令",
            "exit code",
            "失败数量",
            "真实输出摘要",
            "未运行项",
            "结论",
        ),
        "skills/verification-before-completion/references/completion-claim-checklist.md": (
            "完成声明检查清单",
            "新鲜验证",
            "完整命令",
            "完整输出",
            "不能用 should",
            "不能用 probably",
            "不能只依赖上一次结果",
        ),
        "skills/verification-before-completion/references/red-green-verification-template.md": (
            "Red-Green Verification",
            "先证明测试会失败",
            "再证明修复后会通过",
            "失败原因必须符合预期",
            "恢复修复后再次通过",
        ),
    }

    for path, phrases in expected.items():
        content = read(path)
        for phrase in phrases:
            assert phrase in content


def test_systematic_debugging_skill_requires_root_cause_before_fix() -> None:
    skill = read("skills/systematic-debugging/SKILL.md")

    assert "name: systematic-debugging" in skill
    assert "修复前必须先完成根因调查" in skill
    assert "Investigation Task 只做复现、诊断、直接原因和根源原因" in skill
    assert "`root_cause_found` 表示根因、事实 owner、影响范围和风险已形成" in skill
    assert "低、中风险不新增人工 Gate" in skill
    assert "高风险依次等待根因确认和最小修复方案确认" in skill
    assert "不能复现时停止并要求更多信息，不修行为" in skill
    assert "禁止先猜修复" in skill
    assert "Phase 1：根因调查" in skill
    assert "Phase 2：模式分析" in skill
    assert "Phase 3：假设与最小验证" in skill
    assert "Phase 4：风险分级与交接" in skill
    assert "- status: root_cause_found | blocked | needs_user_input" in skill
    assert "3 次修复失败" in skill
    assert "质疑架构" in skill
    assert ".factory/workitems/<WORKITEM-ID>/evidence/" in skill
    assert "低、中风险默认在当前任务状态包中保存紧凑调查结论" in skill
    assert "高风险、真实阻塞或需要跨会话恢复时" in skill
    assert "与其他 skill 的关系" not in skill
    assert "verification-before-completion" not in skill
    assert "requesting-code-review" not in skill
    assert "docs/superpowers" not in skill
    assert "Phase 4：根因修复" not in skill


def test_systematic_debugging_references_define_investigation_package() -> None:
    expected = {
        "skills/systematic-debugging/references/root-cause-investigation-template.md": (
            "Root Cause Investigation",
            "Bug 症状",
            "复现步骤",
            "失败证据",
            "直接原因",
            "根源原因",
            "最小假设",
            "修复点",
        ),
        "skills/systematic-debugging/references/data-flow-tracing-guide.md": (
            "数据流反向追踪",
            "观察症状",
            "直接原因",
            "上一层调用",
            "继续向上追踪",
            "源头修复",
        ),
        "skills/systematic-debugging/references/defense-in-depth-checklist.md": (
            "防御式校验清单",
            "入口校验",
            "业务逻辑校验",
            "环境保护",
            "诊断日志",
            "让问题结构性不可复现",
        ),
        "skills/systematic-debugging/references/condition-based-waiting-guide.md": (
            "条件等待",
            "等待真实条件",
            "不要猜时间",
            "超时错误",
            "轮询间隔",
        ),
    }

    for path, phrases in expected.items():
        content = read(path)
        for phrase in phrases:
            assert phrase in content


def test_tdd_workflow_links_debugging_and_verification_gate_without_routing() -> None:
    skill = read("skills/tdd-workflow/SKILL.md")
    reference = read("skills/tdd-workflow/references/tdd-debugging-verification-gate.md")

    assert "references/tdd-debugging-verification-gate.md" in skill
    assert "低、中风险不新增人工 Gate" in skill
    assert "高风险必须先通过根因确认和修复方案确认 Gate" in skill
    assert "单次缺陷修复不默认运行全仓测试" in skill
    assert "先看测试失败，再写实现" in reference
    assert "修 Bug 时先写根因记录" in reference
    assert "完成声明前必须有新鲜验证证据" in reference
    assert "禁止测试后补" in reference
    assert "禁止用兜底替代根因修复" in reference
    assert "与其他 skill 的关系" not in reference
    assert "verification-before-completion" not in reference
    assert "systematic-debugging" not in reference


def test_verification_debugging_openai_metadata_is_chinese() -> None:
    verification_metadata = read("skills/verification-before-completion/agents/openai.yaml")
    debugging_metadata = read("skills/systematic-debugging/agents/openai.yaml")

    assert 'display_name: "完成前验证"' in verification_metadata
    assert "新鲜验证证据" in verification_metadata
    assert "完成声明" in verification_metadata

    assert 'display_name: "系统化调试"' in debugging_metadata
    assert "根因" in debugging_metadata
    assert "修复前" in debugging_metadata


def test_workflow_skills_expose_human_readable_test_bug_and_repair_facts() -> None:
    verification = read("skills/verification-before-completion/SKILL.md")
    debugging = read("skills/systematic-debugging/SKILL.md")
    tdd = read("skills/tdd-workflow/SKILL.md")

    for phrase in (
        "正式测试计划、测试案例目录和本轮测试报告",
        "total | passed | failed | error | blocked | skipped | not_run | cancelled",
        "测试 ID、关联功能、可观察现象和当前归因",
        "根因待调查",
        "本轮覆盖范围",
        "未覆盖范围",
        "局部通过不得表述为项目通过",
    ):
        assert phrase in verification

    for phrase in (
        "现象、影响、复现、直接原因、根源原因、事实 owner、风险、修复状态和回归验证",
        "当前任务验收前",
        "同一根因、同一允许范围",
        "原任务整改，不新建 TaskCard",
        "已交付或已验收功能的回归",
        "创建 Bug TaskCard",
        "同一根因只创建一张 Bug TaskCard",
        "测试预期、夹具、脚本、配置或环境错误",
        "不创建产品 Bug TaskCard",
        "TEST-*",
        "REQ-*",
        "来源任务",
        "根因证据",
    ):
        assert phrase in debugging

    for phrase in (
        "RED 测试范围",
        "GREEN 回归范围",
        "覆盖与未覆盖范围",
    ):
        assert phrase in tdd


def test_status_package_and_taskcard_decision_are_structured_contracts() -> None:
    verification = read("skills/verification-before-completion/SKILL.md")
    debugging = read("skills/systematic-debugging/SKILL.md")

    status_package = verification.split("## 状态包", maxsplit=1)[1]
    for field in (
        "- total: <integer | 无法计算>",
        "- passed: <integer | 无法计算>",
        "- failed: <integer | 无法计算>",
        "- error: <integer | 无法计算>",
        "- blocked: <integer | 无法计算>",
        "- skipped: <integer | 无法计算>",
        "- not_run: <integer | 无法计算>",
        "- cancelled: <integer | 无法计算>",
        "- covered_scope:",
        "- uncovered_scope:",
        "- failed_or_error_cases:",
        "test_id: <TEST-*>",
        "feature: <关联功能>",
        "symptom: <可观察现象>",
        "attribution: <当前归因 | 根因待调查>",
    ):
        assert field in status_package
    assert "无法计算（不可估算）" in verification

    decision = debugging.split("### 修复 TaskCard 决策", maxsplit=1)[1].split(
        "## 禁止", maxsplit=1
    )[0]
    assert "只作以下一种决定" in decision
    assert "原任务整改，不新建 TaskCard" in decision
    assert "创建 Bug TaskCard" in decision
    assert "回对应事实 owner，不创建产品 Bug TaskCard" in decision


def test_debugging_and_tdd_status_packages_include_change_locations() -> None:
    debugging = read("skills/systematic-debugging/SKILL.md")
    tdd = read("skills/tdd-workflow/SKILL.md")

    debugging_package = debugging.split("## 状态包", maxsplit=1)[1]
    tdd_package = tdd.split("## 输出契约", maxsplit=1)[1]
    tdd_flow = tdd.split("## 默认流程", maxsplit=1)[1].split("\n## ", maxsplit=1)[0]
    for content in (debugging_package, tdd_package):
        assert "change_locations" in content
        for field in ("file", "symbol", "change", "reason", "verification"):
            assert field in content

    assert "未修复时为 none" in debugging_package
    assert "code_shape_check: passed | failed | not_applicable" in tdd_package
    assert "执行两条代码形状禁令" in tdd_package
    assert "凡修改源码或测试代码不得用 N/A" in tdd_package
    for phrase in (
        "不得定义局部函数",
        "单调用点且无独立职责的 helper 必须内联",
    ):
        assert phrase in tdd_flow
