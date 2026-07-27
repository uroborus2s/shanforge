# Go 后端工程规范

## 工程事实优先

- 先读 `go.mod`、`go.work`、Makefile、CI 和现有测试命令。
- 现有项目版本和目录优先于模板。
- 新依赖必须有当前需求依据；标准库能满足时不增加包装库。
- 不创建只为转发一次调用的 manager、factory、registry 或 helper。
- 不把连续流程拆成只调用一次的私有函数或方法。没有稳定资源、协议或包边界时必须内联。
- 先删除代码和抽象，再考虑增加模式；完整规则见 [Ponytail、代码形状与设计规则](simplicity-and-design.md)。

## 包与目录

- 可执行入口放在 `cmd/<service>/`。
- 非公开业务代码放在 `internal/`。
- 按业务能力划分 package；不要建立 `utils`、`common`、`helpers` 大杂烩。
- interface 由调用方定义，并保持最小方法集。
- 单一真实实现默认使用具体类型；不得为测试方便或未来扩展预建接口。
- composition 只在入口完成；handler、service、repository 不自行查找全局依赖。

## 函数与对象设计

- 控制流嵌套目标不超过 2 层，硬上限 3 层；错误和非法状态立即返回。
- 禁止用只调用一次的 helper 隐藏嵌套；优先简化条件、状态和数据流。
- struct 只聚合有共同不变量或资源所有权的数据，receiver method 负责维护这些不变量。
- 优先组合，不模拟继承，不建立万能 base type、空壳 service 或全局 service locator。
- Strategy、Factory、Adapter、State、Observer、Functional Options 等模式必须满足 [设计模式采用门槛](simplicity-and-design.md#设计模式采用门槛)，不得按模板默认生成。

## Context 与并发

- `context.Context` 是函数首参，不允许为 nil。
- 从入站请求传递 context；超时和取消必须向数据库、Consul和下游 HTTP 传播。
- 不把 context 放入 struct，也不创建无法停止的 goroutine。
- 后台 goroutine 必须有 owner、取消路径、错误回传和关闭等待。
- 共享状态必须有明确同步策略；增加并发前先确认实际收益与顺序语义。

## 错误

- 失败立即返回；使用 `%w` 保留原因链。
- 只在能增加动作信息时包装错误。
- handler 把领域错误映射到稳定 HTTP 错误契约。
- 业务层不调用 `panic`、`logrus.Fatal` 或 `os.Exit`。
- 同一错误只在最终处理边界记录一次；上层需要判断时用 `errors.Is/As`。
- 禁止错误后尝试未在契约中声明的第二格式、第二地址、第二驱动或旧字段；未知输入失败，不扩大兼容面。

## API 与安全

- 明确请求大小上限、超时、认证、授权、限流和幂等要求。
- 所有外部输入都校验；绑定成功不等于业务合法。
- 响应不暴露数据库错误、SQL、堆栈、Consul token 或内部路径。
- 健康检查区分 liveness 与 readiness；readiness 可验证必要依赖。
- 生产服务设置 `ReadHeaderTimeout`、`ReadTimeout`、`WriteTimeout`、`IdleTimeout`。

## 数据与事务

- 事务边界由用例决定，不由 repository 随意扩大。
- 事务函数内只使用传入的 `tx`。
- 写操作必须检查错误和受影响行数。
- 大结果集使用分页、流式或批处理；禁止无界 `Find`。
- 索引、唯一约束、外键和迁移脚本属于数据库契约，不能只写在 GORM tag 中。

## 测试

- service 使用表驱动单元测试覆盖业务分支。
- handler 使用 `httptest` 验证状态码、响应体和错误契约。
- repository 使用真实兼容数据库做集成测试；仅 mock GORM 链式调用不能证明 SQL 行为。
- 配置测试覆盖缺 key、非法值、Consul 不可达、无效更新和 last-known-good。
- 日志测试验证字段和脱敏，不依赖完整文本顺序。

## 质量门

```bash
gofmt -w <changed-go-files>
go vet ./...
go test ./...
go test -race ./...
```

`go test -race ./...` 是否强制由项目风险和 CI 约束决定。未运行必须写明原因。
