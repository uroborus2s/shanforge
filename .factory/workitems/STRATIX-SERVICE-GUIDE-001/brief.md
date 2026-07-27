# STRATIX-SERVICE-GUIDE-001

- 名称：按 Stratix 真实框架规范重写 stratix-service 开发指南
- 状态：`in_progress`
- 当前任务：`STRATIX-SERVICE-GUIDE-001-T01`
- 目标：以 `/Users/uroborus/NodeProject/wps/obsync-root` 当前源码、模板、类型和应用后端指南为事实源，补齐配置、环境、模块与 API 到 Kysely 的完整开发规范。
- 验收：
  - 提供当前 `src/stratix.config.ts` 模板。
  - 说明项目读取 `STRATIX_ENCRYPTION_KEY`、测试模式和模块 manifest 的正确 API 与边界。
  - 给出 Controller → Service → Repository → Kysely 的可追踪完整示例。
  - 移除已确认的过期或错误口径，并由独立回归测试锁定。
- 不包含：修改 Stratix 框架仓库、业务项目、远端、PR、部署或其他 skill。
