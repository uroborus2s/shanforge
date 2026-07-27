# FLOW-TASK-015 方案整改验证证据

## 范围

- 正式基线：`docs/05-design/workflow-execution-design.md`
- 受控候选：`.factory/workitems/FLOW-CONTRACT-001/drafts/FLOW-TASK-015-workflow-contract.v1.2.0.candidate.md`
- 结构测试：`tests/test_full_project_session_workflow_routing.py`
- 状态独立回归：
  - `tests/fixtures/workflow-gates/missing-review-snapshot.json`
  - `.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-012-gate-smoke-transcript.v2.md`
  - `tests/test_black_box_workflow_eval.py`
  - `tests/test_project_memory_skill.py`

## 基线与候选绑定

- 正式版本：`v1.1.0`
- 正式基线 SHA-256：`5769beb3478d528a0b0888328381173aa799e1e137925fc393bd98d97d3eb687`
- 候选版本：`v1.2.0`
- 候选 SHA-256：`3d5f4cbabda86312da0603db5662175453d12dd5966c788301b0c79c2cb4992f`
- 正式文档本轮未修改。

## Red

命令：

```bash
.venv/bin/python -m pytest tests/test_full_project_session_workflow_routing.py -q
```

结果：

```text
6 failed, 1 passed
```

失败原因符合预期：受控候选尚不存在，完整行为合同、工作流字段、写入矩阵、节点转换和基线绑定均无法读取。

前置相邻回归：

```text
2 failed, 47 passed
```

- Gate smoke 的 S9/S10 绑定已完成 Review 的真实 `FLOW-TASK-013`。
- current-state 测试把活跃任务硬编码为 `FLOW-TASK-014`。

## Green

命令：

```bash
.venv/bin/python -m pytest tests/test_full_project_session_workflow_routing.py -q
```

结果：

```text
7 passed
```

结构断言覆盖：

- 16 个稳定行为 ID 和完整中文行为集合；
- 每个行为恰好一个默认工作流，Handler 独立登记；
- 13 个工作流逐行包含写策略、触发、优先级、输入、允许、禁止、输出、ledger、evidence、进入和退出 Gate；
- 5 类写入策略与缺身份、仅 memory、越界 identity creation 负例；
- 每个工作流的节点、合法主路径、停止态和人工 Gate 规则；
- 正式基线 SHA-256 动态回读一致，候选明确未生效。

## Iteration 2 Red / Green

第二轮 Reviewer 发现身份创建路由死锁和重复 ID 测试缺口。

Red：

```text
4 failed, 3 passed
```

失败点为缺 `tracking-identity-workflow`、缺工作流写策略列、身份创建节点/路由不可达和缺重复行断言。

Green：

```text
7 passed
```

整改后：

- 新增 `tracking-identity-workflow`，优先级 120，只处理身份缺失的原子创建、readback 和 reroute；
- 新增 `tracking_identity_intake` 路由包，使用 proposed IDs 和精确三路径写集；
- `SB-RESUME` 条件必需 WorkItem/TaskCard；
- 行为、workflow、节点表均断言行数、唯一 ID 数和期望集合数相等；
- 跨表验证 5 个写策略均有 workflow 可达，身份策略绑定明确节点。

## 状态独立回归

根因：测试把“当时某真实任务尚未 Review”和“当时活跃任务是 Task 14”误当成永久事实。

修复：

- S9/S10 使用 `GATE-MISSING-REVIEW-001` 自包含快照，不再轮换到另一个 pending 真实任务。
- current-state 测试从投影解析当前 active task，再与该任务最新 ledger 动态对账。

命令：

```bash
.venv/bin/python -m pytest tests/test_black_box_workflow_eval.py tests/test_project_memory_skill.py -q
```

结果：

```text
22 passed
```

## 规定组合与静态检查

命令：

```bash
.venv/bin/python -m pytest tests/test_full_project_session_workflow_routing.py tests/test_black_box_workflow_eval.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py -q
```

结果：

```text
56 passed
```

命令：

```bash
.venv/bin/ruff check tests/test_full_project_session_workflow_routing.py tests/test_black_box_workflow_eval.py tests/test_project_memory_skill.py
git diff --check -- <FLOW-TASK-015 scheme remediation scope>
```

结果：

```text
All checks passed!
diff check 无输出
```

## 未运行项

