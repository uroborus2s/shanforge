# 模块边界文档

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 模块边界基线
**负责人：** 仓库维护者
**主要读者：** 架构 | 平台开发 | 业务 Agent 开发 | 测试
**上游输入：** 系统架构 | 平台架构设计
**下游输出：** API 设计 | 实施计划 | 测试计划
**关联 ID：** `MOD-001` ~ `MOD-014`, `REQ-001` ~ `REQ-010`
**最后更新：** 2026-04-15

## 1. 边界原则

- 系统只有一套正式分层口径：用户界面层、接口/网关层、业务调度层、业务模型层、基础能力层、基础设置层。
- `ports` 跟随消费者所在层定义，不构成额外层次。
- 基础设置层统一收口到 `src/settings/`；层内可再按实现领域和支撑模块分组，但不构成额外层次。
- 依赖只能单向向下：`access -> application -> domain -> runtime/basic-capability -> settings`。
- 业务调度层只做编排，不吸收基础能力层和基础设置层细节。
- 业务模型层拥有业务逻辑；基础能力层只提供通用技术能力；基础设置层只负责实现和装配。
- `session ledger` 是第一事实源，记忆只能作为派生资产存在。

## 2. 模块归属矩阵

| 模块 | 主归属层 | 可触达层 | 说明 |
|---|---|---|---|
| `MOD-001` Business Agent Apps | 业务模型层 | 业务调度层 | 业务 app、workflow、输出契约 |
| `MOD-002` Application Use Cases | 业务调度层 | 接口/网关层 | 平台薄编排层 |
| `MOD-003` Agent Domain Model | 业务模型层 | 业务调度层 | 稳定领域对象与规则 |
| `MOD-004` Workflow | 业务模型层 | 基础能力层 | 业务流程规则归领域，运行辅助走基础能力 |
| `MOD-005` Model | 业务模型层 | 基础能力层、基础设置层 | 模型策略归领域，调用能力走下层 |
| `MOD-006` Capability | 业务模型层 | 基础能力层、基础设置层 | 能力声明、风险和结果语义归领域 |
| `MOD-007` Memory | 业务模型层 | 业务调度层、基础能力层、基础设置层 | 记忆业务逻辑 owner |
| `MOD-008` Approval | 业务模型层 | 基础能力层、基础设置层 | 审批语义与规则归领域 |
| `MOD-009` Delegation | 业务模型层 | 基础能力层、基础设置层 | 委派语义与合并规则归领域 |
| `MOD-010` Session & Evidence | 业务模型层 | 基础能力层、基础设置层 | 会话、档案和证据模型归领域 |
| `MOD-011` Interface & Gateway Entry | 接口/网关层 | 业务调度层 | API、CLI、HTTP、MCP 入口收口 |
| `MOD-012` Consumer-Owned Ports | 跟随消费者 | 接口/网关层、业务调度层、业务模型层、基础能力层 | 消费者向下依赖接口 |
| `MOD-013` Base Setting Implementations | 基础设置层 | 基础能力层 | provider、store、外部系统、容器装配 |
| `MOD-014` Response | 业务模型层 | 基础能力层 | 标准响应语义归领域 |

## 3. 允许依赖

| 层 / 模块 | 允许依赖 | 禁止依赖 |
|---|---|---|
| 接口/网关层 | 业务调度层、自己拥有的 ports | 业务模型内部实现、基础能力实现、基础设置细节 |
| 业务调度层 | 业务模型层、自己拥有的 ports | runtime provider、settings 实现 |
| 业务模型层 | 基础能力层能力接口、自己拥有的 ports | UI、gateway、adapter、store、SDK |
| 基础能力层 | 基础设置 provider ports | 业务编排、业务规则判断、UI 协议 |
| 基础设置层 | 业务模型层持久化 ports、基础能力层 provider ports | 业务编排、业务规则分支、UI 协议 |

## 4. `ports` 的正式边界

`ports` 的正式定义是：

```text
消费者定义的向下依赖接口
```

因此：

- `src/access/ports/` 属于接口/网关层。
- `src/application/ports/` 属于业务调度层。
- `src/domain/*/ports.py` 属于业务模型层。
- `src/runtime/ports/` 属于基础能力层。
- `MOD-012` 只是这一设计原则的汇总编号，不代表额外新层。

## 5. 基础设置层的正式边界

基础设置层只做下面三类事：

- 提供真实资源：文件系统、数据库、本地 JSONL、provider SDK、远程系统。
- 实现上层声明的持久化与 provider 端口：domain-owned repository/store ports，以及 runtime-owned provider/backend ports。
- 进行装配选择：settings、container、runtime binding。

基础设置层不能做的事：

- 决定业务 app 如何执行。
- 决定 workflow 的业务分支。
- 决定记忆是否晋升、审批是否放行这类上层规则。
- 向上泄漏 SDK 原始对象或底层数据库语义。

## 6. 典型禁止耦合

- 用户界面层或外部 Web 项目直接调用 `src/runtime/` 内部对象。
- 接口/网关层直接调用 `src/settings/` 具体实现。
- 业务调度层直接选择 `JSONL`、`SQLite`、`OpenAIProvider` 之类的实现。
- 业务模型层直接持有 SDK、数据库驱动或网关协议对象。
- 基础能力层直接依赖外部 UI 协议。
- 基础设置层出现业务规则分支。
- 记忆领域绕过 session facts 直接覆盖人工确认事实。

## 7. 迁移与实现规则

- 旧脚本、文件合同、CLI 执行器和外部桥接统一归入基础设置层实现区。
- 统一界面必须保留在调用方所在层，不得被基础设置层反向拉平。
- 新增能力时先决定它属于哪一层，再决定它属于哪个领域，最后再决定目录位置。
- 实现顺序固定为：定义 access 用例接口 -> 定义 application 领域服务接口 -> 定义 domain 能力接口 -> 定义 runtime provider 接口 -> 实现 settings。

## 8. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v2.0` | 2026-04-13 | 重写模块边界，按平台内核、业务 App、ports、adapters 重新定义依赖规则 |
| `v2.1` | 2026-04-14 | 建立六层边界基线 |
| `v2.2` | 2026-04-15 | 收口为单向依赖链，并把业务 owner 统一回业务模型层 |
