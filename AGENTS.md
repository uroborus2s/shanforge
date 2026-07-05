# shanforge Agent 规则

- 项目：`shanforge`，根目录：`.`。
- 默认只读 `.factory/memory/agent-session.md`；缺上下文再读 `.factory/memory/runtime-brief.md`、`.factory/memory/current-state.md`、`.factory/memory/doc-map.md`、`.factory/project.json` 和相关 summary。正式事实按 `doc-map.md` 单文件回源，不散读 `docs/`。
- 会话恢复：`skills/project-memory/SKILL.md`。流程路由、review gate、人工确认、提交门：`skills/using-shanforge/SKILL.md`。
- `/技能名` 直接执行默认工作流；高风险动作真正执行前确认。
- 明确执行请求优先同轮落地；本地提交用 `gitcommitzh`，只提交当前任务范围。
- 只按真实命令和文件结果报告；禁止把计划、占位或进行中说成完成。
- 禁止恢复旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。
- `AGENTS.md` / `GEMINI.md` 只放稳定入口，不写当天状态、安装结果或测试结论。

## 架构底线

- 依赖链：`access -> application -> domain -> runtime -> settings`；`src/` 顶层只允许这 5 个目录。
- 职责：`access` 入站，`application` 编排，`domain` 业务规则，`runtime` 通用能力，`settings` 实现与装配。
- 接口由调用下层的一方定义；`settings` 只实现上层 port。跨层装配只在 `src/settings/composition/`。
- 仓内不重建 DI 内核；resolver / loader / registry / factory / manifest 交给 `shanforge-di`。
- 分层、目录或接口 owner 变化时，同步设计文档、测试和 `.factory/memory/`；事实冲突先修事实源。
