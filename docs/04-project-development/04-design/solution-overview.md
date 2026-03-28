# 总体方案与协作总览

**项目名称：** 山海工枢 / shanforge  
**文档状态：** 已确认基线  
**负责人：** 仓库维护者  
**主要读者：** 维护者 | 架构 | 协作者 | 项目负责人  
**上游输入：** 项目章程 | PRD | 需求分析  
**下游输出：** 系统架构 | 技术选型 | 模块边界 | 用户指南  
**最后更新：** 2026-03-27  

## 1. 这份文档的作用

这份文档是软件工厂项目的人类总览文档，用来快速回答四个问题：

- 这套系统到底是什么
- 当前版本做到哪里
- 由哪些层和哪些角色共同工作
- 日常推进时应遵守哪些总规则

它不替代更细的 `PRD`、系统架构、技术选型、模块边界或用户指南，而是作为这些文档之间的总导航。

## 2. 产品定位

软件工厂的定位是“AI 驱动的软件交付操作系统”，不是单一模型的自由发挥式代码生成器。

在当前版本中：

- 宿主环境是 `Codex` 和 `Gemini CLI`
- 正式人类文档统一在 `docs/`
- 被管理项目中的 `.factory/` 保存状态、工作项、过程文档和 AI 记忆
- 本地 `factory-*` 脚本承担低自由度、可重复、可校验的执行动作
- 共享 `skills/` 为不同阶段和不同角色提供方法与约束

## 3. 当前版本范围

当前版本明确是 `CLI-first`：

- 支持从创意初始化一个软件工厂项目
- 支持构思、需求、设计、计划、实施、测试、验收、发布、维护全生命周期
- 支持 `TASK`、`CR`、`BUG` 三类工作项
- 支持角色协作、PR 闭环、阶段 Gate、交接、复盘与快照
- 支持人类文档与 AI 记忆双轨治理

当前不把独立 API 平台作为实现边界，也不把完整 DevOps 平台化作为当前阻塞项。

## 4. 核心分层

```text
+----------------------------------------------------+
| 使用与协作层                                       |
| Codex / Gemini CLI / 审批 / 人类查看 docs          |
+----------------------------------------------------+
| 工作流与治理层                                     |
| Stage / Gate / Profile / Workflow / PR / Handover  |
+----------------------------------------------------+
| 执行层                                             |
| Role Agents / Local Scripts / Git / Tests          |
+----------------------------------------------------+
| 文档与追踪层                                       |
| docs / traceability / process docs / workitems     |
+----------------------------------------------------+
| 规则与记忆层                                       |
| AGENTS / GEMINI / skills / .factory / summaries    |
+----------------------------------------------------+
```

对人类来说，最需要记住的是：

- `docs/` 负责正式说明
- `skills/` 负责方法和约束
- `scripts/` 负责确定性动作
- `.factory/` 负责项目运行事实和 AI 记忆

## 5. 资产模型

软件工厂相关项目至少有四类核心资产：

1. 项目规则
   - `AGENTS.md`
   - `GEMINI.md`
   - `.factory/project.json`
2. 正式人类文档
   - `docs/04-project-development/01-governance/*`
   - `docs/04-project-development/02-discovery/*`
   - `docs/04-project-development/03-requirements/*`
   - `docs/04-project-development/04-design/*`
   - `docs/04-project-development/05-development-process/*`
   - `docs/04-project-development/06-testing-verification/*`
   - `docs/04-project-development/07-release-delivery/*`
   - `docs/04-project-development/08-operations-maintenance/*`
   - `docs/02-user-guide/*`
   - `docs/04-project-development/09-evolution/*`
   - `docs/04-project-development/10-traceability/*`
3. 过程与执行资产
   - `.factory/process/*`
   - `.factory/workitems/*`
4. AI 压缩记忆
   - `.factory/memory/*`

正式事实始终先进入 `docs/`，再压缩进入 `.factory/memory/`。

