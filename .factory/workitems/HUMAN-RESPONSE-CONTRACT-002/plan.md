# HUMAN-RESPONSE-CONTRACT-002 实施计划

**目标：** 用一个共享状态头和按工作类型选择的正文合同，让开发、测试、Bug/修复结果在会话中可直接理解。

**架构：** `using-shanforge` 负责从 WBS、ledger 和工作 Skill 状态包生成用户响应；工作 Skill 只提供本职事实。详细场景规则放在一个按需 reference，避免把总控继续写长。

**复杂度 / 风险：** `complex / medium`。

**状态：** `ready_for_commit`

## Work Breakdown

| id | parent_id | title | status |
|---|---|---|---|
| HUMAN-RESPONSE-CONTRACT-002-T01 | | 响应需求与决策合同 | completed |
| HUMAN-RESPONSE-CONTRACT-002-T02 | | 总控、WBS、共享回写合同与用户指南 | completed |
| HUMAN-RESPONSE-CONTRACT-002-T03 | | 测试、Bug 与修复任务卡合同 | completed |
| HUMAN-RESPONSE-CONTRACT-002-T04 | | 集中验证与独立评审 | completed |

## T01：响应需求与决策合同

- 交付：本 brief、计划、TaskCard 和首条 ledger。
- 验收：开发基于 WBS、测试基于完整测试基线/报告、Bug 基于根因、修复任务卡三分支均有明确规则。

## T02：总控、WBS 与共享回写合同

- 修改：`skills/using-shanforge/SKILL.md`、新增 `skills/using-shanforge/references/human-readable-status.md`、更新 `skills/using-shanforge/references/work-skill-return-contract.md`。
- 同步：`docs/02-user-guide/user-guide.md` 的人类可读进度说明。
- 测试：`tests/test_skill_progress_visibility_and_continuation.py`、`tests/test_work_skill_status_envelope_ownership.py`。
- 验收：三段式外壳不变；开发/计划响应按 WBS 展示完成、进行中、剩余、阻塞；缺分母时失败关闭；内部字段不直接暴露为正文。

## T03：测试、Bug 与修复任务卡合同

- 修改：`skills/systematic-debugging/SKILL.md`、`skills/tdd-workflow/SKILL.md`、`skills/verification-before-completion/SKILL.md`。
- 测试：`tests/test_verification_debugging_workflow_skills.py`。
- 验收：测试七态汇总、失败项解释、Bug 八项事实和修复任务卡决策可由总控消费。

## T04：集中验证与独立评审

- 定向测试：上述三个测试文件。
- 关联测试：会话可见性、状态信封 owner、调试/验证合同。
- 静态检查：Ruff、Skill validator、JSONL 和 `git diff --check`。
- 独立评审：Terra/high，只读；Critical/Important 必须为 0。
- 提交：只提交本工作项精确范围；不包含并行生命周期治理工作项的脏文件。

## 执行模型

- T02：`gpt-5.6-terra / medium` worker。
- T03：`gpt-5.6-terra / medium` worker。
- T04：`gpt-5.6-terra / high` independent reviewer。
- T02/T03 文件无重叠，可并行；任何 scope expansion 交回 Sol。

## 计划自审

- 需求覆盖：HRC-REQ-001/002/006 -> T02；HRC-REQ-003/004/005/006 -> T03；全部 -> T04。
- 文件职责：总控只路由和翻译，专业 Skill 保留事实 owner，没有新增中心运行时。
- 可构建性：所有修改路径存在；新增一个按需 reference；测试入口已登记。
- 质量收口：一次集中验证和独立评审，不逐任务重复评审。
