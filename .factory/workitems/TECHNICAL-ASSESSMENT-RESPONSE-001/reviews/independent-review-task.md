# Independent Review Task

- work_item: `TECHNICAL-ASSESSMENT-RESPONSE-001`
- task: `TECHNICAL-ASSESSMENT-RESPONSE-001-T01`
- review_type: `shared response contract task review`
- write_policy: `read_only`
- current_gate: `needs_independent_review`
- human_confirmation_required: `false`

## Requirements

技术评估回复必须把需求、可观察现象和代码事实连成可读因果链，说明代码为什么造成现象、现象怎样影响需求，以及建议修改位置和验证方法。评估建议不得冒充已修复。

## Inputs

- brief：`.factory/workitems/TECHNICAL-ASSESSMENT-RESPONSE-001/brief.md`
- task brief：`.factory/workitems/TECHNICAL-ASSESSMENT-RESPONSE-001/task-briefs/TECHNICAL-ASSESSMENT-RESPONSE-001-T01.md`
- ledger：`.factory/workitems/TECHNICAL-ASSESSMENT-RESPONSE-001/ledger.jsonl`
- diff package：当前工作树中下列五个文件的 diff
  - `skills/using-shanforge/references/human-readable-status.md`
  - `skills/using-shanforge/references/work-skill-return-contract.md`
  - `skills/humanizer/SKILL.md`
  - `tests/test_human_response_contract_integration.py`
  - `tests/test_response_owner_contracts.py`

## Fresh Verification

- 定向及相关契约测试：`33 passed in 0.04s`，exit 0。
- Ruff：`All checks passed!`，exit 0。
- 代码形状检查：无违规输出，exit 0。
- `using-shanforge` Skill 校验：`Skill is valid!`，exit 0。
- `humanizer` Skill 校验：`Skill is valid!`，exit 0。
- `git diff --check`：无输出，exit 0。
- work item ledger：逐行 JSON 有效，event_id 无重复。

## Review Focus

1. 是否明确说明需求、实际/期望现象、触发与证据。
2. 代码证据是否包含真实文件、符号和控制流/数据流，而非路径清单。
3. 是否形成“代码行为 → 现象 → 需求影响”的因果链，并区分直接原因、根源原因和未知。
4. 修改建议是否包含文件/符号、目的和验证方法，且没有冒充已修复。
5. 示例是否事实一致、能被非实现者读懂，没有测试语境复制残留。
6. 是否复用唯一共享合同，没有新增重复模板、运行时、依赖或无必要抽象。
7. 测试是否覆盖事实链、历史记录时间点和 humanizer 保真边界。

## Output Contract

只读评审，不得修改任何文件。返回 reviewer_type、reviewer_id、reviewer_independence_evidence、评分明细、Critical/Important/Minor findings、review_status 和 next_gate_status。`approved` 默认返回 `return_to_orchestrator`；不得把评审通过写成任务完成。
