# SOFTWARE-LIFECYCLE-GOVERNANCE-001 验证证据

## 基本信息

- Work item：`SOFTWARE-LIFECYCLE-GOVERNANCE-001`
- Actor：`gpt-5.6-sol`
- 时间：`2026-09-01T21:41:49+08:00`
- 验证声明：当前候选已统一正式设计事实，补齐生命周期输入/输出/Gate 矩阵，建立跨文档一致性回归保护，并完成两轮 Review 整改。
- 结论：`review_approved`

## TDD 与根因整改

- 初始 Red：`tests/test_lifecycle_governance.py` 为 `5 failed / 1 passed`，真实暴露版本漂移、旧平台路径、退休附件/来源根、过期 `REQ-SF-008` 和缺失生命周期矩阵。
- 首轮 Green：生命周期专项 `8 passed`；正式测试登记治理 `1 passed`。
- 首轮定向回归：`44 passed / 8 failed`，定位到工作流重写误删现行路由/风险/Gate 合同和登记集合未同步；回原 Terra owner 整改。
- 首轮完整回归：`277 passed / 10 failed / 4 subtests passed`，定位到剩余工作流细则、API 快速通道和 memory 投影遗漏；回原 owner 修复。
- memory 定向回归：`2 passed`。

## 最终候选验证

| 检查 | 真实结果 | exit code |
|---|---|---:|
| `uv run pytest -p no:cacheprovider -q` | `290 passed, 4 subtests passed in 2.21s`；failed/error/skipped/not_run 为 0 | 0 |
| `uv run ruff check .` | `All checks passed!` | 0 |
| 全部 Skill `quick_validate.py` | `38/38` 返回 `Skill is valid!` | 0 |
| TOML / JSON / JSONL 解析 | `6 TOML / 176 JSON / 47 JSONL valid` | 0 |
| 测试案例目录 validator | `catalog: valid (5 cases)` | 0 |
| `git diff --check` | 无输出 | 0 |

## 需求核对

- 正式设计事实：10 份当前设计/接口 owner 已改为 Skill-first；旧 OpenAPI、manifest、tokens 与来源登记已删除。
- 生命周期：矩阵覆盖触发、输入、准入、活动、输出、保存、owner/模型、验证、退出 Gate 和回流；明确阶段门、Spike/原型、TDD、根因、定向回归、Review、候选验证与发布。
- 一致性：`TEST-BB-002` 检查正式版本索引、旧平台路径、退休附件/来源、需求状态、生命周期矩阵结构与逐阶段语义、设计导航、测试文档控制、current memory 和来源候选。
- 过程数据：WorkItem brief、plan、四张 task brief、ledger、T01 evidence、本验证证据、实现摘要和 review input 均可回源。

## 偏离与残余风险

- UI、HTTP API、服务、E2E、安全和性能运行测试未运行：本次只变更 Markdown/JSON 治理合同和 pytest 静态/结构守卫，没有可启动的 UI/API/服务运行面。
- 首轮独立 Review 为 `58 / C0-I4-M0`；两轮整改后，同一 reviewer iteration 3 为 `approved / 97 / C0-I0-M0`。
- 本地提交和提交后干净克隆尚未执行；它们是复审通过后的 Gate，不被本候选验证结论替代。

## 结论

`review_approved`
