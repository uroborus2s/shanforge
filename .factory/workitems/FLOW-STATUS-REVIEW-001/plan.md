# 状态与评审流程优化实施计划

- 工作项：FLOW-STATUS-REVIEW-001
- 状态：ready_for_commit
- 批准输入：本轮用户批准上轮建议；brief 的五项需求。
- 架构：保留 skill-first 与现有需求矩阵，不新增 runtime；pytest 核对事实，独立前向试用生成真实回复，另一个 reviewer 核对正文。
- 测试设计：本地文件场景，无服务、数据、凭证操作；事实判断与自由文本语义验证分层。

## Work Breakdown

| id | parent_id | title | status |
|---|---|---|---|
| WBS-FLOW-SR-01 | | 状态与证据评审合同 | completed |
| WBS-FLOW-SR-02 | | 状态与评审行为回归 | completed |
| WBS-FLOW-SR-03 | | 独立试用及集中质量收口 | current |

## 文件与职责

T01/T02 精确写集分别在对应 task brief；写集不交叉。父线程只写本 work item 与必要 memory，验证并收口，不替代 worker 写源码/测试。

## 任务与验证

1. T01（REQ-FLOW-01..04）：保留 scope_remaining 授权范围语义，增加总体范围事实；取消默认评分与阈值，兼容历史值只读；同步指南/相关测试。
2. T02（REQ-FLOW-05）：至少六个原始输入场景，oracle 不给试用者；新测试先因缺真实记录或错误事实而 RED，再消费真实返回；变异范围、完成、证据、候选与发现必须失败。不以自动事实判断冒充自由文本语义验收。
3. T03 依赖 T01/T02：独立代理实际执行场景，父线程忠实存档，独立 reviewer 检查正文/事实/缺陷发现/中文可读性；通过后本地中文提交，不推送。

运行：uv run pytest tests/test_delivery_status_review_behavior.py -q；相关合同集合；最终 uv run pytest -q、变更 Python 的 Ruff/代码形状、git diff --check。正式文档保持现有登记布局。

## 计划自审

五项需求均覆盖，任务写集独立，集中质量门不逐项评审。中风险本地流程资产，无生产/安全实现变更，无需单独计划评审。真实试用前不预填输出或通过。
