---
name: go-developer
description: Go / Golang 后端工程开发 skill。用于明确采用 Gin + GORM + Logrus + Consul 组合栈的 HTTP API、微服务和后台服务开发、重构、评审及测试；当用户指定该组合栈，或工程事实显示同时采用这四项技术时使用。仅命中其中单个库、非 Go 项目或其他技术栈不触发。
---

# Go Developer

用于 Gin + GORM + Logrus + Consul 后端项目。先识别阶段和现有工程事实，再执行最小改动。

## 触发

- 新建或维护 Go HTTP API、微服务和后台服务。
- 用户明确指定 Gin + GORM + Logrus + Consul 组合栈。
- 项目的 `go.mod` 和代码事实显示同时采用这四项技术。
- 实现 handler、service、repository、中间件、事务、配置加载、结构化日志和优雅停机。
- 用户要求该技术栈的工程规范、代码评审或项目骨架。

## 不适用

- 非 Go 项目。
- Go CLI、纯算法库或未使用 Gin/GORM/Logrus/Consul 的通用 Go 任务。
- 只使用其中单个库的任务，例如 Gin + Zap 项目或 GORM-only 数据工具；单库命中不得推定迁移其余技术栈。
- Stratix、Java/Spring Boot 或 Python 服务。
- API 契约尚未确定时，不代替 `api-design`。
- Bug 根因未知时，不代替 `systematic-debugging`。

已有项目若采用其他框架或库，先遵守项目事实。不得为了套用本 skill 擅自迁移技术栈；技术栈冲突时返回 `needs_user_input`。

## 固定技术基线

| 领域 | 基线 | 硬规则 |
|---|---|---|
| HTTP | Gin | 使用 `gin.New()` 显式装配中间件；handler 只做 HTTP 适配 |
| ORM | GORM | repository 承担持久化；所有请求链路传递 `context.Context` |
| 日志 | Logrus | 注入独立 `*logrus.Logger`；生产使用 JSON 和结构化字段 |
| 配置中心 | Consul KV | 使用官方 Go client；启动配置与远端业务配置分离 |

GORM 是数据访问工具，不是物理数据库。PostgreSQL、MySQL、SQLite 等数据库引擎必须依据项目需求、部署环境和数据基线单独确定。

Logrus 官方处于 maintenance mode。本 skill 因用户明确选型继续使用 Logrus，但不得把它描述成新项目的无条件通用最优选择，也不得静默替换为其他日志库。

## 阶段判断

| 阶段 | 允许动作 | 禁止 |
|---|---|---|
| 需求 / 设计 | 明确 API、数据、事务、配置、日志和部署约束 | 直接生成完整服务 |
| 新建项目 | 选择 Go 和依赖版本，渲染最小模板，补业务代码 | 复制模板后不验证 |
| 实现 / 重构 | 沿用现有目录和契约，写最小代码与测试 | 新增无依据抽象 |
| Bug 修复 | 根因明确后先写失败测试，再修根因 | fallback、吞错或盲目重试 |
| Review | 报告正确性、安全、并发、事务和测试缺口 | 只做风格评价 |

## 默认工作流

1. 读取 `go.mod`、现有目录、API/数据契约和测试命令。
2. 确认 Go、Gin、GORM、Logrus、Consul client 及数据库 driver 的实际版本。
3. 判断物理数据库、迁移工具、Consul key 结构和配置失败策略是否已明确。
4. 按 [工程规范](references/engineering-standards.md) 和 [技术栈契约](references/stack-contract.md) 实现最小改动。
5. 按 [Ponytail、代码形状与设计规则](references/simplicity-and-design.md) 删除推测性抽象、单次调用 helper 和未获批准的兼容回退。
6. 新项目才使用 [服务模板](references/template-usage.md)；已有项目不得强套模板目录。
7. 按“验证范围”运行定向或全量检查；项目已有 lint、race 或集成测试只在对应风险、Gate 或项目规则要求时运行。
8. 只按真实命令结果报告，作者状态最多到 `ready_for_review`。

## 验证范围

