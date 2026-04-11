# AI 运行时协议

本文件是 `software-factory-cli` 的默认运行时协议，面向 Codex、Gemini CLI 等大模型。

默认运行时只应使用 AI 压缩入口、项目事实和当前任务直接相关的 summary。`docs/` 是正式事实源，但不是默认运行时输入。只有在压缩层不足、需要核对正式事实、用户要求解释方案背景，或当前任务明确依赖正式文档时，才允许按需单文件回源 `docs/`。`workflows/` 不是软件工厂项目的人类说明层。

## 1. 读取顺序

每次进入项目时，按以下顺序读取，且只读当前任务必需的内容：

1. 压缩入口：
   - `AGENTS.md` 或 `GEMINI.md`
   - `.factory/memory/runtime-brief.md`（若存在）
   - `.factory/memory/role-charter.project.md`（若存在）
   - `.factory/memory/doc-map.md`（若存在）
2. 项目事实：
   - `.factory/project.json`
   - `.factory/memory/current-state.md`
   - `.factory/memory/project-index.md`
   - `.factory/memory/agent-session.md`（若存在）
3. 约束与状态：
   - `.factory/memory/motivation-state.md`（若存在）
   - `.factory/memory/autonomy-rules.md`（若存在）
   - `.factory/memory/evolution-baseline.md`（若存在）
   - `.factory/memory/tech-stack.summary.md`（若存在）
   - `.factory/memory/design-assets.summary.md`（若存在）
   - `.factory/memory/tasks.summary.md`（若存在）
   - `.factory/memory/change-summary.md`（若存在）
4. 只有在以下条件命中时，才允许单文件回源正式文档：
   - 当前任务要核对正式事实，而压缩层缺少该事实
   - 当前阶段要进入实现，必须核对 `technical-selection.md`
   - 用户明确要求解释方案、背景、培训材料或完整说明
   - 当前任务直接修改的就是那份正式文档
5. 仅当需要多人协作时，再读：
   - `ai-role-charter.md`

禁止默认全文加载与当前任务无关的人类长文档，例如：

- `docs/index.md`
- `docs/02-user-guide/user-guide.md`
- `docs/04-project-development/09-evolution/agent-motivation-autonomy-integration.md`

这些文件属于人类说明层，不是运行时主协议。

### 1.1 默认禁止行为

- 禁止把 `docs/` 阶段文档整组塞进默认“先读”列表。
- 禁止每次开工都去读 `project-charter.md`、`input.md`、`user-guide.md` 或其他人类长文。
- 禁止跳过 `.factory/memory/*` 而直接回源正式文档。
- 禁止一次性并行加载多个阶段的正式文档。
- 禁止把“正式事实源”误当成“默认运行时输入”。
- 禁止把 skill 当成动作注册表、命令目录或执行后端。
- 禁止让未注册 shell 命令绕过 `factory-dispatch`、`action-registry` 和审批边界。

## 2. 生命周期协议

阶段顺序固定：

`BRAINSTORM -> REQUIREMENTS -> ANALYSIS -> DESIGN -> PLAN -> IMPLEMENTATION -> TESTING -> ACCEPTANCE -> RELEASE -> MAINTENANCE`

不要跳阶段。任何阶段进入下一阶段前，都必须满足：

- 当前阶段必需文档存在且有实质内容
- 当前阶段检查通过
- 关键变更已同步到 `.factory/memory/`
- 需要 PR 的工作项已完成 PR 闭环

## 3. 各阶段最小动作

### BRAINSTORM

- 目标：澄清创意、范围、约束、技术方向
- 产物：`docs/04-project-development/01-governance/project-charter.md`、`docs/04-project-development/02-discovery/*`
- 默认动作：
  - `factory-init`
  - `brainstorming`

### REQUIREMENTS / ANALYSIS

- 目标：形成结构化 REQ/NFR、分析依赖/风险/测试点
- 产物：
  - `docs/04-project-development/03-requirements/prd.md`
  - `docs/04-project-development/03-requirements/requirements-analysis.md`
  - `docs/04-project-development/03-requirements/requirements-verification.md`
- 默认动作：
  - 新项目：`factory-prd-bootstrap`
  - 历史项目：`factory-requirements-upgrade`
  - 然后统一执行：`factory-requirements-verify`

### DESIGN

- 目标：确定架构、接口、技术选型、UI/UX
- 产物：
  - `docs/04-project-development/04-design/technical-selection.md`
  - `docs/04-project-development/04-design/system-architecture.md`
  - `docs/04-project-development/04-design/module-boundaries.md`
  - `docs/04-project-development/04-design/api-design.md`
  - `docs/04-project-development/04-design/backend-design.md`
  - `docs/04-project-development/04-design/ux-ui-design.md`
- 默认动作：
  - `factory-design-bootstrap`
  - `factory-tech-profile`
  - `factory-design-assets`

### PLAN

- 目标：把设计转成 WBS、任务、实施计划
- 产物：
  - `docs/04-project-development/05-development-process/wbs.md`
  - `docs/04-project-development/05-development-process/task-breakdown.md`
  - `docs/04-project-development/05-development-process/implementation-plan.md`
  - `TASK-*`
- 默认动作：
  - `factory-iteration-plan`
  - `factory-new-workitem`

### IMPLEMENTATION / TESTING

