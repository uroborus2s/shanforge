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

## `v2` 架构与编码硬规则

这些规则适用于所有开发子 agent；除非用户明确要求推翻当前架构，否则禁止绕过。

### 架构事实源

- 进入实现前，至少核对：
  - `docs/04-project-development/04-design/technical-selection.md`
  - `docs/04-project-development/04-design/system-architecture.md`
  - `docs/04-project-development/04-design/module-boundaries.md`
  - `docs/04-project-development/04-design/architecture-layer-code-mapping.md`
- 涉及基础能力层时，再读：
  - `docs/04-project-development/04-design/basic-capability-layer-design.md`
- 涉及基础设置层时，再读：
  - `docs/04-project-development/04-design/infrastructure-layer-design.md`

### 六层口径不可破坏

- 正式依赖链只有一条：`access -> application -> domain -> runtime -> settings`。
- 用户界面层主要在仓外；本仓正式代码顶层只允许：`src/access`、`src/application`、`src/domain`、`src/runtime`、`src/settings`。
- 禁止重新引入顶层 `src/adapters`、`src/storage`、`src/bootstrap` 作为正式代码根。
- 新代码必须先判断“属于哪一层”，再判断“属于哪一个领域”，最后才决定文件落点。

### 每层职责不可混写

- `access` 只做协议绑定、请求归一化、响应输出和入口收口。
- `application` 只做 use case 编排，不写业务规则，不直接选择 provider/store 实现。
- `domain` 是业务逻辑 owner；workflow、memory、capability、approval、delegation、response 等语义必须收口到领域层。
- `runtime` 只提供通用技术能力与统一能力语义，不拥有业务决策。
- `settings` 只提供真实实现、桥接和装配，不得主导业务编排或业务规则分支。

### 接口 owner 规则

- 谁调用下层，谁定义接口；禁止重新引入统一 `ports_layer`。
- `src/access/ports/` 属于 access。
- `src/application/ports/` 属于 application。
- `src/domain/*/ports.py` 属于 domain。
- `src/runtime/ports/` 属于 runtime。
- `settings` 只能实现上层声明的 port，不能反向定义上层业务接口。

### `src/settings/` 归并规则

- 基础设置层唯一正式代码根是 `src/settings/`。
- 当前层内正式实现领域包括：
  - `model`
  - `memory`
  - `session`
  - `skills`
  - `workspace`
  - `approval`
  - `delegation`
  - `gateway`
  - `capability_registry`
  - `hermes`
- `composition`、`shared` 是层内支撑模块，不是新的架构层，也不是业务领域。
- 新增基础设置实现时，优先放进现有领域目录；只有现有领域无法承载时，才能新增 `src/settings/<new-domain>/`。
- 禁止把具体实现再次散落到新的顶层目录或把 `settings` 与旧三分区并列描述。

### 组合根与装配规则

- 当前跨层具体对象装配统一收口在 `src/settings/composition/`。
- 除 `src/settings/composition/` 外，其他目录禁止做跨层对象拼装、服务定位或容器式偷穿透。
- `settings/composition` 是“并入后的 bootstrap/support 模块”和本地业务绑定层，不是业务领域；后续若重构，只能更纯，不能更散。
- 反射式 / 注册式 / DI 技术内核统一外置到独立库 `shanforge-di`；`shanforge` 仓内禁止重新引入 `loader / registry / resolver / manifest / factory` 一类自研内核。
- `application / domain / runtime` 不得直接调用 resolver/loader/factory 获取具体实现；这些层只能消费已注入好的接口对象。
- 前端、用户配置和业务策略对象只允许出现 `provider_id / backend_id / profile_id / policy_id` 这类业务字符串。

### Hermes 复用规则

- 先定义 shanforge 自己的契约、对象和层边界，再谈复用 Hermes。
- 禁止直接搬运 Hermes 目录结构来决定本仓分层。
- 允许在函数实现层参考 Hermes 的成熟行为、算法和防护思路。
- 若引入 Hermes 风格的桥接代码、provider 适配或反腐封装，正式落点应在 `src/settings/`。
- 禁止让 `domain`、`application` 因为复用 Hermes 而直接持有 Hermes 私有协议、对象或主循环语义。
- 若 Hermes 具体实现需要被动态选择，应通过 `src/settings/composition/component_bindings.py` 的业务绑定和外部 `shanforge-di` 管理，不得把 Hermes class path 暴露到业务层。

### 基础能力层编码规则

- 新能力先补契约，再补实现；至少先有请求对象、结果对象、治理对象、服务接口和 provider 依赖描述。
- 能力包必须显式考虑：审批、沙箱、证据、可观测性、错误语义。
- 能力输出优先返回平台统一对象，不向上泄漏 SDK、数据库游标、原始 shell/HTTP 结果。
- 高风险能力不得绕过 `ApprovalPolicyPort`、`SandboxPolicyPort` 和证据留存要求。

### 禁止耦合清单

- 禁止 `access` / `application` / `domain` 直接 import `src/settings/` 具体实现。
- 禁止 `application` 直接依赖数据库、JSONL、供应商 SDK、shell、HTTP client。
- 禁止 `domain` 直接持有外部 SDK、数据库驱动、CLI 协议对象。
- 禁止 `runtime` 直接把底层实现细节泄漏给上层。
- 禁止在 `settings` 中写 workflow 分支、memory 晋升决策、approval 业务规则这类上层语义。

### 变更同步规则

- 任何分层、目录、接口 owner 变更，必须同步更新：
  - 代码
  - 对应设计文档
  - 测试
  - `.factory/memory/`
- 若修改了分层边界或目录事实，优先同步：
  - `system-architecture.md`
  - `module-boundaries.md`
  - `architecture-layer-code-mapping.md`
  - `basic-capability-layer-design.md` 或 `infrastructure-layer-design.md`
- 若发现正式文档与代码冲突，以“先修正式文档和 memory，再继续写代码”为默认动作。
