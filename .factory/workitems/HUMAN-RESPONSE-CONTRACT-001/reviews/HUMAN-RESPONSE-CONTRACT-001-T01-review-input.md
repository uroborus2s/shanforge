# HUMAN-RESPONSE-CONTRACT-001-T01 独立评审输入

## 评审目标

判断三段式人类响应合同是否完整覆盖用户批准的语义，同时不破坏连续执行、真实人工 Gate、快速通道和工作 Skill 状态边界。

## 必读输入

- `.factory/workitems/HUMAN-RESPONSE-CONTRACT-001/brief.md`
- `.factory/workitems/HUMAN-RESPONSE-CONTRACT-001/task-briefs/HUMAN-RESPONSE-CONTRACT-001-T01.md`
- `.factory/workitems/HUMAN-RESPONSE-CONTRACT-001/reports/HUMAN-RESPONSE-CONTRACT-001-T01-implementer-report.md`
- `.factory/workitems/HUMAN-RESPONSE-CONTRACT-001/evidence/HUMAN-RESPONSE-CONTRACT-001-T01-verification.md`
- `skills/using-shanforge/SKILL.md`
- `tests/test_skill_progress_visibility_and_continuation.py`
- 上述两个候选文件的限定 `git diff`

## 评审问题

1. 是否先直接回应，再给处理结果，最后明确需要用户回复什么。
2. 项目位置是否只作为第二部分内容。
3. “无需回复”是否明确不会停止仍有剩余范围的内部执行。
4. 最终回复是否只允许出现在终态、真实人工 Gate、blocker 或权限扩展场景。
5. 是否错误修改了工作 Skill、项目记忆或 PM/SQLite 边界。
6. 测试是否能防止核心语义回退。

## Reviewer 边界

- 只读。
- 不修改实现、测试、WorkItem、ledger、Git index 或外部系统。
- 输出 `approved` 或 `changes_requested`，并给出评分、C/I/M、独立性证据和实际验证结果。
