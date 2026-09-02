# 软件工程 Skill 审计闭环与复评计划

**工作项：** `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001`

**状态：** `completed`

**目标：** 逐条核销五位专家的 `C0 / I27 / M18`，修复仍未关闭的问题，并生成有证据的整改前后评分，而不是覆盖整改前基线。

## Work Breakdown

| id | parent_id | title | status |
|---|---|---|---|
| WBS-AUDIT-09 |  | 建立 45/45 原始问题闭环表与评分结构 | completed |
| WBS-AUDIT-10 | WBS-AUDIT-09 | 补齐可执行性与真实样本验证 | completed |
| WBS-AUDIT-11 | WBS-AUDIT-10 | 补齐响应、评审和状态 owner 合同 | completed |
| WBS-AUDIT-12 | WBS-AUDIT-11 | 清理专业歧义和重复合同 | completed |
| WBS-AUDIT-13 | WBS-AUDIT-12 | 五专家复评与集中质量门 | completed |
| WBS-AUDIT-13-R01 | WBS-AUDIT-13 | 更新与单一结果包 owner 冲突的旧回归断言 | completed |
| WBS-AUDIT-13-R02 | WBS-AUDIT-13 | 补齐正式计划模板、owner、依赖 DAG 与真实贯通测试 | completed |
| WBS-AUDIT-13-R03 | WBS-AUDIT-13 | 补齐 Crawler4j/Stratix lock 与 CLI smoke | completed |
| WBS-AUDIT-13-R04 | WBS-AUDIT-13 | 阻止嵌套 lambda 绕过代码形态门 | completed |
| WBS-AUDIT-13-R05 | WBS-AUDIT-13 | 补齐 T10–T12 父工具派发回执证据 | completed |
| WBS-AUDIT-13-R06 | WBS-AUDIT-13 | 迁移当前工作项 TaskCard owner 与依赖图 | completed |

## T09：逐条确认原始问题状态

**解决的问题：** 原整改只按主题说明完成，没有把五份专家报告中的 45 个原始 Finding 逐项核销。

**写入：**

- `reports/finding-closure-matrix.md`：每项记录来源、严重度、问题、根因、精确位置、状态、证据和后续任务。
- `reports/post-remediation-scoring-rubric.md`：冻结整改后评分字段、评分锚点和质量 Gate。
- `evidence/T09-count-and-trace-check.md`：证明 `I=27`、`M=18`、总数 45、ID 唯一。

**验收：** 45/45 可追踪；所有未关闭项都有 T10–T12 的准确 owner、文件和验证目标。

## T10：补齐真实可执行验证

**解决的问题：** DOCX/XLSX 主要是语法或说明级检查；资源 manifest 和代码形状仍可能依赖人工自报。

**允许修改：**

- `skills/docx/SKILL.md` 及 `skills/docx/scripts/office/{pack.py,unpack.py,validate.py}`。
- `skills/xlsx/SKILL.md` 及 `skills/xlsx/scripts/office/{pack.py,unpack.py,validate.py}`。
- `skills/art-asset-pipeline/SKILL.md` 与新建 `skills/art-asset-pipeline/scripts/validate_manifest.py`。
- `skills/verification-before-completion/SKILL.md`。
- `skills/crawler4j-model-project/SKILL.md` 与新建 `skills/crawler4j-model-project/scripts/check_compatibility.py`。
- `skills/stratix-service/SKILL.md`、`skills/stratix-service/references/cli-workflow.md` 与新建 `skills/stratix-service/scripts/check_compatibility.py`。
- `skills/tdd-workflow/SKILL.md` 与新建 `skills/tdd-workflow/scripts/check_code_shape.py`。
- `tests/test_external_tool_skill_fallbacks.py`。
- 新建 `tests/test_office_skill_roundtrip.py`、`tests/test_art_asset_manifest_contract.py`。
- `tests/test_crawler4j_model_skill_integration.py`、`tests/test_stratix_service_skill.py`、`tests/test_stratix_service_framework_guide.py`。
- `tests/test_verification_debugging_workflow_skills.py`、新建 `tests/test_code_shape_check.py`。
- `tests/test_writing_plans_skill.py`、`tests/test_using_shanforge_snapshot.py`。

**最小实现：** 使用现有脚本和 Python 标准库构造最小 OOXML/manifest 样本；验证解包→打包→再次验证和 manifest 路径存在性。manifest 与版本 fixture 必须执行所属 Skill 的真实校验入口；Office 测试不得以替换安全 XML 解析器换取通过。只有测试证明现有脚本有缺陷时才改脚本，不新增依赖或无职责公共 helper。

**定向验证：**

```bash
uv run pytest -q tests/test_external_tool_skill_fallbacks.py tests/test_office_skill_roundtrip.py tests/test_art_asset_manifest_contract.py
uv run ruff check tests/test_external_tool_skill_fallbacks.py tests/test_office_skill_roundtrip.py tests/test_art_asset_manifest_contract.py
```

## T11：补齐响应、评审和状态 owner 合同

**解决的问题：** 原审计指出 receiving/requesting review 的 triage owner、project-memory 无活动状态分支和工作 Skill 共享响应接入可能不一致。

**允许修改：**

