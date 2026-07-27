# Gin、GORM、Logrus、Consul 技术栈契约

## Gin

- 使用 `gin.New()`，按顺序显式安装 request ID、访问日志、recovery、认证和业务中间件。
- 使用 `ShouldBindJSON`、`ShouldBindQuery` 等返回错误的方法，由 handler 决定统一错误响应。
- handler 负责协议适配：解析、校验、调用 use case、映射响应。
- service、domain 和 repository 不接收 `*gin.Context`。
- 中间件启动 goroutine 前复制必要值；优先把可取消工作交给受控 service。

## Logrus

- composition root 使用 `logrus.New()` 创建独立 `*logrus.Logger`，通过构造函数注入。
- 生产输出 JSON 到 stdout/stderr，由运行平台负责采集和轮转。
- 复用 `*logrus.Entry` 携带 `service`、`environment`、`request_id`、`trace_id` 等稳定字段。
- 错误字段使用 `WithError`；动态数据使用 `WithField(s)`，避免拼接长字符串。
- 业务层禁止 `Fatal` 和 `Panic`；它们分别会退出进程或触发 panic。
- 不启用昂贵 caller 信息，除非基准测试和排障需求证明值得。
- Logrus 已进入 maintenance mode。保留它是当前栈契约，不代表忽略迁移风险；更换日志库必须单独决策。

## GORM

- composition root 创建 `*gorm.DB`，再取得底层 `*sql.DB` 配置连接池和健康检查。
- repository 每次操作使用 `db.WithContext(ctx)`，或使用接收 context 的 Generics API。
- 多步写操作使用 `db.Transaction(func(tx *gorm.DB) error { ... })`；回调返回错误触发回滚。
- 不默认关闭 GORM 写事务。只有基准和一致性分析证明安全时才允许 `SkipDefaultTransaction`。
- 生产 schema 通过版本化迁移工具管理；`AutoMigrate` 仅限明确批准的开发/测试场景。
- 查询必须显式选择关联加载策略；防止 N+1、无界扫描和隐式全表更新/删除。
- GORM model 不自动等于 API DTO 或领域模型；只有结构和生命周期完全一致时才允许复用。

### 物理数据库选型

GORM 不代替数据库选型。至少比较：

- 事务与一致性要求。
- 数据关系、查询和索引形态。
- 预计容量、吞吐、延迟和增长。
- 高可用、备份、恢复和运维能力。
- 云服务、许可、团队经验和成本。
- GORM driver 的兼容性与测试环境可获得性。

模板使用 PostgreSQL 作为可编译示例。正式项目必须在数据库 baseline 中确认；若选择其他数据库，只替换 driver 和数据库专属配置，不改写上层 repository 契约。

## Consul

- 使用 `github.com/hashicorp/consul/api` 官方 Go client。
- `CONSUL_HTTP_ADDR`、`CONSUL_HTTP_TOKEN`、datacenter、namespace/partition 和 key prefix 属于 bootstrap 配置。
- 默认配置优先级：编译默认值 < 本地文件 < Consul KV < 环境变量/secret mount < 显式启动参数。项目已有规则优先。
- Consul KV 只存非秘密业务配置和元数据。密码、私钥、token、数据库 DSN 交给 secret manager 或 secret mount。
- key 建议按 `<service>/<environment>/<config>` 隔离，并用 ACL 最小授权。
- 首次加载必须使用带超时的 context；必要 key 缺失、解码失败或校验失败时启动失败。
- 需要热更新时使用 blocking query/watch；每次完整解码和校验后原子替换快照。
- watch 必须支持取消、退避和抖动；失败时保留 last-known-good，不允许忙循环。
- Consul KV 是配置和元数据 KV，不是业务数据库。

## 组合顺序

1. 读取 bootstrap 配置。
2. 创建 Logrus logger，保证后续启动失败可观测。
3. 创建 Consul client，加载并校验远端业务配置。
4. 创建数据库连接，配置连接池并执行 ping。
5. 构造 repository、service、handler 和 Gin router。
6. 启动 HTTP server 和受控配置 watcher。
7. 收到 signal 后先停止接流量，再停止 watcher、等待任务并关闭数据库。