- 普通低、中风险改动：仅对实际改动的 Go 文件运行 `gofmt`，运行受影响包的 `go test`，并按风险和改动需要运行受影响包 `go vet`。
- 批次、里程碑、高风险、发布或项目既有 Gate 明确要求时：运行全量集合，可包括 `go test ./...`、`go vet ./...`，以及项目既有的 race、集成测试或其他质量门。
- 先读取项目实际包、测试与质量门入口；以上是范围规则，不把示例命令或路径假定为所有项目都存在。
- 每次回复必须列出已运行范围、未运行的全量项及原因；定向通过不得表述为全量通过。

## 必须遵守

- 以 `context.Context` 贯穿 Gin 请求、service、repository、GORM 和 Consul 调用；禁止存入 struct 长期持有。
- Gin 使用 `ShouldBind*` 并由应用统一返回错误契约；禁止让领域或 service 依赖 `*gin.Context`。
- Gin 请求日志与 recovery 统一接入 Logrus；禁止同时启用重复访问日志。
- Logrus 使用显式 logger/entry 和字段；禁止在业务层调用 `Fatal`、`Panic`，禁止记录 token、密码、DSN 和完整敏感请求体。
- GORM 查询必须带 context；事务回调内只使用 `tx`；生产迁移必须由显式迁移流程管理，禁止服务启动时无条件 `AutoMigrate`。
- repository 不向上泄漏 `*gorm.DB`；避免 N+1，关联加载必须基于真实查询场景。
- Consul 地址、ACL token、datacenter 和 key prefix 属于 bootstrap 配置，从环境变量或 secret mount 注入；Consul KV 不存放数据库密码、访问令牌等秘密。
- Consul 配置先解码、校验，再整体替换当前快照；无效更新保留 last-known-good 并记录错误，禁止部分字段生效。
- 必需远端配置首次加载失败时启动失败；只有项目明确批准降级策略时才允许本地兜底。
- HTTP server 必须设置超时并支持 signal-aware graceful shutdown。
- 错误必须保留原因链；只在系统边界记录一次，不重复逐层刷日志。
- 按 Ponytail 决策顺序选择现有代码、标准库、已有依赖和最少新代码；禁止为未来可能性新增层、接口、依赖或配置项。
- 禁止仅为缩短函数或制造步骤感而拆分只调用一次的私有函数/方法；没有稳定边界的单次调用 helper 必须内联。
- 普通业务函数嵌套目标不超过 2 层、硬上限 3 层；优先 guard clause，禁止用单次调用 helper 隐藏深层嵌套。
- 使用 Go 式面向对象：struct 管状态和不变量、组合优先、interface 由消费方定义；单一真实实现不得预建接口。
- 设计模式只有在当前问题和真实变化点存在时使用；禁止默认 Factory、Repository、DI 容器、Functional Options 或事件总线。
- 禁止未获批准的 fallback、旧字段 alias、dual-read/dual-write、多驱动包装、宽松解析和“失败后再试另一方案”的兼容扩张。

## 按需读取

- Gin、GORM、Logrus、Consul 的组合规则：[技术栈契约](references/stack-contract.md)。
- Go 代码、并发、错误、测试和质量门：[工程规范](references/engineering-standards.md)。
- Ponytail、单次调用拆分、嵌套、Go 式对象设计、模式门槛和回退禁令：[简洁与设计规则](references/simplicity-and-design.md)。
- 新服务代码骨架：[服务模板](references/template-usage.md)。
- 外部参考的可靠性和版本快照：[来源评估](references/source-evaluation.md)。

本 skill 不是第三方库 API 全集。具体 API 签名、兼容性和安全变更以项目锁定版本及官方文档为准。

## 失败语义

- `needs_user_input`：物理数据库、API 契约、配置失败策略或技术栈冲突会改变实现结果。
- `blocked`：依赖版本不兼容、Consul/数据库不可达、测试无法运行或根因未知，导致无法安全继续。
- `ready_for_review`：代码、测试和新鲜验证已完成，但尚未经过独立评审。

## 输出

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: go-developer
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <代码、迁移、配置或评审位置>
- evidence:
  - 已运行范围：<实际 gofmt、受影响包 test/vet、或全量命令及结果>
  - 未运行的全量项及原因：<未运行的全量 test/vet/race/集成测试及原因；全量执行时写无>
  - <定向通过不得表述为全量通过>
- ledger_event: <event id or none>
- needs:
  - review | verification | root_cause | user_input | none
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
