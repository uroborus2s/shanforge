# Skill 流程完整性测试报告

## 评估结论

当前 skill 流程基本覆盖软件开发本地闭环：需求澄清、PRD/设计、计划、执行、TDD/调试、验证、独立 review、review 反馈处理、人工确认、本地提交都有对应入口和门禁。黑盒 eval 契约也已存在，覆盖 6 类场景，并有结构测试固定。

主要边界：完整闭环只到本地提交较扎实；远端 PR / push / merge 目前只作为禁止冒充的边界存在，不是已实现闭环。另一个主要缺口是部分需求/文档类 skill 的 Shanforge 状态包、ledger、review gate 没有执行类 skill 那么明确。

## 流程矩阵

| 环节 | 输入 | 动作 | 输出 / 证据 | 门禁 | 评估 |
|---|---|---|---|---|---|
| 会话恢复 | `.factory/memory/*`、ledger | `using-shanforge` 路由，`project-memory` 恢复 | 会话卡、已读/排除文件、当前 work item | 禁止散读 docs，ledger 优先 | 覆盖清楚 |
| 一句话新功能 | 用户一句话、会话卡 | `brainstorming` 澄清，必要时 `requirements-engineering` | brief、PRD、summary | 用户批准后才能计划 | 覆盖，但需求 skill 偏方法论 |
| PRD / 文档 | brief / 已批准输入 | `requirements-engineering`、`document-templates` | PRD、正式 docs、memory summary | 不写未批准事实 | 中等，状态回写偏弱 |
| 计划 | 已批准 spec / brief | `writing-plans` 生成 plan/task briefs | plan、task briefs、review handoff | plan 只能 ready_for_review | 覆盖清楚 |
| 执行 | approved plan、task brief、ledger | `subagent-driven-development` 或 `executing-plans` | evidence、report、review input、ledger | 实现者只能 ready_for_review | 覆盖清楚 |
| Bug 修复 | 失败输出 / 症状 | `systematic-debugging` + `tdd-workflow` | 根因报告、失败测试、验证证据 | 先复现和根因，禁兜底掩盖 | 覆盖清楚 |
| 完成验证 | 完成声明、diff、plan | `verification-before-completion` | 新鲜命令、exit code、失败/跳过统计 | 无新鲜证据不得说完成 | 覆盖清楚 |
| 独立 review | task brief、diff、evidence | `requesting-code-review` | review 文件、review ledger | same_thread 不能 approved | 覆盖清楚 |
| Review 反馈 | reviewer comments | `receiving-code-review` | triage、response、fix report、验证 | 先核实，不盲改 | 覆盖清楚 |
| 人工确认 | execution report、evidence、review | 流程总控停在确认包 | human_approved / changes_requested | reviewer approved 不等于人工确认 | 覆盖清楚 |
| 本地提交 | human_approved、ledger、diff | `gitcommitzh` | 中文提交说明、真实 hash | 只提交当前任务范围 | 覆盖清楚 |
| 远端 PR | 本地提交 / PR diff | 目前仅边界声明 | 无固定 skill 闭环 | 禁止把本地 commit 冒充 PR | 有缺口 |

## 6 类场景覆盖

- 新功能 / 一句话需求：黑盒契约 `SF-SP-009-S1` 覆盖，不应直接改代码。
- Bug 修复：`S2` 覆盖复现、根因、回归验证。
- Review 反馈：`S3` 覆盖逐条核实、pushback / clarification。
- 压缩恢复：`S4` 覆盖读取 ledger、跳过已完成 idempotency。
- 完成声明 / 收尾：`S5` 覆盖新鲜验证、review、commit/PR、memory sync 缺口报告。
- 自评隔离：`S6` 覆盖 self_check 与 independent review 分离。

已有黑盒 eval 契约在 `skills/using-shanforge/references/black-box-flow-eval.md`，结构测试在 `tests/test_black_box_workflow_eval.py`。

## 主要缺口 / 风险

1. `requirements-engineering` 主文件更像通用方法论，缺 Shanforge 标准状态包、ledger 输出、review gate；PRD 模板补了一部分，但流程门不够硬。
2. `brainstorming` 仍有“下一步 skill”交接字段，和 `using-shanforge` “只有总控决定下一步”的规则存在轻微冲突。
3. 黑盒 eval 当前测试主要验证契约文本结构，不是真正运行 6 个场景的行为回放；能防止文档缺失，不能证明代理实际遵守。
4. PR 闭环没有本地专用执行 skill；`gitcommitzh` 只做本地提交，远端 PR / push / merge 只能靠边界约束。
5. 真值第 7.1 的固定读取清单与当前 `project-memory` 的最小读取策略有差异；建议以“不散读、可解释读取”为准，不强制读全套。

## 最小测试断言建议

- 新增断言：`requirements-engineering/SKILL.md` 必须包含输出位置、ledger/memory sync、状态包、不得 approved/done。
- 新增断言：除 `using-shanforge` 外，工作 skill 不得出现“下一步 skill”作为决策字段；可保留 `needs`。
- 新增黑盒 smoke：用 6 条输入生成 dry-run transcript，断言没有写文件、没有越过 gate、状态包正确。
- 新增 PR 边界断言：完成声明中若无 PR/push/merge 证据，必须明确“仅本地闭环”。
- 新增 ledger 恢复断言：同一 `idempotency_key` 已 `done/approved/passed` 时，恢复流程必须跳过。
