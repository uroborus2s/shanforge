# Gemini 项目说明

默认先读压缩入口，不要全文加载长篇说明。

项目根目录：`.`
项目名称：`shanforge`

优先读取顺序：
- `.factory/memory/runtime-brief.md`
- `.factory/memory/role-charter.project.md`
- `.factory/memory/doc-map.md`
- `.factory/project.json`
- `.factory/memory/current-state.md`
- `.factory/memory/motivation-state.md`
- `.factory/memory/autonomy-rules.md`
- `.factory/memory/evolution-baseline.md`
- 相关 summary 文档
- 必要时按 `doc-map.md` 单文件回源正式文档

全局补充协议：
- `skills/software-factory-cli/references/ai-runtime-protocol.md`
- `skills/software-factory-cli/references/ai-role-charter.md`

Gemini 默认职责：
- 需求、分析、架构、影响分析、复核

规则：
- 默认只读压缩入口、项目事实和 summary。
- 当用户直接输入 `/技能名` 或消息以 `/技能名` 开头时，禁止把它理解成“查看技能定义”；必须把它理解成“立即使用该 skill 执行默认工作流”。
- 对 slash 触发的 skill，禁止只回复“已收到 skill”或“如果需要再告诉我”；必须直接进入该 skill 的首个可执行步骤。
- 若 slash 触发的 skill 涉及潜在破坏性动作，且用户未明确授权，则先执行该 skill 的非破坏性默认步骤，再在真正执行高风险动作前确认。
- 当用户明确写出“提交 / commit / 执行提交”时，视为已授权执行本地 `git commit`；禁止在没有具体阻塞原因的情况下停在摘要阶段。
- 禁止默认把阶段 `docs/` 文档列入“先读”。
- 禁止每次开工都去读 `project-charter.md`、`input.md`、`user-guide.md` 或其他人类长文。
- 禁止跳过 `.factory/memory/*` 直接回源正式文档。
- 禁止把 skill 当成命令目录；命令执行统一走 `factory-dispatch`、`action-registry` 和 `scripts/factory-*`。
- `AGENTS.md` / `GEMINI.md` 只保留稳定协作入口，不写安装结果、测试状态或当天运行结论。
- 编写需求后，如 summary 不足，再单文件回源 `requirements-verification.md`。
- 进入实现前必须单文件回源 `technical-selection.md`。
- 需要视觉交付时，先读设计相关 summary，不足时再回源 `ux-ui-design.md` 和设计资产。
