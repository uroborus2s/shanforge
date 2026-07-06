# 子任务：Skill 流程完整性测试

## 角色

Skill 流程测试工程师。

## 输入

- `.factory/memory/runtime-brief.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/tests.summary.md`
- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- workflow skills：
  - `brainstorming`
  - `requirements-engineering`
  - `document-templates`
  - `writing-plans`
  - `subagent-driven-development`
  - `executing-plans`
  - `tdd-workflow`
  - `systematic-debugging`
  - `verification-before-completion`
  - `requesting-code-review`
  - `receiving-code-review`
  - `gitcommitzh`
- `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md` 的第 7、10、11、14、15 节。

## 禁止

- 禁止修改文件。
- 禁止运行破坏性命令。
- 禁止把已有结构测试通过等同于流程语义通过。
- 禁止把 same-thread 自检写成独立 approved。

## 测试场景

- 新功能 / 一句话需求。
- Bug 修复。
- Review 反馈。
- 压缩恢复。
- 完成声明 / 收尾。
- 自评隔离。

## 输出

直接返回中文报告：

- 流程矩阵：场景、入口 skill、后续 skill、输入、动作、输出、证据、门禁。
- 缺口和风险。
- 最小新增 / 修改测试断言建议。
- 明确说明只读测试，没有修改文件。

## 已创建子 agent

- agent id：`019f3329-96f2-7340-8e8d-620329e378db`
- nickname：`Archimedes`