- 尚未同步 runtime Skills；候选复审批准前按 Gate 禁止执行。
- 尚未发布正式 `v1.2.0`；正式版本仍为 `v1.1.0`。
- 尚未运行发布后的全量测试与站点快照。

## 结论

首轮 C3/I4 的方案级整改和相邻状态独立修复已形成新鲜证据，当前仅可进入同一 Reviewer 复审。

## 正式实施证据（2026-07-27）

用户批准的冻结输入保持不变：

- 候选 SHA-256：`3d5f4cbabda86312da0603db5662175453d12dd5966c788301b0c79c2cb4992f`
- 原正式基线 SHA-256：`5769beb3478d528a0b0888328381173aa799e1e137925fc393bd98d97d3eb687`
- 发布后正式文档 SHA-256：`d330a3bc1e20cb160163e865aed83a2ddf4a4d395704880f31b3fb74e44d2d5d`
- 发布事务：`FLOW-TASK-015-RELEASE-TX-001`

正式文档已原位晋升为 `v1.2.0`，旧 `0.2.0 / 评审中` 重复控制块已删除；未在 `docs/` 新建第二份文档。
9 个 TaskCard allowlist runtime Skills 均新增最小 `v1.2.0 运行时路由合同`。

### Runtime Skill Red / Green

Red：

```text
uv run pytest tests/test_full_project_session_workflow_routing.py
1 failed, 7 passed
```

失败断言精确指向 runtime Skills 尚未暴露 v1.2.0 路由合同。同步后 Green：

```text
.venv/bin/python -m pytest tests/test_full_project_session_workflow_routing.py
8 passed
```

### 规定组合

```text
uv run pytest tests/test_full_project_session_workflow_routing.py \
  tests/test_black_box_workflow_eval.py tests/test_project_memory_skill.py \
  tests/test_writing_plans_skill.py tests/test_execution_workflow_skills.py \
  tests/test_review_workflow_skills.py \
  tests/test_verification_debugging_workflow_skills.py
57 passed

uv run ruff check tests/test_full_project_session_workflow_routing.py
All checks passed!
```

9 个修改 Skill 使用 `quick_validate.py` 验证，结果均为 `Skill is valid!`；任务范围 `git diff --check`
无输出。

### 补充回归与范围外遗留

补充运行 `.venv/bin/python -m pytest tests/test_doc_factory_restructure.py -q`，结果 `2 failed, 7 passed`：

- 一个旧断言仍要求已被 v1.2.0 发布事务删除的 pre-v1 重复版本历史，属于过期契约断言。
- 一个旧断言要求 `DOC-FACTORY-RESTRUCTURE-001` 全部 ledger actor 只有“用户授权代执行”，实际已有
  `AI_EXECUTOR`；该工作项不在 FLOW-TASK-015 允许修改范围。

这两项未计入规定组合通过数，也未在本任务越权修改。

## 正式实施结论

正式文档、9 个 runtime Skills、结构测试和 memory 投影已形成新鲜证据；当前状态为
`ready_for_independent_implementation_review`，尚未提交、push、创建 PR、merge 或部署。

## 独立实现 Review 整改

首轮独立实现 Review：`changes_requested / 76 / C0-I3-M0`。

整改 Red：

```text
.venv/bin/python -m pytest tests/test_full_project_session_workflow_routing.py -q
2 failed, 6 passed
```

失败点精确为旧自动人工 Gate 文案，以及 queue / tests summary 未与最新 ledger 对账。整改内容：

- 收窄两处旧 Review 规则，只有真实 `needs_human_decision` 才进入人工 Gate。
- 正式/候选四张核心表逐表一致；禁止旧冲突文案。
- runtime Skill 字段、policy 和 workflow 只在 v1.2.0 区块内验证，并核对 16 个精确行为映射。
- implementation queue 与 FLOW-TASK-015 最新 ledger status 动态对账；tests summary 同步当前 57-pass。

整改后正式文档 SHA-256：
`739a9920c9956b02af0d6e8498b706bd0e4fb778a71d21e0f3e7ae5c5f72abd7`；
结构测试 SHA-256：
`acad1e2962bc2b7b7cd98dbb5c82f210f13039d6e9d01dcd72916fcc3ac6b88c`。

整改 Green：

```text
定向：8 passed
规定组合：57 passed
Ruff：All checks passed!
Skill validator：9 / 9 valid
ledger JSONL：valid
diff check：无输出
```

当前可进入同一 Reviewer 实现复审；未执行 Git 写动作或远端动作。
