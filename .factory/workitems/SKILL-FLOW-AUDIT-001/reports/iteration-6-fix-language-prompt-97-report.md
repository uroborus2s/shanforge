# Iteration 6 Fix Language Prompt 97 Report

status: ready_for_review
work_item: SKILL-FLOW-AUDIT-001
author_status: ready_for_review

## 含义保留清单

本清单写在 skill 修改前，用于约束本轮最小修复。

### 全局保留

- 目标：只修 iteration-6 三份报告点名的中文语言和 Prompt 问题，目标为后续独立复评中文语言平均分 >= 97、Prompt 平均分 >= 97、Critical / Important 为 0。
- 触发：本轮只处理 `SKILL-FLOW-AUDIT-001` iteration-6 task brief 要求的 skill 文本修复。
- 输入：task brief、三份 iteration-6 报告、当前 `skills/*/SKILL.md`、相关结构测试。
- 步骤：先读 brief 和报告；修改前写含义保留清单；再做最小 skill 修改；运行最小验证；写 report、evidence、review input。
- 输出：本报告、验证 evidence、review input，以及被点名 skill 的最小文本修复。
- 禁止项：不提交、不 push、不建 PR、不 merge；不改 ledger、memory；不覆盖 iteration-6 原始报告；不恢复旧中心脚本、旧 `factory-*` gate 或远端闭环冒充。
- 例外：为达到 97 分，可继续触碰低于 95 分或报告明确点名的 skill；不重写高分且无问题的 skill。
- 验收：作者只能回写 `ready_for_review`，不能写 `approved`；独立 reviewer 才能判断最终通过。
- 风险：自评分不是独立复评；若无法可靠达到 97，必须写明残留风险。
- handoff：远端 PR / push / merge 仍由远端 handoff 契约处理；本轮不触发远端动作。

### 必修 skill 保留

| skill | 必须保留的语义 |
|---|---|
| `agent-harness-construction` | agent harness、工具 schema、观察格式、恢复路径和上下文预算是职责核心；不接管 Shanforge 路由、review gate、人工确认或提交；Codex skill 文本、触发和打包归 `skill-creator`；工作项状态包必须可追踪。 |
| `ai-first-engineering` | 只给 AI 参与工程的规则、评审标准、测试策略和协作模式；不替代实施、正式文档、review 或人工确认；Bug 修复必须根因先行，禁止兜底冒充修复。 |
| `article-writing` | 负责发布型长文、博客、指南、教程和时事通讯；不接管正式项目文档；事实不足时不虚构；风格参考必须有授权来源；默认不落盘。 |
| `using-shanforge` | 只做流程总控和路由；Bug / 测试失败必须先由 `systematic-debugging` 做根因调查；根因和修复方案双 gate 通过后才进入 TDD / 回归；远端 handoff 不冒充完成。 |
| `frontend-patterns` | 负责前端实现模式、组件边界、状态、性能和可访问性；不替代 UX 设计、系统化调试或完成前验证；作为 work item owner 时状态词要和 Shanforge 标准兼容。 |
| `tdd-workflow` | 测试先行、根因先行、风险分级验证；根因报告和修复方案 gate 未通过前不得进入 `GREEN`；本轮只删重复表达，不弱化 gate。 |
| `art-asset-pipeline` | 先确认美术方向，再确认资源清单，最后生产资源包；未确认内容只能在 `tmp/`，确认后才进入 `approved/`；最终包和 `manifest.json` 不得泄漏未确认资源；作者不自批。 |
| `requesting-code-review` | review 必须独立；同线程作者自检只能 `self_check_passed`，下一 gate 是 `needs_independent_review`；真实独立 reviewer 才能 `approved`；人工确认不可由 review 替代。 |

## 实际修改文件清单

