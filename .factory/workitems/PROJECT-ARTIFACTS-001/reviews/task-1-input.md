# T01 独立评审输入

## 输入

- Work item：`PROJECT-ARTIFACTS-001`
- Task：`T01 Penpot 设计资产合同`
- task brief：`task-briefs/T01-penpot-design-assets.md`
- implementer report：`reports/task-1.md`
- verification evidence：`evidence/task-1.md`
- ledger：`ledger.jsonl`
- 计划：`plan.md` 的 R5 approved 版本

## Diff 范围

- `src/domain/project_artifacts/`
- `src/application/project_artifacts/`
- `src/settings/project_artifacts/`
- `src/access/project_cli.py`
- `src/application/project_knowledge/query_service.py`
- `src/settings/composition/project_knowledge.py`
- `design/ux-ui/`
- `contracts/schemas/design-artifact-manifest.schema.json`
- `docs/05-design/ux-ui-design.md`
- `tests/test_project_artifact_contracts.py`
- `pyproject.toml` / `uv.lock` 中 PyYAML 运行时依赖 hunk

`types-pyyaml` 是本任务开始前已有脏改动，不属于 T01；评审不得把它视为本任务交付。
全局 memory 在 T01-T04 全部完成后一次同步，本任务已写 work item ledger、evidence 和 report。

## 评审重点

1. Spec：是否不伪造 `.penpot`，waiting 状态是否准确。
2. Architecture：application port owner、domain 无 I/O、settings 严格读取。
3. Security：仓内路径、symlink、文件大小、safe YAML。
4. Contract：Schema 与 validator 的 required/enum 是否一致。
5. CLI：三条 root 命令扩展是否破坏既有 project 命令。

## 输出要求

按 task review template 给出 Spec Review、Quality Review、0-100 评分、findings 和
`approved | changes_requested`。评审只读，不修改任何文件。
