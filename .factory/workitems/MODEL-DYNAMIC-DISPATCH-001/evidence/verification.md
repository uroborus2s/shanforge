# 动态派发验证记录

## RED

T02 首次新检查 `UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q tests/test_dynamic_model_dispatch.py`：exit 1，1 failed / 1 passed；旧合同缺少动态模型决策表。补强负向变异后重跑仍 exit 1、2 failed，失败原因同为缺表。未改旧证据使检查通过。

## 隔离候选

目录：/private/tmp/shanforge-dynamic-dispatch-01a07e6a。无服务、端口、数据库、账号或外部 API 操作；使用仓库既有 uv 环境。

- 父验证：`UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q tests/test_dynamic_model_dispatch.py tests/test_model_tier_routing.py tests/test_black_box_workflow_eval.py tests/test_residual_audit_contracts.py`，exit 0，31 passed。
- worker 报告：对应四文件 Ruff、代码形状检查、diff check、using-shanforge quick_validate、task-reader TOML/read-only/无固定模型强度断言均 exit 0；最终父验证另行记录。
- 父全量：`UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q`，exit 1，418 passed、2 failed、11 subtests passed，10.61 秒。

两项失败属于隔离快照中前置任务尚未完成的历史验证绑定：

1. `test_behavior_evidence_is_bound_to_current_inputs`：FLOW-STATUS-REVIEW-001 的历史 manifest 被拿来比较现行 SKILL，当前修改后哈希不再相同。
2. `test_formal_contract_preserves_v1_2_baseline_and_adds_delivery_workflows`：测试仍将现行设计版本固定为 v2.0.0，而本候选为 v2.2.0。

前置 MODEL-ORCHESTRATOR-SELECTION-001 正在修复这两个事实 owner；本批等待其提交后集成与复验。此轮全量结论 failed，不能以定向31通过替代。

## 行为与派发证据

- 12个前向场景原始输入为 reviews/forward-input.md，实际独立代理原始回复为 forward-trial.json；它们是路由模拟，未实际派发12个代理。
- 本批真实宿主回执为 reviews/dispatch-receipts.jsonl，分别请求 Astra/high、Terra/medium、Terra/high；accepted 只证明宿主接受请求。
- task-reader 的新会话宿主加载/运行尚未实测；合同要求未暴露时失败关闭。TOML 校验不证明热加载。

## MODEL-DYN-I-01整改复验

worker先添加反例RED，exit1；改有序分支后四文件31 passed。父复跑tests/test_black_box_workflow_eval.py：15 passed，exit0；Ruff exit0。父对using-shanforge、subagent-driven-development、writing-plans运行quick_validate均exit0；四个Python文件Ruff与代码形状检查exit0。代码形状只报告既有单调用helper候选，本轮未增加对应helper，未产生拒绝。

## 版本消费者与预合并

新增授权的版本消费者先RED（旧2.1与当前2.2不符），修复后父验证10 passed、Ruff exit0。对照前置任务当前文件、隔离起始基线和本候选做临时三方合并：0冲突，19文件输出逐个等于已评审v3指纹；仅准备临时结果，尚未覆盖主目录。

## 主目录首次集成

前置实现提交1b64734后，三方合并0冲突，19/19文件与独立批准v3指纹一致，已写入主目录。父运行完整pytest：exit1，419 passed、1 failed、11 subtests passed，10.15秒；唯一失败为tests/test_lifecycle_governance.py中的索引来源固定为前置任务。其余原隔离失败已解决。Ruff、3个skill validator、19/19哈希与task-reader静态TOML验证均exit0。

该索引测试是本次正式来源更新的直接消费者，扩展T02仅修复该文件，保持历史来源断言，交同reviewer复查。

## 最终有效验证（主目录）

- 基线：前置提交1b64734 / 242af89；最终候选candidate-v5-sha256.json，父回读20/20一致。
- `UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q`：exit0，**420 passed, 11 subtests passed in 10.32s**。包含已同步本任务身份/下一动作的memory。
- 六个变更Python文件 `uv run ruff check`：exit0，All checks passed；`git diff --check`：exit0，无输出。
- 三个变更skill的quick_validate：exit0，全部Skill is valid。task-reader TOML：read-only、无固定model/effort断言通过；仅静态证据。
- 代码形状：首次扩大到六文件扫描exit1，暴露两个本次新增lambda和一个HEAD既有local permits；两处lambda已由T02等价整改。最终用同一ShapeVisitor逐文件与HEAD比较，exit0、无新增named local function/lambda。full_project:215的既有permits保留，故不能声称整文件形状扫描零存量问题；其余helper提示未升级为新增抽象。
- 当前WorkItem JSONL均可解析；独立最终review为v5 approved，20文件，MODEL-DYN-I-01 closed。

初始RED、整合失败、首轮漏检均保留以上历史。没有外部API/服务/数据库/账号操作；没有task-reader新会话宿主加载或完整模型组合穷举验收。

提交态memory回写后：`uv run pytest -q tests/test_project_memory_skill.py tests/test_using_shanforge_snapshot.py`，exit0，27 passed / 4 subtests passed，0.76秒。此前一次误写测试类选择器exit4，no tests ran；已改用这两个真实文件完成检查。

暂存后diffcheck首次exit2：485项全部来自5份原始candidate*.diff中的单空格上下文标记（统一补丁格式），并非源码尾随空白。逐条断言均为单空格行；保留原始评审补丁不改写。对明确排除这5份原始补丁的其余暂存文件运行`git diff --cached --check -- <明确文件列表>`，exit0。
