# T01 验证证据

## Red

```text
uv run pytest -q tests/test_requirements_analysis_mode_contract.py
1 failed
```

预期失败：需求工程尚未声明 `analysis_mode`，文档清单和 Gate 仍把独立文件视为无条件必备。

## Green

```text
uv run pytest -q tests/test_requirements_analysis_mode_contract.py \
  tests/test_requirements_engineering_skill.py \
  tests/test_sf_sp_010_documentation_navigation.py::test_document_templates_register_formal_docs_and_keep_temporary_docs_out
6 passed
```

## 相邻测试说明

原计划中的整个 `test_sf_sp_010_documentation_navigation.py` 另有一项既存失败：
共享脏文件 `.factory/memory/current-state.md` 不再包含旧工作项
`DOC-FACTORY-RESTRUCTURE-001`。该失败与本任务允许路径及需求分析合同无关，本任务未修改共享 memory。