## 6. 生命周期与角色分工

当前生命周期固定为：

`BRAINSTORM -> REQUIREMENTS -> ANALYSIS -> DESIGN -> PLAN -> IMPLEMENTATION -> TESTING -> ACCEPTANCE -> RELEASE -> MAINTENANCE`

默认角色包括：

- 项目协调者
- 需求分析师
- 解决方案架构师
- UX/UI 设计师
- 后端工程师
- 前端工程师
- QA 工程师
- 发布经理
- 文档与记忆管理员
- 学习与演进职责

默认模型分工建议：

- `Gemini` 偏创意澄清、PRD、需求分析、架构设计、影响分析、长文综合
- `Codex` 偏代码实现、测试补齐、重构、缺陷修复、仓库内修改
- 评审与总结角色用于交叉复核、摘要收敛和阶段报告

## 7. 运行控制原理

真正约束大模型行为的不是“模型自己知道该怎么做”，而是下面这组边界共同生效：

- 宿主 CLI 的系统规则
- 项目根目录下的 `AGENTS.md`、`GEMINI.md`
- `.factory/project.json` 里的阶段、角色和状态
- `.factory/memory/agent-session.md`、`.factory/memory/current-state.md` 等压缩上下文
- 本地 `factory-*` 脚本限制可执行动作和输出落点

因此，软件工厂的核心设计不是“让模型自由发挥”，而是“让模型在规则、文档和脚本边界内工作”。

## 8. 总体治理规则

### 8.1 文档治理

- `docs/` 是软件工厂项目的人类正式文档唯一入口
- 与软件工厂项目本身相关的人类说明文档不再保留在 `workflows/`
- 每类正式文档采用单文件演化，不额外维护 `v2/final` 副本

### 8.2 任务治理

- 工作项分为 `TASK`、`CR`、`BUG`
- 估算单位是 `人天`
- 最小精度是 `0.5 人天`
- 默认保持粗粒度，不做机械拆分

### 8.3 变更治理

任何已接受的变更都必须同步：

1. 代码
2. 人类文档 `docs/`
3. 测试与测试文档
4. AI 记忆 `.factory/memory/`

### 8.4 代码治理

代码类工作项必须经过：

1. `factory-pr-start`
2. `factory-pr-review`
3. `factory-pr-merge`
4. `factory-close-workitem`

没有 PR 闭环，不应关单，也不应推进相关代码阶段 Gate。

### 8.5 高主动性治理

系统鼓励 Agent 主动推进、主动补证据、主动扩查同类问题，但不得：

- 跳阶段
- 越过审批
- 擅自改写正式事实
- 用羞辱或情绪压迫代替工程方法

## 9. 自我进化机制

当出现以下任一情况时，应优先修流程、协议或脚本，而不是只修当前项目：

- 检查失败是流程缺陷造成的
- 历史项目无法通过新治理规则
- 同类问题在多个项目中重复出现
- 运行时默认读取过多无关长文，造成明显 token 浪费

推荐闭环：

`观察输出 -> 归纳模式 -> 修流程/脚本/协议 -> 回归验证 -> 更新基线`

## 10. 与其他文档的关系

- 看正式需求边界：读 [prd.md](../03-requirements/prd.md)
- 看详细系统分层和数据流：读 [system-architecture.md](./system-architecture.md)
- 看工程规则和技术画像：读 [technical-selection.md](./technical-selection.md)
- 看模块职责和禁止耦合：读 [module-boundaries.md](./module-boundaries.md)
- 看实际使用方式：读 [user-guide.md](../../02-user-guide/user-guide.md)
- 看高主动性、自主性和恢复机制：读 [agent-motivation-autonomy-integration.md](../09-evolution/agent-motivation-autonomy-integration.md)

## 11. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-03-25 | 初始版本，承接原合并版需求与设计主文档中的人类总览内容，迁入 `docs/` | Codex |
