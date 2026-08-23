# Agent 会话卡

- 生成时间：2026-08-23 10:16 +0800
- 项目：`shanforge`
- 当前工作项：`MODEL-ROUTING-001`
- 当前任务：`MODEL-ROUTING-001-T03`
- 当前状态：`approved_ready_for_local_commit`
- 当前焦点：模型路由集中质量门、独立评审与本地提交
- 下一动作：`create_exact_local_commit_then_clean_clone_verify`

## 当前事实

- 用户要求的顺序不可交换：先事实统一、工作区清理和干净克隆全绿，再实现模型路由。
- 正式架构已确定 Shanforge 是 skill-first 资产，不是 Agent 平台运行时；仓库没有 `src/`。
- 当前工作区历史过程资产已做可恢复备份并按正式留存规则裁剪。
- 清理前完整测试为 `220 passed / 8 failed / 4 subtests`；仅跟踪文件模拟克隆为 `205 passed / 16 failed / 4 subtests`。
- 额外 8 个克隆失败来自未跟踪但被合同测试引用的最小事实资产，已识别并保留。

## 当前 Gate

- `T03_exact_local_commit_and_clean_clone_verification`
- 独立复审 `approved / 98 / C0-I0-M0`；当前进入精确本地提交和提交后干净克隆复验。

## 后续授权范围

- T01 通过后，Sol 作为唯一设计、分级和路由控制者；Terra/Luna 只执行路由包。
- 不新增模型服务、数据库、依赖或 `src/` 运行时。
- 不执行 push、PR、merge 或部署。

## 恢复入口

- `.factory/workitems/MODEL-ROUTING-001/brief.md`
- `.factory/workitems/MODEL-ROUTING-001/plan.md`
- `.factory/workitems/MODEL-ROUTING-001/ledger.jsonl`
