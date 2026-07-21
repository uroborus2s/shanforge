---
name: skill-creator
description: 创建、修改、压缩、翻译、评审和评估 Codex skill；当用户要求新建 skill、改写现有 skill、提高触发准确性、做 skill 评估或 benchmark 时使用。
---

# Skill Creator

用于创建和改写 skill。默认目标是：主入口短、中文清楚、触发边界准、输出契约完整。

## 适用边界

适用于：

- 新建 `SKILL.md`。
- 修改、压缩、翻译或评审已有 skill。
- 为 skill 补测试、schema、rubric、reference 或 helper code。
- 用户明确要求 skill 评估、benchmark、描述优化或打包。

不适用于：

- 普通业务功能实现。
- 只需要执行某个已有 skill。
- Shanforge 阶段路由、review gate、人工确认或本地提交。
- 没有明确目标能力、触发条件或使用者的泛 prompt 优化请求；先澄清目标。

## 强制原则

- 所有项目内 skill 默认使用中文；工具名、命令名、路径、文件名、API 名和代码标识符保留原文。
- 用户可见文本必须中文；引用英文资料时，只保留必要专名，并用中文解释作用。
- 编写者必须以“丰富经验的中文语言专家和 prompt 专家”身份处理 skill 文本。
- 中文表达使用短句；完整保留原文所有含义，不省略约束、例外、触发条件、禁止项、输出要求和验收门槛。
- 删除废话、寒暄、重复铺垫和无效形容词；不得为了省 token 删除流程控制语义。
- 修改已有 skill 前，先写含义保留清单，覆盖目标、触发、输入、步骤、输出、禁止项、例外、验收、风险和 handoff。
- 改写者不能批准自己的 skill。作者自检只能把状态推进到 `ready_for_review`。
- 必须交给独立 reviewer、reviewer 子 agent 或单独 review task 判断 `approved` / `changes_requested`。
- 有问题就修复并复审，直到评审和验证通过；禁止用“已自评通过”代替独立评审。
- 修改 skill 时同步必要测试、eval、模板、schema、rubric、文档和 `.factory/memory/` 摘要。
- 目标明确、重复、确定性的 helper code 可以放入该 skill 自己的 `scripts/` 或等价 helper 目录。
- `SKILL.md` 必须写清输入、输出、触发、失败语义和风险边界。
- 文档模板、schema、rubric、评审表和长背景放入 `references/`，由 `SKILL.md` 按需引用。
- 禁止把全局中心脚本、隐藏执行器或仓库级 CLI 当成 skill 流程主控；skill 是流程入口，helper code 只是 skill 内部工具。

## 默认流程

1. 确定目标能力、触发场景、使用边界和预期输出。
2. 读取原 skill、相关 references 和必要事实；不要散读无关材料。
3. 新建时写新增能力清单；改写时写含义保留清单。
4. 编写或改写 `SKILL.md`，保持中文短句和最小主入口。
5. 长模板、schema、rubric、评估数据结构和背景说明下沉到 `references/`。
6. 更新或补充最小测试；没有测试价值时写明原因。
7. 作者自检并输出 `ready_for_review`，不得自批 `approved`。
8. 交给独立 reviewer 按清单、测试和风险边界复核。

## 创建检查

- `name` 是稳定技能标识。
- `description` 写清功能和具体触发场景，避免压过更具体 skill。
- 正文只保留工作流、硬规则、输出契约和失败语义。
- `scripts/` 只放确定性 helper code。
- `references/` 放模板、schema、rubric、评审表、示例和长背景。
- `assets/` 放模板文件、图标、字体等静态资产。

## 改写检查

1. 提取原文含义保留清单。
2. 用中文短句重写，不合并会改变责任边界的句子。
3. 保留“必须、禁止、只允许、先、后、直到、例外、用户明确要求”等强制语义。
4. 删除空话和重复，但保留状态流转、失败处理和验收门槛。
5. 对照含义保留清单逐项自检。
6. 交给未参与改写的 reviewer 复核。

## 评估、benchmark、描述优化和打包

只有用户明确要求评估、benchmark、描述优化或打包时，才进入这条支线。

- 先读取 [schemas](references/schemas.md)，确认当前仓库实际支持的输入和输出格式。
- 先核实当前仓库里是否存在对应脚本、模板或打包工具；找不到就报告缺口，不编造旧工具链事实。
- 评估时必须保持“作者 / 裁判”隔离：作者可设计测试和自检，最终质量判断交给独立 reviewer、评分员子代理或用户。
- 描述优化只改触发准确性，不扩大 skill 职责。
- 打包只在目标格式和安装方式已确认后执行。

## 输出契约

创建或修改 skill 时，输出至少包含：

- 目标 skill 路径。
- 触发条件和不适用场景。
- 输入、输出、失败语义和风险边界。
- 含义保留清单或新增能力清单。
- 已更新的测试、eval、模板、schema、rubric，或说明为什么不需要。
- 作者自检结论，只能到 `ready_for_review`。

Shanforge 状态包：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: skill-creator
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <path>
- evidence:
  - <测试、eval 或自检记录>
- ledger_event: <event id or none>
- needs:
  - review | user_input | none
```

`blocked` 用于目标能力、触发范围、原始含义、评审隔离条件或验证方式缺失，导致继续改写会丢失语义或无法判断质量的情况。

`needs_user_input` 用于必须由用户决定目标能力、触发边界、兼容取舍或交付格式的情况。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