- `skills/receiving-code-review/SKILL.md`。
- `skills/requesting-code-review/SKILL.md`。
- `skills/project-memory/SKILL.md`。
- `skills/project-memory/references/session-card-template.md`。
- `skills/writing-plans/references/plan-review-template.md`、`skills/writing-plans/references/workitem-plan-template.md`。
- `skills/webapp-testing/SKILL.md`、`skills/agent-harness-construction/SKILL.md`、`skills/release-deployment/SKILL.md`。
- `skills/using-shanforge/references/work-skill-return-contract.md`、`skills/using-shanforge/references/human-readable-status.md`。
- `tests/test_review_workflow_skills.py`。
- `tests/test_project_memory_skill.py`。
- `tests/test_work_skill_status_envelope_ownership.py`。
- `tests/test_remaining_skill_project_status_contract.py`、`tests/test_human_response_contract_integration.py`。
- 新建 `tests/test_response_owner_contracts.py`。

**最小实现：** 先用现有测试确认 32 个工作 Skill 是否已经且只引用一次共享合同；已满足则不批量改 32 个文件。只修实际冲突：谁生成 triage/response、无活动 WorkItem 的 `SB-STATUS/no_project_write`、未授权 memory/ledger 路径的交还方式。

**定向验证：**

```bash
uv run pytest -q tests/test_review_workflow_skills.py tests/test_project_memory_skill.py tests/test_work_skill_status_envelope_ownership.py
uv run ruff check tests/test_review_workflow_skills.py tests/test_project_memory_skill.py tests/test_work_skill_status_envelope_ownership.py
```

## T12：清理歧义和已确认重复合同

**解决的问题：** `ui-ux-pro-max` 的“数据库命中”、`frontend-patterns` 的“远端组件”、`stratix-admin-web` 的“总结相似组件”存在专业歧义；`using-shanforge` 可能重复承载已在 reference 中定义的机器合同。

**允许修改：**

- `skills/ui-ux-pro-max/SKILL.md`。
- `skills/frontend-patterns/SKILL.md`。
- `skills/stratix-admin-web/SKILL.md`。
- `skills/browser-control/SKILL.md`、`skills/article-writing/SKILL.md`。
- `skills/writing-plans/SKILL.md`、`skills/executing-plans/SKILL.md`、`skills/subagent-driven-development/SKILL.md`。
- `skills/using-shanforge/SKILL.md`。
- `skills/using-shanforge/references/work-skill-return-contract.md`。
- `skills/using-shanforge/references/human-readable-status.md`。
- `skills/using-shanforge/references/pm-dashboard-rendering.md`。
- `skills/using-shanforge/references/black-box-flow-eval.md`。
- `tests/test_ui_ux_pro_max_skill.py`。
- `tests/test_stratix_admin_web_skill.py`。
- `tests/test_browser_control_skill.py`、`tests/test_writing_plans_skill.py`、`tests/test_execution_workflow_skills.py`。
- `tests/test_black_box_workflow_eval.py`。
- 新建 `tests/test_residual_audit_contracts.py`。

**最小实现：** 把歧义词改成明确动作和边界；只删除测试能证明与既有 reference 重复的条款，不创建新总控层、新 schema 或新 reference。

**定向验证：**

```bash
uv run pytest -q tests/test_ui_ux_pro_max_skill.py tests/test_stratix_admin_web_skill.py tests/test_residual_audit_contracts.py
uv run ruff check tests/test_ui_ux_pro_max_skill.py tests/test_stratix_admin_web_skill.py tests/test_residual_audit_contracts.py
```

## T13：五专家复评和最终质量门

全量验证若发现旧测试与已批准的新单一 owner 合同冲突，创建精确回归修复 TaskCard；只更新冲突断言，禁止借机修改 Skill 实现或扩大范围，修复后必须先定向再全量重跑。

**复评方式：** 中文语言、Skill 设计、软件工程、项目管理、沟通五类 reviewer 均独立只读审核 38 个 Skill；每位输出 38 个分数、评分理由、原 Finding 关闭结论和新 Finding。

**评分结构：**

- 原始评分保留为 baseline。
- 新表逐 Skill 显示五个整改前分数、五个整改后分数、综合变化、原始/已关闭/剩余 C-I-M 和证据。
- 系统表显示覆盖率 `190/190`、原始 `85.6`、整改后分数和差值。
- 分数不能覆盖 Gate：存在任一 Critical 或 Important 时，最终结论必须是 `changes_requested`。

**集中验证：**

```bash
uv run pytest -q
uv run ruff check skills tests
git diff --check
```

并运行 38 个 Skill validator、45 项追踪检查和代表性黑盒响应检查。集中 evidence、实现摘要和 review input 齐全后进入五专家复评；未关闭 Important 时自动在原范围整改并由相关专家复审。

## 风险和边界

- 风险为 `medium`：修改公共协作合同但不涉及生产、数据、安全、外部写入或发布。
- T10–T12 为 `source_or_test_write`，必须由授权 Terra worker 实现并回写 `code_shape_check: passed|failed`。
- T13 reviewer 固定 Terra/high/read-only，不得参与实现或写文件。
- 原始审计报告和原始分数不覆盖；只追加整改后事实和链接。
- 提交只在 review、verification、memory sync 全部完成后由 `gitcommitzh` 执行；不 push。

## 计划自审

- 45 个原始 Finding 先逐项登记，再决定修复，不再用合并主题替代原始问题。
- T10–T12 各有精确写集、测试入口和最小实现形状。
- T13 明确五专家覆盖、评分结构、质量 Gate 和全量验证。
- WBS、TaskCard、ledger 身份使用同一组 T09–T13 / WBS-AUDIT-09–13。
- 没有把计划、评分或 reviewer 派发写成已经完成。
