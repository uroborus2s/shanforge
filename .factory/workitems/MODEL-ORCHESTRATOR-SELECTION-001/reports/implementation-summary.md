# 实现摘要

- 删除项目级主会话 `model` 与 `model_reasoning_effort` 固定项，保留用户并发值 10。
- 将现行合同中的 Sol 主控身份改为用户所选主会话；父会话继续负责子任务分级、授权、派发、失败关闭与收口。
- 保持现有 Luna/Terra worker 与 Terra reviewer 配置不变；动态子任务模型选择不在本任务范围。
- 同步 PRD、执行设计、用户指南、Skill 合同、代理说明、任务模板和定向测试。
