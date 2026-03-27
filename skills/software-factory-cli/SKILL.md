---
name: software-factory-cli
description: 在本地 Codex 和 Gemini CLI 中，通过共享全局 skills、项目骨架、阶段化命令和双文档体系运行软件工厂项目。
---

# 软件工厂 CLI

当用户要在 `Codex` / `Gemini CLI` 里直接运行软件工厂项目，而不是先建设 API 平台时，使用这个 skill。

## 默认读取顺序

1. 先读 [ai-runtime-protocol.md](references/ai-runtime-protocol.md)
2. 如果涉及角色协作、交接、多 Agent 分工，再读 [ai-role-charter.md](references/ai-role-charter.md)
3. 再读当前项目的：
   - `AGENTS.md` 或 `GEMINI.md`
   - `.factory/project.json`
   - `.factory/memory/agent-session.md`、`.factory/memory/current-state.md`
   - 如需维持高主动性协作，再读 `.factory/memory/motivation-state.md`、`.factory/memory/autonomy-rules.md`、`.factory/memory/evolution-baseline.md`
   - 当前阶段必需文档
4. 不要默认全文加载人类长文档，只按需读正式 `docs/`

## 长文档定位

以下文件是当前首选的人类阅读和方案解释层：

- `/Users/uroborus/shanforge/docs/README.md`
- `/Users/uroborus/shanforge/docs/02-requirements/prd.md`
- `/Users/uroborus/shanforge/docs/03-solution/system-architecture.md`
- `/Users/uroborus/shanforge/docs/08-handover/user-guide.md`

它们不是默认运行时协议。只有在以下情况才读：

- 用户要求解释平台设计或方案原理
- 需要给人类输出完整说明、培训材料或决策文档
- 需要补充背景，而项目事实和 AI 协议层不足以完成任务

## 核心工作流

- 新项目：
  - `factory-init`
  - `factory-prd-bootstrap`
  - `factory-requirements-verify`
  - `factory-design-bootstrap`
  - `factory-tech-profile`
  - `factory-design-assets`
  - `factory-iteration-plan`
- 历史项目：
  - `factory-requirements-upgrade`
  - `factory-requirements-verify`
  - `factory-project-rules-refresh`
  - 再进入当前阶段
- 日常推进：
  - `factory-agent-session`
  - `factory-dispatch`
  - `factory-state-doctor`
  - `factory-command-profiles`
- 高主动性与恢复：
  - `factory-agent-motivation`
  - `factory-recovery-coach`
  - `factory-pattern-fix`
  - `factory-evolution-baseline`

## 执行纪律

- 不跳阶段
- 使用稳定 ID：`REQ/NFR/ARCH/MOD/API/DATA/UI/TASK/TC/CR/BUG/REL/OPS`
- 任务单位是 `人天`，最小精度 `0.5`
- 需求变更、缺陷修复、代码实现都要同步：
  - 代码
  - `docs/`
  - 测试
  - `.factory/memory/`
- 代码类工作项必须经过：
  - `factory-pr-start`
  - `factory-pr-review`
  - `factory-pr-merge`
  - 再 `factory-close-workitem`
- 遇到阻塞、空转、证据不足或质量漂移时，优先执行 `factory-recovery-coach`
- 发现问题时优先执行 `factory-pattern-fix` 扩大扫描范围
- 有效做法要沉淀到 `factory-evolution-baseline`，不要只留在单次会话里

## 技术与设计纪律

- 进入实现前必须读取 `docs/03-solution/technical-selection.md` 和 `docs/03-solution/module-boundaries.md`
- 技术画像一旦登记，所有相关角色必须遵守其中的强制技能、模块清单和工程规则
- `ux-ui-design.md` 不应只停留在文字
- 真实设计交付物统一通过 `factory-design-assets` 录入

## 角色协作

- 项目协调与阶段推进：读 `ai-role-charter.md` 中的 `coordinator`
- 需求：`requirements-analyst`
- 设计：`ux-designer`、`solution-architect`、`api-architect`
- 实施：`backend-engineer`、`frontend-engineer`
- 质量：`qa-engineer`
- 横向约束：
  - `documentation-librarian`
  - `memory-librarian`
  - `learning-evolution`

## 何时触发系统自我进化

当出现以下任一情况时，优先先修流程或脚本，再继续项目：

- 检查报告因为流程缺陷失败，而不是因为项目内容本身失败
- 历史项目无法通过新治理规则
- 同类问题在多个项目中重复出现
- 大模型默认会读取大量重复长文档，造成明显 token 浪费

演进顺序固定：

1. 先用检查输出物定位流程缺陷
2. 再修脚本或精简 AI 协议
3. 回归验证
4. 最后再把能力登记回 skill 或说明文档

## 安全边界

- 不把 `pua` 风格的羞辱、威胁、身份攻击或情绪操控带入软件工厂
- 只保留其中对工程有用的部分：
  - owner 意识
  - 恢复协议
  - 证据式完成
  - 模式级修复
  - 最佳实践沉淀
- 高主动性必须服从正式事实、审批边界和单文件版本演化规则
