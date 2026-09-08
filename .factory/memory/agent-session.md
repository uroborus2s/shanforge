# Agent 会话卡

- 生成时间：2026-09-08
- 项目：`shanforge`
- 项目是否完成：无法确认；本轮只评定动态子任务模型合同
- 总体阶段与当前活动：Shanforge 全产品阶段未核对；本任务实现、独立终审和验证已通过，进入提交
- 本批剩余：本地中文提交与提交回执
- 已批准产品剩余：未知（未核对 Shanforge 完整产品基线）
- 未知/未验证与未开始：新增 task-reader 的新会话宿主加载和执行未实测
- 遗漏核对：八项合同验收均有对应实现与检查；宿主角色加载不以 TOML 校验代替
- 项目整体进度：无法计算；本批不能代表全产品进度
- 当前工作项：`MODEL-DYNAMIC-DISPATCH-001`
- 当前任务：`MODEL-DYNAMIC-DISPATCH-001-T00`
- 当前 WBS：`WBS-MODEL-DYNAMIC-00`
- 当前状态：`ready_for_commit`
- 当前 Gate：`commit`
- 停止原因：无
- 下一动作：`create_exact_local_commit`

## 当前事实

- 主会话由用户选择，每个子任务按复杂度、风险、推理需求和角色显式选 model / reasoning_effort，fork_turns=none。
- 合同默认 Luna/low、Terra/medium，设计判断 Astra/high，深度或高风险 Astra/xhigh，有证据的单个难题 Astra/max；普通独立评审 Terra/high。
- v5独立终审批准20文件，MODEL-DYN-I-01已关闭；最终完整420 passed / 11 subtests passed，代码形状无新增违规。
- 真实派发回执与12个路由模拟分开保存；新task-reader未实测宿主加载，未暴露时拒绝使用。
- 前置解耦提交1b64734 / 242af89已完成；旧FLOW候选指纹不变，并发值10不变。

## 已读取上下文

- 当前工作项 brief、plan、任务卡、ledger、候选指纹、独立review和验证记录。
- 当前模型工具能力、OpenAI官方模型/子代理文档、现行skill合同和直接测试消费者。

## 未读 / 已排除上下文

- 其他产品业务服务、数据库、凭证及全产品验收；历史正式证据保持不变。

## 禁止动作

- 不将本批通过解释为Shanforge全产品完成，不将模拟或工具accepted解释为内部模型/宿主加载证明。
- 不恢复中心runtime、不新增依赖、不改全局配置、不推送。

## 恢复入口

- `.factory/workitems/MODEL-DYNAMIC-DISPATCH-001/ledger.jsonl`
- `.factory/workitems/MODEL-DYNAMIC-DISPATCH-001/reviews/final-review.md`
- `.factory/workitems/MODEL-DYNAMIC-DISPATCH-001/evidence/verification.md`
- `.factory/workitems/MODEL-DYNAMIC-DISPATCH-001/reports/delivery.md`
