# Hermes Agent 源码与实现原理调研报告

**文档类型：** 外部项目源码调研 / 需求方案输入  
**主要读者：** 项目协调者 | 产品 | 架构师 | 后端维护者 | Agent Runtime 设计者  
**负责人：** Codex  
**状态：** 已确认  
**关联 ID：** `DISC-HERMES-001`  
**最后更新：** 2026-04-13  

## 1. 调研目标与范围

### 1.1 调研目标

本报告面向 `shanforge` 的后续能力演进，分析第三方开源项目 [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) 的源码结构、实现原理和工程取舍，回答以下问题：

1. Hermes Agent 的本质系统定位是什么。
2. 它为什么能同时支持 CLI、消息平台、编辑器接入和长期会话。
3. 它的“自我改进”能力具体是如何在工程上实现的。
4. 其中哪些机制适合作为 `shanforge` 的需求方案参考。

### 1.2 调研范围

- 分析对象：`NousResearch/hermes-agent` GitHub 仓库 `main` 分支源码快照。
- 调研时间：2026-04-13。
- 重点源码范围：
  - `run_agent.py`
  - `agent/`
  - `tools/`
  - `gateway/`
  - `acp_adapter/`
  - `cron/`
  - `hermes_state.py`
  - `hermes_cli/`
- 辅助依据：
  - `README.md`
  - `pyproject.toml`

### 1.3 调研方法

本报告以源码阅读为主，README 只用于核对项目对外宣称的能力边界。由于仓库内关于内核架构的正式文档较少，部分结论属于基于代码路径、调用关系和状态结构得出的实现性判断，而非来自项目作者的显式设计说明。

## 2. 项目概述与核心判断

### 2.1 项目概述

Hermes Agent 是一个面向多模型、多工具、多入口和长期会话的 Agent Runtime。项目在 `pyproject.toml` 中声明的包版本为 `0.8.0`，入口脚本包括：

- `hermes = hermes_cli.main:main`
- `hermes-agent = run_agent:main`
- `hermes-acp = acp_adapter.entry:main`

从对外能力看，它同时覆盖：

- 交互式 CLI
- Telegram、Discord、Slack、WhatsApp、Signal 等消息平台
- ACP 编辑器接入
- MCP 扩展工具
- 定时任务调度
- 子代理委派
- 程序化工具调用
- 跨会话记忆、技能和历史检索

### 2.2 核心判断

Hermes Agent 的本质不是“一个会调工具的聊天机器人”，而是一个统一的 `Agent Runtime`。它的工程核心不在模型本身，而在四个闭环：

1. `主任务执行闭环`：模型、工具、错误恢复和回合控制。
2. `长期状态闭环`：memory、skills、session search、session DB。
3. `上下文控制闭环`：system prompt 稳定化、临时上下文注入、context compression。
4. `多入口分发闭环`：CLI、gateway、cron、ACP 共用同一套 agent 内核。

### 2.3 关键结论

- Hermes 的“self-improving”不是参数训练，而是 `经验外部化`。
- 它把长期学习拆成三类工件：
  - `memory`：声明式事实。
  - `skill`：程序化方法。
  - `session_search`：历史轨迹检索。
- 它的长期可用性依赖两个关键工程点：
  - 稳定 system prompt 与 prompt cache 友好的上下文注入策略。
  - 面向长会话的压缩、分叉和检索机制。
- 它已经从“单代理工具循环”演化为“带状态、带协议适配、带任务管理的 agent 系统”。

## 3. 总体架构

### 3.1 架构分层

Hermes 可以分为六层：

| 层级 | 主要模块 | 主要职责 |
|---|---|---|
| 入口层 | `hermes_cli/`、`gateway/`、`acp_adapter/` | 接收来自终端、消息平台、编辑器的输入 |
| 编排层 | `run_agent.py`、`agent/` | 构造 prompt、驱动主循环、处理重试与回退 |
| 工具层 | `tools/`、`model_tools.py`、`toolsets.py` | 注册、裁剪、调度和执行工具 |
| 状态层 | `hermes_state.py`、memory、skills、todo、checkpoint | 维护长期状态和可恢复上下文 |
| 执行环境层 | `tools/terminal_tool.py`、`tools/environments/` | 统一本地与远程执行后端 |
| 扩展层 | MCP、ACP、plugins、skills | 扩展工具表面和接入协议 |

### 3.2 核心编排中心

系统的绝对中心是 `run_agent.py` 中的 `AIAgent`。它承担以下职责：

