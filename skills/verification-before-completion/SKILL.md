---
name: verification-before-completion
description: 准备声明完成、修复、通过、可提交、可开 PR 或进入下一阶段前使用；要求先运行新鲜完整验证命令，读取输出和 exit code，再写完成声明。
---

# 完成前验证

本 skill 用于阻止没有证据的完成声明。核心规则很简单：没有新鲜验证证据，不得声明完成。

## v1.2.0 运行时路由合同

- `SB-TEST` 进入 `testing-workflow`，`write_policy: source_or_test_write`；`SB-VERIFY` 进入
  `verification-workflow`，`write_policy: state_or_gate_write`。
- 写测试、验证状态或 evidence 前，route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确
  `allowed_paths`、`forbidden_actions`、`current_gate`、`write_policy`。
- 返回 `status`、`outputs`、`evidence`、`ledger_event`、`gate`、`next_required_action`；只接受新鲜命令、
  exit code 和当前输出，Verification 不替代 Review 或人工批准。

## 触发

- 准备说“完成”“已修复”“通过”“可以提交”“可以进入下一阶段”。
- 准备关闭 work item、提交、开 PR 或交付给用户。
- 需要证明测试、lint、build、需求或 bug 修复已经成立。
- 收到子 agent 或外部工具的成功报告后，需要独立核实。

## 输入

- 当前 work item id。
- 需要验证的声明。
- 相关 plan、task brief、review、diff 或 bug report。
- 可证明该声明的命令、检查清单或人工验收项。
- 当前 `project_position`、声明的完成层级和授权范围内剩余工作。

## 输出

- evidence：`.factory/workitems/<WORKITEM-ID>/evidence/`
- verification report：`.factory/workitems/<WORKITEM-ID>/reports/`
- ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

## 含义保留清单

- 证据先于声明。
- 不能用旧结果、推测、信心或子 agent 报告代替验证。
- 每个完成声明都必须先识别能证明声明的命令。
- 必须运行完整命令。
- 必须读取完整输出。
- 必须检查 exit code。
- 必须统计失败数量、跳过项和未运行项。
- 需求满足不能只靠测试通过，必须逐项核对。
- 回归测试必须证明 Red-Green，而不是只看最后一次通过。

## 默认流程

1. 写出要验证的声明。
2. 先识别能证明声明的命令、检查项或证据。
3. 运行完整命令；不要只跑局部替代命令，除非记录偏离原因。
4. 读取完整输出。
5. 检查 exit code。
6. 统计失败数量、错误数量、跳过数量和未运行项。
7. 对照 [completion-claim-checklist.md](references/completion-claim-checklist.md) 判断能否声明成功。
8. 对 Red-Green 场景按 [red-green-verification-template.md](references/red-green-verification-template.md) 记录。
9. 按 [completion-evidence-template.md](references/completion-evidence-template.md) 写 evidence。
10. 判断完成层级，明确当前声明只覆盖 task、stage 还是 project，并列出 `scope_remaining`。
11. 更新 ledger，输出 `status`、`project_position`、`completion_level`、`stop_reason` 与 `needs`。

## 项目级测试治理

验证计划必须按变更影响选择测试层级，不能只列当前最容易运行的测试：

| 层级 | 适用场景 | 稳定编号 |
|---|---|---|
| 单元 / 契约 | 局部规则、数据结构、接口契约 | `TEST-UNIT-*` / `TEST-CONTRACT-*` |
| 整体黑盒 | 用户流程、CLI 或跨层闭环 | `TEST-BB-*` |
| UI | 页面结构、交互、可访问性和响应式 | `TEST-UI-*` |
| API | schema、状态码、鉴权和兼容性 | `TEST-API-*` |
| 发布回归 | 影响正式交付、公共契约或发布门 | `TEST-REL-*` |

- 每个正式测试必须建立 `需求 -> 任务 -> 测试 -> 证据` 追踪，使用稳定 `TEST-*` ID；一次运行日志只作为 evidence，不产生新的测试定义。
- 改动不涉及某一层级时写 `N/A` 并说明不适用原因；不得省略层级后把“未运行”误报成“通过”。
- 整体黑盒、UI、API 或发布回归需要启动进程时，evidence 必须记录启动命令、端口、健康检查和关闭方式。
- 静态 HTML、进程内 API 或纯 schema 检查没有独立服务时，对端口和关闭方式写 `N/A`，同时写明静态文件路径或进程内测试入口。
- 环境字段缺失时只能输出 `needs: verification_plan`，不能开始声称项目级验证完成。

## 完成层级

- `completion_level: task | stage | project` 必须与实际证据范围一致。
- 任务完成不等于项目完成。任务验证通过时，还要说明所属阶段和项目是否仍有剩余工作。
- 阶段完成必须有该阶段全部任务、review、verification 和 Gate 状态证据。
- 项目完成必须证明所有项目步骤和正式交付要求均已满足，不能从单个 task 的 `passed` 推导。
- `scope_remaining` 列出当前授权范围内尚未完成的动作；若为空，写 `none`。
- `project_position` 写项目第几步、总步数、阶段和当前任务。
- `stop_reason` 只能是 `none`、真实 blocker 或真实人工 Gate，不能把普通 review/verification checkpoint 写成停止原因。

## 通过标准

- 验证命令是本轮新鲜运行。
- 输出能直接证明声明。
- exit code 与失败数量支持结论。
- 未运行项、偏离原因和风险已写明。
- evidence 文件已落盘。

## 关闭 gate

- 关闭前必须检查新鲜命令、exit code、输出和 evidence。
- 无 evidence 不能关闭。
- review 不能替代 verification。
- verification 不能替代 human confirmation。

## 失败处理

- 如果验证失败，只能报告真实状态。
- 如果验证不完整，只能报告 `partial`。
- 如果不知道该跑什么命令，输出 `needs: verification_plan`。
- 如果工具不可用，记录不可用原因、替代检查和残余风险。

## 禁止

- 禁止用 “should / probably / seems” 暗示成功。
- 禁止把上一次验证当作新鲜证据。
- 禁止只看部分输出就声明通过。
- 禁止把 lint 通过当作 build 或测试通过。
- 禁止把子 agent 的成功报告当作验证。
- 禁止把未运行的命令写成已经通过。

## 状态包

```text
工作结果：
- work_item: <ID>
- skill: verification-before-completion
- status: passed | partial | failed | blocked
- project_position: <step / total / stage / task>
- completion_level: task | stage | project
- stop_reason: <none | blocker | human_gate>
- scope_remaining: <remaining work | none>
- outputs:
  - <evidence path>
- evidence:
  - <command and output summary>
- ledger_event: <event id>
- needs:
  - none | rerun | verification_plan | human_confirmation
```
