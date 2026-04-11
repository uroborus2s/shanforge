# AI 软件工厂规则

默认不要散读整仓文档。

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

补充协议：
- `skills/software-factory-cli/references/ai-runtime-protocol.md`
- `skills/software-factory-cli/references/ai-role-charter.md`

规则：
- 默认只读压缩入口、项目事实和 summary。
- 当用户直接输入 `/技能名` 或消息以 `/技能名` 开头时，禁止把它理解成“查看技能定义”；必须把它理解成“立即使用该 skill 执行默认工作流”。
- 对 slash 触发的 skill，禁止只回复“已收到 skill”或“如果需要再告诉我”；必须直接进入该 skill 的首个可执行步骤。
- 若 slash 触发的 skill 涉及潜在破坏性动作，且用户未明确授权，则先执行该 skill 的非破坏性默认步骤，再在真正执行高风险动作前确认。
- 当用户明确写出“提交 / commit / 执行提交”时，视为已授权执行本地 `git commit`；禁止在没有具体阻塞原因的情况下停在摘要阶段。
- 禁止把“正在执行”“准备执行”或占位文本描述成已经完成的结果；只有观察到真实命令结果后，才能报告成功状态。
- 当用户原始消息已明确要求执行某个可落地动作时，优先在同一轮内完成并返回最终结果；禁止先交付中间态，再等用户下一轮重复要求。
- 禁止默认把阶段 `docs/` 文档列入“先读”。
- 禁止每次开工都去读 `project-charter.md`、`input.md`、`user-guide.md` 或其他人类长文。
- 禁止跳过 `.factory/memory/*` 直接回源正式文档。
- 禁止把 skill 当成命令目录；命令执行统一走 `factory-dispatch`、`action-registry` 和 `scripts/factory-*`。
- `AGENTS.md` / `GEMINI.md` 只保留稳定协作入口，不写安装结果、测试状态或当天运行结论。
- 只在解释背景、方案原理、核对正式事实或用户明确要求时，才按 `doc-map.md` 单文件读取相关 `docs/*.md`。
- 代码类工作必须走 PR 闭环。
- 变更必须同步代码、文档、测试、`.factory/memory/`。