- 保存当前运行时配置和 provider 信息。
- 组装 system prompt。
- 维护消息历史。
- 调用模型接口。
- 解析 assistant text 与 tool calls。
- 执行工具调用并将结果回写消息流。
- 管理上下文压缩、fallback、rate limit 恢复、中断和子代理。

换句话说，CLI、Gateway 和 ACP 都只是不同“前台壳”，真正的系统核心仍然是 `AIAgent`。

### 3.3 统一入口，多壳复用

#### CLI

`hermes_cli/main.py` 提供终端产品壳，负责：

- 配置读取
- profile 处理
- 模型选择
- 交互命令
- 会话恢复
- gateway/cron/setup/status 等外围命令入口

#### Gateway

`gateway/run.py` 负责多消息平台适配。平台事件会被标准化为 `SessionSource` 和 `SessionContext`，再交给统一的 `AIAgent` 处理。

#### ACP

`acp_adapter/server.py` 和 `acp_adapter/session.py` 负责把编辑器协议会话映射到 Hermes session。ACP 并不是另一套 agent 逻辑，而是相同内核在编辑器场景下的协议包装。

### 3.4 工具系统架构

Hermes 的工具系统不是把函数直接塞给模型，而是分成三层：

1. `tools/registry.py`
   - 每个工具在 import 时向 registry 注册 schema、handler、toolset、availability check。
2. `model_tools.py`
   - 负责工具发现、tool definition 输出、统一 dispatch、sync/async bridge。
3. `toolsets.py`
   - 负责按场景组装工具集，例如 `web`、`terminal`、`file`、`browser`、`delegation`、`hermes-acp`。

这种设计使 Hermes 具备两个重要特性：

- 工具可按入口裁剪，而非全量暴露。
- MCP、插件和内建工具可以进入同一个统一调用面。

### 3.5 状态系统架构

Hermes 的状态不是单一对象，而是多个互相配合的长期工件：

| 状态类型 | 存储方式 | 用途 |
|---|---|---|
| Session transcript | SQLite `sessions/messages/messages_fts` | 长期会话、检索、恢复、统计 |
| Memory | `~/.hermes/memories/MEMORY.md`、`USER.md` | 持久化声明式事实 |
| Skills | `~/.hermes/skills/` | 持久化程序化经验 |
| Todo | 内存 + 对话恢复 | 当前任务规划 |
| Checkpoint | 工作目录快照 | 文件变更前保护 |
| Tool result storage | 工具级预算与裁剪 | 控制返回上下文体积 |

状态层的一个关键思想是：`把“模型记住的东西”变成“系统能管理的工件”`。

### 3.6 扩展架构

#### MCP

`tools/mcp_tool.py` 会读取配置中的 MCP server，动态发现外部工具并注册到 Hermes 工具表面中。这样外部能力和内建能力在模型视角下是统一的。

#### ACP

ACP 层除了转发消息，还能把编辑器提供的 MCP servers 注入当前 session，实现“编辑器上下文 + Hermes 工具系统”的融合。

#### Skills

skills 不是插件代码，而是结构化文档型能力资产，兼顾：

- 过程性知识
- 用户偏好
- 可读性
- 可被 agent 自行修补

## 4. 核心算法与实现机制

### 4.1 Agent 主循环

Hermes 的主循环可概括为：

1. 准备消息历史与当前轮输入。
2. 构造 system prompt 与临时上下文。
3. 生成 API 请求。
4. 调用模型。
5. 解析 assistant 响应。
6. 若有 tool calls，则执行工具。
7. 把 tool results 追加为后续输入。
8. 重复直到得到最终回答或达到预算/中断条件。

这是一种强化版的 ReAct / tool-calling loop，但比典型实现多了：

- 工具修复
- 并行调度
- context overflow 恢复
- prompt cache 友好的 system prompt 管理
- 背景 review 和长期状态同步

### 4.2 System Prompt 组装算法

Hermes 将 system prompt 拆成稳定层和临时层。

#### 稳定层

`_build_system_prompt()` 组装以下内容：

1. 身份层：优先 `SOUL.md`，否则默认 identity。
2. 工具行为规则：如 memory/session_search/skills 的使用指导。
3. 特定模型的 tool-use enforcement 与执行纪律。
4. 当前 session 的 memory snapshot。
5. external memory provider 的 system prompt block。
6. skills 索引。
7. 项目上下文文件：
   - `.hermes.md` / `HERMES.md`
   - `AGENTS.md`
   - `CLAUDE.md`
   - `.cursorrules`