- `skills/agent-harness-construction/SKILL.md`
- `skills/ai-first-engineering/SKILL.md`
- `skills/article-writing/SKILL.md`
- `skills/using-shanforge/SKILL.md`
- `skills/frontend-patterns/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `skills/art-asset-pipeline/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `tests/test_skill_flow_process_audit.py`
- `tests/test_task_workflow_semantics.py`
- `tests/test_bug_fix_root_cause_skill_rules.py`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-6-fix-language-prompt-97-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-6-fix-language-prompt-97-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-6-fix-language-prompt-97-review-input.md`

## 分项修复说明

| 文件 | 中文语言提升 | Prompt 提升 |
|---|---|---|
| `agent-harness-construction` | 用短句补边界，避免 harness 与 skill 写作混读。 | 状态包补 `work_item` / `ledger_event`；补 `needs_user_input` 例子；Codex skill 写作归 `skill-creator`。 |
| `ai-first-engineering` | 把末尾失败语义拆成两段，读者可直接判断停在何处。 | 状态包补 `work_item` / `ledger_event`；`blocked` 和 `needs_user_input` 变成可执行分支。 |
| `article-writing` | 用一句话区分发布型长文与工作文档，减少边界歧义。 | 状态包补 `work_item` / `ledger_event` / `verification`；补 `needs_user_input` 语义。 |
| `using-shanforge` | bug 场景文字直接写出根因调查 owner，减少绕读。 | Bug / 测试失败路由显式落到 `systematic-debugging`；修复阶段状态词对齐 `tdd-workflow` / `ai-regression-testing`。 |
| `frontend-patterns` | 明确 `design_decision` 不是状态，避免术语混用。 | work item 状态改为 `ready_for_review | blocked | needs_user_input`，与 Shanforge owner 契约一致。 |
| `tdd-workflow` | 删除“无根因确认不得进入 GREEN 实现”的重复短句。 | 保留根因报告和修复方案双 gate，未削弱根因先行语义。 |
| `art-asset-pipeline` | 把 `tmp/`、`approved/`、用户确认和最终包泄漏规则合并成短表。 | 阶段推进、目录流转、最终交付、收尾清理四类规则更可审计。 |
| `requesting-code-review` | 合并同线程作者自检重复表达，保留独立性硬门。 | 仍明确 `self_check_passed`、`needs_independent_review`、禁止 `approved` / `review_score` / `pending_human_confirmation`。 |
| 相关测试 | 断言改为当前唯一 gate 文案，避免测试要求重复句。 | 新增状态包、`needs_user_input`、frontend status 和目标 skill 缺口回归断言。 |

## 自评分

- 中文语言平均分：97.1。
- Prompt 平均分：97.2。
- 低于 90 数量：0。
- Critical：0。
- Important：0。
- Minor：2。

说明：这是作者自检评分，只表示本轮修复包达到 `ready_for_review`。最终分数必须由独立复评确认。

## 未处理项和原因

- 未统一 `project-memory` 为标准 `工作结果` 状态包。原因：iteration-6 Required Fixes 未要求；该 skill 当前承担会话卡格式，报告也把它列为可决定是否豁免的问题。
- 未触碰 `crawler4j-model-project`、`python-uv-project`、`receiving-code-review` 等中文 91 分 skill。原因：本轮优先 Required Fixes；这些文件没有 Critical / Important，也没有明确要求本轮重写，扩大范围会增加无关语义漂移风险。
- 未重写 94-96 分 skill。原因：task brief 明确不要重写高分且无问题的 skill。
- 残留风险：独立 reviewer 若按全量 36 个 skill 重新严格打分，可能继续对未触碰的 91-94 分入口扣语言扫描成本分。

## Shanforge 状态包

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: skill-creator
- status: ready_for_review
- outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-6-fix-language-prompt-97-report.md
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-6-fix-language-prompt-97-review-input.md
  - skills/agent-harness-construction/SKILL.md
  - skills/ai-first-engineering/SKILL.md
  - skills/article-writing/SKILL.md
  - skills/using-shanforge/SKILL.md
  - skills/frontend-patterns/SKILL.md
  - skills/tdd-workflow/SKILL.md
  - skills/art-asset-pipeline/SKILL.md
  - skills/requesting-code-review/SKILL.md
- evidence:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-6-fix-language-prompt-97-verification.md
- ledger_event: none
- needs:
  - review
```
