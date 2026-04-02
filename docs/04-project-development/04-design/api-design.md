# API 设计文档

**项目名称：** 山海工枢 / shanforge  
**负责人：** 仓库维护者  
**主要读者：** 前后端 | 测试 | 集成方 | 运维  
**上游输入：** PRD | 技术选型 | 系统架构 | 模块边界  
**下游输出：** 接口实现 | 测试用例 | 契约文件  
**最后更新：** 2026-04-02  

## 1. 接口目录

| API ID | 路径/入口 | 方法/类型 | 关联需求 | 说明 |
|---|---|---|---|---|
| `API-001` | `factory-dispatch <action>` | CLI Command | `REQ-003`, `REQ-006` | 统一动作分派入口 |
| `API-002` | `factory-agent-session --project <path>` | CLI Command | `REQ-003`, `REQ-006` | 生成会话卡、推荐阅读和下一步命令 |
| `API-003` | `config/software-factory.defaults.json` | File Contract | `REQ-001`, `REQ-002`, `REQ-004` | 全局默认配置和文档入口合同 |
| `API-004` | `.factory/project.json` | File Contract | `REQ-004`, `REQ-005` | 被管理项目的运行状态合同 |
| `API-005` | `docs/*` | Document Contract | `REQ-001`, `REQ-002`, `REQ-006` | 正式人类文档合同 |
| `API-006` | `factory-dispatch historical-project-onboarding` | CLI Command | `REQ-007` | 历史项目纳管自动化入口，支持 `legacy-onboard` 别名 |
| `API-007` | `scripts/sync-codex-skills` | CLI Command | `REQ-003` | 把仓库内 `skills/` 增量同步到 `~/.codex/skills` 与 `~/.gemini/skills` |
| `API-008` | `factory-dispatch docs-standard-upgrade` | CLI Command | `REQ-001`, `REQ-002`, `REQ-006` | 一键把项目 docs 升级到最新源文档标准 |
| `API-009` | `factory-dispatch docs-standard-upgrade-batch` | CLI Command | `REQ-001`, `REQ-002`, `REQ-006` | 批量扫描并升级多个山海工枢项目的 docs |
| `API-010` | `config/action-registry.json` | File Contract | `REQ-003`, `REQ-005`, `REQ-006` | 已实现的动作注册表契约，定义首批高层动作的 ID、风险、前置条件和验证规则 |
| `API-011` | `config/autonomy-policy.json` | File Contract | `REQ-003`, `REQ-005`, `REQ-006` | 已实现的自治策略契约，定义 `L0` ~ `L3` 风险级别和默认审批边界 |
| `API-012` | `config/frontends/*.json` | File Contract | `REQ-003`, `REQ-005` | 已实现的前台能力画像契约，描述 Codex、Gemini CLI、opencode 等宿主能力 |
| `API-013` | `factory-multi-agent-board --project <path>` | CLI Command | `REQ-005` | 当前多代理协作看板入口，后续演进为正式调度与观测面 |
| `API-014` | `factory-dispatch intent-resolver` | CLI Command | `REQ-003`, `REQ-006` | 最小自然语言意图解析入口，把目标映射到已注册动作和风险策略 |
| `API-015` | `factory-dispatch intent-eval` | CLI Command | `REQ-003`, `REQ-005`, `REQ-006` | 基于固定样本集回放评估意图解析能力，统计命中率并暴露失败样本 |
| `API-016` | `factory-dispatch intent-approval` | CLI Command | `REQ-003`, `REQ-005`, `REQ-006` | 查看或处理意图审批票据，并在批准后执行冻结计划 |
| `API-017` | `config/reply-policy.json` | File Contract | `REQ-003`, `REQ-005`, `REQ-006` | 对话摘要、审批票据触发条件和 skill 正式变更批准边界的运行时契约 |

## 2. 设计原则

- 错误契约：CLI 命令应返回可读的失败原因，文档应指向推荐补救动作。
- 认证授权：当前主要依赖本地仓库权限和 CLI 宿主环境，不定义独立鉴权协议。
- 版本策略：当前版本采用单文件演进和兼容更新，避免同时维护多个平行入口。
- 接口边界：当前版本的“API”主要是命令入口和文件契约，不假设存在对外 HTTP API。

