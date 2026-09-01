# T08 集中质量门验证证据

- work_item_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001`
- task_card_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T08`
- wbs_id: `WBS-REM-08`
- baseline_head: `d6f8745fdcbcb6fbcdd5fe0de9ca429be15ea077`
- branch: `v2`
- completion_level: `stage`

## T01-T07 定向验证

| 任务 | pytest | 其他检查 |
|---|---|---|
| T01 WBS/身份 | 31 passed，4 subtests passed | Ruff passed；diff check passed；code shape passed |
| T02 状态分层 | 19 passed，4 subtests passed | Ruff passed；diff check passed；code shape passed |
| T03 worker/evidence | 31 passed | Ruff passed；diff check passed；code shape passed |
| T04 人类响应 | 30 passed | Ruff passed；diff check passed；code shape passed |
| T05 Go/Python 范围 | 7 passed | Ruff passed；diff check passed；code shape passed |
| T06 工具探测 | 7 passed | Ruff passed；diff check passed；缺失脚本检查 passed；code shape passed |
| T07 版本兼容门 | 30 passed | Ruff passed；diff check passed；code shape passed |

## 集中验证

1. `uv run pytest -q`
   - 首轮：316 passed、2 failed、4 subtests passed，exit 1。
   - 根因：`writing-plans/SKILL.md` 错误拥有项目级 `next_required_action`；references 模板字段本身正确。
   - 修复：只修改 `skills/writing-plans/SKILL.md` 的“v1.2.0 运行时路由合同”和“任务身份”。
   - 评审前：319 passed、4 subtests passed，exit 0。
   - 关闭评审整改后：322 passed、4 subtests passed，exit 0。
2. `uv run ruff check skills tests`
   - `All checks passed!`，exit 0。
3. 38 个 Skill validator
   - 使用项目现有 uv 环境运行 Skill Creator `quick_validate.py`。
   - 精确脚本：`/Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py`。
   - 精确命令：

     ```bash
     uv run python -c 'import runpy,sys; from pathlib import Path; validate=runpy.run_path("/Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py")["validate_skill"]; paths=sorted(Path("skills").glob("*/SKILL.md")); results=[(p.parent.name,*validate(p.parent)) for p in paths]; [print(f"{name}: {message}") for name,ok,message in results]; passed=sum(ok for _,ok,_ in results); print(f"summary: {passed}/{len(results)} passed"); sys.exit(0 if passed == len(results) == 38 else 1)'
     ```

   - `38/38 passed`，exit 0；未安装新依赖。
   - 评审整改后使用相同命令重跑：首次受沙箱限制无法读取现有 uv cache，未进入校验；获准读取后 `38/38 passed`，exit 0。该次基础设施失败未计作 Skill 失败。
   - 通过项：agent-harness-construction、ai-first-engineering、ai-regression-testing、algorithmic-art、api-design、art-asset-pipeline、article-writing、brainstorming、browser-control、crawler4j-model-project、doc-coauthoring、document-templates、docx、executing-plans、frontend-patterns、gitcommitzh、go-developer、humanizer、java-developer、pdf、project-memory、python-uv-project、receiving-code-review、release-deployment、requesting-code-review、requirements-engineering、shadcn、stratix-admin-web、stratix-service、subagent-driven-development、systematic-debugging、tdd-workflow、ui-ux-pro-max、using-shanforge、verification-before-completion、webapp-testing、writing-plans、xlsx。
4. `git diff --check`
   - 无输出，exit 0。

## 独立评审整改验证

- I-01：`skills/subagent-driven-development/SKILL.md` 与 `tests/test_execution_workflow_skills.py`，关闭 review approved 被误当作 TaskCard 可跳过状态的问题。
- I-02：`skills/stratix-service/references/cli-workflow.md`、`tests/test_stratix_service_skill.py`、`tests/test_stratix_service_framework_guide.py`，关闭 latest/dist-tags 绕过本地版本矩阵的问题。
- I-03：`evidence/T08-black-box-v6.md` 与本文件，补齐可复核的完整输入、输出、断言和 validator 命令。
- 定向复验：41 passed；Ruff passed；diff check passed；worker `code_shape_check: passed`。
- 整改后集中复验：322 passed、4 subtests passed；Ruff passed；38/38 Skill validators passed；diff check passed。

## 黑盒行为验证

场景链路：已批准 WBS → TaskCard partial → 完整测试基线 failed/error → Bug 根因 → 精确修复位置 → review approved → TaskCard completed → 下一 WBS active。

前五次发现并关闭三个真实缺口：

- 测试统计被压缩，遗漏零值状态。
- 完整测试基线与修复后的定向重跑混在一起。
- 一个失败用例的 owner 被错误继承给另一个错误用例。

最终 v6 使用全新独立代理显式加载 `$using-shanforge`；完整输入、实际输出、代理回执和逐项断言见 `T08-black-box-v6.md`。结果包含：

- `2/4` WBS 进度、当前 WBS-03、WBS-04 未开始。
- 固定八标签基线：`total 8；passed 5；failed 1；error 1；blocked 0；skipped 1；not_run 0；cancelled 0`。
- `TEST-AUTH-006` 与 `TEST-AUTH-007` 的功能、现象、归因和各自 owner；缺失 owner 写“未分配/待确认”。
- `web/src/features/auth/LoginForm.tsx`、`LoginForm`、改动、原因和定向回归结果。
- review approved 与 TaskCard completed 分层。
- 唯一下一动作；明确无需用户回复。

结论：黑盒通过。

## 未运行项

- 未执行发布、远端写入或外部系统操作：本工作项仅修改 Skill、测试和本地项目事实，不包含发布范围。

## Memory closeout 验证

- 首轮提交前全量：321 passed、1 failed、4 subtests passed。
- 失败：`ProjectSnapshotTest.test_shanforge_session_card_matches_current_mainline_ledger` 无法读取会话卡的 `下一动作` 字段。
- 根因：`.factory/memory/agent-session.md` 在关闭同步时把机器可读字段名写成了 `唯一下一动作`，并把当前 work item/task 写成 `none`，不符合主线 ledger 对账合同。
- 修复位置：`.factory/memory/agent-session.md` 的会话卡头部；恢复 `下一动作` 字段，并写入最新已关闭的 work item、T08、WBS-REM-08 和 `closed` Gate。`.factory/memory/session-ledger.jsonl` 同步相同身份。
- 最终：322 passed、4 subtests passed；Ruff、JSONL、diff check passed。
