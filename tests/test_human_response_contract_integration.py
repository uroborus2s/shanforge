from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_humanizer_preserves_status_facts_and_brainstorming_only_gates_material_decisions() -> None:
    humanizer = (REPO_ROOT / "skills/humanizer/SKILL.md").read_text(encoding="utf-8")
    brainstorming = (REPO_ROOT / "skills/brainstorming/SKILL.md").read_text(encoding="utf-8")

    for phrase in (
        "Shanforge 状态回复",
        "三段式语义",
        "进度、验证、Bug、修复位置和唯一下一动作",
        "只能润色段内措辞",
        "技术评估的需求依据、现象、代码证据、因果链、影响与满足度结论、建议修改位置和验证方法",
    ):
        assert phrase in humanizer

    status_section = humanizer.split("## Shanforge 状态回复", maxsplit=1)[1].split(
        "\n## ", maxsplit=1
    )[0]
    for phrase in (
        "评估时点与修复状态必须保留",
        "不得把评估建议改写成已修复",
    ):
        assert phrase in status_section

    for phrase in (
        "改变目标、范围、验收或不可逆取舍",
        "合并为一次用户确认",
        "普通章节确认不得制造 Gate",
    ):
        assert phrase in brainstorming


def test_project_reply_merges_local_facts_with_the_project_envelope_without_guessing() -> None:
    contract = (
        REPO_ROOT / "skills/using-shanforge/references/work-skill-return-contract.md"
    ).read_text(encoding="utf-8")

    for phrase in (
        "专业增量",
        "项目化回复必须合并",
        "human_summary、`progress_delta`、`verification_summary`、"
        "`defect_summary`、`change_locations` 与项目状态信封",
        "缺事实不得猜",
    ):
        assert phrase in contract


def test_project_reply_preserves_the_complete_test_baseline_and_nonpassing_facts() -> None:
    status = (REPO_ROOT / "skills/using-shanforge/SKILL.md").read_text(encoding="utf-8")

    for phrase in (
        "每个 failed/error 的 TEST-ID、关联功能、现象和当前归因",
        "不得为了摘要或 humanizer 润色省略",
        "无法计算，不得猜",
        "数值为 0 的类别也必须输出，不得省略",
        "最后一次完整测试基线与修复后的定向重跑必须分开报告",
        "定向用例转为 passed 不能改写或重算最后一次完整基线",
        "每个 failed/error 的 owner 只能来自该用例自身事实",
        "未提供时写未分配/待确认",
        "不得从兄弟用例或模块推断/继承",
        "测试基线：total <值>；passed <值>；failed <值>；error <值>；"
        "blocked <值>；skipped <值>；not_run <值>；cancelled <值>",
    ):
        assert phrase in status


def test_status_examples_are_real_consumable_three_part_responses_with_one_next_action() -> None:
    status = (
        REPO_ROOT / "skills/using-shanforge/references/human-readable-status.md"
    ).read_text(encoding="utf-8")
    examples = {
        "开发示例": (
            "WBS 总数：5；已完成：2；进行中：1；未开始：1；阻塞：1",
            "当前 TaskCard：SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T04",
            "可观察功能",
            "验证：",
            "无需回复",
        ),
        "测试示例": (
            "总数：8；passed：5；failed：1；error：1；blocked：0；skipped：1；not_run：0；cancelled：0",
            "TEST-ID：TEST-CONTRACT-STATUS-002（failed）",
            "TEST-ID：TEST-CONTRACT-STATUS-003（error）",
            "关联功能：",
            "现象：",
            "当前归因：",
        ),
        "Bug 示例": (
            "现象：",
            "影响：",
            "复现：",
            "直接原因：",
            "根源原因：待调查",
            "owner：",
            "风险：",
            "Bug TaskCard 决策：",
        ),
        "修复示例": (
            "file：",
            "symbol：文档章节",
            "change：",
            "reason：",
            "verification：",
            "回归结果：",
        ),
        "发布示例": (
            "发布候选：",
            "环境：",
            "发布状态：released",
            "健康检查：passed",
            "冒烟结果：passed",
            "缺陷：无",
            "file：",
            "symbol：文档章节",
            "change：",
            "reason：",
            "verification：",
        ),
    }

    for heading, required_facts in examples.items():
        example = status.split(f"## {heading}", maxsplit=1)[1].split("\n## ", maxsplit=1)[0]
        for phrase in (
            "### 处理结果",
            "### 验证与风险",
            "### 下一步",
            "无需回复",
            *required_facts,
        ):
            assert phrase in example
        assert example.count("唯一下一动作：") == 1


def test_technical_assessment_example_keeps_a_user_consumable_fact_chain() -> None:
    status = (
        REPO_ROOT / "skills/using-shanforge/references/human-readable-status.md"
    ).read_text(encoding="utf-8")
    example = status.split("## 技术评估示例", maxsplit=1)[1].split("\n## ", maxsplit=1)[0]

    for phrase in (
        "### 处理结果",
        "整改前静态评估记录",
        "需求依据：目标：",
        "验收：",
        "约束：",
        "现象：实际：",
        "期望：",
        "触发：",
        "证据：",
        "代码证据：file：",
        "symbol：",
        "控制流：",
        "因果链：直接原因：",
        "根源原因：",
        "需求影响：",
        "影响与满足度结论：",
        "建议：修改位置：",
        "验证方法：",
        "尚未修复",
        "### 验证与风险",
        "其他未覆盖的技术评估回复路径可能仍遗漏需求 → 现象 → 代码因果链",
        "### 下一步",
        "唯一下一动作：在记录时点确认建议范围",
        "无需回复",
    ):
        assert phrase in example
    assert example.count("唯一下一动作：") == 1
