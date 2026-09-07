# 流程优化独立评审输入包

- Work item / Task：FLOW-STATUS-REVIEW-001 / FLOW-STATUS-REVIEW-001-T03
- 标准：本批 brief.md 的 REQ-FLOW-01..05（2026-09-07 批准范围）；现有 skill-first、总控唯一事实 owner、中文可读性和独立评审硬门。
- candidate_fingerprint：evidence/candidate-sha256.txt，复审清单 SHA-256 `3e86f667d21da7aac61aaa388fd9f642a233e3d12714ae47ea7a761c074ae4dc`；23 个 skill/模板/文档/测试文件加原始输入与v3回复的工作树内容，不以 HEAD 冒充未提交内容。首轮指纹保留在 independent-review.md。
- 实现摘要与证据：evidence/verification.md、brief.md、plan.md；父全量416 passed / 11 subtests passed，行为6 passed（含8份真实回复、mutation和新鲜性绑定）。评审独立核对，不照抄通过结论。
- 实际行为：evidence/raw-behavior-inputs.json、behavior-observations.json、behavior-observations-v2.json、behavior-observations-v3.json。前两轮失败原样保留，不是当前通过样本。
- 追踪与派发：ledger.jsonl、reviews/dispatch-receipts.jsonl；当前 .factory/memory 的 session/current-state/tasks/tests/skill-updates 五份摘要。

## 只读工作

1. 完整读当前 requesting-code-review skill、rubric、本批 brief 和已冻结候选 diff；检查上述五项需求有没有遗漏、矛盾或回归。
2. 独立核对 raw facts 与 v3 的8份正文，不以结构测试绿代替语义判断。尤其核对全产品/本批、总体阶段/活动、基线未知、未映射需求、已知未联调、权限缺陷、保留 Finding 与同候选新增证据原因、真正完成正例。判断中文是否能让用户直接知道是否完成、缺什么、下一步是什么。
3. 核对 oracle 是否源于输入，是否误把同义词当错误；核对 mutation 是否真实拒绝错误值，而不是 case ID 错配导致空过。语法、摘录存在和列表非空不是缺陷发现能力证明。
4. 核对默认不评分；有真实独立身份、候选/标准/范围/证据，未检查范围明示；历史评分不被擦除，若复审必须稳定 Finding ID。
5. 可运行：`shasum -a 256 -c <candidate manifest>`；`UV_CACHE_DIR=/private/tmp/shanforge-flow-uv-cache uv run --no-sync pytest -q`；变更 Python 的 Ruff/代码形状和 `git diff --check`。只读检查，允许测试临时缓存，不改源码/测试/状态，不提交、不推送，不操作服务/数据/凭证。

## 输出与范围

输出中文独立评审报告给父线程，由父忠实保存一份最终报告；不要写文件。包含 reviewer_type/id/independence_evidence、候选指纹、已检查/未检查范围、8案例语义结论、稳定 Finding ID/严重度/行号/证据、实际验证、review_status 与 next_gate_status。默认无总分。

只有 Critical/未接受 Important 均无且证据充分才可 approved；不足则 changes_requested 或证据不足，不以“没有找到”冒充保证。无真实人工 Gate，若 approved 返回 return_to_orchestrator，不标记任务 done。

不覆盖：其他软件产品验收或UI美术认可；真实项目长周期使用；模型长期稳定性/未见输入分布；发布部署；历史完整流程 eval 的重新前向运行。pytest 中的行为检查是本轮真实回复存档的确定性回放，不会每次调用模型。

## 同一reviewer复审输入

标准和范围不变。首轮FLOW-SR-REV-I-01要求补核心正文声明负向回归；只修改test_delivery_status_review_behavior.py，补完成状态明确声明、本批/产品剩余作用域、删除/反转/错配和自然否定拒绝。没有改skill、oracle、raw或v3正文；未知新表述仍需独立语义评审，不声称通用NLP。

父整改后完整pytest为416 passed / 11 subtests passed（10.45s，exit0）；行为6 passed；Ruff/shape/diff和25文件指纹均exit0。请复核Finding并在原报告追加复审差异，不擦除首轮。
