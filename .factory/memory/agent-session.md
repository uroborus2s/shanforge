# Agent 会话卡

- 生成时间：2026-09-07
- 项目：`shanforge`
- 项目是否完成：无法确认；本轮只评定已批准的流程优化批次
- 总体阶段与当前活动：Shanforge 全产品阶段未核对；本批已完成，无活动开发任务
- 本批剩余：无
- 已批准产品剩余：未知（未核对 Shanforge 完整产品基线）
- 未知/未验证与未开始：本批实现和验证无剩余；其他产品不在本轮范围
- 遗漏核对：本批五项需求均有实现、验证和独立评审，无未映射项；Shanforge 全产品基线尚未核对
- 项目整体进度：无法计算；不以本批任务数代表产品进度
- 当前工作项：`FLOW-STATUS-REVIEW-001`
- 当前任务：`FLOW-STATUS-REVIEW-001-T03`
- 当前 WBS：`WBS-FLOW-SR-03`
- 当前状态：`closed`
- 当前 Gate：`closed`
- 停止原因：无
- 下一动作：`none`

## 当前事实

- 用户已批准上轮状态与评审优化建议；T01 修改现有合同，T02 补事实与行为回归，已真实派发。
- 已完成：合同与测试修改、三轮真实试用、父全量416 passed / 11 subtests passed、行为6 passed；独立复审approved，FLOW-SR-REV-I-01已关闭。前两轮失败原样保留，实现已本地提交27fe2cd，未推送。
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

- `.factory/workitems/FLOW-STATUS-REVIEW-001/ledger.jsonl`
- `.factory/workitems/FLOW-STATUS-REVIEW-001/plan.md`
- `.factory/workitems/FLOW-STATUS-REVIEW-001/reviews/dispatch-receipts.jsonl`
- `.factory/workitems/FLOW-STATUS-REVIEW-001/task-briefs/FLOW-STATUS-REVIEW-001-T03.md`
