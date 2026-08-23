---
name: release-deployment
description: 发布、部署、回滚和生产观察工作流。用于已有精确候选和最终测试报告，需要核对生产授权、执行项目现有部署入口、健康检查、关键冒烟、观察或回滚，并输出最小发布回执时。
---

# 发布与部署

## 职责

只闭合一次发布事务：核对候选与授权，调用项目已有部署 / 回滚入口，验证并记录结果。

不创建部署平台，不发明脚本，不管理凭证，不代替测试、代码评审或本地提交。

## v1.3.0 运行时路由合同

| behavior_id | workflow_id | write_policy |
|---|---|---|
| `SB-RELEASE` | `release-workflow` | `state_or_gate_write` |

路由输入必须包含 `work_item_id`、`task_card_id`、精确 `allowed_paths`、`forbidden_actions`、`current_gate` 和
`write_policy`。结果只回写 `status`、`outputs`、`evidence`、`ledger_event`、`gate` 和本地 `needs`；项目级下一动作交还 `using-shanforge` 决定。

## 进入条件

- 精确候选：不可变版本、镜像 digest 或提交 SHA。
- 最终测试报告：必需发布测试已通过，残余风险已登记。
- 环境别名、部署入口、健康检查、关键冒烟和回滚入口均来自项目事实。
- 生产部署或回滚有本次动作的显式人工授权。

任一条件缺失时返回 `blocked`，不得用口头版本、旧测试结果或推测的命令继续。

## 工作流

1. 回读候选、最终测试报告、环境别名和授权，确认四者指向同一发布事务。
2. 读取项目已有运行手册或 CI/CD 入口；只执行已登记命令。命令会改变外部或生产状态时，在真正执行前再次核对授权。
3. 记录开始时间、操作者、候选和脱敏后的命令 / 流水线 receipt。
4. 部署完成后执行已有健康检查和关键冒烟，再按项目规定观察指标与日志。
5. 检查失败或超过回滚阈值时停止扩散，并仅在已有回滚入口和授权下回滚；回滚后重复健康检查与冒烟。
6. 输出一个最小发布回执，不复制测试案例、完整日志或凭证。

## 发布回执

```text
status: released | rolled_back | blocked
candidate_ref: <immutable ref>
environment: <alias>
authorization_ref: <ref>
deployment_receipt: <pipeline/run ref>
health: passed | failed | not_run
smoke: passed | failed | not_run
observation: <window and summary>
rollback_receipt: <ref or none>
residual_risks: <items or none>
evidence: <paths or refs>
```

环境只写别名。不得在 Skill 输出、报告或 ledger 中保存完整内部 URL、IP、端口、账号、密码、令牌、DSN、个人信息或原始敏感日志。

## 停止规则

- 授权、候选、报告、部署入口或回滚入口不明确：`blocked`。
- 部署失败且未授权回滚：`blocked`，报告当前外部状态并等待决定。
- 回滚成功：`rolled_back`；不得写成发布成功。
- 健康、冒烟和观察均满足项目阈值：`released`。

Skill 完成时只返回回执，不决定下一步 Skill，不自动 push、merge、提交或再次发布。

发布回执是本 skill 的专业输出；项目化执行所需的任务身份、`needs` 和 ledger 事件由共享回写契约补齐，不复制进回执。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
