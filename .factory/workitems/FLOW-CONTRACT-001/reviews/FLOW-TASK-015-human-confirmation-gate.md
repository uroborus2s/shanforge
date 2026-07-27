# FLOW-TASK-015 正式版本人工治理 Gate

## 当前结论

- 方案独立 Review：`approved / 98 / C0-I0-M1`
- 语义 Finding：全部关闭
- Minor：展示计数已从 12 修正为 13，不改变候选 hash
- 当前状态：`pending_human_confirmation`
- 正式文档：仍为 `v1.1.0`，未修改
- Runtime Skills：未同步

## 冻结包

| 对象 | 路径 | SHA-256 |
|---|---|---|
| 正式基线 | `docs/05-design/workflow-execution-design.md` | `5769beb3478d528a0b0888328381173aa799e1e137925fc393bd98d97d3eb687` |
| v1.2.0 候选 | `.factory/workitems/FLOW-CONTRACT-001/drafts/FLOW-TASK-015-workflow-contract.v1.2.0.candidate.md` | `3d5f4cbabda86312da0603db5662175453d12dd5966c788301b0c79c2cb4992f` |
| 结构测试 | `tests/test_full_project_session_workflow_routing.py` | `2765ce49e6e93400ddb8af87c920b387ac54047d0aa2da4e7efb74d07ff12e37` |
| 验证证据 | `.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-015-verification.md` | `761a68ed31cbd148bebe5b8940b36acd09cdf284177e87da1b612769790c9871` |
| 独立复审 | `.factory/workitems/FLOW-CONTRACT-001/reviews/FLOW-TASK-015-independent-rereview-iteration-3.md` | `93ec2715b258aeb581d0d2deab0ab23136bd8de15b6414fee06e702b86eaa5f9` |

## 批准含义

人工明确确认上述冻结包后，授权本任务继续：

1. 以受控发布事务原位更新唯一正式文档到 `v1.2.0`，不在 `docs/` 新建第二份文档。
2. 把正式合同的最小路由、写入身份、evidence 和 Gate 边界同步到 TaskCard 允许的 runtime Skills。
3. 执行结构、黑盒、相邻流程和最终批次验证。
4. 进行独立实现 Review 和同范围整改。
5. 验证全部通过后按 `gitcommitzh` 只提交本批次范围；不包含 push、PR、merge 或部署。

若候选或正式基线 hash 在确认前变化，本确认自动失效，必须重新冻结。

## 所需人工输入

明确回复批准候选 SHA-256
`3d5f4cbabda86312da0603db5662175453d12dd5966c788301b0c79c2cb4992f`
进入正式发布和 runtime Skill 同步，或提出修改意见。