8. 当前时间、模型、provider、平台环境提示。

#### 临时层

当前轮才会注入：

- memory provider prefetch 的 recall block
- plugin 的 pre_llm_call 上下文

这些内容只参与本轮 API 调用，不会直接改写持久消息历史，也不会改变缓存 system prompt。

#### 设计价值

该策略解决了两个常见问题：

1. 避免 system prompt 每轮漂移，提升 cache 命中率。
2. 避免短期上下文污染长期 session transcript。

### 4.3 工具治理算法

Hermes 的工具治理不是“模型说调什么就调什么”，而是包含一整套防御逻辑：

#### 工具名修复

若模型输出不存在的工具名，系统会尝试：

- 小写化
- 连字符/空格归一化为下划线
- 模糊匹配

这降低了模型输出近似工具名时的失败率。

#### 参数 JSON 校验

工具调用参数不是直接相信，而是先做 JSON 校验。若参数为空字符串，会自动修复为 `{}`。若明显因截断导致 JSON 残缺，系统会拒绝执行并要求继续生成或终止为 partial。

#### 重复调用去重

同一轮内若模型输出相同 `(tool_name, arguments)` 的重复调用，系统会去重。

#### delegation 限流

即使模型一轮内发出多个 `delegate_task` 调用，也会被限制在配置上限之内。

#### 并行判定

Hermes 不会盲目并发所有工具。只读工具或路径独立的文件工具才进入并行执行路径；交互式或带共享副作用的工具则走串行路径。

### 4.4 子代理委派算法

`delegate_task` 的核心不是“再创建一个 agent”，而是“创建一个受控 worker”：

- 子代理使用新的 `task_id`。
- 拥有独立 conversation。
- 默认继承有限工具集。
- 显式禁止：
  - 再次 delegation
  - clarify
  - memory
  - send_message
  - execute_code

这说明 Hermes 对子代理的定位不是“复制主代理”，而是“让子代理在受约束的执行面上完成聚焦任务”。

### 4.5 程序化工具调用算法

`execute_code` 是 Hermes 的一个重要差异点。

它允许模型输出一个 Python 脚本，由该脚本通过 `hermes_tools.py` stub 对父进程发起 RPC 工具调用。这样复杂任务可以从：

- 多轮“思考 -> 调工具 -> 读结果 -> 再调工具”

压缩成：

- 一轮生成程序
- 程序内部多次工具调用
- 最终只把程序 stdout 返回给模型

其价值在于：

- 降低 token 往返成本
- 减少中间 tool results 进入上下文窗口
- 让复杂多步操作转为程序控制流

### 4.6 上下文压缩算法

Hermes 的 context compression 不是简单删除历史，而是有结构的：

1. 先清理旧 tool outputs。
2. 保护首部消息。
3. 保护最近尾部消息。
4. 仅对中间部分做摘要。
5. 生成 handoff summary。
6. 重新构造 message list。

其摘要前缀明确声明：

- 这是压缩交接摘要。
- 仅作为背景参考。
- 不应被当作仍待执行的指令。

这类提示是为了防止模型把旧需求误当作当前仍需执行的任务。

### 4.7 Session Split 算法

压缩完成后，Hermes 不是简单覆盖原 session，而是：

1. 结束旧 session。
2. 新建一个新 session。
3. 将旧 session id 写入 `parent_session_id`。
4. 把压缩后的消息写入新 session。

这个设计的价值是：

- 保留 lineage
- 保留压缩前的完整历史
- 允许搜索和追踪“压缩前后”两段会话关系

### 4.8 历史检索算法

`session_search` 的处理链路是：

1. 在 SQLite FTS5 中搜索消息内容。
2. 按 session 聚合高相关结果。
3. 加载相关 session transcript。
4. 用 cheap/fast auxiliary model 做聚焦摘要。
5. 返回针对当前问题相关的历史结论。

这意味着 Hermes 区分了两种长期知识来源：

- 明确值得长期保留的 memory / skill
- 不值得固化但可能未来有用的历史对话

### 4.9 经验沉淀算法

Hermes 的自我改进不是自动改代码，而是自动沉淀经验。

#### Memory flush

在 compression 之前，系统会给模型一次短回合机会，让它把值得保留的信息写入 memory，避免摘要后丢失。

#### Background review

当达到 memory/skill nudge 条件后，系统会 fork 一个后台 review agent，用专门 prompt 检查：

