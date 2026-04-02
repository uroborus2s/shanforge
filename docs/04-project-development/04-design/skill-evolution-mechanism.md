# Skill 进化机制设计

**文档状态：** 已确认方向  
**主要读者：** 技能维护者 | 架构师 | 平台维护者 | QA  
**负责人：** 仓库维护者  
**关联 ID：** `REQ-003`, `REQ-005`, `REQ-006`, `API-010`, `API-011`, `API-015`  
**最后更新：** 2026-04-02  

## 1. 设计定位

山海工枢未来仍然会大量依赖 `skill`，但 `skill` 的职责必须收敛为：

- 阶段协议
- 角色约束
- 阅读顺序
- 专业知识与思维框架

不应把 `skill` 当成整个运行时的唯一骨架。

因此，`skill` 的正确位置是：

- 不是执行主骨架
- 是“认知与约束层”
- 与 `Action Registry`、`Workflow`、`Adapter`、`Eval`、`Recovery` 共同形成完整能力体系

## 2. 能力固化分层

| 能力类型 | 适合固化成什么 | 例子 |
|---|---|---|
| 如何理解问题、读取上下文、保持阶段边界 | `skill` | 需求阶段 skill、设计阶段 skill |
| 一个可稳定复用的执行动作 | `action` | `docs.standard_upgrade` |
| 多步执行顺序与分支控制 | `workflow` | `historical_onboarding_flow` |
| 不同宿主的能力差异适配 | `adapter` | `codex-adapter`、`gemini-adapter`、未来 `opencode-adapter` |
| 质量验证和回放 | `eval suite` | 意图识别回放、策略门槛回归 |
| 失败处理和安全重试 | `recovery playbook` | `policy_denied`、`looping` 恢复方案 |

## 3. 什么应该固化成 skill

### 应固化成 skill 的情况

- 这是一个跨多次任务都会重复出现的认知模式
- 它需要规定先读什么、后读什么
- 它需要限制模型不要做什么
- 它主要解决“怎么理解和约束问题”，而不是“如何直接执行”

### 不应直接固化成 skill 的情况

- 它本质上只是一个脚本入口
- 它本质上是审批策略
- 它本质上是多步编排
- 它本质上是适配前台工具差异
- 它主要价值在验证或恢复，而不是思维协议

## 4. Skill 生命周期

### 4.1 信号采集

从以下信号中识别需要进化的能力：

- 高频成功案例
- 高频失败案例
- 人工反复纠正的行为
- 恢复成功记录
- 多代理冲突记录
- 上下文过载记录

### 4.2 分类判断

先判断问题属于哪一类：

- `skill` 缺失或约束不清
- `action` 缺失
- `workflow` 缺失
- `adapter` 缺失
- `eval` 缺失
- `recovery` 缺失

### 4.3 生成候选变更

新能力不直接进入正式 skill，而是先生成候选变更：

- 变更目标
- 触发条件
- 新增或修改的约束
- 预期提升指标
- 回放样本

### 4.4 回放评估

候选变更必须经过历史样本回放，至少检查：

- 触发是否更准确
- 首次完成率是否提升
- 重试次数是否下降
- 越权率是否上升
- 人工打断率是否上升
- 上下文成本是否失控

### 4.5 人工审定

评审重点：

- trigger 是否过宽
- 约束是否与现有规则冲突
- 是否把执行问题错误地塞进 skill
- 是否遗漏了评估和恢复资产

### 4.6 晋升与发布

通过评审后，才允许：

- 更新正式 `skill`
- 补齐对应 `action` / `workflow` / `adapter` / `eval`
- 更新用户文档和追踪矩阵
- 正式 `skill` 变更必须具备候选草案、评估结果和批准记录

### 4.7 发布后观测

上线后持续记录：

- 完成率
- 越权率
- 误判率
- 人工干预率
- 恢复成功率

## 5. Skill 进化约束

### 允许的进化

- 更清晰的阶段边界
- 更准确的触发条件
- 更短但更有效的阅读顺序
- 更稳定的失败恢复提示
- 更完整的证据要求

### 禁止的进化

- 直接自动覆盖核心系统规则
- 把任意一次成功经验直接升级为全局默认
- 通过修改 skill 绕过审批边界
- 把高风险执行能力隐藏进 skill 文本中
- 让系统无约束地“自改人格”或“自改使命”

## 6. 评价指标

| 指标 | 说明 |
|---|---|
| 触发准确率 | 是否在正确场景触发正确 skill |
| 首次完成率 | 第一次执行是否直达目标 |
| 重试次数 | 平均需要重试几次 |
| 越权率 | 是否触发了不应自动发生的动作 |
| 人工打断率 | 用户是否频繁打断并纠偏 |
| 上下文成本 | 为使用该 skill 需要加载多少额外上下文 |
| 恢复成功率 | 失败后是否能回到正确轨道 |

## 7. 新能力固化流程

统一采用下面 7 步：

1. 发现重复需求或重复失败
2. 定义能力边界
3. 分类到 `skill`、`action`、`workflow`、`adapter`、`eval` 或 `recovery`
4. 编写最小候选版本
5. 准备回放样本和评估标准
6. 人工审定并正式晋升
7. 发布后持续观测

## 8. 示例

### 8.1 docs 标准升级能力

正确固化方式：

- `skill`：告诉模型何时应升级 docs、先检查什么、不要手工重写目录
- `action`：`docs.standard_upgrade`
- `workflow`：`docs_upgrade_flow`
- `eval`：检查升级后是否达到 `就绪`

### 8.2 支持新的前台工具，如 opencode

正确固化方式：

- 不优先改 `skill`
- 先增加 `frontend adapter`
- 定义能力矩阵和降级策略
- 再让现有 `skill` 在新前台复用

### 8.3 新的设计阶段能力

正确固化方式：

- `skill`：补设计阶段的输入、输出、异常路径和评审约束
- `action`：补齐特定设计动作
- `eval`：检查是否跳过需求前置、是否缺高风险决策

## 9. 推荐配套资产

未来建议逐步补齐：

- `skill` 候选变更提案
- 技能回放样本集
- 技能评估脚本
- 技能发布记录
- 技能回退机制

当前已落地的第一个回放资产：

- `config/evals/intent-resolver-cases.json`
- `scripts/factory-intent-eval`

它用于固定评估自然语言到动作解析的命中率、审批边界和安全执行结果，是后续 skill / intent / policy 联合进化的起点，而不是终点。

## 10. 与现有山海工枢资产的衔接

| 现有资产 | 在新模型中的定位 |
|---|---|
| `skills/` | 正式技能资产库 |
| `factory-agent-motivation` | 正向强化与自治预算校准器 |
| `factory-recovery-coach` | 恢复 playbook 生成器 |
| `factory-evolution-baseline` | 有效做法沉淀入口 |
| `factory-pattern-fix` | 从单点问题扩展到同类问题扫描 |

## 11. 外部参考

- [claw-code](https://github.com/ultraworkers/claw-code)
- [Prompt Engineering Guide - Reflexion](https://www.promptingguide.ai/techniques/reflexion)
- [Prompt Engineering Guide - Context Engineering](https://www.promptingguide.ai/agents/context-engineering)

## 12. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-04-02 | 初始版本，定义 skill 的分层定位、进化约束和新能力固化流程 | Codex |
| 2026-04-02 | 增加首个已落地回放资产 `intent-eval`，把固定样本回放纳入进化基线 | Codex |
| 2026-04-02 | 将 skill 正式变更的候选优先、评估先行、显式批准边界固化到 `reply-policy.json` | Codex |
