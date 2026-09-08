# 动态子模型与推理强度实施计划

- 状态：closed；实现提交7955a02，独立终审、验证与memory已同步。
- 架构：只改现有 skill 合同与消费它们的测试；无生产、网络 API、数据写入或新依赖。
- 共享文件依赖：MODEL-ORCHESTRATOR-SELECTION-001 完成提交后开始 T01 和 T02 的已有文件编辑；本工作项材料和新增测试可先行。

## Work Breakdown

| id | parent_id | title | status |
|---|---|---|---|
| WBS-MODEL-DYNAMIC-00 | | 授权与批次质量收口 | done |
| WBS-MODEL-DYNAMIC-01 | WBS-MODEL-DYNAMIC-00 | 当前合同及正式说明 | done |
| WBS-MODEL-DYNAMIC-02 | WBS-MODEL-DYNAMIC-00 | 动态路由及拒绝行为验证 | done |
| WBS-MODEL-DYNAMIC-03 | WBS-MODEL-DYNAMIC-00 | 独立试用与评审 | done |

## 共享合同

主会话确定 reasoning_demand：routine=步骤与验收明确；judgment=需要设计/架构/调用链判断；deep=疑难根因、并发状态或高风险验证；extreme=已具备复现、候选根因和排查证据，仍未解的单个难题。信息不足至少 judgment，并按既有风险规则处理。route_reason 必须解释选择和证据，Max 无证据不派发。

唯一模型表位于 using-shanforge/SKILL.md 的 `### 子任务模型决策表`；按首行命中，字段为 dispatch_role、task_complexity、risk_level、reasoning_demand、execution_model、requested_reasoning_effort，值中 `*` 为兜底：

| dispatch_role | task_complexity | risk_level | reasoning_demand | execution_model | requested_reasoning_effort |
|---|---|---|---|---|---|
| * | * | * | extreme | gpt-6-astra | max |
| * | * | high | * | gpt-6-astra | xhigh |
| * | * | * | deep | gpt-6-astra | xhigh |
| reviewer | * | * | * | gpt-5.6-terra | high |
| * | * | * | judgment | gpt-6-astra | high |
| * | complex | * | * | gpt-6-astra | high |
| * | simple | low | routine | gpt-5.6-luna | low |
| * | * | * | * | gpt-5.6-terra | medium |

先校验角色/授权/输入/风险与 effort 能力，后查表。routine 不覆盖审查下限、高风险或复杂任务。role 仅 worker / analyst / reviewer；none 不选模型。规则是项目选档策略，不能表述为官方每类工作的硬要求。

新增只读 analyst 子任务分支：父会话决定值得拆出且有清楚问题与只读范围时，将该子任务设为 direct-answer-workflow / no_project_write / analyst / execution_authorized=true；项目化时继承已存在任务身份，不改变父工作流阶段。它只返证据/建议，不写项目文件，不作为独立质量批准。普通直接回答仍不强制派发、不创建项目身份或 ledger。

现有三个固定 role 留作明确匹配的 presets；增加 `.codex/agents/task-reader.toml`，只固定只读职责与 sandbox，不固定 model/effort。父调用仍必须显式传值；宿主未加载该角色时不能假装可用。当前会话可用 terra-reviewer/high 做普通独立评审；Astra 深度 reviewer 必须选择可用且不冲突的只读角色。

## 分工与验证

- T01：Astra/high，跨合同判断；修改 skill、模板、正式指南/PRD/设计和 task-reader preset。最小同步，不回改历史条目。先等待测试 RED。
- T02：Terra/medium，验收已锁定；拥有 tests/test_dynamic_model_dispatch.py、tests/test_model_tier_routing.py、tests/test_black_box_workflow_eval.py、tests/test_residual_audit_contracts.py。新测试解析真实合同表，不新增产品 runtime。保留历史回执；负例覆盖降高风险、review 用低档、缺模型/effort、fork=all、回执不匹配和能力不支持。测试是合同检查，真实语义另以独立试用验证。
- T03：只读独立试用返回原始场景响应，再由未实施 reviewer 审查最终 diff、失败用例和中文准确性。父会话保存真实工具回执和候选内容指纹。
- 父会话拥有本 WorkItem、.factory/memory/{agent-session.md,current-state.md,runtime-brief.md,tasks.summary.md,tests.summary.md,review-ledger.jsonl}；只同步当前批次事实，并等待另一任务的共享 memory 写入结束。

定向：UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q tests/test_dynamic_model_dispatch.py tests/test_model_tier_routing.py tests/test_black_box_workflow_eval.py tests/test_residual_audit_contracts.py。
最终：同环境 uv run pytest -q；变更 Python 的 uv run ruff check 和 uv run python skills/tdd-workflow/scripts/check_code_shape.py；quick_validate.py 校验变更 skill；git diff --check。最终一轮全量用于跨合同消费者收口，修复阶段仅跑受影响项。

## 自审与边界

brief 八项验收都有任务覆盖。T01/T02 写集独立，T02 写好 RED 后 T01 执行；集中评审一次。用户授权的是本地可回滚治理资产，风险 medium，无需新增人工 Gate。不覆盖其他任务、并发数 10、全局配置和历史审计事实，不自动安装或推送。

## 只读派发边界补强

analyst 仅从 processing_mode=project_workitem/tracked_task 派生，必须已有任务身份、父阶段和明确只读输入；父会话主动声明 analyst 才命中。子任务 direct-answer-workflow/no_project_write 不改变父阶段。普通 direct_answer/lightweight_analysis 仍不创建身份或 ledger、不强制派发。原生 task-reader 供 analyst/reviewer 共用，只读 role 不可用时不冒充可用；父会话可继续已授权直接只读分析并注明未派发，不能代写 worker。新 role 文件解析验证与宿主热加载/执行证据必须分别报告。

## 隔离实施更新

前置任务继续评审整改，为解除共享写集等待，T01/T02 已转入 /private/tmp/shanforge-dynamic-dispatch-01a07e6a。原相对写集、模型与 effort 不变；以当前前置候选快照为基线，父会话待前置提交后只合入本任务增量，冲突由对应 worker 处理。主工作区的 .factory 工作项仍是执行事实源。

## 集成事实同步扩展

T01追加docs/document-index.md当前版本与来源同步；T02追加tests/test_full_project_session_workflow_routing.py，仅将当前版本/来源的过期固定值改为正式头部、索引及最新版本记录一致性；历史候选v1.2/v1.1哈希和语义断言保持。两者均为本次模型合同版本更新的直接消费者，原授权范围内必要同步。

## 最终集成消费者修复

主目录完整验证暴露tests/test_lifecycle_governance.py索引来源仍固定为前置任务。追加T02最小写集仅此文件，改为当前索引头部与其最新历史条目一致性，保留其余历史来源断言；同reviewer复审后最终全量。父事实同步补充change-summary.md，仅按本次实际提交回执更新。
