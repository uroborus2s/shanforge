# TASK-SKILL-001 Revision 4 实施报告

## 结果

用户提出的六项修改已落到 skill 规则、来源评估、服务模板和结构测试：

- GitHub 候选：重点评估 `samber/cc-skills-golang`、`Melkeydev/go-blueprint`、`evrone/go-clean-template`，记录可借鉴项与拒绝项。
- Ponytail：现有代码、标准库、已有依赖、最少新代码的顺序成为硬规则。
- 代码形状：禁止仅为排版拆分单次调用私有 helper；嵌套目标 2 层、硬上限 3 层。
- Go 式对象设计：struct 所有权、组合、消费方小接口；不把 Java 分层和继承模型移植到 Go。
- 模式门槛：Strategy、Factory、Adapter、Middleware、State、Observer、Functional Options 均要求当前真实问题。
- 回退与兼容：禁止推测性 fallback、alias、dual-read/dual-write、多驱动包装、宽松解析和失败后尝试第二方案。

模板同步减重：删除两个单次调用包装 package 和两个私有流程 helper；随机 request ID 失败时不再生成弱 fallback，而是记录结构化错误并明确失败。

## 状态

作者自检通过，状态为 `ready_for_review`。独立评审与人工确认尚未完成。
