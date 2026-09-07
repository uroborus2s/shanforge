# 工作 Skill 回写契约

本文件只定义项目化执行中的结果交接边界，不是 dispatcher、registry、runtime manager 或中心脚本。工作 Skill 保留自己的专业流程、状态枚举、输出格式、失败语义和人工决策边界；`using-shanforge` 只负责在这些事实之上生成项目级状态。

## 工作 Skill 本职结果包

工作 Skill 在已授权范围内连续完成本职动作、验证和执行事实回写，不在内部检查点要求用户“继续”。返回内容以各 Skill 的既有专业契约为准，项目化交接时至少让总控能识别：

```text
- work_item: <WORKITEM-ID>
- task_id: <TASK-ID or none>
- task_type: <formal task type>
- skill: <executor skill name>
- status: <该 Skill 的既有本地状态>
- outputs: <该 Skill 的既有输出>
- evidence: <验证或执行证据>
- ledger_event: <event id or path>
- needs: <该 Skill 的既有本地 needs>
- human_summary: <面向用户的本职事实摘要>
- progress_delta: <本轮已完成、开始、阻塞或未改变的本职事实；按适用性提供>
- verification_summary: <本轮验证范围、结果和未运行项；按适用性提供>
- defect_summary: <已知缺陷现象、归因和影响；按适用性提供>
- technical_assessment_summary: <需求依据（目标、验收、约束）、现象（实际、期望、触发、证据；静态审查可注明）、代码证据（真实 file、symbol、控制流或数据流）、因果链（代码行为→现象→需求影响；区分直接原因、根源原因和未知）、影响与满足度结论、建议修改位置与验证方法；按适用性提供>
- release_summary: <发布候选、环境、回执与健康/冒烟结果；仅发布工作按适用性提供>
- code_shape_check: passed | failed | not_applicable
- change_locations: <按适用性提供；每项提供 file、symbol、change、reason、verification>
```

`task_id/task_type 表示正式任务身份`，`skill 表示执行者身份`；二者不是替代关系。不得统一或改写工作 Skill 的既有专业输出，也不得为了共享本合同而收窄其 `status`、`outputs`、`evidence`、`needs`、真实 blocker 或人工确认语义。

`human_summary` 是可直接翻译的本职结论；其余三项按适用性提供，缺失时总控不得猜测。工作 Skill 不得推断 WBS 分母、产品功能完成度或项目完成层级；项目完成层级仍由 `using-shanforge` 结合项目事实决定，总体事实只由 `using-shanforge` 生成。

`code_shape_check` 只有本轮没有修改代码时才可 `not_applicable`；凡修改源码或测试代码不得用 N/A，必须回写 `passed` 或 `failed`。

## 项目化回复合并

上述局部结果包是工作 Skill 的专业增量，不是项目化回复本身。项目化回复必须合并 human_summary、`progress_delta`、`verification_summary`、`defect_summary`、`change_locations` 与项目状态信封；技术评估工作再按适用性合并 `technical_assessment_summary`，发布工作再按适用性合并 `release_summary`。按事实组织成面向用户的处理结果、验证与风险、下一步。字段不适用或缺事实时明确说明或省略该局部字段，缺事实不得猜；项目状态信封仍只由 `using-shanforge` 生成。

技术评估必须让用户沿“需求 → 现象 → 代码 → 原因 → 影响 → 建议”理解问题。不得用“架构不合理、耦合高、建议重构”等抽象判断，不得用评分、内部 ID、路径或术语清单替代解释；未知原因须明确为未知并说明已有证据。评估阶段的建议不得把建议表述为已修复。

## evidence 分层

普通低、中风险 TaskCard 使用可回读的新鲜命令回执，不强制单独落盘。
批次、里程碑、高风险专项，以及任何阶段、项目或关闭声明必须落盘 evidence。
落盘 evidence 证明对应声明，不得用普通 TaskCard 的局部命令回执推导批次、阶段或项目完成。

## 修复位置与代码形状

Bug、修复或代码写入结果的 `change_locations` 必须逐项使用以下结构：

