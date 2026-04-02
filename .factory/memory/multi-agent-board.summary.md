# 多 Agent 协作看板摘要

- 时间：2026-04-02 15:19:02
- 当前阶段：MAINTENANCE
- 看板负责人：Codex
- 焦点：写集冲突治理
- 活跃工作项：0
- 开放风险：0
- 待审批票据：0
- 未分派工作项：0
- 写集冲突：0

## 当前主要角色

- `项目协调者` | 工具：codex / gemini | 共享技能：brainstorming、document-templates、doc-coauthoring
- `发布经理` | 工具：gemini / codex | 共享技能：document-templates、doc-coauthoring
- `文档与记忆管理员` | 工具：gemini / codex | 共享技能：document-templates、doc-coauthoring

## 角色泳道

### 项目协调者
- 说明：负责阶段推进、跨角色协作、审批门禁和交接节奏控制。
- 推荐工具：codex / gemini
- 共享技能：brainstorming、document-templates、doc-coauthoring
- 优先文档：.factory/project.json、AGENTS.md、GEMINI.md
- 写入集合：无
- 当前工作项：无
- 推荐动作：
  - `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch session --project /Users/uroborus/AiProject/shanforge --owner Codex --focus '写集冲突治理'`
  - `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch workbench --project /Users/uroborus/AiProject/shanforge --role coordinator --owner Codex --focus '写集冲突治理'`

### 发布经理
- 说明：负责交付说明、部署运行、发布准备和交接闭环。
- 推荐工具：gemini / codex
- 共享技能：document-templates、doc-coauthoring
- 优先文档：.factory/project.json、AGENTS.md、GEMINI.md
- 写入集合：无
- 当前工作项：无
- 推荐动作：
  - `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch session --project /Users/uroborus/AiProject/shanforge --owner Codex --focus '写集冲突治理'`
  - `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch workbench --project /Users/uroborus/AiProject/shanforge --role release-manager --owner Codex --focus '写集冲突治理'`

### 文档与记忆管理员
- 说明：负责人类文档与 AI 记忆同步、摘要收敛和项目上下文恢复。
- 推荐工具：gemini / codex
- 共享技能：document-templates、doc-coauthoring
- 优先文档：.factory/project.json、AGENTS.md、GEMINI.md
- 写入集合：无
- 当前工作项：无
- 推荐动作：
  - `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch session --project /Users/uroborus/AiProject/shanforge --owner Codex --focus '写集冲突治理'`
  - `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch workbench --project /Users/uroborus/AiProject/shanforge --role memory-manager --owner Codex --focus '写集冲突治理'`

## 审批与边界

- 当前项目暂无待审批票据。
- `项目协调者`：动作：`command-profiles/pre-gate` | 风险：`L2` | 审批：`summary_confirm`；先由主代理申请审批票据。

## Ownership 与冲突

- `项目协调者` | 负责人：项目协调者 | 状态：未分派 | 写入集合：无
- `发布经理` | 负责人：发布经理 | 状态：未分派 | 写入集合：无
- `文档与记忆管理员` | 负责人：文档与记忆管理员 | 状态：未分派 | 写入集合：无

- 当前未发现写集冲突。

## Ownership 提醒

- 当前未发现未分派工作项。

## 最近交接

- 当前暂无角色交接记录。
