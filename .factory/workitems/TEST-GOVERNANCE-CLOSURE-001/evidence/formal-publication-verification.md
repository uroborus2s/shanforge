# TEST-GOVERNANCE-CLOSURE-001 正式发布验证

## 声明与候选

- 声明层级：`stage`，覆盖测试治理剩余闭环，不代表并行 Skill 优化工作项完成。
- 正式发布：`TEST-PLAN-001 v3.2.0`、`TEST-CATALOG-SHANFORGE-001 v1.0.0`。
- 候选构造：当前 `HEAD 28b82dd` 加本 WorkItem 精确暂存差异；并行 `SKILL-FULL-OPTIMIZATION-001` 全部排除。

## 新鲜验证

| 检查 | 结果 | Exit code |
|---|---|---:|
| 治理专项 `uv run pytest -q tests/test_project_test_governance.py` | `16 passed` | 0 |
| 隔离候选完整 pytest | `246 passed, 4 subtests passed` | 0 |
| 隔离候选 Ruff | `All checks passed!` | 0 |
| 正式案例目录校验 | `catalog: valid (4 cases)` | 0 |
| `document-templates` Skill validator | `Skill is valid!` | 0 |
| `verification-before-completion` Skill validator | `Skill is valid!` | 0 |
| 校验器 `py_compile` | 无错误 | 0 |
| 项目 JSON / JSONL 解析 | `44 JSON / 38 JSONL valid` | 0 |
| 隔离候选 `git diff --check` | 无输出 | 0 |

## Red-Green 与评审

- 初始 Red：`6 failed / 9 passed`；缺正式版本、案例目录、校验器和报告负例。
- Review 整改 Red：`3 failed / 12 passed / 1 deselected`；暴露裸 `python`、索引漂移和负数计数绕过。
- 最终 Green：正式发布门切换后治理专项 `16 passed`；隔离完整候选 `246 passed / 4 subtests passed`。
- 独立复审：`approved / 98 / C0-I0-M0`，允许正式发布。

## 合并工作区诊断

合并工作区完整 pytest 曾为 `2 failed / 247 passed / 4 subtests passed`。两个失败稳定定位到并行 WorkItem 在 22:41 改写的 `.factory/memory/current-state.md` 与 `.factory/memory/agent-session.md`：前者缺稳定 ledger 回源，后者的下一动作不符合反引号字段合同。本 WorkItem 未越权修改或暂存这两个文件；隔离候选完整回归证明本候选无这些失败。

## 未运行与残余风险

- 网络 API、动态 UI、性能和安全专项未运行：Shanforge 当前没有对应运行时暴露面。
- 提交后仍需以不可变提交运行一次干净克隆终验，再生成最终人类可读测试报告并关闭 WorkItem。