- 用户偏好、约束、风格是否值得写入 memory
- 本轮方法是否值得新建或修补 skill

因此 Hermes 的 self-improving 更接近：

`轨迹反思 -> 工件更新 -> 后续复用`

而不是在线微调。

### 4.10 辅助模型与回退机制

Hermes 将部分旁路任务交给 auxiliary client：

- compression
- session search
- vision
- web extract
- memory flush

辅助模型可以与主模型不同，从而降低成本。

同时，主循环还带有一套比较完整的恢复策略：

- rate limit 等待与退避
- provider fallback
- context limit 探测
- 输出 token 上限缩减
- long-context tier 降级
- transport recovery

这使 Hermes 更像一个“长期运行的服务”，而不是一次性脚本。

## 5. 关键数据结构

### 5.1 SQLite SessionDB

`hermes_state.py` 中的 SQLite 状态层是核心基础设施。

#### `sessions` 表

存储：

- `id`
- `source`
- `model`
- `model_config`
- `system_prompt`
- `parent_session_id`
- token 与 cost 统计
- title 与生命周期字段

#### `messages` 表

存储逐条消息，包含：

- `role`
- `content`
- `tool_call_id`
- `tool_calls`
- `tool_name`
- `finish_reason`
- `reasoning`
- `reasoning_details`
- `codex_reasoning_items`

#### `messages_fts`

FTS5 虚拟表，用于全文检索。

### 5.2 Message 结构

Hermes 的消息不仅有 `user/assistant/tool/system` 基本角色，还携带：

- tool call 元数据
- reasoning 内容
- finish reason
- Codex 响应式推理项

说明 Hermes 的消息流已经不是简单 chat transcript，而是包含执行轨迹与推理恢复信息的结构化日志。

### 5.3 ToolEntry 与 ToolRegistry

`ToolEntry` 主要字段包括：

- `name`
- `toolset`
- `schema`
- `handler`
- `check_fn`
- `requires_env`
- `is_async`
- `description`
- `emoji`
- `max_result_size_chars`

这使每个工具都具备：

- 被模型调用的 schema
- 被系统调度的 handler
- 被入口裁剪的能力分组
- 被环境检查的可用性门禁

### 5.4 MemoryStore

`MemoryStore` 的一个关键设计是双态：

- `_system_prompt_snapshot`
  - session 启动时冻结，用于 system prompt。
- `memory_entries / user_entries`
  - 运行时实时更新并落盘。

这意味着：

- 当前 session 内，memory 写入立即 durable。
- 但不会立刻改变 prompt，从而保持缓存稳定。

### 5.5 Skill 目录结构

skill 本质上是一个目录化文档包：

- `SKILL.md`
- `references/`
- `templates/`
- `scripts/`
- `assets/`

这使 skill 可以同时承载：

- 说明
- 支撑材料
- 模板
- 可执行脚本

也说明 Hermes 把“经验”建模成“可维护的文件系统对象”。

### 5.6 SessionContext 与 SessionSource

Gateway 中的 `SessionSource` 和 `SessionContext` 用于表达：

- 来自哪个平台
- 哪个 chat / thread / user
- 哪些平台已连接
- 哪些 home channels 可用

这是 Hermes 能在消息平台里做 `origin delivery`、`home delivery` 和多平台协作的基础。

### 5.7 ACP SessionState

ACP 的 `SessionState` 存储：

- `session_id`
- `agent`
- `cwd`
- `model`
- `history`
- `cancel_event`

这说明编辑器接入被视为“同一个 agent 系统中的另一种 session 形态”，而不是外挂插件。

### 5.8 ContextEngine 抽象

`ContextEngine` 定义了：

- `should_compress`
- `compress`
- `update_from_response`
- `on_session_start`
- `on_session_end`
- `get_tool_schemas`
- `handle_tool_call`

默认实现是 `ContextCompressor`，但抽象层表明项目作者希望未来可替换为其他上下文管理引擎。

## 6. 运行时流程

### 6.1 CLI 流程

CLI 的典型运行流程如下：

1. 读取 profile 与 config。
2. 解析当前 provider/model。
3. 初始化 `AIAgent`。
4. 加载历史 session。
5. 用户输入进入 `run_conversation()`。
6. 若返回流式 delta，则交给 TUI 渲染。
7. 完成后更新 SQLite、memory、skills review 状态。

CLI 是最完整的产品壳，也是其他入口的能力参考基准。

### 6.2 Gateway 流程