## 3. 接口详情

### `API-001` 统一动作分派入口

- 请求：用户提供动作名和必要参数，例如 `init`、`prd-bootstrap`、`design`、`memory`。
- 响应：分派到具体 `factory-*` 脚本，并输出执行结果。
- 校验规则：
  - 动作名称必须在支持列表或别名列表中。
  - 透传参数由目标脚本负责进一步校验。
- 错误处理：
  - 未知动作返回“分派失败：未知动作”。
  - 具体脚本失败时返回对应 stderr 和退出码。

### `API-002` 会话入口生成

- 请求：项目路径、负责人、焦点等参数。
- 响应：生成给模型直接读取的 Agent 会话卡，包含推荐阅读、活跃项、阶段文档就绪度和下一步命令。
- 校验规则：
  - 项目路径必须可解析。
  - 当前阶段和推荐文档来源于项目状态。
- 错误处理：
  - 缺失状态文件或项目锁异常时，应输出明确失败原因。

### `API-003` 全局默认配置合同

- 请求：当前仓库内的配置读取或刷新。
- 响应：返回阶段顺序、共享 skills、脚手架目录和人类文档入口等默认值。
- 校验规则：
  - 所有文档路径必须存在且可读。
  - `human_workflow_docs` 与 `workflow_docs` 应统一指向 `docs/` 下的正式说明文档。
- 错误处理：
  - 配置不合法时，应阻止初始化或规则刷新继续推进。

### `API-004` 项目状态合同

- 请求：被管理项目读取或更新 `.factory/project.json` 与相关摘要。
- 响应：提供当前阶段、角色、技术画像、工作流和最近动作。
- 校验规则：
  - 必须使用标准 JSON 结构。
  - 关键字段缺失时，脚本应报错或回退到安全默认行为。
- 错误处理：
  - 读取失败或结构损坏时，应提示先修复状态文件。

### `API-005` 正式文档合同

- 请求：人类读者或维护者访问 `docs/` 中的正式文档。
- 响应：提供项目定位、需求、设计、用户指南和追踪关系。
- 校验规则：
  - 文档应包含更新时间、目标读者和变更记录。
  - 核心文档应在 `docs/index.md` 中可被发现。
- 错误处理：
  - 文档缺失时，应在索引和追踪矩阵中体现缺口。

### `API-006` 历史项目纳管自动化入口

- 请求：用户提供一个尚未纳入软件工厂的历史项目路径、负责人和纳管目标，可通过 `factory-historical-project-onboarding` 或 `factory-dispatch historical-project-onboarding` 调用。
- 响应：扫描当前真实状态、补齐软件工厂最小骨架，生成基线文档、AI 记忆、`agent-session`、`state-doctor` 和纳管报告。
- 校验规则：
  - 若项目已经存在完整软件工厂骨架，应拒绝再次当作“未纳管历史项目”初始化。
  - 必须先识别代码、配置、现有文档和最新发布结果，再生成纳管基线。
- 错误处理：
  - 项目目录为空时，应提示改用 `factory-init`。
  - 项目已纳管时，应提示改用 `agent-session`、`state-doctor` 等标准维护入口。

### `API-007` 全局 skills 同步入口

- 请求：用户从当前仓库执行 `python3 scripts/sync-codex-skills`，可选指定源目录、Codex 目录、Gemini 目录、冲突前缀与 dry-run。
- 响应：把仓库内 `skills/` 下的每个可见 skill 目录增量软链接到 `~/.codex/skills` 和 `~/.gemini/skills`，并输出逐项同步结果。
- 校验规则：
  - 默认跳过 `.system` 一类隐藏目录，避免覆盖宿主工具保留目录。
  - 若目标目录已有同名项且不是指向当前 skill 的软链接，则回退到 `shanforge-<skill>` 形式的别名。
  - 若目标根目录是损坏的软链接，默认报错；显式传入 `--repair-broken-target-links` 时才允许修复。
- 错误处理：
  - 源目录不存在或不可读时，应直接失败并提示源路径。
  - 若目标目录存在无法自动解决的命名冲突，应保留原有项并返回冲突摘要。

### `API-008` docs 标准升级入口

