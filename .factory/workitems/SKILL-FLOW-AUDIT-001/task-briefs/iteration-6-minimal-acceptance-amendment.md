# Iteration 6 最小验收修订

## 决策

用户于 2026-07-27 批准最小路径。本修订替代
`iteration-6-fix-language-prompt-97.md` 中“全仓 Skill 平均分 >=97”的不可达
口径；原始评审报告保留为历史事实，不覆盖。

## 冻结评分集合

只复评 Iteration 6 明确整改的 8 个 Skill：

| Skill | 候选 SHA-256 |
|---|---|
| `agent-harness-construction` | `25af3a31ab0a02f83f1f686d669828529d3bc6f080a1daf251eb7c9323905ee9` |
| `ai-first-engineering` | `17257ec97e11baced6756077026e4aea389e8f772b27fd7f9765da7abbb98b84` |
| `article-writing` | `ea8b087e79535164e4c13c618977492bfe17a3a8519de6c52e5fd1b2becaa56f` |
| `using-shanforge` | `aed46504cc8dac71ce6af3a98901a309e44715cab0d4a50bcc738b5bcf6389b1` |
| `frontend-patterns` | `89b7eca52eadaaaf41cdb28832a91443c0cae4e1495a8b40f49025b8b5a7f790` |
| `tdd-workflow` | `91948522259bdc91ac241db0ea0eb96f9369e4664030a9d04d74c838f9c1abb3` |
| `art-asset-pipeline` | `c5b74505c6dabe8887d6bf183ea9c173e36e758a6eae80273ffd409ed45165fa` |
| `requesting-code-review` | `98c949d01f5af3755f26a6f9172ee37c18aad385105b86390b11e248903f9979` |

候选哈希变化时必须记录原因并重新冻结，不能混用旧评分。

工作 Skill 的项目状态信封已由后续已批准架构收口到共享契约。复评
`agent-harness-construction`、`ai-first-engineering`、`article-writing`、
`frontend-patterns`、`art-asset-pipeline` 时，必须同时读取
`skills/using-shanforge/references/work-skill-return-contract.md`
（SHA-256：
`caeb1b370e8d835682ece43a7c93cfda40f582a40473dff94fbad94717b1ffbd`），
不得因 Skill 不再重复项目状态信封而扣分。

## 冻结评分公式

每个 Skill 分别给出中文语言分和 Prompt 工程分，均为 0-100：

- 中文语言：清晰 30、简洁与去重 25、术语一致 20、自然表达 15、可扫描性 10。
- Prompt 工程：触发/路由边界 20、指令优先级 15、动作/工具/子 agent
  边界 15、输出与证据 20、失败语义 15、Gate 安全与旧流程隔离 15。
- 每个维度总分 = 8 个 Skill 的等权算术平均，保留两位小数。

通过条件：

- 中文语言平均分 `>=97`；
- Prompt 工程平均分 `>=97`；
- Critical = 0，Important = 0；
- Required Fixes 1-8 全部关闭；
- 下列冻结 workflow 测试和 Ruff 全绿。

当前 37 个 Skill 的全仓平均分只保留为诊断指标，不再作为本整改包 Gate。

## 冻结 Workflow 测试清单

旧完整清单同时包含已删除文件、已关闭任务的历史投影和其他并行 WorkItem
契约，不能作为 8 Skill 整改包的隔离 Gate。关闭门只冻结下列 9 个节点：

```text
tests/test_skill_flow_process_audit.py::test_agent_harness_construction_has_work_item_status_package
tests/test_bug_fix_root_cause_skill_rules.py::test_ai_first_engineering_defines_team_bug_fix_discipline
tests/test_skill_flow_process_audit.py::test_article_writing_has_work_item_status_package
tests/test_task_workflow_semantics.py::test_flow_controller_defines_processing_modes_before_skill_routing
tests/test_task_workflow_semantics.py::test_frontend_patterns_work_item_status_uses_design_decision_as_need
tests/test_bug_fix_root_cause_skill_rules.py::test_tdd_workflow_requires_root_cause_before_bug_fix
tests/test_task_workflow_semantics.py::test_art_asset_pipeline_skill_outputs_confirmed_assets_only
tests/test_review_workflow_skills.py::test_requesting_code_review_skill_is_shanforge_localized
tests/test_work_skill_status_envelope_ownership.py::test_shared_contract_separates_local_results_from_project_envelope
```

每个节点只读取一个冻结 Skill 或共享回写合同；不读取范围外 Skill、动态全仓集合、
历史 WorkItem 或共享 memory。任一节点后续删除或职责变化时，先形成新的验收修订，
不得静默缩减清单。

## 执行边界

- 本次最小修正只冻结验收合同并重跑当前候选，不启动 37 Skill 全量改造。
- 当前旧失败 `tests/test_independent_review_gate.py` 已无法复现，不额外改测试。
- 文件级旧套件的其他失败只记录为跨 WorkItem 漂移，不纳入本整改包 Gate。
- 作者只能推进到 `ready_for_review`；最终结论必须来自独立 reviewer。
- 不恢复旧中心脚本、`factory-*` Gate 或旧远端闭环。
