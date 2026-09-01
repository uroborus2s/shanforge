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
- 返回 `status`、`outputs`、`evidence`、`ledger_event`、`gate` 和本地 `needs`；只接受新鲜命令、
  exit code 和当前输出，Verification 不替代 Review、项目状态判断或人工批准。

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
- 由总控给出的待验证声明、范围和适用验收条件。

## 输出

- 低、中风险任务：当前状态包中的新鲜命令、exit code 和结果摘要，不强制落盘文件。
- 批次 / 里程碑 / 项目或高风险专项：`.factory/workitems/<WORKITEM-ID>/evidence/` 和必要的
  `.factory/workitems/<WORKITEM-ID>/reports/`。
- ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

## 含义保留清单

- 证据先于声明。
- 不能用旧结果、推测、信心或子 agent 报告代替验证。
- 每个完成声明都必须先识别能证明声明的命令；只有批次、里程碑、项目或高风险声明需要持久化 evidence。
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
9. 低、中风险任务把命令、exit code 和结果写入状态包；批次、里程碑、项目或高风险专项才按
   [completion-evidence-template.md](references/completion-evidence-template.md) 写一份 evidence。
10. 明确本次证据实际覆盖的声明和未验证项，不把局部通过外推为项目完成。
11. 更新 ledger，输出验证 `status`、证据与本地 `needs`，交还 `using-shanforge` 生成项目状态。

## 项目级测试治理

- 案例运行结果：`passed | failed | error | blocked | skipped | not_run | cancelled`。
- 批次验证结论：`passed | partial | failed | blocked`。`partial` 只表示批次仍有未运行项或验证缺口，不是单个案例结果。

### 本轮测试事实

有正式测试时，以正式测试计划、测试案例目录和本轮测试报告为范围；三者缺失或不完整时明确写“无法计算”，不得估算总数或把局部结果外推。

基线缺失或不完整时，汇总字段写“无法计算（不可估算）”，范围字段说明缺失的测试计划、案例目录或本轮报告；不得以已运行命令数代替测试基线。

- 汇总固定为 `total | passed | failed | error | blocked | skipped | not_run | cancelled`；零项也要如实列出。
- 每个 `failed` 或 `error` 项列出测试 ID、关联功能、可观察现象和当前归因；尚未证实时写“根因待调查”，不猜测产品根因。
- 同时说明本轮覆盖范围和未覆盖范围。局部通过不得表述为项目通过。
- 本 skill 只报告测试事实；缺陷根因、修复状态和 TaskCard 决策由事实 owner 的调试流程提供。

验证计划必须按变更影响选择测试层级，不能只列当前最容易运行的测试：

| 层级 | 适用场景 | 稳定编号 |
|---|---|---|
| 单元 / 契约 | 局部规则、数据结构、接口契约 | `TEST-UNIT-*` / `TEST-CONTRACT-*` |
| 整体黑盒 | 用户流程、CLI 或跨层闭环 | `TEST-BB-*` |
| UI | 页面结构、交互、可访问性和响应式 | `TEST-UI-*` |
| API | schema、状态码、鉴权和兼容性 | `TEST-API-*` |
| 发布回归 | 影响正式交付、公共契约或发布门 | `TEST-REL-*` |

- 批次、发布或长期维护的正式测试建立 `需求 -> 任务 -> 测试 -> 证据` 追踪并使用稳定 `TEST-*` ID；
  普通任务的定向单测不为追踪而新增测试定义或证据文件。
- 发布测试必须绑定不可变候选。首个候选运行完整必需发布测试并登记缺陷；每个修复只运行原失败案例、根因案例和
  受影响调用方 / 契约；阻断缺陷关闭后冻结最终候选，再运行一次完整必需发布测试。V4 或项目明确要求时才运行字面全仓测试。
- 只列按风险适用的测试层级；不得为了模板补 `N/A`，也不得把未运行误报成通过。
- 整体黑盒、UI、API 或发布回归需要启动进程时，evidence 必须记录启动命令、端口、健康检查和关闭方式。
- 静态 HTML、进程内 API 或纯 schema 检查没有独立服务时，对端口和关闭方式写 `N/A`，同时写明静态文件路径或进程内测试入口。
- 环境字段缺失时只能输出 `needs: verification_plan`，不能开始声称项目级验证完成。
- 案例目录、运行结果和聚合报告分离。最终报告只保留候选、环境别名、汇总、失败 / 阻塞 / 跳过、缺陷、残余风险和证据引用；
  不复制请求 body、预期断言或完整日志，不记录完整内部 URL、IP、端口、凭证、令牌、DSN 或个人信息。
- 变更包含人类可读案例目录或 WorkItem 测试报告时，必须运行项目登记的文档校验入口；使用 `document-templates` 默认资产时，将 `<skill-dir>` 替换为该 Skill 的实际安装目录并运行 `uv run python <skill-dir>/scripts/validate_test_documents.py`，验证自动化节点、七态计数、批次结论和 GO/NO-GO 一致性。

## 声明范围核对

- 任务验证通过不等于阶段或项目完成；只报告证据直接覆盖的声明和未验证项。
- 阶段或项目级声明必须收到对应全部任务、review、verification 和 Gate 事实后再验证，不能从单个 task 的 `passed` 推导。
- 项目位置、完成层级、停止原因和剩余工作由 `using-shanforge` 结合 ledger 统一生成，本 skill 不在结果包中重复维护。

## 通过标准

- 验证命令是本轮新鲜运行。
- 输出能直接证明声明。
- exit code 与失败数量支持结论。
- 未运行项、偏离原因和风险已写明。
- 批次、里程碑、项目或高风险声明的 evidence 文件已落盘；普通任务已有可回读命令结果。

## 关闭 gate

- 关闭前必须检查新鲜命令、exit code、输出和 evidence。
- 无批次级 evidence 不能关闭批次、阶段或项目；普通任务 checkpoint 不触发关闭。
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
- outputs:
  - <evidence path>
- evidence:
  - <command and output summary>
- total: <integer | 无法计算>
- passed: <integer | 无法计算>
- failed: <integer | 无法计算>
- error: <integer | 无法计算>
- blocked: <integer | 无法计算>
- skipped: <integer | 无法计算>
- not_run: <integer | 无法计算>
- cancelled: <integer | 无法计算>
- covered_scope: <本轮覆盖的功能、路径或测试层级>
- uncovered_scope: <未覆盖范围，或基线缺失说明>
- failed_or_error_cases:
  - test_id: <TEST-*>
    feature: <关联功能>
    symptom: <可观察现象>
    attribution: <当前归因 | 根因待调查>
- ledger_event: <event id>
- needs:
  - none | rerun | verification_plan | human_confirmation
```
