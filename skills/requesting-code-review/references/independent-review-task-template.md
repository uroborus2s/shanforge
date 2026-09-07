# Independent Review Task

用于真实独立 reviewer 执行 review。目标是隔离实现者和裁判。

同线程作者自检不能使用本模板伪装成独立评审。同线程只能输出 `review_status=self_check_passed`，并把 `next_gate_status` 写成 `needs_independent_review`。

## Dispatch

```markdown
你是独立 reviewer。

不要读取实现者会话历史。
重新读取输入包。

## Inputs

- Work item：
- Review type：
- Requirements：
- task brief：
- implementer report：
- verification evidence：
- diff package：
- relevant architecture constraints：
- candidate_fingerprint：<工作树内容指纹或 commit；工作树不得只写 HEAD>
- requirements_or_standard_version：
- 已检查范围：
- 未检查范围：

## Job

1. 核对需求符合度。
2. 核对架构和质量。
3. 核对测试证据。
4. 核对文档与 memory 同步。
5. 先写 reviewer 独立性元数据。
6. 按 rubric 给出范围结论。
7. 输出 approved、changes_requested、needs_independent_review 或 self_check_passed。
8. 如果 approved，默认写 return_to_orchestrator；只有输入包已声明真实人工 Gate 且写明原因时，才写 pending_human_confirmation。
```

## Output

写入 `.factory/workitems/<WORKITEM-ID>/reviews/<review-name>.md`。

reviewer 不能把任务标记为 `done`。

```markdown
# Independent Review

- Work item:
- reviewer_type: independent_subagent | external_human | github_review | same_thread
- reviewer_id:
- reviewer_independence_evidence:
- review_status: approved | changes_requested | self_check_passed
- next_gate_status: return_to_orchestrator | pending_human_confirmation | needs_independent_review | changes_requested
- scope_conclusion: 本范围通过 | 需整改 | 证据不足

## Findings

### Critical
- Finding ID: <stable id>; status: open | fixed | accepted | not_reproduced; 证据: <path/command>; [file:line] <issue>

### Important
- Finding ID: <stable id>; status: open | fixed | accepted | not_reproduced; 证据: <path/command>; [file:line] <issue>

### Minor
- Finding ID: <stable id>; status: open | fixed | accepted | not_reproduced; 证据: <path/command>; [file:line] <issue>

## Verification

- <command>: <real result>

## 复审历史

- Finding ID: <stable id>; status: <current status>; 证据: <new evidence>; 差异原因: <relative to prior review>

## Gate

return_to_orchestrator | pending_human_confirmation | needs_independent_review | changes_requested
```

## 独立性门

- `same_thread` 只能写 `self_check_passed`。
- 没有 `reviewer_type`、`reviewer_id` 和 `reviewer_independence_evidence` 时，`next_gate_status` 必须写 `needs_independent_review`。
- `needs_independent_review` 不是 review 通过结论。
- 没有 reviewer 独立性证据时，不得写 `approved` 或 `pending_human_confirmation`。
- `approved` 默认返回 `return_to_orchestrator`；只有明确的产品决策、风险接受、范围扩大、破坏性/外部动作或治理 Gate 才进入人工确认。
