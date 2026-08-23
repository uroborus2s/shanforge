# MODEL-ROUTING-001-T01 实施报告

## 完成内容

- 将项目配置、技术画像、正式 PRD、追踪矩阵、文档索引和当前 memory 统一到 skill-first 产品边界。
- 备份并删除约 95MB 历史过程资产，只保留可复现所需的最小事实集。
- 修复 8 个旧事实断言、补齐 Bug 根因门，并把未跟踪但被合同依赖的最小资产纳入候选。
- 将完整 pytest 从 `8 failed` 收敛到 `228 passed / 4 subtests passed`，根 Ruff 与 diff check 通过。

## 既有脏工作区归属

| 变更组 | 归属 | 处置 |
|---|---|---|
| PM 快照 renderer、UI 文档及相邻测试 | `SKILL-FIRST-PM-001` / `PM-DASHBOARD-005` 的既有用户工作 | 保留实现，只裁过程截图和重复 review；纳入基线 |
| FLOW 计划、TaskCard、ledger 和流程测试 | `FLOW-CONTRACT-001` 既有合同演进 | 保留正式合同和最小测试证据；纳入基线 |
| AI 剧本、Skill 流程、提交门和任务范围测试 | 既有工作 Skill 合同演进 | 保留并修复旧事实断言；纳入基线 |
| project、tech profile、PRD、追踪矩阵和当前 memory | `MODEL-ROUTING-001-T01` | 重写冲突事实 owner；纳入基线 |
| 大型候选、原始证据、截图和多轮 review | 已过期过程资产 | 备份后删除；不纳入 Git |

精确提交候选以复审时的 `git diff --cached --name-only` 为准；本任务不按来源伪造作者，
而是依据用户“清理工作区”的明确要求把全部已验证既有改动收口为本地基线。

## 未提前声明

- 尚未声明干净克隆通过；该验证等待本地基线提交后执行。
- 尚未实现 Sol/Terra/Luna 路由；该工作属于 T02。
- 未执行 push、PR、merge 或部署。

## 独立 review 整改

- 删除 PRD 和追踪矩阵中未隔离的旧平台运行时正文，只保留当前 skill-first 需求集合。
- 关闭 `.factory/project.json` 的 `api_platform/public_api/sdk/self_hosted` 当前能力声明。
- 对齐 current-state、session 与 ledger 的 review remediation Gate。
- 把 JSON/JSONL 命令改为可直接运行的原文，增加归档 SHA-256、1806 条内容校验和三文件恢复比对。
- 通过既有变更归属表和暂存区精确文件清单限定 T01 本地基线范围。