- 请求：用户提供项目路径、负责人，以及可选 `--force` / `--check`。
- 响应：按需执行旧 docs 结构迁移、刷新根索引和目录首页，并返回最终 `docs-stratego` 源文档状态。
- 校验规则：
  - 若项目不存在 `docs/`，应直接失败。
  - `--check` 只报告“是否需要迁移”和当前是否已经 `就绪`。
  - 正式执行时，若根导航中已有人工维护的页面级权限和标题，应尽量保留。
- 错误处理：
  - 结构迁移遇到冲突文件时，默认失败；显式传入 `--force` 才允许覆盖。
  - 最终状态若不是 `就绪`，命令应以非零退出码结束。

### `API-009` docs 标准批量升级入口

- 请求：用户提供一个或多个 `--root` 扫描根目录，或显式传入多个 `--project`。
- 响应：识别已纳管项目，逐个执行检查或升级，并输出汇总结果。
- 校验规则：
  - 默认只处理同时具备 `.factory/project.json` 与 `docs/` 的项目。
  - 扫描时跳过 `node_modules`、`.git`、`dist` 等无关目录。
  - 任一项目失败或未就绪时，批量命令应以非零退出码结束。
- 错误处理：
  - 未发现任何候选项目时，应直接失败并提示补充 `--project` 或 `--root`。
  - 单个项目异常不能阻断其他项目继续处理，但要出现在最终汇总中。

### `API-010` 动作注册表契约

- 请求：运行时加载动作注册信息，供动作解析、策略判断和后续工作流编排使用。
- 响应：返回动作元数据，包括动作 ID、别名、输入结构、前置条件、风险等级、所需能力、验证方式和恢复提示。
- 校验规则：
  - 每个动作 ID 必须全局唯一。
  - 不允许缺少 `risk_level`、`preconditions` 或 `verification` 的动作进入自动执行层。
- 错误处理：
  - 动作注册结构损坏时，应阻止自治执行并提示回退到手工入口。
  - 若发现同名动作冲突，应返回冲突摘要并停止加载。
- 当前状态：
  - MVP 已实现，注册表文件为 `config/action-registry.json`。
  - `factory-dispatch` 已优先使用注册表解析首批高层动作。
  - 已支持 `subtargets` 元数据，允许对 `command-profiles` 等高层动作的子目标单独提高风险等级。
  - 其余历史动作仍由 legacy 映射兼容承载。

### `API-011` 自治策略契约

- 请求：运行时在动作执行前读取自治策略，判断是否自动执行、是否需要确认、是否必须阻断。
- 响应：给出基于风险等级、项目状态、宿主能力和证据门槛的执行判定。
- 校验规则：
  - 策略必须显式覆盖 `L0` ~ `L3`。
  - 高风险动作不能因为缺省值而降级为自动执行。
- 错误处理：
  - 策略缺失或解析失败时，应回退到最保守策略。
- 当前状态：
  - MVP 已实现，策略文件为 `config/autonomy-policy.json`。
  - 当前主要用于 `factory-dispatch --list-actions` 展示已登记动作的默认策略和风险等级。
  - `L2/L3` 动作的最小审批票据 hook 已实现，但尚未接入 UI / 远程审批入口。

### `API-012` 前台能力画像契约

- 请求：前台适配层读取某个宿主的能力画像，决定是否支持 shell、文件编辑、子代理、MCP 和审批 hook。
- 响应：返回当前前台的能力集合与降级策略。
- 校验规则：
  - 最低必须声明是否支持文件读写、命令执行和上下文压缩。
  - 不允许未声明能力的宿主假装支持高阶功能。
- 错误处理：
  - 能力画像缺失时，应回退到最低能力模式，禁止依赖可选能力的工作流自动执行。
- 当前状态：
  - MVP 已实现，能力画像文件位于 `config/frontends/*.json`。
  - 当前提供 `codex`、`gemini`、`opencode` 三份画像。
  - `factory-frontend-capabilities` 与 `factory-dispatch frontend-capabilities` 已可查询画像。
  - `factory-chat-bootstrap` 已开始消费该契约。

### `API-013` 多代理协作看板入口

- 请求：用户提供项目路径、负责人和焦点信息，生成当前项目的多代理协作看板。
- 响应：输出角色分工、活跃任务、依赖关系、风险点和下一步建议。
- 校验规则：
  - 项目路径必须已经纳入软件工厂。
  - 看板中的角色与工作项引用应来自当前项目状态。
