# shanforge Agent 规则

- 项目：`shanforge`，根目录：`.`。
- 先根据当前消息判定处理模式。无项目影响的直接回答和轻量分析不读取 `.factory/memory/`，不创建任务卡、ledger 或项目状态包。
- 项目状态查询、任务延续、项目事实修改或仓内持久化才进入项目化流程：默认先读 `.factory/memory/agent-session.md`；缺上下文再读 `.factory/memory/runtime-brief.md`、`.factory/memory/current-state.md`、`.factory/memory/doc-map.md`、`.factory/project.json` 和相关 summary。正式事实按 `doc-map.md` 单文件回源，不散读 `docs/`。
- 会话恢复：`skills/project-memory/SKILL.md`。流程路由、review gate、人工确认、提交门：`skills/using-shanforge/SKILL.md`。
- 已授权 `source_or_test_write` worker 与身份、范围完整的独立只读 reviewer 必须按模型派发合同子代理执行；主会话不得静默实现或代替 reviewer。Codex `spawn_agent` 参数、回执和失败关闭规则：`skills/using-shanforge/SKILL.md` 与 `skills/using-shanforge/references/codex-tools.md`；已批准计划的隔离 worker 实现：`skills/subagent-driven-development/SKILL.md`。
- `/技能名` 直接执行默认工作流；高风险动作真正执行前确认。
- 明确执行请求优先同轮落地；本地提交用 `gitcommitzh`，只提交当前任务范围。
- 只按真实命令和文件结果报告；禁止把计划、占位或进行中说成完成。
- 禁止恢复旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。
- `AGENTS.md` / `GEMINI.md` 只放稳定入口，不写当天状态、安装结果或测试结论。

## 架构底线

- Shanforge 是 `skill-first` 工程协作资产，不提供仓内 `src/` 平台运行时。
- 可重复、确定性的辅助能力放在所属 skill 的 `scripts/`，优先只用标准库。
- 目标项目只保存自己的代码、正式文档和 `.factory/` 事实；不得依赖 Shanforge 源码路径、虚拟环境或本机绝对路径。
- `scripts/` 只放仓库级同步工具，不承载软件工厂流程主控。
- skill、目录或执行入口变化时，同步用户指南、测试和 `.factory/memory/`；事实冲突先修事实源。
