# Agent 高主动性与自进化集成方案

**项目名称：** 山海工枢 / shanforge  
**负责人：** 仓库维护者  
**主要读者：** 维护者 | 项目协调者 | 协作者  
**最后更新：** 2026-03-27  

## 1. 目标

把 `pua` 类高压工作方式中真正对工程有用的部分，安全地改造成软件工厂里的正向协作协议。

保留的只有这些工程能力：

- owner 意识
- 证据式完成
- 失败模式分类
- 恢复协议
- 模式级修复
- 最佳实践沉淀

不会引入的内容：

- 身份羞辱
- 同侪羞辱
- 威胁式施压
- 情绪操控
- 永久抬高标准且不可回退

## 2. 设计原则

- 高主动性不等于越权。
- 恢复优先于施压。
- 完成必须带证据。
- 修一个点，要检查一类问题。
- 有效做法要沉淀成基线，而不是留在单次会话里。

## 3. 已落地能力

当前软件工厂已经落地以下命令：

| 命令 | 作用 | 主要产物 |
|---|---|---|
| `factory-agent-motivation` | 刷新团队动能、角色自治预算和正向强化信号 | `team-energy.md`, `agent-achievements.md`, `motivation-state.md`, `autonomy-rules.md` |
| `factory-recovery-coach` | 在阻塞、空转、证据不足、过早升级、路径耗尽、质量漂移时生成恢复方案 | `recovery-review.md`, `recovery-playbook.md` |
| `factory-pattern-fix` | 把单点问题扩展为同类扫描、影响资产和预防动作 | `pattern-fix-report.md`, `pattern-fix.summary.md` |
| `factory-evolution-baseline` | 把有效做法沉淀成项目默认基线 | `evolution-baseline.md` |

## 4. 资产分层

### 4.1 人类过程文档

- `.factory/process/team-energy.md`
- `.factory/process/agent-achievements.md`
- `.factory/process/recovery-review.md`
- `.factory/process/pattern-fix-report.md`

### 4.2 AI 记忆文档

- `.factory/memory/motivation-state.md`
- `.factory/memory/autonomy-rules.md`
- `.factory/memory/recovery-playbook.md`
- `.factory/memory/evolution-baseline.md`
- `.factory/memory/pattern-fix.summary.md`

## 5. 失败模式与恢复协议

当前默认失败模式包括：

- `blocked`
- `looping`
- `unverified`
- `premature-escalation`
- `path-exhausted`
- `quality-drift`

统一恢复步骤：

1. 复述当前目标。
2. 标出当前失败模式。
3. 列出已经排除的路径。
4. 明确下一条明显不同的路径。
5. 明确本轮必须补齐的证据。

## 6. 与软件工程流程的结合方式

### 需求阶段

- 写完需求后，主动做遗漏扫描和一致性校验。
- 不允许只停留在抽象概念，不写边界、异常和约束。

### 设计阶段

- 设计必须带可评审的交付物。
- UI/UX 不只写文字，优先给页面、状态、交互和可视化产物。

### 开发阶段

- 完成一个任务时，必须同步代码、测试、文档和 AI 记忆。
- 遇到重复问题时，优先做模式级修复。

### 测试与交付阶段

- 质量结论必须可回链到测试、PR、文档或运行记录。
- 发布、交接和复盘后应刷新自进化基线。

## 7. 运行时约束

- 这些能力是工程协议，不是人格压力模式。
- 任何高主动性动作都必须服从正式文档、审批边界、PR/Gate 规则和单文件版本演化。
- 如果发现共性问题是流程缺陷，应优先修软件工厂本身，而不是把压力转嫁给单个 Agent。

## 8. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-03-25 | 将高主动性、恢复、自进化方案正式并入 docs/ 文档体系 | Codex |
