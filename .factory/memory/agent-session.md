# Agent 会话卡

- 生成时间：2026-04-12 01:10:24
- 会话负责人：Codex
- 项目名称：shanforge
- 当前阶段：MAINTENANCE
- 当前模式：cli_direct
- 当前焦点：验证 /gitcommitzh 直执行语义
- 活跃工作项：0
- 阻塞项：0
- 开放风险：0
- 最近发布包：无
- 最近交接包：无
- 最近快照：无

## 先读

- `.factory/memory/runtime-brief.md`
- `.factory/memory/role-charter.project.md`
- `.factory/memory/doc-map.md`
- `.factory/project.json`
- `.factory/memory/project-index.md`
- `.factory/memory/current-state.md`
- `.factory/memory/agent-session.md`
- `.factory/memory/motivation-state.md`
- `.factory/memory/autonomy-rules.md`
- `.factory/memory/evolution-baseline.md`
- `.factory/memory/tech-stack.summary.md`
- `.factory/memory/design-assets.summary.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/change-summary.md`

## 当前角色与规则

- `项目协调者` | 工具：codex / gemini
- `发布经理` | 工具：gemini / codex
- `文档与记忆管理员` | 工具：gemini / codex
- 当前技术画像未额外要求专用 skills。
- 默认只读 `.factory/memory/*`、`.factory/project.json` 和规则入口。
- 当用户直接输入 `/技能名` 时，将其视为立即调用该 skill 的默认工作流，而不是展示 skill 定义。
- slash 触发的 skill 禁止只回复“已收到 skill”之类的占位文本，必须直接进入首个可执行步骤。
- 禁止把 `docs/` 阶段文档当作默认先读清单。
- 只有当 `.factory/memory/` 无法支撑当前任务时，才允许按 `doc-map.md` 单文件回源正式文档。
- 当前默认补充读取：`.factory/memory/motivation-state.md`、`.factory/memory/autonomy-rules.md`、`.factory/memory/evolution-baseline.md`
- 当前无项目锁。

## 当前关注项

- 当前无活跃工作项。
- 当前无阻塞工作项。
- 当前无开放风险。

## 正式事实回源候选

- `docs/04-project-development/08-operations-maintenance/operations-runbook.md`：就绪，已具备实质内容
- `docs/02-user-guide/user-guide.md`：就绪，已具备实质内容
- `docs/04-project-development/09-evolution/retrospective.md`：就绪，已具备实质内容
- `docs/04-project-development/10-traceability/requirements-matrix.md`：就绪，已具备实质内容

## 最近记录

- 2026-04-03: 创建 intent 审批票据 `IA-20260403192712-commandprofi-e79541`，动作 `command-profiles`，项目 `/var/folders/zt/9v3d_j0x747348s_5wdxw5j00000gn/T/tmpf18eopm9/managed-project`。
- 2026-04-03: 执行状态诊断，范围：docs，结果：未通过，负责人：项目医生。
- 2026-04-07: 生成项目压缩入口文档并刷新 `AGENTS.md` / `GEMINI.md`，负责人：Codex，备注：tighten-ai-runtime-boundary。

## 下一步命令

- `python3 scripts/factory-dispatch board --project "." --owner "Codex" --focus "验证 /gitcommitzh 直执行语义"`
- `python3 scripts/factory-dispatch release --project "." --owner "Codex"`
- `python3 scripts/factory-dispatch handover --project "." --owner "Codex"`
- `python3 scripts/factory-dispatch motivation --project "." --owner "Codex" --focus "验证 /gitcommitzh 直执行语义"`
- `python3 scripts/factory-dispatch evolution --project "." --owner "Codex" --note "验证 /gitcommitzh 直执行语义"`
