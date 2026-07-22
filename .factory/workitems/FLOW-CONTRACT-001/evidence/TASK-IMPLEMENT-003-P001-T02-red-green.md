# T02 Source Registry、提取器与增量索引 Red/Green 证据

- Work item：`FLOW-CONTRACT-001`
- Task：`TASK-IMPLEMENT-003-P001-T02`
- Actor：`AI_EXECUTOR`
- 日期：2026-07-22
- 状态：`green`

## Red

```bash
UV_CACHE_DIR=/tmp/shanforge-pki-uv-cache PYTHONPATH=src uv run pytest \
  tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py -q
```

真实结果：2 个 collection error，exit 2；缺少 runtime extractors 与 application index service，符合新功能预期失败。

## Green

同一测试命令结果：`6 passed in 0.10s`。同时运行目标文件 Ruff 和 mypy：`All checks passed!`、`Success: no issues found in 5 source files`，总 exit 0。失败 0，错误 0，跳过 0，未运行 0。

## 硬门覆盖

- Markdown `document_id + section_id` JCS Hash locator。
- Python AST qualified symbol、JSON Pointer、JSONL event UID。
- 同 registry 组两个 concrete source。
- warm refresh 解析数 0，无变化不生成新 generation。
- 删除一个同实体来源后仍保留其他定义，current generation 无幽灵贡献。
- 同权威冲突 generation 回滚，并发 reader 继续看到上一 current。
- 路径越界失败关闭，冷重建 source root 确定性一致。

## 结论

T02 进入 `ready_for_review`；本结论不包含 CLI、HTML、PM 和异步同步。