```text
- file: <实际修改文件>
  symbol: <实际函数、方法或符号；没有函数边界时写模块、配置项或文档章节>
  change: <具体改动>
  reason: <为什么需要该改动>
  verification: <验证命令、测试或检查结果>
```

每个 `source_or_test_write` 授权包还必须明确：禁止函数或方法体内定义命名函数、局部 helper 或方法；禁止抽取只有一个调用点且无独立职责的公共 helper。正常函数调用组合不是嵌套函数定义。框架强制入口、接口实现、回调注册或资源生命周期边界仅在承担真实职责时例外，不得包装一次转发。实际实现结果以 `code_shape_check: passed | failed` 回写两条禁令的检查结论。

## 测试类 verification_summary

测试、验证或回归工作必须用下列结构提供 `verification_summary`；没有完整测试基线时，相应计数写“无法计算”，不得猜测。`failed_or_error_cases` 为每个失败或错误用例提供 `TEST-ID`、关联功能、可观察现象和当前归因；根因未知写“待调查”。

```text
- total: <number>
- passed: <number>
- failed: <number>
- error: <number>
- blocked: <number>
- skipped: <number>
- not_run: <number>
- cancelled: <number>
- covered_scope: <本轮覆盖范围>
- uncovered_scope: <未覆盖范围>
- failed_or_error_cases: <TEST-ID、关联功能、现象、归因；无则 none>
```

非测试工作可以使用通用 verification_summary，概述验证范围、结果和未运行项。

工作 Skill 可以返回本地 `blocked`、`needs_user_input` 或 human-confirmation need，但不自行决定下一步 Skill、项目完成层级、项目是否停止、提交或正式发布。

## 项目状态信封

`using-shanforge` 接收本职结果包后，结合当前 work item ledger、review ledger、已授权范围和真实 Gate，统一生成：

```text
- project_completion: complete | incomplete | unknown
- overall_phase_and_current_activity: <总体阶段；当前活动>
- project_position: <第 N/TOTAL 步 / 阶段 / 当前任务>
- completion_level: none | task | stage | project
- stop_reason: none | blocker | human_gate
- scope_remaining: <已授权范围内剩余工作；没有则写“无”>
- approved_product_remaining: <完整批准产品范围内剩余；缺完整基线写“未知”>
- unknown_unverified_or_not_started: <未知、未验证与未开始项；没有则写“无”>
- scope_reconciliation: <基线定位/版本；checked | incomplete | not_checked；未映射或未知项>
- next_required_action: <唯一 `next_required_action`；没有则写“无”>
```

没有真实 blocker 或有效 human Gate 时，`stop_reason` 必须是 `none`；既有授权范围内仍有内部验证、评审、整改或收口动作时继续路由，不把内部 checkpoint 变成用户 Gate。

`scope_remaining` 只表示当前已授权批次，不能推导已批准产品的剩余或完成。总控先回答项目是否完成，再分别报告总体阶段与当前活动、已批准产品剩余和未知/未验证/未开始；缺完整基线明确“未知”，不得估算。

已知本批缺口可确定产品尚不能交付；缺完整产品基线时必须分开写“已知缺口”和“完整产品剩余未知”，不得以本批缺口替代完整产品剩余。进行中的 bug 修复属于当前进行中，不得列为未知/未验证与未开始。

`scope_reconciliation` 记录完整批准需求/变更的核对依据和结果；普通本批收口可为 `not_checked`，不因此阻塞连续执行，但必须列出基线定位/版本和未映射或未知项。用户可见时翻译为“已核对 | 核对不完整 | 尚未核对”；基线不存在不得写已核对，存在已知缺陷不得把全部状态写成未知。字段存在不等于已核对或已验收。

## 适用边界

- `project_workitem` 与 `tracked_task` 使用上述两段式交接。
- `direct_answer` 与 `lightweight_analysis` 只返回当前会话答案，不加载或输出项目状态信封，也不写 work item、ledger 或 memory。
- 真实人工决策、权限扩大、破坏性或外部动作，以及各工作 Skill 已定义的用户选择仍按原边界停止。
