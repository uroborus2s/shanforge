---
name: java-developer
description: Java / Spring Boot 工程开发 skill。用于 Java 后端、Spring MVC、Spring Data、Spring Security、接口实现、代码评审、重构、Bug 修复方案、开发文档和工程规范；先判断阶段和工作方式，再按需读取 references。
---

# Java Developer

用于 Java / Spring Boot 项目的工程开发。先判断当前阶段和工作方式，再执行最小动作。

## 触发

- Java 或 Spring Boot 项目开发、重构、评审和测试。
- Controller、Service、Repository、DTO、Entity、配置、异常、事务、安全、日志和测试相关工作。
- 用户要求 Java 后端工程规范、代码规范、文档规范或 Review checklist。
- Bug 修复方案需要确认是否针对根因。

## 边界

- Bug 根因不清楚时，先进入 `systematic-debugging`；本 skill 不替代根因调查。
- API 契约设计优先交给 `api-design`；本 skill 只约束 Java / Spring Boot 落地。
- 正式文档体系变更优先交给 `document-templates`；本 skill 只给 Java 开发侧文档要求。
- 不为“以后可能”新增依赖、接口、工厂、manager、registry 或公共工具类。

## 阶段判断

每次先读 [工程阶段与工作方式](references/engineering-standards.md)，判断一个阶段：

| 阶段 | 本 skill 允许做什么 | 禁止 |
|---|---|---|
| 需求 / 澄清 | 明确业务目标、边界、验收和未决问题 | 写实现 |
| 技术设计 | 定分层、接口、数据、事务、测试和文档影响 | 直接开写代码 |
| 实现 | 按既有结构写最小代码和测试 | 新增无依据抽象 |
| Bug 修复 | 根因已明确后写复现测试和根因修复 | fallback 式补丁 |
| 重构 | 保持行为，删除重复，收敛工具方法 | 顺手改需求 |
| Review | 按 checklist 报可执行问题 | 泛泛评价代码丑 |
| 文档 | 更新与代码行为对应的开发文档 | 写空壳文档 |

## 按需读取

- 代码实现、重构、Bug 修复和代码评审：读 [代码规范](references/code-standards.md)。
- README、接口说明、开发文档和变更说明：读 [文档规范](references/documentation-standards.md)。
- 只问概念时直接回答，不读取无关 reference。

## 工作方式

| 工作方式 | 默认动作 | 必要输出 |
|---|---|---|
| 新功能 | 先确认需求和设计，再实现最小代码 | 改动文件、测试、文档影响 |
| Bug 修复 | 先确认根因证据，再改根因路径 | 复现、根因、回归测试 |
| 重构 | 先列行为不变边界，再小步改 | 删除/收敛内容、验证 |
| 代码评审 | 只报风险、Bug、规范违背和缺测试 | 文件行号、原因、建议 |
| 文档 | 只写当前代码事实和使用方式 | 文档路径、事实来源 |
| 工程规范 | 输出可执行约束和 Review checklist | 适用范围、禁止项、门槛 |

## 输出

实现或评审时输出：

- 当前阶段和工作方式。
- 已读取的 reference。
- 改动文件或评审位置。
- 复用的已有工具、模式或 Spring 能力。
- 删除或拒绝新增的抽象。
- 验证命令和结果。

Shanforge work item 状态包：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: java-developer
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <changed file path or review notes>
- evidence:
  - <test/lint/build/root-cause evidence summary>
- ledger_event: <event id or none>
- needs:
  - review | verification | root_cause | user_input | none
```

`blocked` 用于阶段不清、Bug 根因不明、项目现有模式冲突、测试无法运行且风险不可判断，或用户要求与最小可维护实现冲突。

`needs_user_input` 用于 Java / Spring Boot 版本、分层边界、设计模式取舍、公共工具 owner、安全策略、兼容策略或文档公开范围必须由用户决定的情况。