Gateway 的运行流程大致如下：

1. 各平台适配器收消息。
2. 构造 `SessionSource`。
3. 生成或查找 `SessionContext`。
4. 创建新的 `AIAgent` 实例处理这条消息。
5. 流式输出通过 `GatewayStreamConsumer` 发送到平台。
6. 需要时支持 interrupt、busy handling、follow-up delivery。

这里的一个重要取舍是：

- Gateway 往往“每条消息新建一个 AIAgent 实例”。
- 但长期 session 状态不靠 agent 实例内存，而靠 SQLite、memory 文件和其他持久状态恢复。

### 6.3 流式输出流程

`GatewayStreamConsumer` 的职责是：

- 接收同步回调中的 token delta
- 放入线程安全队列
- 在异步任务中节流、缓冲和编辑平台消息

其设计说明 Hermes 非常重视跨平台“连续感”，而不是只在模型结束后一次性输出。

### 6.4 Cron 流程

Cron 的流程是：

1. scheduler 定期 tick。
2. 查找 due jobs。
3. 为 job 启动 agent 执行。
4. 结果存档。
5. 根据 `deliver` 策略把结果投递回：
   - `local`
   - `origin`
   - `platform`
   - `platform:chat_id`

这意味着 cron 不是单独的自动化系统，而是“用同一内核做无人值守调用”。

### 6.5 ACP 流程

ACP 侧的运行流程是：

1. 编辑器初始化 ACP 会话。
2. Hermes 创建 session 并绑定 `cwd`。
3. 编辑器发 prompt。
4. ACP server 在后台线程里运行 `AIAgent`。
5. tool start / progress / complete 被转为 ACP tool call events。
6. session 持久化到同一个 SessionDB。

该设计的价值在于：

- 编辑器会话与 CLI/Gateway 会话共享同一套状态能力。
- ACP 并未引入第二套 agent core。

## 7. 工程优势与主要风险

### 7.1 主要优势

#### 优势一：系统化完整

Hermes 已经把 agent 所需的核心运行时要素做全：

- 会话
- 工具
- 状态
- 压缩
- 协议
- 调度
- 回顾学习

#### 优势二：长期状态设计成熟

它没有把长期能力寄托在模型上下文，而是外部化为 memory、skills、session search、session DB。

#### 优势三：多入口统一

CLI、Gateway、Cron、ACP 共用一个内核，避免能力碎片化。

#### 优势四：上下文治理强

prompt 稳定化、context compression、session split 和历史检索形成了较完整的长会话治理体系。

### 7.2 主要风险

#### 风险一：编排层过重

`run_agent.py` 已接近超大编排器。虽然内部已分拆出多个模块，但大量全局运行时逻辑仍集中在主文件中，维护门槛高。

#### 风险二：状态一致性复杂

系统同时维护：

- agent 实例状态
- SQLite session
- memory 文件
- skills 文件
- tool result budget
- gateway session store

一旦后续继续扩展，状态一致性和边界会变得更脆弱。

#### 风险三：文档弱于实现

项目 README 偏产品说明，内核设计主要靠代码阅读恢复。对二次维护者而言，理解成本较高。

#### 风险四：入口壳增多后回归复杂

CLI、Gateway、ACP、Cron 共用内核虽是优势，但任何主循环变更都可能影响所有前台壳，回归测试要求高。

## 8. 对 shanforge 的需求方案启发

### 8.1 可直接借鉴的能力

#### 借鉴一：稳定 system prompt + 当前轮临时注入

这是 Hermes 最值得借鉴的设计之一。对于 `shanforge` 而言，可复用为：

- 会话级稳定上下文
- 当前任务级临时上下文
- memory 检索结果不直接污染历史

#### 借鉴二：状态外部化

将以下能力从“模型记忆”转为“系统工件”：

- 用户偏好
- 任务方法
- 历史会话
- 调度状态

这比单纯堆积上下文更适合工程化维护。

#### 借鉴三：ContextEngine 抽象

若 `shanforge` 后续要做压缩、摘要、工作台视图或任务图谱，建议一开始就把上下文管理抽象成可替换接口，而不是把压缩写死在主循环里。

#### 借鉴四：工具注册层

应采用 registry + toolset 的能力管理方式，避免入口层直接拼装工具列表。

### 8.2 适合谨慎借鉴的能力

#### 谨慎项一：超大单文件编排器

Hermes 的成功不代表 `run_agent.py` 的体量值得复制。`shanforge` 更适合在早期就把：

