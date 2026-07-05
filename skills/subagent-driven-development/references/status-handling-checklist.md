# Status Handling Checklist

用于控制器处理实现者返回状态。

## DONE

- 确认 evidence 和 implementer report 存在。
- 生成 review input package。
- ledger 写 `ready_for_review`。
- 状态包写 `needs: review`。

## DONE_WITH_CONCERNS

- 先读 concerns。
- 如果 concern 涉及正确性、范围、测试或架构，先处理。
- 如果只是非阻塞观察，记录到 review input package。
- ledger 写 `ready_for_review`。
- 状态包写 `needs: review`。

## NEEDS_CONTEXT

- 补充最小必要上下文。
- 不散读整仓。
- 重新派发同一任务。
- ledger 记录 context supplied。

## BLOCKED

判断 blocker 类型：

- 上下文不足：补充上下文。
- 任务过大：拆小任务。
- 模型能力不足：换更强执行者或改为主线程执行。
- 计划错误：写入 `needs: plan_rewrite`，交还 `using-shanforge` 流程总控。
- 需要用户决策：停止并问用户。

连续三次同类 blocker 后，不得继续空转。

## 已有 review feedback

- 本 skill 不接收 reviewer 结论来推进状态。
- 若输入包中已经包含 review feedback，只能按反馈修复实现或补 evidence。
- 修复后重新生成 review input package。
- ledger 重新写 `ready_for_review`。
- 状态包写 `needs: review`。

本 skill 不批准任务，只把修复后的状态重新写成 `ready_for_review`。
