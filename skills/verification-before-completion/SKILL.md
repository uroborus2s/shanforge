---
name: verification-before-completion
description: 准备声明完成、修复、通过、可提交、可开 PR 或进入下一阶段前使用；要求先运行新鲜完整验证命令，读取输出和 exit code，再写完成声明。
---

# 完成前验证

本 skill 用于阻止没有证据的完成声明。核心规则很简单：没有新鲜验证证据，不得声明完成。

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
10. 更新 ledger，输出 `status` 与 `needs`。

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
- outputs:
  - <evidence path>
- evidence:
  - <command and output summary>
- ledger_event: <event id>
- needs:
  - none | rerun | verification_plan | human_confirmation
```
