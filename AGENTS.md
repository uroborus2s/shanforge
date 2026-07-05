# shanforge Agent 规则

- 项目根目录：`.`；项目名：`shanforge`。
- 默认先读 `.factory/memory/agent-session.md`；不足时再按需读 `.factory/memory/runtime-brief.md`、`.factory/memory/current-state.md`、`.factory/memory/doc-map.md`、`.factory/project.json` 和相关 summary。
- 不默认散读 `docs/`、旧用户指南或长篇背景；需要正式事实时，按 `.factory/memory/doc-map.md` 单文件回源。
- 会话恢复用 `skills/project-memory/SKILL.md`；流程路由只由 `skills/using-shanforge/SKILL.md` 判断。工作 skill 只回写 `status`、`outputs`、`evidence`、`needs`。
- `/技能名` 表示立即执行该 skill 的默认工作流，不是查看说明；高风险动作先做非破坏性步骤，真正执行前再确认。
- 用户明确要求执行的可落地动作，优先同轮完成。用户写出“提交 / commit / 执行提交”即视为授权本地提交；提交必须使用 `gitcommitzh`，且只提交当前任务范围。
- 只有观察到真实命令或文件结果后，才能报告成功；禁止把“正在执行”或占位文本说成完成。
- 禁止恢复旧中心命令、动作注册表、`factory-*` 脚本或旧全局流程脚本作为主控。
- `AGENTS.md` / `GEMINI.md` 只保留稳定协作入口，不写当天状态、安装结果或测试结论。
- 代码类工作必须经过验证、独立 review、人工确认和提交 / PR 闭环；已接受变更同步代码、文档、测试和 `.factory/memory/`。

## 架构硬规则

- 正式依赖链：`access -> application -> domain -> runtime -> settings`。
- `src/` 顶层只允许 `access`、`application`、`domain`、`runtime`、`settings`；禁止恢复 `adapters`、`storage`、`bootstrap` 作为正式代码根。
- 职责边界：`access` 做协议入口；`application` 做 use case 编排；`domain` 拥有业务规则；`runtime` 提供通用能力；`settings` 实现、桥接和装配。
- 接口由调用下层的一方定义：`src/access/ports/`、`src/application/ports/`、`src/domain/*/ports.py`、`src/runtime/ports/`；`settings` 只实现上层 port。
- 跨层装配只在 `src/settings/composition/`；仓内不重建 resolver、loader、registry、factory、manifest 等 DI 内核，反射注册交给 `shanforge-di`。
- 新能力先补契约、治理、证据和错误语义；高风险能力必须经过 approval、sandbox 和 evidence 约束。
- 涉及实现或分层变更时，按需回源 `technical-selection.md`、`system-architecture.md`、`module-boundaries.md`、`architecture-layer-code-mapping.md`；涉及基础能力层或基础设置层时再读对应设计文档。
- 分层、目录或接口 owner 变化时，同步设计文档、测试和 `.factory/memory/`；若正式文档与代码冲突，先修事实源。
