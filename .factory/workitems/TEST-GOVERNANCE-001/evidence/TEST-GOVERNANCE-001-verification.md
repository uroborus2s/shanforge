# TEST-GOVERNANCE-001 验证证据

## 基本信息

- Work item：`TEST-GOVERNANCE-001`
- 候选：`9f21380` 加本工作项未提交差异
- 时间：2026-08-23 21:19 +08:00
- 当前结论：`partial`，独立评审、精确提交和提交后干净克隆待执行

## Red / Green

### Red

```bash
UV_CACHE_DIR=/tmp/shanforge-test-governance-red-cache uv run pytest -q tests/test_project_test_governance.py
```

- exit code：1
- 结果：`4 failed, 9 passed`
- 预期与实际一致：发现 7 个不存在的旧测试文件、失效平台案例目录、缺失案例模板和未区分的状态合同。

### Green

```bash
UV_CACHE_DIR=/tmp/shanforge-test-governance-green-cache uv run pytest -q tests/test_project_test_governance.py tests/test_full_project_session_workflow_routing.py::test_delivery_stage_gate_bug_loop_and_release_receipt_are_closed
```

- exit code：0
- 结果：`14 passed`
- 后续删除一条过度约束具体文件名的断言后，当前治理、交付相邻流程和会话事实定向集新鲜结果为 `14 passed`。

## 完整与静态检查

```bash
UV_CACHE_DIR=/tmp/shanforge-test-governance-final-cache uv run pytest -q
```

- exit code：0
- 结果：`237 passed, 4 subtests passed`
- 说明：运行时工作区包含另一个并行任务新增的 1 个测试；本任务提交后的干净克隆将重新取得精确计数。

```bash
UV_CACHE_DIR=/tmp/shanforge-test-governance-final-cache uv run ruff check tests/test_project_test_governance.py tests/test_using_shanforge_snapshot.py tests/test_work_skill_status_envelope_ownership.py
```

- exit code：0
- 结果：`All checks passed!`

```bash
UV_CACHE_DIR=/tmp/shanforge-test-governance-final-cache uv run python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/document-templates
UV_CACHE_DIR=/tmp/shanforge-test-governance-final-cache uv run python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/verification-before-completion
```

- exit code：0
- 结果：两个 Skill 均为 `Skill is valid!`

- `.factory` JSON/JSONL：有效。
- 本任务路径 `git diff --check`：通过。
- `document-templates` 专业前缀 SHA-256：`0a1b1a36466106da20b42079864b8dd780200e29310191b8aab1ee87222317b3`，与冻结夹具一致。

## 偏离与隔离

- 当前混合工作区另有 `SKILL-COMPLETENESS-P0-001`、`scripts/sync-codex-skills`、`skills/brainstorming`、`skills/requirements-engineering` 和两个新测试的并行改动。
- 当前全量 Ruff 会被这些未归属本任务的新测试阻断；本任务没有修改或纳入它们。
- 最终结论以本任务精确提交后的干净克隆执行完整 pytest、Ruff、JSON/JSONL 和 Git 卫生门为准。

## 独立评审整改后隔离候选

候选从 Git 暂存区导出到 `/tmp/shanforge-test-governance-index.OOQCpU`，只包含本工作项文件与 hunk；并行任务的布局、Skill、脚本、正式设计和新测试均未进入候选。导出目录初始化本地 Git 后执行：

- `uv run pytest -q`：exit 0，`236 passed, 4 subtests passed`。
- `uv run ruff check .`：exit 0，`All checks passed!`。
- 两个 Skill `quick_validate.py`：exit 0，均为 `Skill is valid!`。
- `.factory` JSON/JSONL：有效。
- `git status --short` 与 `git diff --check`：无输出，exit 0。

此前未初始化 Git 的首次隔离 pytest 为 `235 passed / 1 failed / 4 subtests`；唯一失败来自测试调用 `git ls-files` 时不存在 `.git`。初始化临时 Git 后同一完整测试集全绿，环境根因已证实。

## 提交后干净克隆最终验证

- 实现提交：`c4534ba`。
- 干净克隆：`/tmp/shanforge-test-governance-clean.VQRkaO/shanforge`。
- `uv run pytest -q`：exit 0，`236 passed, 4 subtests passed`。
- `uv run ruff check .`：exit 0，`All checks passed!`。
- `quick_validate.py skills/document-templates`：exit 0，`Skill is valid!`。
- `quick_validate.py skills/verification-before-completion`：exit 0，`Skill is valid!`。
- `.factory` 数据：`valid json=25 jsonl=36`。
- `git diff --check`、`git status --short`：无输出，exit 0。
- `git rev-parse --short HEAD`：`c4534ba`。

最终结论：`passed`，失败 0、错误 0、跳过 0、未运行 0。