- API 调用
- 消息规整
- tool governance
- recovery policy
- background review

拆为独立 orchestrator/service 层。

#### 谨慎项二：过早做全平台入口

Hermes 已完成 CLI、gateway、ACP、cron 的统一，但这是一条高投入路线。`shanforge` 若尚未稳定主循环，不应过早分散到多入口。

### 8.3 现阶段推荐采纳顺序

建议 `shanforge` 按以下顺序吸收 Hermes 的设计：

1. `AIAgent 主循环 + ToolRegistry`
2. `SessionDB + session_search`
3. `memory + skills`
4. `ContextEngine + compression`
5. `delegate_task / execute_code`
6. `gateway / cron / ACP`

该顺序的原则是：先把 `内核` 和 `状态` 做对，再做入口扩展。

## 9. 复刻建议

### 9.1 最小可行版本

若以 Hermes 为参考复刻一个最小可用系统，建议第一版只实现：

- 单入口 CLI
- `AIAgent` 主循环
- `ToolRegistry`
- `terminal`、`read_file`、`write_file`、`search_files`、`web_search`
- SQLite session storage
- 简化版 context compressor

这一阶段的目标不是功能齐全，而是建立可持续迭代的 runtime 骨架。

### 9.2 第二阶段

第二阶段补长期状态与方法沉淀：

- `MEMORY.md`
- `USER.md`
- skill 目录系统
- FTS5 session search
- prompt cache 友好的 memory 注入

这是从“会做事”升级为“会积累经验”的关键一步。

### 9.3 第三阶段

第三阶段补高级执行能力：

- delegation
- execute_code
- checkpoint
- background review

这一阶段的目标是降低复杂任务的回合成本，提高长任务完成率。

### 9.4 第四阶段

第四阶段补多入口与外部协议：

- messaging gateway
- cron scheduler
- ACP
- MCP

此时系统才真正具备 Hermes 风格的“统一 agent runtime”能力。

### 9.5 工程建议

复刻时建议坚持以下原则：

1. 将“长期知识”外部化，不依赖模型自然记住。
2. 将“当前轮检索结果”作为临时注入，而不是永久写进 transcript。
3. 为 context overflow、rate limit 和 provider fallback 提前设计恢复路径。
4. 不要把所有 orchestrator 逻辑都堆在一个文件里。
5. 在入口扩张之前，先保证主循环、状态层和压缩层稳定。

## 10. 结论

Hermes Agent 的技术价值不在于“它支持多少平台”，而在于它已经把 Agent 系统中最难工程化的部分组合到一起：

- 主循环可持续运行
- 长期状态可管理
- 上下文可压缩可检索
- 多入口共享同一内核
- 经验可以被系统性沉淀

对于 `shanforge` 来说，这份调研最重要的结论不是“照搬 Hermes”，而是：

`应优先建设统一 agent runtime 与状态系统，再决定前台壳和平台接入形态。`

Hermes 提供的是一套值得参考的工程路线图，而不是必须逐项复制的产品清单。

## 附录 A：建议重点阅读的源码入口

| 入口 | 作用 |
|---|---|
| `run_agent.py` | 核心编排与主循环 |
| `agent/prompt_builder.py` | system prompt 组装 |
| `agent/context_compressor.py` | 上下文压缩 |
| `agent/memory_manager.py` | memory provider 协调 |
| `model_tools.py` | 工具发现与调度 |
| `tools/registry.py` | 工具注册中心 |
| `tools/delegate_tool.py` | 子代理委派 |
| `tools/code_execution_tool.py` | 程序化工具调用 |
| `hermes_state.py` | SQLite session 存储 |
| `gateway/run.py` | 消息平台入口 |
| `gateway/session.py` | gateway session 上下文 |
| `acp_adapter/server.py` | ACP 编辑器接入 |
| `cron/scheduler.py` | 定时任务调度 |

## 附录 B：术语解释

- **Memory**：长期声明式事实，不等于完整历史。
- **Skill**：可复用方法，不等于一般性记忆。
- **Session Search**：从历史 transcript 中召回上下文。
- **Context Compression**：压缩历史消息，不是删除 session。
- **Session Split**：压缩后新建 continuation session，并保留 lineage。
- **Auxiliary Model**：用于旁路任务的廉价或快速模型，不一定等于主模型。
- **Gateway**：消息平台接入层。
- **ACP**：编辑器 Agent Client Protocol 接入层。
- **MCP**：外部工具或上下文能力接入协议。
