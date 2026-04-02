# 多前台适配与多代理协作设计

**文档状态：** MVP 部分已实现  
**主要读者：** 架构师 | 平台维护者 | 脚本维护者 | 协作负责人  
**负责人：** 仓库维护者  
**关联 ID：** `REQ-003`, `REQ-005`, `API-002`, `API-012`, `API-013`  
**最后更新：** 2026-04-02  

## 1. 设计目标

在保持 `CLI-first` 的前提下，让山海工枢能够稳定支撑多个前台宿主，并把多代理协作从“临时并行”升级成“可分工、可观测、可恢复”的正式运行模式。

确认的前提：

- 当前主要前台：`Codex`、`Gemini CLI`
- 长期需要支持更多工具，如 `opencode`
- 多代理协作应服务于工程分工，而不是为了并行而并行

当前已落地的 MVP：

- `config/frontends/codex.json`
- `config/frontends/gemini.json`
- `config/frontends/opencode.json`
- `factory-frontend-capabilities`
- `factory-dispatch frontend-capabilities`
- `factory-chat-bootstrap` 已改为通过前台画像支持 `opencode`
- `factory-multi-agent-board` 已开始展示待审批票据、高风险推荐动作和未分派工作项提醒

当前仍未落地的部分：

- 前台适配层与工作流编排的正式联动
- 多前台回放评估
- 多代理 ownership 与冲突控制的运行时强约束接入

## 2. 前台适配原则

- 不为某个前台重写整套工程协议
- 统一抽象前台能力，而不是统一 prompt 文风
- 前台差异通过 `adapter` 和能力画像解决
- 同一动作在不同前台上尽量保持语义一致

## 3. Frontend Adapter 契约

每个前台适配器都应提供统一能力画像。

### 3.1 最小能力集

| 能力 | 说明 |
|---|---|
| `file_read` | 能读取仓内文件 |
| `file_write` | 能修改仓内文件 |
| `command_exec` | 能运行命令并拿到结构化结果 |
| `tool_call` | 能调用结构化工具或函数 |
| `context_compaction` | 能在长会话中做压缩或摘要 |

### 3.2 可选能力集

| 能力 | 说明 |
|---|---|
| `subagent` | 能派生子代理并接收结果 |
| `mcp` | 能访问 MCP server 或外部工具源 |
| `stream_observation` | 能持续返回中间观察结果 |
| `approval_hook` | 能在高风险动作前等待用户批准 |

### 3.3 能力降级规则

- 如果没有 `subagent`，则退化为单代理串行执行
- 如果没有 `mcp`，则退化为本地文件、脚本和 shell 路径
- 如果没有 `context_compaction`，则加强 `Context Compiler` 的最小上下文策略
- 如果没有 `approval_hook`，则高风险动作只能停在建议状态，不自动执行

## 4. 目标支持的前台

| 前台 | 当前角色 | 长期定位 |
|---|---|---|
| `Codex` | 主前台 | 标准前台之一 |
| `Gemini CLI` | 主前台 | 标准前台之一 |
| `opencode` | 规划接入 | 新前台适配器目标 |

这里的设计不依赖某个前台的私有实现细节，只依赖它是否能暴露前述能力契约。

当前 MVP 状态：

- `Codex`：已登记画像
- `Gemini CLI`：已登记画像
- `opencode`：已登记画像，状态为 `planned`，用于先定义能力边界和降级策略

## 5. 多代理协作模型

### 5.1 角色划分

| 角色 | 主要职责 |
|---|---|
| `planner` | 规划、分解任务、确定关键路径 |
| `explorer` | 收集上下文、定位代码和文档事实 |
| `worker` | 执行具体改动，持有明确写入 ownership |
| `reviewer` | 独立审查变更、发现风险和回归 |
| `qa` | 做验证、复查证据和回归结果 |

### 5.2 协作原则

- 只有可拆分、可隔离的任务才并行
- 写入集合必须明确 ownership
- 审查角色尽量与实现角色分离
- 关键路径任务优先本地主代理处理，不盲目下发
- 多代理结果必须回收到统一证据层

## 6. Ownership 与冲突控制

多代理协作的最低约束：

- 每个 worker 必须声明负责的文件或模块边界
- 不允许多个 worker 无约束地改同一写集
- 若发现写集冲突，应升级为串行或由 planner 重新拆分
- 若子代理返回结果与主线上下文冲突，应优先保守收敛，而不是强行合并

## 7. 多代理观测面

建议把现有 `factory-multi-agent-board` 升级为正式协调面，至少可展示：

- 当前任务分解
- 每个代理的 ownership
- 当前阻塞项
- 最近验证结果
- 待合并风险
- 恢复建议

当前 MVP 状态：

- 已展示当前项目的待审批票据
- 已标记推荐动作中需要主代理审批的高风险注册动作
- 已提醒未分派工作项，避免并行协作时 ownership 漏空
- 已支持在 `factory-role-assign` 中声明显式写入集合，并默认阻断与现有角色分派的写集冲突
- `factory-multi-agent-board` 已开始展示角色 ownership、写集冲突和并行阻断状态
- 尚未覆盖真实子代理提交阶段的隐式写集探测，也不会自动拆分角色职责

## 8. 示例流程

### 8.1 单项目 docs 升级

- `planner`：确认是否已纳管、判断是否需要结构迁移
- `worker`：执行 docs 标准升级动作
- `reviewer`：检查导航、权限和契约页纳入情况
- `qa`：执行最终 `--check`

### 8.2 新前台接入

- `explorer`：识别前台能力是否满足最小契约
- `planner`：选择适配策略和降级路径
- `worker`：补适配器与能力画像
- `qa`：回放关键场景，检查与现有前台是否语义一致

## 9. 安全与恢复

- 多代理协作不应绕过分级自治策略
- 高风险动作仍由主代理持有审批边界
- 子代理失败后必须返回结构化失败模式和恢复建议
- 若前台能力不足，应降级，而不是假装支持

## 10. 与现有山海工枢资产的衔接

| 现有资产 | 新定位 |
|---|---|
| `factory-multi-agent-board` | 多代理调度和观测面的现有入口 |
| `factory-role-sync` / `factory-team-sync` | 团队协作辅助入口 |
| `factory-agent-session` | 主代理的上下文编译入口 |
| `factory-state-doctor` | 多代理收口时的统一健康检查器 |

## 11. 验收标准

- 同一类自然语言请求可以在不同前台宿主中映射到一致的动作语义
- 前台缺失某项能力时，系统能明确降级而不是静默失败
- 多代理协作时能明确写入 ownership 和风险边界
- 多代理输出能统一回收到证据层和项目状态层

## 12. 外部参考

- [claw-code](https://github.com/ultraworkers/claw-code)
- [CLAW.md](https://github.com/ultraworkers/claw-code/blob/main/CLAW.md)
- [Prompt Engineering Guide - Function Calling](https://www.promptingguide.ai/agents/function-calling)

## 13. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-04-02 | 初始版本，定义多前台适配契约、降级策略和多代理协作约束 | Codex |
| 2026-04-02 | 落地前台能力画像配置、查询入口，并让 chat-bootstrap 支持 opencode | Codex |
| 2026-04-02 | 增强 `factory-multi-agent-board`，开始暴露待审批票据、高风险推荐动作和未分派工作项提醒 | Codex |
| 2026-04-02 | 增加显式写集声明、分派冲突默认阻断，以及看板中的 ownership/冲突摘要 | Codex |
