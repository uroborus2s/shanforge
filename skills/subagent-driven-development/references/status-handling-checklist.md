# Status Handling Checklist

用于控制器处理 worker 实现者返回状态；本 skill 只回写 `status` 与 `needs`，后续 Skill 由流程控制器决定。

## DONE

- 确认实现内容、真实测试结果和文件清单存在。
- 低、中风险任务继续当前批次，不生成逐任务 review input。
- 高风险专项或批次末才写 `ready_for_review` 和 `needs: review`。

## DONE_WITH_CONCERNS

- 先读 concerns。
- 如果 concern 涉及正确性、范围、测试或架构，先处理。
- 如果只是非阻塞观察，保留在批次汇总中并继续。
- 只有高风险 concern 才提前生成专项 review input。

## NEEDS_CONTEXT

- 补充最小必要上下文。
- 不散读整仓。
- 重新派发同一任务。
- ledger 记录 context supplied。

## BLOCKED

判断 blocker 类型：

- 上下文不足：补充上下文。
- 任务过大：拆小任务。
- 模型能力不足：保持原 `execution_model` 并交还主会话；由主会话补上下文、拆任务或改计划。
- 模型或工具不可用：`worker_unavailable` 或 `dispatch_failed`，交还主会话；不得换模型或由主会话代写。
- 计划错误：写入 `needs: plan_rewrite`，交还流程控制器。
- 需要用户决策：停止并问用户。

连续三次同类 blocker 后，不得继续空转。

## 已有 review feedback

- 本 skill 不接收 reviewer 结论来推进状态。
- 若输入包中已经包含 review feedback，只能按反馈修复实现并重跑受影响测试。
- 只有 Critical、Important 或高风险路径变化才更新集中 review input 并复审受影响范围。

本 skill 不批准任务；普通整改继续批次，高风险或批次候选才重新写成 `ready_for_review`。
