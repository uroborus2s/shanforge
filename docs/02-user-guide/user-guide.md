# 使用指南

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-USER-GUIDE-001` |
| 正式版本 | `v1.3.0` |
| 来源候选 | `2026-08-08 用户阶段门控与闭环优化决策` |
| 发布事务 | `N/A（直接策略变更）` |
| 负责人 | `HUMAN_PRODUCT_ANALYST` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `PRD`、`workflow-execution-design` |
| 下游 | `prompt-templates` |

## 文档职责

- 允许保存：日常使用；会话交互；状态理解；常见问题。
- 禁止保存：内部实现；候选流程；会话全文。
- 主要读者：最终用户、项目协作者。

## 正式内容

这篇文档说明如何用当前的 `shanforge`。

## 1. 一句话理解

`shanforge` 不是 GUI，也不是命令大全。它是一套让 `Codex` / `Gemini CLI` 按软件工厂规则推进项目的 skills、文档和记忆体系。

你通常只做三件事：

1. 用自然语言说明项目路径、当前状态、目标和禁止事项。
2. 让 `using-shanforge` 判断当前流程位置。
3. 让对应 skill 完成需求、设计、计划、实现、评审、验证、提交或发布。

## 2. 使用前准备

进入仓库根目录后，确认这些目录存在：

- `skills/`
- `docs/`
- `.factory/memory/`

如果需要把仓内 skills 同步到本地宿主，可以执行：

```bash
uv run python scripts/sync-codex-skills
```

这只是同步工具，不是项目流程入口。

skill 自带的确定性脚本会随整个 skill 目录一起同步。目标项目不需要复制或调用
Shanforge 仓库源码。

UI 设计系统检索输出的是候选，不是已定稿视觉。例如：

```bash
python3 <skill-dir>/scripts/search.py "预约诊所 healthcare appointment calm" --design-system --platform web --surface persuade --locale zh-CN --stack react --json --persist -p care-console
```

`--json` 输出候选及未决项；`--persist` 只会在 `design-system/<project>/candidates/` 创建候选 JSON，不再生成或覆盖 `MASTER.md` 和页面正式文件。`dials` 只表达意图，不能替设计结论；`--domain` 与 `--design-system` 等冲突参数会报错。Flutter/React Native 等跨端栈需显式 `--platform`，不要假定单端。宿主若是仓内 skill 的 symlink 会自动读取最新内容；副本安装才按已有同步脚本实际支持范围操作，并在同步后回读，不假定存在单 skill 参数。

API 迁移：`generate_design_system` 保留原位置参数并返回 `str`，`output_format=json` 时为 JSON 字符串；`DesignSystemGenerator.generate` 返回新的 candidates dict，旧 `style`/`colors`/`typography` 最终字段不兼容。非 JSON 的 `--persist` 同时显示候选文本和实际创建路径，不再自动决定 `MASTER`。

新 UI 或整体重设计先确定平台、业务对象和关系如何组织页面，再用少量同内容、同视口的方向比较和真实截图核查收敛；已批准设计只继承扩展，局部修改不重做视觉。工具/操作页不等于后台模板，即使不需图片也要以信息层级、排版、密度和状态反馈服务任务。方向样板与正式美术资源职责不同；设计质量截图验收与实现还原验收也要分开。真实产品多端截图盲评必须另行运行，候选检索、静态检查或 AI 自评不能替代它。

## 3. 第一轮会话怎么说

推荐直接给 AI 这些信息：

```text
项目路径：[项目路径]
当前状态：[空目录 / 已有代码 / 已纳管项目 / 不确定]
本轮目标：[一句话目标]
禁止事项：[不要散读 docs / 不要直接编码 / 不要提交等]
完成后输出：[需要的结果]
```

AI 应该先走 `using-shanforge`，必要时用 `project-memory` 恢复上下文，再选择唯一下一步 skill。

## 4. 模型如何分工

当前 Codex 宿主能力按三层协作：`gpt-5.6-sol` 负责总体设计、风险和任务复杂度分级及最终路由；
`gpt-5.6-terra` 执行标准、复杂或中高风险的已授权任务；`gpt-5.6-luna` 只执行简单且低风险的已授权任务。
Terra/Luna 不能自行改级、扩范围或批准完成，出现范围、输入、风险、连续验证失败或人工 Gate 时交还 Sol。

真实子代理派发有两个互斥分支：`execution-workflow` 的已授权源码或测试写入是 worker，简单且低风险使用 Luna（low），其余使用 Terra（medium）；
`review-workflow` 的 `state_or_gate_write`、身份和范围完整、实现和验证已完成的独立只读 review 是 reviewer，固定 Terra（high）。
workflow/写策略与声明分支不匹配，或两个分支同时可命中时会失败关闭并交还 Sol；直接答复、设计、计划、非独立 review、Gate 和最终收口仍由 Sol 控制。
父会话每次都显式调用 `spawn_agent`，带上模型、推理强度和 `fork_turns="none"`，并保存成功工具回执；工具、模型或回执异常会失败关闭并交还 Sol，不会由 Sol 静默代写、换模型或代替 reviewer。

`.codex/config.toml` 和 `.codex/agents/*.toml` 是宿主配置层，不是每次派发的证明。真实绑定以父会话的显式派发参数和成功回执为准；
仓内无法读取或验证模型内部身份。

这些名称描述当前项目可见的当前 Codex 宿主能力，不代表公开 API 型号、价格或可用性承诺。

## 5. 常见场景

| 场景 | 正确入口 |
|---|---|
| 不知道下一步 | 让 `using-shanforge` 判断当前阶段和阻塞项 |
| 需要恢复上下文 | 使用 `project-memory` |
| 需要澄清想法或范围 | 使用 `brainstorming` |
| 需要需求或验收标准 | 使用 `requirements-engineering` |
| 需要文档体系或技术文档 | 使用 `document-templates` |
| 已有需求，需要计划 | 使用 `writing-plans` |
| 已有计划，需要执行 | 使用 `subagent-driven-development` 或 `executing-plans` |
| 出现 Bug 或测试失败 | 使用 `systematic-debugging` 复现、归因和分级；只有高风险等待双确认 |
| 需要评审 | 使用 `requesting-code-review` |
| 需要处理评审意见 | 使用 `receiving-code-review` |
| 准备声明完成 | 使用 `verification-before-completion` |
| 用户明确要求提交 | 使用 `gitcommitzh` |
| 最终候选测试通过并准备部署 | 使用 `release-deployment`，生产动作必须显式授权 |

## 6. 完成标准

一次任务不能只靠“代码改了”算完成。至少要有：

- 代码、文档、测试和 `.factory/memory/` 同步。
- 新鲜验证命令和结果。
- 需要评审时，独立 review 结论。
- 需要人工确认时，等待用户明确通过。

## 7. 不要做什么

- 不要把 skill 当命令目录。
- 不要把旧中心命令当流程主控。
- 不要默认全文读取阶段文档。
- 不要把“准备执行”写成“已经完成”。
- 不要在未确认范围时提交整个工作区。

## 8. 如何阅读开发、测试和修复状态

本节是 `HUMAN-RESPONSE-CONTRACT-002` 与 `HUMAN-RESPONSE-CONTRACT-003` 的候选修订，待正式批准/发布后才会纳入正式版本。

开发或计划更新先回答项目是否完成，再说明总体阶段与当前活动、本批剩余、已批准产品剩余、未知/未验证与未开始、阻塞和唯一下一动作。产品进度按已批准 WBS 和任务卡展示为“已完成、进行中、未开始、阻塞”；已完成项应附可观察结果和验证状态。缺少完整 WBS、批准总数或完整基线时，状态会写“未知”或“无法计算”，不会猜测百分比。本批剩余不等于已批准产品剩余；评审、系统治理和提交可以单列为交付状态，但不等于产品功能完成。

测试更新会说明本轮覆盖和未覆盖范围，以及总数、通过、失败、错误、阻塞、跳过、未运行和取消数量。每个失败或错误应说明关联功能、可观察现象和当前原因；根因还未确认时会明确写“待调查”。局部测试通过只表示已覆盖的部分通过，不表示整个项目通过。

Bug 或修复更新会说明问题现象、影响、复现、已知原因、风险、修复状态和回归验证，并逐项列出修改文件、实际函数/方法/符号（没有函数边界时写模块、配置项或文档章节）、具体改动、改动原因和验证结果。代码写入任务禁止在函数或方法体内定义局部函数，也禁止为只有一个调用点且无独立职责的逻辑抽取公共 helper；正常函数调用组合不属于嵌套函数定义。框架强制入口、接口实现、回调注册或资源生命周期边界只能承担真实职责，不能包装一次转发。任务卡会按事实分流：当前未验收任务内、同一根因且仍在原范围内的问题直接整改；已交付功能的回归、跨任务问题或需要独立排期的问题创建单独的 Bug TaskCard；测试预期、夹具、脚本、配置或环境问题则交给对应 owner 处理，不作为产品 Bug 新建任务卡。

内部 ID、Gate、路径和命令只作为末尾技术记录，帮助追溯，不代替上述状态说明。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.3.0` | 2026-08-23 | 增加 Sol 控制分级和 Terra/Luna 受控执行说明 | `AI_EXECUTOR` | `集中质量门` | `uroborus` |
| `v1.2.0` | 2026-08-08 | 增加 Bug 风险分流、最终候选测试和发布部署入口 | `AI_EXECUTOR` | `集中质量门` | `uroborus` |
| `v1.1.0` | 2026-07-28 | 明确 skill 自带脚本并取消目标项目源码依赖 | `uroborus` | `uroborus` | `uroborus` |
| `v1.0.0` | 2026-07-18 | 基于 `TASK-DESIGN-001-R019` 正式落档 | `uroborus` | `uroborus` | `uroborus` |

候选修订（2026-08-24）：真实模型派发、父回执和失败关闭合同待 `MODEL-DISPATCH-RUNTIME-001` 独立评审；未正式发布。

候选修订（2026-09-07）：项目总体与本批状态分离、需求追踪和证据化评审合同待 `FLOW-STATUS-REVIEW-001` 评审；未正式发布。
