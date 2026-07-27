# FLOW-TASK-015 Review Checkpoint

## Review 输入

- 任务卡：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-015.md`
- 正式文档：`docs/05-design/workflow-execution-design.md`（`v1.2.0`，SHA-256
  `d330a3bc1e20cb160163e865aed83a2ddf4a4d395704880f31b3fb74e44d2d5d`）
- 受控候选：`.factory/workitems/FLOW-CONTRACT-001/drafts/FLOW-TASK-015-workflow-contract.v1.2.0.candidate.md`
- 测试：`tests/test_full_project_session_workflow_routing.py`
- 验证证据：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-015-verification.md`
- 实现报告：`.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-015-implementer-report.md`
- ledger：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`
- runtime Skills：TaskCard “允许修改”中的 9 个 Skill。

## Reviewer 检查项

- 正式方案是否覆盖完整软件项目会话行为。
- 每类会话行为是否归到明确工作流。
- 每个工作流是否有触发、输入、允许动作、禁止动作、输出、ledger/evidence 和 gate。
- 静默修改定义是否足以阻止未路由写文件。
- 方案是否避免创建孤立方案文件。
- 文档控制信息是否明确区分已发布基线和未批准方案候选，避免把候选伪装为正式契约。
- 是否清楚说明本轮尚未修改 workflow skill 运行规则。
- 结构测试是否解析 16 个行为、13 个工作流、必需列、写入负例、转换和基线 hash，而不只是搜索短语。
- 状态依赖测试是否使用专用快照或动态对账，不再绑定会变化的真实任务。
- 本轮新鲜验证是否支持 `ready_for_same_reviewer_rereview`。
- 正式文档是否原位发布且只保留一个当前版本控制块。
- 9 个 runtime Skills 是否只同步最小 route/result/write-policy 边界，没有重建中心路由器。
- 规定组合 `57 passed`、Ruff、9 个 Skill validator 和补充失败归因是否可复算。

## 当前结论

三轮方案 Review 最终 `approved / 98 / C0-I0-M1`，用户已批准冻结 hash。正式 v1.2.0 与 runtime Skill
同步的首轮实现 Review 为 `changes_requested / 76 / C0-I3-M0`，整改复审为
`approved / 98 / C0-I0-M0`。当前可进入精确本地提交；不授权远端动作。
