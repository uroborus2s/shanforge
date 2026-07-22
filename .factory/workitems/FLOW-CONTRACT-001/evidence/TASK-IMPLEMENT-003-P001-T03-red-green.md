# T03 稳定定位、关系图与查询 CLI Red/Green 证据

- Work item：`FLOW-CONTRACT-001`
- Task：`TASK-IMPLEMENT-003-P001-T03`
- Actor：`AI_EXECUTOR`
- 日期：2026-07-22
- 状态：`green`

## Red

`tests/test_project_knowledge_query.py tests/test_project_cli.py` 首次运行产生 2 个 collection error，exit 2；缺少 query service 和 access CLI，失败原因符合预期。

## Green

- T03 定向：`5 passed in 0.09s`。
- T01–T03 组合：`13 passed in 0.18s`。
- Ruff：`All checks passed!`。
- mypy：`Success: no issues found in 15 source files`。
- exit 0；失败 0，错误 0，跳过 0，未运行 0。

## 实仓 CLI 证据

```text
project index rebuild --json
source_count=442 parsed_count=442 source_root=f5bb3c...2745db9
real=1.59s exit=0

project index check --json
integrity=ok source_count=442
real=0.23s exit=0

project index refresh --json (no change)
parsed_count=0 reused_count=442 changed=false
real=0.28s exit=0
```

注：过程中实仓冷构建首次暴露重复标题 provisional ID 冲突和 extractor 版本快速复用缺陷；两者均有复现测试并修正。缩小 JSON registry 为精确 R009/R014/稳定配置后，冷构建达到 1.59s。

## 结论

T03 进入 `ready_for_review`；CLI 已能在会话中直接运行，后续 T04 扩展 snapshot/HTML。
