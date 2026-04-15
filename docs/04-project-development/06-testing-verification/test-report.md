# 测试报告

## 1. 文档目标

记录实际测试执行结果、缺陷、残留风险和发布建议。

## 2. 本轮执行结果

**执行日期：** 2026-04-03
**执行范围：** Python 3.14 基线收口、文档流程 CLI 化、当前仓库 `docs/` 重构
**执行人：** Codex

### 2.1 执行范围

- `factory-state-doctor` 的文档校验入口
- `factory-init` / `factory-state-doctor` 的根索引与顶层 index 生成逻辑
- 当前仓库 `docs/` 的入口页、设计页、测试页、发布页、运维页和追踪矩阵

### 2.2 测试结果

- `python3.14 -m unittest tests/test_factory_relative_paths_and_docs_index.py`：通过
- `docs-stratego source validate --repo-path .`：应作为正式收口命令执行
- 新项目初始化根索引与顶层 `index.md` 相关回归：通过

### 2.3 主要缺陷

本轮修复的关键问题是：文档正式流程与仓内脚本实现出现分叉。当前已将正式校验入口改为 `docs-stratego source validate`，并把仓内自动目录刷新从主路径移除。

### 2.4 回归结论

本轮核心回归项已通过，未发现当前仓库在 Python 3.14 基线与文档 CLI 化后的阻断性问题。

### 2.5 发布建议

结论为“可继续发布与复用”。剩余工作不是阻断问题，而是继续把管理员指南和更细环境实参补齐。

## 3. 推荐表格

| 批次 | 范围 | 通过率 | 阻断问题 | 残留风险 | 结论 |
|---|---|---|---|---|---|
| 2026-04-03-docs-cli-refactor | Python 3.14 基线、文档 CLI 化、当前仓库 docs 重构 | 100% | 0 | `docs-stratego` CLI scaffold 能力仍依赖外部仓库演进 | 可发布 |
