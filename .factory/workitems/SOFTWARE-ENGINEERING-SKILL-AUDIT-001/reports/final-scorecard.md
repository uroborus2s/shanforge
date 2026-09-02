# 软件工程 Skill 五专家完整评分表

## 评分口径

- 每个专家独立覆盖 38 个 Skill，只按自己的专业视角评分。
- 单 Skill 综合分 = 中文、Skill 设计、软件工程、项目管理、沟通五项等权平均。
- 系统矩阵总分 = 38 个 Skill 综合分的平均值。
- 专家另外给出系统级整体判断；整体判断用于评估跨 Skill 问题，不替代逐 Skill 矩阵。

## 总分

- 190 个逐项评分覆盖：`190/190`
- 系统矩阵总分：`85.6/100`
- 专家整体判断等权平均：`85.1/100`
- 逐项维度均值：中文 `87.3`、Skill 设计 `86.0`、软件工程 `80.6`、项目管理 `83.7`、沟通 `90.2`
- 审计结论：`changes_recommended`；无 Critical，但存在多项 Important 合同冲突和可执行性缺口。
- 审计提交：`4929f58`（`docs: 完成软件工程 Skill 五专家审计`）。
- 工作项状态：审计交付已关闭；整改尚未实施，需要另行授权整改批次。

## 38 个 Skill 五维评分

| Skill | 中文 | Skill 设计 | 软件工程 | 项目管理 | 沟通 | 综合 |
|---|---:|---:|---:|---:|---:|---:|
| agent-harness-construction | 88 | 87 | 78 | 83 | 82 | 83.6 |
| ai-first-engineering | 93 | 88 | 83 | 82 | 86 | 86.4 |
| ai-regression-testing | 93 | 91 | 86 | 86 | 91 | 89.4 |
| algorithmic-art | 92 | 86 | 82 | 82 | 94 | 87.2 |
| api-design | 91 | 91 | 87 | 88 | 92 | 89.8 |
| art-asset-pipeline | 89 | 72 | 76 | 84 | 94 | 83.0 |
| article-writing | 89 | 90 | 85 | 79 | 86 | 85.8 |
| brainstorming | 81 | 88 | 76 | 85 | 83 | 82.6 |
| browser-control | 87 | 74 | 83 | 84 | 93 | 84.2 |
| crawler4j-model-project | 86 | 86 | 74 | 88 | 88 | 84.4 |
| doc-coauthoring | 93 | 89 | 88 | 83 | 94 | 89.4 |
| document-templates | 87 | 84 | 79 | 90 | 92 | 86.4 |
| docx | 89 | 83 | 84 | 83 | 94 | 86.6 |
| executing-plans | 82 | 84 | 71 | 80 | 84 | 80.2 |
| frontend-patterns | 88 | 91 | 87 | 82 | 93 | 88.2 |
| gitcommitzh | 90 | 92 | 86 | 87 | 95 | 90.0 |
| go-developer | 87 | 89 | 85 | 84 | 83 | 85.6 |
| humanizer | 95 | 90 | 90 | 79 | 78 | 86.4 |
| java-developer | 93 | 87 | 78 | 82 | 89 | 85.8 |
| pdf | 90 | 82 | 86 | 83 | 94 | 87.0 |
| project-memory | 83 | 80 | 80 | 75 | 91 | 81.8 |
| python-uv-project | 88 | 84 | 82 | 83 | 85 | 84.4 |
| receiving-code-review | 86 | 82 | 78 | 85 | 90 | 84.2 |
| release-deployment | 93 | 90 | 84 | 90 | 88 | 89.0 |
| requesting-code-review | 85 | 91 | 82 | 89 | 93 | 88.0 |
| requirements-engineering | 86 | 87 | 79 | 86 | 92 | 86.0 |
| shadcn | 88 | 85 | 82 | 82 | 93 | 86.0 |
| stratix-admin-web | 85 | 86 | 84 | 84 | 90 | 85.8 |
| stratix-service | 86 | 86 | 72 | 85 | 89 | 83.6 |
| subagent-driven-development | 78 | 85 | 68 | 79 | 85 | 79.0 |
| systematic-debugging | 92 | 91 | 88 | 88 | 95 | 90.8 |
| tdd-workflow | 87 | 90 | 79 | 87 | 96 | 87.8 |
| ui-ux-pro-max | 83 | 86 | 80 | 85 | 90 | 84.8 |
| using-shanforge | 73 | 83 | 70 | 76 | 91 | 78.6 |
| verification-before-completion | 81 | 92 | 75 | 89 | 96 | 86.6 |
| webapp-testing | 88 | 85 | 85 | 87 | 93 | 87.6 |
| writing-plans | 82 | 77 | 68 | 74 | 93 | 78.8 |
| xlsx | 91 | 84 | 84 | 83 | 94 | 87.2 |

## 排名观察

- 前五：`systematic-debugging 90.8`、`gitcommitzh 90.0`、`api-design 89.8`、`ai-regression-testing 89.4`、`doc-coauthoring 89.4`。
- 后五：`using-shanforge 78.6`、`writing-plans 78.8`、`subagent-driven-development 79.0`、`executing-plans 80.2`、`project-memory 81.8`。
- 分数最低的不是具体语言/框架 Skill，而是总控、计划、执行、子代理和恢复链路，说明主要风险集中在跨 Skill 协作合同。

## 专家整体判断

| 专家 | 整体分 | 原始严重度 |
|---|---:|---|
| 中文语言 | 87.3 | C0 / I7 / M6 |
| Skill 设计 | 86.0 | C0 / I5 / M4 |
| 软件工程 | 81.0 | C0 / I5 / M3；原审计输入 Critical 已复核关闭 |
| 软件项目管理 | 81.0 | C0 / I5 / M2 |
| 沟通 | 90.0 | C0 / I5 / M3 |

原始专家 Findings 合计 `C0 / I27 / M18`；相同根因在跨专家报告中有重复，最终按主题去重和优先级见 `consolidated-audit.md`。

## 整改后复评（2026-09-02）

- 五专家再次覆盖全部 38 个 Skill，评分覆盖仍为 `190/190`。
- 系统矩阵总分从 `85.6` 提升到 `92.9`，变化 `+7.3`。
- 原始 `C0 / I27 / M18` 共 45 个问题已关闭 `45/45`。
- 最终剩余 `Critical 0 / Important 0 / Minor 0`，五专家均给出 `approved`。
- 本节只追加整改后事实，不覆盖上方审计基线。完整前后评分、问题关闭说明和验证证据见 `../../SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001/reports/post-remediation-scorecard.md`。
