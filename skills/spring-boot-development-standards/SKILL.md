---
name: spring-boot-development-standards
description: Spring Boot / Java 项目的技术开发规范、代码评审和小范围重构约束。用于用户提到 Spring Boot、Spring MVC、Spring Data、Spring Security、Java 后端分层、接口实现、Bug 修复纪律、工具方法复用或 Java 设计模式时；Bug 根因调查仍由 systematic-debugging 接管。
---

# Spring Boot 开发规范

用于约束 Spring Boot 项目的工程结构、编码风格、Review 和修复纪律。目标是少写代码、写对位置、可测试、可维护。

## 触发

- 新建或维护 Spring Boot / Java 后端项目。
- 设计 Controller、Service、Repository、配置、DTO、异常处理和测试。
- 评审 Spring Boot 代码是否符合团队开发规范。
- 重构重复工具函数、过深嵌套、坏味道 Service 或滥用设计模式。
- 处理 Spring Boot Bug 修复方案时，需要确认是否针对根因。

## 边界

- Bug 根因不清楚时，先进入 `systematic-debugging`；本 skill 不替代复现、日志、调用链和根因报告。
- API 契约设计优先交给 `api-design`；本 skill 只约束 Spring Boot 落地方式。
- 数据库、消息队列、缓存和安全配置按项目现有栈执行，不为“以后可能”加框架。
- 用户只问概念时直接回答，不创建项目结构或文档。

## Ponytail 约束

先按这个顺序决策：

1. 这段代码是否需要存在；不需要就删。
2. 项目里是否已有工具方法、基类、配置或模式；先查再写。
3. Java 标准库、Spring Boot、Spring Framework 是否已经提供。
4. 已安装依赖是否已经覆盖。
5. 只在以上都不满足时，写最小实现。

硬规则：

- 禁止为了分段而写只被引用一次的 helper 方法。
- 只被引用一次的方法只有在表达领域概念、实现接口/多态、隔离副作用、降低过深嵌套或形成测试边界时允许。
- 禁止每个类都写自己的 `parse`、`format`、`convert`、`isEmpty`、`buildXxx` 等工具方法。
- 写工具方法前必须先查项目内是否已有同类方法；优先复用最近 owner 的工具，不默认新增全局 `Utils`。
- 只要出现相同功能工具函数，就提升到最近公共 owner；两处以上稳定复用才进入公共工具类。
- 禁止把默认值、空对象、吞异常、重试、宽松解析或 fallback 当作 Bug 修复。
- 修 Bug 必须先找到直接原因、根源原因和证据，再改造成问题的真实代码路径。
- 禁止超过 3 层核心业务嵌套；优先用 guard clause、早返回、领域对象、多态或策略拆掉。
- 禁止为了“以后扩展”写接口、工厂、manager、registry、adapter 或抽象父类。
- 不简化输入校验、认证鉴权、事务一致性、数据完整性、错误处理和审计日志。

## Spring Boot 分层

默认分层：

```text
controller      HTTP 入站、参数校验、响应转换
application     用例编排、事务边界、权限上下文
domain          领域对象、规则、策略和状态变化
infrastructure  Repository、外部系统、消息、缓存、文件
config          Spring 配置和 Bean 装配
```

规则：

- Controller 不写业务逻辑。
- Entity、DTO、Domain Object 不混用。
- 事务边界优先放在 application/service 用例入口。
- Repository 不做业务决策。
- Domain 尽量不依赖 Spring 注解；需要依赖时说明原因。
- 配置类只装配 Bean，不塞业务流程。

## Java 设计模式

善用面向对象，但不表演设计模式。

- 有真实可替换算法时，用策略模式。
- 有多个创建分支且调用方不该知道细节时，用工厂。
- 有领域事件或跨边界通知时，用观察者 / Spring event。
- 有类型差异行为时，用多态和动态绑定，不写长 `if/else` 或 `switch`。
- 只有一个实现、一个调用方或没有变化轴时，不新增接口、抽象类或工厂。
- 模式引入后必须减少条件分支、重复代码或错误边界；否则删掉。

## API 和校验

- 请求 DTO 使用 `jakarta.validation` 做边界校验。
- 响应 DTO 不直接暴露 Entity。
- 统一异常入口使用 `@RestControllerAdvice`。
- 错误响应至少包含稳定错误码、用户可读消息和 traceId。
- 分页、排序、过滤格式按项目已有约定；没有约定时先给最小契约。
- Controller 方法保持薄；超过参数校验和调用用例的逻辑要下沉。

## 配置和依赖

- 配置统一走 `application.yml`、profile、环境变量或配置中心。
- 密钥、token、连接串禁止硬编码。
- 新依赖必须先确认 Spring Boot starter、Java 标准库或已有依赖不能覆盖。
- 禁止同时引入功能重复的 JSON、HTTP、日期、校验或映射工具。
- Bean 装配只放跨对象协作，不用 Spring 容器替代清晰的构造函数依赖。

## 持久化和事务

- 修改数据库结构必须有 migration。
- 查询方法命名表达业务意图，不把复杂条件散在 Controller。
- 写操作默认有事务边界；读操作不随手加写事务。
- 禁止在循环里做可批量化数据库调用。
- N+1、懒加载、分页和大事务必须在 Review 中检查。

## 测试

- 新业务规则优先单元测试。
- Controller 行为用 `MockMvc` 或项目已有 HTTP 测试方式。
- Repository 行为用项目已有数据库测试方式；不要为了一个断言引入新测试框架。
- 修 Bug 必须有复现测试或明确验收用例，断言根因路径，不为 fallback 背书。
- 非平凡分支、循环、解析、权限、金钱和事务路径必须留下最小可运行检查。

## Review Checklist

- 是否先查了项目已有工具方法和同类实现。
- 是否新增了只被引用一次的 helper、接口、工厂或抽象类。
- 是否有相同功能工具函数没有收敛到公共 owner。
- 是否用 fallback、默认值、吞异常、宽松解析掩盖 Bug。
- 是否定位了 Bug 的直接原因、根源原因和证据。
- Controller 是否薄，事务是否在用例入口。
- DTO、Entity、Domain Object 是否边界清楚。
- 嵌套是否超过 3 层，是否能用 guard clause 或多态降低。
- 设计模式是否对应真实变化轴，是否减少了重复或分支。
- 输入校验、鉴权、事务、错误响应和日志是否完整。
- 是否运行了项目已有测试、lint、格式化或构建命令。

## 输出

实现或评审时输出：

- 改动文件或评审位置。
- 复用的已有工具、模式或 Spring 能力。
- 删除或拒绝新增的抽象。
- 验证命令和结果。

Shanforge work item 状态包：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: spring-boot-development-standards
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <changed file path or review notes>
- evidence:
  - <test/lint/build/root-cause evidence summary>
- ledger_event: <event id or none>
- needs:
  - review | verification | root_cause | user_input | none
```

`blocked` 用于 Bug 根因不明、项目现有模式冲突、关键配置缺失、测试无法运行且无法判断风险，或用户要求的抽象与最小可维护实现冲突。

`needs_user_input` 用于 Spring Boot 版本、分层边界、设计模式取舍、公共工具 owner、安全策略或兼容策略必须由用户决定的情况。
