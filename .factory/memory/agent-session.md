# Agent 会话卡

- 生成时间：2026-09-08
- 项目：`shanforge`
- 项目是否完成：无法确认；本轮只评定主会话模型解耦任务
- 总体阶段与当前活动：Shanforge 全产品阶段未核对；本任务已完成并本地提交
- 本批剩余：无
- 已批准产品剩余：未知（未核对 Shanforge 完整产品基线）
- 未知/未验证与未开始：宿主侧实际模型选择未做 UI 验收；并行动态派发任务不在本任务范围
- 遗漏核对：本任务验收项均有实现、验证和独立评审；Shanforge 全产品基线尚未核对
- 项目整体进度：无法计算；不以本批任务数代表产品进度
- 当前工作项：`MODEL-ORCHESTRATOR-SELECTION-001`
- 当前任务：`MODEL-ORCHESTRATOR-SELECTION-001-T01`
- 当前 WBS：`WBS-MODEL-ORCHESTRATOR-01`
- 当前状态：`closed`
- 当前 Gate：`closed`
- 停止原因：无
- 下一动作：`none`

## 当前事实

- 项目配置不再固定主会话模型和推理强度；主会话模型由用户选择。
- 子任务派发合同仍由主会话执行，Luna/Terra worker 与 Terra reviewer 的模型、强度和沙箱未变。
- 全量418 passed / 11 subtests passed；R6 独立复审 approved，无剩余 Critical/Important。
- 旧 FLOW-STATUS-REVIEW-001 manifest 已保持原始指纹；当前测试不再把历史候选当作可变缓存。
- 本任务已本地提交 `1b64734`，未推送；并行动态派发任务未包含在该提交中。
- 不修改 ita-club 或医院项目，不生成它们的完成度。
- UI-CLIENT-CRAFT-001 已关闭，本地提交 cb867e5 / b4706b4；其候选与生产边界不变，不恢复旧 Gate。

## 已读取上下文

- 本工作项 brief、plan、task-briefs、ledger 和派发回执。
- 状态与评审合同、skill-creator、计划/执行/验证 skill、相关测试。
- 用户指南按 doc-map 单文件回源；历史摘要只读顶部。

## 未读 / 已排除上下文

- 不读取或修改其他产品正式文档、业务服务、数据库或凭证。
- 不对其他产品作全需求验收；不读取历史任务全文。

## 禁止动作

- 不将结构事实检查当作自由文本语义验收，不将本批完成当作其他产品完成。
- 不新增中心 runtime/依赖或平行需求台账；不伪造真实试用响应。
- 不推送，不安装新依赖，不修改全局配置或全局 memory。

## 恢复入口

- `.factory/workitems/MODEL-ORCHESTRATOR-SELECTION-001/ledger.jsonl`
- `.factory/workitems/MODEL-ORCHESTRATOR-SELECTION-001/reviews/independent-review.md`
- `.factory/workitems/MODEL-ORCHESTRATOR-SELECTION-001/evidence/final-verification.md`
- `.factory/workitems/MODEL-ORCHESTRATOR-SELECTION-001/task-briefs/MODEL-ORCHESTRATOR-SELECTION-001-T01.md`
