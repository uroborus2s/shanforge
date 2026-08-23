# TEST-GOVERNANCE-CLOSURE-001 Review Feedback Triage

## I1：文档命令不可执行

- 来源：独立 reviewer `/root/t01_review`。
- severity：Important。
- 要求：将 `python ...validate_test_documents.py` 统一为项目支持的可复制入口，并增加回归。
- 技术核实：成立。`command -v python` 无输出；当前文档中的命令会 exit `127`。项目正式 Python 工具链是 `uv run python`。
- 决定：Fixed。统一正式文档和三份模板，并用测试拒绝裸 `python` 入口。

## I2：校验器未完整 fail-closed

- 来源：独立 reviewer `/root/t01_review`。
- severity：Important。
- 要求：索引/详情字段一致、七态计数非负，并覆盖完整案例结构。
- 技术核实：成立。索引名称单独漂移仍返回 valid；`通过=5, 失败=-1, 总数=4` 仍返回 valid。
- 决定：Fixed。统一在 `validate_test_documents.py` 的目录/报告边界校验，并增加名称漂移、负数和缺少清理/标签等负例。

## 边界

- 两项均在原目标和 allowlist 内，不涉及产品取舍、依赖或新系统。
- 修复后由同一 reviewer 复审；正式发布门保持未切换。