- 错误处理：
  - 项目未纳管时，应提示先完成纳管或生成单代理 session，而不是继续生成协作看板。
- 当前状态：
  - MVP 已实现，入口为 `scripts/factory-multi-agent-board`。
  - 当前看板已开始暴露待审批票据、高风险推荐动作、未分派工作项提醒，以及角色写入集合与冲突摘要。
  - `factory-role-assign` 已支持 `--write-targets`，并会默认阻断与现有角色分派的显式写集冲突。
  - 尚未覆盖真实子代理提交阶段的隐式写集探测，也未形成完整的多代理调度与自动恢复闭环。

### `API-014` 最小意图解析入口

- 请求：用户提供自然语言目标、项目路径，以及可选前台工具 ID。
- 响应：返回主推荐动作、候选动作、风险级别、审批策略、项目事实和建议命令；显式传入 `--execute-safe` 时，可直接执行默认策略为 `auto` 的主推荐动作。
- 校验规则：
  - 只允许输出已注册动作，不允许直接映射任意 shell。
  - 解析结果必须包含项目识别、前台识别和风险策略。
  - 若无明显专项语义，应回退到基于项目事实的安全默认动作。
  - `--execute-safe` 只能放行 `approval=auto` 且 `execution=auto` 的主推荐动作。
- 错误处理：
  - 项目路径不存在或不是目录时应直接失败。
  - 解析不到高置信候选时，应回退到 `state-doctor`、`historical-project-onboarding` 或 `init` 中的安全默认项。
  - 若主推荐动作需要确认或存在阻塞，应返回 `policy_denied` / `blocked`，而不是越过审批边界继续执行。
- 当前状态：
  - MVP 已实现，入口为 `scripts/factory-intent-resolver`。
  - `factory-dispatch intent-resolver` 和别名 `intent` 已接入。
  - 已支持识别 `command-profiles` / `workflow-runner` 的具体子目标，并可通过 `--execute-safe` 自动执行 `L0/L1` 主推荐动作。
  - 已支持对子目标应用风险覆盖；工作流型 profile 在解析时会提升到 `L2` 审批边界。
  - 已支持通过 `--request-approval` 为 `L2/L3` 主推荐动作创建冻结审批票据。
  - 已支持输出 `approval_guidance` 和固定 `reply_summary`，用于当前对话回复和后续审批衔接。
  - 当前解析器仍以关键词和项目事实规则为主，尚未接入学习型排序和 UI / 远程审批入口。

### `API-015` 意图回放评估入口

- 请求：用户提供评估样本文件路径，以及可选前台覆盖参数。
- 响应：返回总样本数、通过数、失败数、命中率、失败样本明细和下一步建议，并写出评估报告。
- 校验规则：
  - 样本文件必须包含非空 `cases`，每条样本必须有 `id`、`intent` 和 `expected`。
  - 评估结果必须显式区分解析失败、策略阻断和安全执行结果。
  - 样本夹具应自包含，不能依赖当前仓库临时状态。
- 错误处理：
  - 样本文件损坏或夹具类型未知时，应直接失败。
  - `--strict` 下若存在失败样本，应返回非 0。
- 当前状态：
  - MVP 已实现，入口为 `scripts/factory-intent-eval`。
  - 默认样本集位于 `config/evals/intent-resolver-cases.json`。
  - 当前已覆盖 `empty`、`historical`、`managed` 三类项目夹具，以及 `action/profile/workflow/safe_execute/approval_request` 五类断言。
  - 已输出固定 `reply_summary`，便于在日常开发回复中给出简短评估结论。

### `API-016` 意图审批票据入口

- 请求：用户提供票据 ID，并显式选择 `--approve` 或 `--reject`；也可只用 `--list` 查看当前票据列表。
- 响应：返回待审批或已处理票据列表；批准时执行票据中冻结的计划，并写回执行结果、审批人和摘要。
- 校验规则：
  - `--approve` 与 `--reject` 不能同时使用。
  - 批准或拒绝时必须提供有效票据 ID。
  - 只有 `pending` 状态的票据允许继续执行。
  - 票据必须包含冻结后的 `plan`，不允许重新推导高风险动作。
