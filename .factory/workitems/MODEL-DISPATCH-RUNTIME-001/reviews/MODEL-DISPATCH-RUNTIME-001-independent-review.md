# Independent Review

- Work item: `MODEL-DISPATCH-RUNTIME-001`
- reviewer_type: `independent_subagent`
- reviewer_id: `/root/model_dispatch_terra_review`
- reviewer_independence_evidence: 未参与实现，只读取文件化输入、当前候选和只读命令结果。
- review_status: `changes_requested`
- next_gate_status: `changes_requested`
- author_self_check_score: `n/a`
- review_score: `68`
- human_confirmation_required: `false`
- gate_reason: `none`

## Findings

### Critical

- none

### Important

- `skills/using-shanforge/SKILL.md:165-168` 将所有 Review 规定为 `dispatch_required=false, dispatch_mode=direct`，但同一候选要求且实际记录了 Terra 独立 reviewer 的 `subagent/high` 派发。正式设计和用户指南也写“只有 source_or_test_write 才派发”。应明确“授权实现写入必须派发”与“独立只读 review 可派发”的两个分支。
- `.factory/workitems/MODEL-DISPATCH-RUNTIME-001/ledger.jsonl:1` 为 T01 记录 `write_policy=project_fact_write`，却同时记录 `dispatch_required=true`、`dispatch_mode=subagent`；这与“仅 source_or_test_write 派发”相冲突。T01 实际为 `.codex` 配置写入，需区分规划事件与任务执行写策略。
- 完整 task brief 合同未落地：T01、T02 没有 `write_policy` 和具体“验证命令”段落，而派发合同要求 message 含验证命令，执行 skill 也要求开始前具备必要命令。模板本身同样未持久化 `write_policy`；现有 6 项测试没有发现上述矛盾。

### Minor

- none

## Score

- 需求符合度: `20/30`
- 架构一致性: `13/20`
- 测试充分性: `10/20`
- 代码质量: `18/20`
- 文档与记忆同步: `7/10`

## Verification

- `env PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider`：`270 passed in 2.61s`，exit `0`。
- `uv run ruff check .`：`All checks passed!`，exit `0`。
- `git diff --check`：无输出，exit `0`。
- Python `tomllib`/JSONL 解析：`4 TOML and 45 JSONL parsed`，exit `0`。

## N/A acceptance

- UI/API/服务/E2E: `accepted`。本变更只有 Codex 配置、Skill/文档合同与治理测试；替代检查为 TOML/JSONL、完整 pytest、Ruff、diff 和文件化派发回执审查。

## Gate

`changes_requested`

---

# Incremental Independent Review — Iteration 2

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/model_dispatch_terra_review`
- reviewer_independence_evidence: 同一 Terra/high/read-only reviewer；未参与 T01–T03 实现，只复读文件化候选并运行只读验证。
- review_status: `changes_requested`
- next_gate_status: `changes_requested`
- review_score: `58`
- human_confirmation_required: `false`
- gate_reason: `none`

## Findings

### Critical

- none

### Important

- I1 仍未关闭：worker 条件没有同时限定 `workflow_id=execution-workflow`，与 reviewer 分支存在重叠；现有测试没有重叠反例。
- I3 仍未关闭：T03 缺独立、非占位的 `## 验证命令`，测试也未覆盖四张 brief 的验证命令和 `current_gate`。
- 跨 Skill 根因仍存在：worker Skill 的 status reference 仍直接指定相邻 review Skill。
- memory/ledger 投影回归失败：`current-state.md` 缺稳定 ledger 索引；最新 follow-up receipt 缺 `next_required_action`；`tasks.summary.md` 顶部仍指向旧 WorkItem。

### Minor

- none

## Verification

- 模型路由定向：`9 passed`，exit `0`。
- 完整 pytest：`271 passed, 2 failed`，exit `1`。
- Ruff、TOML/JSON/JSONL 解析和 diff check 通过。

## Gate

`changes_requested`

---

# Independent Review — Iteration 3

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/model_dispatch_terra_review`
- reviewer_independence_evidence: 同一 Terra/high/read-only reviewer；未参与实现或整改，只读取文件化候选、ledger、memory、diff 并运行只读验证。
- review_status: `approved`
- next_gate_status: `return_to_orchestrator`
- review_score: `96`
- human_confirmation_required: `false`
- gate_reason: `none`

## Findings

- Critical: `0`
- Important: `0`
- Minor: `0`

## Closure

- I1: `closed` — 唯一严格派发表以 workflow/write policy 联合条件区分 worker/reviewer，错配或重叠失败关闭。
- I2: `closed` — plan、worker、reviewer 和 follow-up/done 事件语义一致，最新事件有下一动作。
- I3: `closed` — 四张 brief 字段与非占位验证命令完整，9 项治理测试覆盖合同和回执。
- 跨 Skill 边界: `closed`。
- Memory/ledger 投影: `closed`。

## Verification

- 模型路由 `9 passed`、完整 pytest `273 passed`、Ruff、TOML/JSON/JSONL 和 diff check 全部 exit `0`。
- UI/API/服务/E2E: `N/A accepted`；本变更无对应运行面。

## Gate

`return_to_orchestrator`
