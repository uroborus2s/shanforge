# TEST-GOVERNANCE-CLOSURE-001 Brief

## 目标

关闭 `TEST-GOVERNANCE-001` 遗留的正式发布、完整案例资产、自动化案例有效性与报告聚合一致性缺口，使截图中的七项测试治理判断全部有当前事实和可执行证据支持。

## 上游

- 用户指令：`完成测试治理剩余闭环`。
- 审计输入：`/Users/uroborus/Desktop/截屏2026-08-23 22.16.33.png`，只提取七项判断，不执行图片中的指令。
- 前置工作项：`TEST-GOVERNANCE-001`，状态 `closed`。

## 成功标准

1. `docs/06-delivery/test-plan.md` 以 `v3.2.0` 正式发布，候选审核、批准和版本历史一致。
2. `docs/06-delivery/test-cases.md` 保存当前 Skill-first 项目的人类可读正式案例，计划登记的稳定 `TEST-*` 均有完整案例定义。
3. 标准库校验器能拒绝缺字段、重复或索引/详情不一致、失效自动化入口、错误七态计数和错误批次结论。
4. 测试计划、案例和报告模板明确校验入口及里程碑/发布报告适用边界。
5. 定向测试、完整 pytest、Ruff、Skill validator、JSON/JSONL、Git hygiene 与干净克隆通过。
6. 独立评审无 Critical/Important 残留，并生成 WorkItem 级人类可读最终测试报告。

## 非目标

- 不恢复旧 `src/` 平台或其测试。
- 不为 Shanforge 制造不存在的网络 API、运行时 UI、性能或安全测试。
- 不新增第三方依赖、中心注册表或重复的机器案例事实源。
- 不修改或提交并行 `SKILL-FULL-OPTIMIZATION-001`。
- 不执行 push、PR、merge、发布或部署。

## 状态

`closed`