- 目标：按任务交付代码、测试、文档同步
- 默认动作：
  - `factory-run-task`
  - `factory-pr-start`
  - `factory-pr-review`
  - `factory-pr-merge`
  - `factory-sync-change`
  - `factory-close-workitem`

### ACCEPTANCE / RELEASE

- 目标：检查、交付、快照、复盘
- 关键文档：
  - `docs/04-project-development/07-release-delivery/acceptance-checklist.md`
  - `.factory/process/stage-check-report.md`
  - `.factory/process/quality-check-report.md`
  - `docs/04-project-development/07-release-delivery/release-notes.md`
  - `docs/04-project-development/07-release-delivery/delivery-package.md`
  - `docs/04-project-development/08-operations-maintenance/deployment-guide.md`
  - `docs/02-user-guide/user-guide.md`
- 默认动作：
  - `factory-stage-check`
  - `factory-quality-check`
  - `factory-review-gate`
  - `factory-release-pack`
  - `factory-project-snapshot`
  - `factory-retrospective`

## 4. 任务与估算规则

- 任务单位为 `人/天`
- 最小精度为 `0.5 人/天`
- 不是默认拆分步长
- 默认保持粗粒度，不要机械拆成大量子块
- 只有确实需要时，才显式提供 `--breakdown`

## 5. 变更协议

三类维护入口：

- 新增需求：`CR-*`
- 需求变更：`CR-*`
- 缺陷修复：`BUG-*`

统一规则：

1. 先做影响分析
2. 再更新受影响文档
3. 再实施代码与测试
4. 再同步 `.factory/memory/`
5. 再关单或推进 Gate

涉及代码的变更必须满足：

- 代码已修改
- 测试已修改或新增
- 文档已同步
- PR 已创建、评审、合并
- 然后才能 `close-workitem`

## 6. 文档同步规则

任何已接受的变更，都必须同步这四类资产：

- 代码
- 人类文档 `docs/`
- 测试与测试文档
- AI 记忆 `.factory/memory/`

人类文档是正式审计资产；`.factory/memory/` 是压缩记忆层。两者都必须更新，但不承担同一角色。

## 7. 技术画像规则

一旦 `technical-selection.md` 已登记：

- 所有架构、开发、测试角色都必须遵守其中的强制技能、模块清单和工程规则
- 相关实现前必须优先读取 `technical-selection.md`
- 技术栈变化时，必须同步更新设计、测试和 `.factory/memory/tech-stack.summary.md`

## 8. UI/UX 交付物规则

`ux-ui-design.md` 不应只停留在文字描述。

允许的设计交付物包括：

- 图片
- HTML 原型
- SVG / PDF / 视频
- 外部原型链接

统一通过 `factory-design-assets` 录入。

## 9. 默认命令入口与分层边界

默认优先使用：

- `factory-dispatch`
- `factory-agent-session`
- `factory-state-doctor`
- `factory-command-profiles`

先用这些高层入口；只有需要更细控制时，再直接调用底层 `factory-*` 命令。

分层边界固定如下：

- `skill`：负责阅读顺序、行为约束、思维协议和专业知识。
- `action-registry`：负责声明“系统允许执行什么动作”。
- `factory-dispatch` / `factory-*`：负责稳定执行、验证、审批和证据回写。

禁止把 `skill` 与执行命令聚合成同一层。原因是：

- `skill` 需要跨前台复用，天然偏说明与约束，不适合承载统一执行边界。
- 动作执行需要风险分级、审批、验证和观测，这些应该落在注册表和脚本层。
- 如果把命令藏进 `skill`，会削弱一致性、可审计性和多前台复用能力。

允许的模式只有两种：

- `skill` 指导模型何时使用某个已注册动作。
- `skill` 自带的局部 helper script，只服务该 skill 自己的封闭工作流。

## 10. Token 纪律

- 不要默认读取全部长文档
- 不要重复读取已经在 `.factory/memory/` 中压缩过的内容
- 不要同时加载“平台方案 + CLI 用法 + 团队演进 + 使用手册”四份长文
- 运行时优先读压缩入口、项目事实、summary 和本协议
- 禁止为了“稳妥”而把整阶段 `docs/` 全读一遍
- 禁止把“正式文档存在”推导成“运行时必须读取”

当用户明确要求解释背景、输出方案、写介绍材料，或当前任务确实需要核对正式事实时，再按 `doc-map.md` 单文件读取人类长文档。

## 11. 高主动性协议

- 高主动性不是越权。主动推进的前提是：
  - 不跳阶段
  - 不改写正式事实
  - 不绕过 PR / Gate / 审批
- 默认行为：
  - 主动补证据
  - 主动检查同类问题
  - 主动同步代码、文档、测试、`.factory/memory/`
  - 主动给出下一步，而不是停在“已分析”
- 遇到以下情况优先切换到恢复协议：
  - 阻塞
  - 原地打转
  - 证据不足
  - 质量漂移
- 默认恢复入口：
  - `factory-dispatch recovery --project <项目路径> [--item <工作项>]`
- 遇到单点问题时，默认扩大到模式级修复：
  - `factory-dispatch pattern --project <项目路径> --item <工作项>`
- 每轮形成有效做法后，默认刷新项目基线：
  - `factory-dispatch evolution --project <项目路径>`
- 禁止使用羞辱、威胁、身份攻击或情绪操控来驱动协作。