- 错误处理：
  - 票据不存在时应直接失败。
  - 已处理票据重复批准时，应返回可读状态而不是再次执行。
  - 冻结计划执行失败时，应把票据状态写成 `failed`，并保留执行摘要。
- 当前状态：
  - MVP 已实现，入口为 `scripts/factory-intent-approval`。
  - `factory-dispatch intent-approval` 和别名 `intent-approve` 已接入。
  - 审批票据统一写入 `.factory/process/intent-approvals.json` 与对应视图。
  - 票据已冻结建议 ownership 角色和写入集合；批准执行前会再次校验负责人与显式写集冲突，未通过则阻断执行。
  - 已输出固定 `reply_summary`，便于在对话中摘要展示票据状态和 ownership 校验结果。

### `API-017` 对话摘要与审批回报契约

- 请求：运行时在输出 `intent` 评估、审批和高层解析结果时读取对话摘要契约。
- 响应：返回固定的 `reply_summary` 字段，以及 `intent-resolver` 的 `approval_guidance`。
- 校验规则：
  - 必须明确哪些动作需要对话摘要。
  - 必须明确哪些风险/审批模式需要进入票据链路。
  - 正式 `skill` 变更必须声明候选目录、评估要求和审批要求。
- 错误处理：
  - 契约缺失或损坏时，应回退到最保守的摘要与审批策略。
- 当前状态：
  - MVP 已实现，契约文件为 `config/reply-policy.json`。
  - 当前已覆盖 `intent-resolver`、`intent-eval`、`intent-approval` 3 类运行时入口。
  - 当前已把 skill 正式变更固定为“候选优先、评估先行、显式批准后晋升”的治理边界。

## 4. 契约文件

- 当前已使用的契约：
  - `config/software-factory.defaults.json`
  - `docs/index.md`
  - `docs/04-project-development/03-requirements/prd.md`
  - `docs/04-project-development/04-design/system-architecture.md`
  - `docs/02-user-guide/user-guide.md`
- 入口设计与实现说明：
  - `docs/04-project-development/04-design/historical-project-onboarding-automation.md`
- 未来若引入对外 HTTP API，再补充：
  - `docs/04-project-development/04-design/contracts/api/openapi.yaml`
- 目标架构中规划新增的内部契约：
  - `config/action-registry.json`
  - `config/autonomy-policy.json`
  - `config/frontends/*.json`
  - `config/evals/intent-resolver-cases.json`
  - `.factory/process/intent-approvals.json`

## 5. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-03-25 | 初始版本，定义 CLI 命令入口和文件契约接口 | Codex |
| 2026-03-25 | 更新默认文档入口契约，要求相关人类说明文档统一落在 docs/ | Codex |
| 2026-03-26 | 增加历史项目纳管自动化入口 `API-006` 的提案型定义 | Codex |
| 2026-03-26 | 将 `API-006` 更新为已实现 MVP，并登记脚本与别名入口 | Codex |
| 2026-03-27 | 将项目名称统一更新为“山海工枢 / shanforge”，并同步仓库路径 | Codex |
| 2026-03-27 | 增加 `API-007`，支持把仓库内共享 skills 同步到 Codex / Gemini 全局目录 | Codex |
| 2026-04-01 | 增加 `API-008`，提供 docs 最新源文档标准的一键升级入口 | Codex |
| 2026-04-01 | 增加 `API-009`，支持批量扫描和升级多个项目的 docs 标准 | Codex |
| 2026-04-02 | 增加 `API-010` ~ `API-013`，登记动作注册、自治策略、前台能力画像和多代理协作入口 | Codex |
| 2026-04-02 | 更新 `API-013` 为“显式写集声明 + 冲突默认阻断 + 看板冲突摘要”后的当前状态 | Codex |
| 2026-04-02 | 增加 `API-014`，提供自然语言到已注册动作的最小意图解析入口 | Codex |
| 2026-04-02 | 增加 `API-015`，提供意图回放评估入口和固定样本集契约 | Codex |
| 2026-04-02 | 增加 `API-016`，提供最小审批票据入口和冻结计划执行契约 | Codex |
| 2026-04-02 | 更新 `API-016`，增加冻结 ownership 与批准前冲突校验 | Codex |
