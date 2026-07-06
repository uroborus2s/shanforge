# 子任务：中文语言与 Prompt 质量评审

## 角色

中文语言专家 + prompt 专家。

## 输入

- `.factory/memory/runtime-brief.md`
- `.factory/memory/skill-updates.summary.md`
- `skills/*/SKILL.md`

## 禁止

- 禁止修改文件。
- 禁止评审系统 skill、插件缓存 skill 或仓外 skill。
- 禁止散读 `docs/` 长文。
- 禁止只给总体印象，必须按 skill 给分。

## 检查维度

每个 skill 按 100 分评估：

- 触发条件是否清楚。
- 职责边界是否单一。
- 默认步骤是否可执行。
- 输入、输出、证据和状态是否明确。
- 是否存在啰嗦重复。
- 是否存在语义不清或相互矛盾。
- 中文表达是否自然、短句、少口号。
- prompt 是否避免让工作 skill 自行路由其他 skill。

## 输出

直接返回中文报告：

- 每个 skill 的评分。
- 低于 90 分的 skill，列 1-3 条最关键问题和最小修正建议。
- Top 10 问题模式，按影响排序。
- 明确说明只读评审，没有修改文件。

## 已创建子 agent

- agent id：`019f3329-655c-7a83-84b7-40d8b461b0f6`
- nickname：`Nash`
