# TEST-GOVERNANCE-001 独立复审

## 最终结论

- decision: `approved`
- review_score: `98/100`
- Critical: `0`
- Important: `0`
- Minor: `0`
- human_confirmation_required: `false`
- gate_reason: `none`
- 下一 Gate：将精确暂存候选连同本复审结论做本地提交，然后基于该提交执行干净克隆完整验证；本次 `approved` 不替代提交后干净克隆 Gate，也不制造人工确认 Gate。

## 独立性元数据

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/t01_review`
- reviewer_independence_evidence: reviewer 未参与 `TEST-GOVERNANCE-001` 实现或整改；未读取或依赖实现者对话。本轮只读取整改文件化输入、主仓 Git index 的 `git diff --cached` / `git show :path` 和导出候选 `/tmp/shanforge-test-governance-index.OOQCpU`，未读取主仓 unstaged diff。除本 review 文件外未修改实现、测试、memory、ledger、Git 或外部系统。

## 首轮 Finding 关闭情况

### I1：冻结合同与 evidence 漂移 — Closed

- 主仓暂存的 `skills/document-templates/SKILL.md` 与导出候选 `829890e` 对应 blob 一致。
- 暂存的 `tests/test_work_skill_status_envelope_ownership.py` 只修改 `document-templates` 的一行专业前缀哈希，值为 `0a1b1a36466106da20b42079864b8dd780200e29310191b8aab1ee87222317b3`。
- 导出候选完整 pytest 新鲜结果为 `236 passed, 4 subtests passed`，exit 0；冻结合同已实际通过。更新后的 evidence 如实保留复审和提交后干净克隆为未完成 Gate。

### I2：混入布局 / 迁移行为 — Closed

- `git diff --cached -- skills/document-templates/SKILL.md` 只包含：新增 `test-cases.md` 模板引用、展开测试材料路径，以及明确普通任务 evidence 与阶段/发布报告边界。
- 首轮指出的“已有登记保持布局”、迁移路由、owner 回源及输出行为改写均未进入暂存候选；它们仍属于明确排除的并行工作区。

### M1：测试计划模板换行 — Closed

- 暂存模板在关联 ID 后使用显式 `<br>`，避免尾随空格且保持字段换行。
- 主仓 `git diff --cached --check` 与导出候选差异卫生均通过。

## 当前 Findings

### Critical

无。

### Important

无。

### Minor

无。

## 需求、架构与范围复核

- 正式测试计划只登记当前 Skill-first 测试层级和真实入口，没有恢复旧 `src/` 平台、旧 OpenAPI 路由、平台服务或中心脚本。
- 陈旧入口守卫、案例七态、批次四态、案例模板、报告模板和环境追踪合同均在精确候选中；正式测试引用均可解析。
- 删除的 `project-artifacts.testcases.yaml` 仅包含四个指向已不存在旧平台测试文件的案例，可从 Git 历史恢复，没有删除仍可执行的当前测试事实。
- 暂存候选没有新增依赖、运行时、服务、数据库或测试框架。
- 并行 `SKILL-COMPLETENESS-P0-001`、同步脚本、其他 Skill 和新测试未进入本次精确候选；主仓 index 与导出候选中所有现存候选 blob 一致，旧案例 YAML 在两处均不存在。
- 测试报告保持批次结论 `partial`，明确复审和提交后干净克隆的阶段边界，没有把未执行 Gate 写成通过。

## 新鲜只读验证

| 命令 / 检查 | 结果 |
|---|---|
| `/tmp/shanforge-test-governance-index.OOQCpU` 的 `git rev-parse --short HEAD` | `829890e` |
| `PYTHONDONTWRITEBYTECODE=1 uv run pytest -q -p no:cacheprovider` | `236 passed, 4 subtests passed`，exit 0 |
| `uv run ruff check .` | `All checks passed!`，exit 0 |
| `quick_validate.py skills/document-templates` | `Skill is valid!`，exit 0 |
| `quick_validate.py skills/verification-before-completion` | `Skill is valid!`，exit 0 |
| 解析 `.factory/**/*.json` 与 `.factory/**/*.jsonl` | `valid json=25 jsonl=36`，exit 0 |
| 导出候选 `git status --short` | 无输出，exit 0 |
| 导出候选 `git diff --check HEAD^ HEAD` | 无输出，exit 0 |
| 主仓 `git diff --cached --check` | 无输出，exit 0 |

## 五项评分

| 维度 | 得分 | 说明 |
|---|---:|---|
| 需求与验收符合度 | 30/30 | 陈旧入口、模板、状态语义和双环境门均有明确 owner；提交后门诚实保留 |
| 架构与边界 | 20/20 | 保持 Skill-first，不恢复平台运行时，不新增中心能力 |
| 测试与验证 | 20/20 | Red/Green 可追溯；隔离候选完整 pytest、Ruff、Skill validator 和数据格式门全绿 |
| 实现质量与范围控制 | 19/20 | 精确暂存 hunk 成功隔离并行改动；结构简洁，无新增依赖 |
| 文档、证据与可恢复性 | 9/10 | 报告、evidence、整改响应和删除恢复边界完整；最终干净克隆证据按 Gate 待提交后生成 |
| **总分** | **98/100** | **approved** |
