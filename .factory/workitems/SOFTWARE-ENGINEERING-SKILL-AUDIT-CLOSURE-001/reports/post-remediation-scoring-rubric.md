# 整改后五专家评分结构

## 目的

原评分表是整改前基线。整改后评分必须回答三个不同问题：质量分数是多少、原始问题关闭了多少、是否达到通过 Gate。三者不得混写。

## 保留的五个维度

| reviewer | 维度 | 重点 |
|---|---|---|
| 中文语言专家 | 中文 | 准确、自然、术语首次释义、无歧义 |
| Skill 专家 | Skill 设计 | 触发边界、渐进读取、工具合同、可移植性 |
| 软件工程专家 | 软件工程 | 可执行性、根因、测试、代码形状、失败关闭 |
| 项目管理专家 | 项目管理 | WBS、TaskCard、状态、owner、evidence、Gate |
| 沟通专家 | 沟通 | 用户能否直接看懂进度、测试、Bug、修复位置和下一动作 |

每位 reviewer 对 38 个 Skill 独立给整数分；共 `5 × 38 = 190` 个评分。单 Skill 综合分仍为五项等权平均，系统矩阵分仍为 38 个 Skill 综合分平均，以便和原始 `85.6/100` 对比。

## 评分锚点

| 分数 | 必须满足的事实 |
|---:|---|
| 95–100 | 无该维度 Finding；有行为或结构验证；边界和失败语义完整。100 分不得有 Minor。 |
| 90–94 | 无 Critical/Important；最多存在不影响执行的 Minor；证据可复核。 |
| 80–89 | Skill 可用，但仍有 Important、行为证据缺口或跨 Skill 不一致。 |
| 70–79 | 多个 Important，或关键路径依赖人工猜测、自报、不可执行命令。 |
| 0–69 | 存在 Critical、主要职责不可执行，或会造成安全、数据、生产级错误。 |

限制：没有行为或结构证据时不得给 95 分以上；评分理由必须引用 Finding ID 或验证证据，不能只写主观形容词。

## 逐 Skill 评分表字段

```text
Skill
整改前：中文 / Skill设计 / 软件工程 / 项目管理 / 沟通 / 综合
整改后：中文 / Skill设计 / 软件工程 / 项目管理 / 沟通 / 综合
综合变化
原始 Finding ID
已关闭 Finding ID
剩余 Critical / Important / Minor
验证证据
评分理由
```

## 原始 Finding 闭环字段

```text
finding_id
source_reviewer
original_severity
problem
root_cause
location
status: verified_fixed | unresolved | partially_fixed | rejected_with_reason
verification
repair_task
independent_review_decision
```

`rejected_with_reason` 只有在相关独立 reviewer 接受理由后才算关闭；实现者单方面不采纳不能减少未关闭数量。

## 系统汇总字段

- 覆盖：整改前 `190/190`，整改后必须 `190/190`。
- 分数：整改前系统矩阵 `85.6/100`、整改后系统矩阵、差值。
- 原始问题：`C0 / I27 / M18`。
- 闭环：已关闭、未关闭和拒绝后获批数量。
- 新问题：整改后新发现的 C/I/M。
- 验证：pytest、Ruff、38 Skill validator、45 项追踪、黑盒和 diff check。

## 通过 Gate

只有同时满足以下条件，最终结论才是 `approved`：

1. 整改后评分覆盖 `190/190`。
2. 原始 45 个 Finding 全部有独立 reviewer 结论。
3. 剩余 Critical 为 0、Important 为 0。
4. 完整必需验证全部通过，未运行项已明确且不影响结论。

平均分再高也不能覆盖未关闭的 Critical 或 Important。Minor 可以保留，但必须列出影响、owner 和后续处理决定。
