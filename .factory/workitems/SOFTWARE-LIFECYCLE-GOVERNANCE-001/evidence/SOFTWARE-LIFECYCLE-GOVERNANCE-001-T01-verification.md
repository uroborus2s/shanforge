# T01 生命周期治理验证

- 候选边界：当前工作树；仅 T01 允许文件。
- Red：`uv run pytest tests/test_lifecycle_governance.py -q`，5 failed / 1 passed；锁定版本、旧平台路径、退役附件、REQ-SF-008 与生命周期矩阵漂移。
- I3/I4 Red：矩阵表结构通过；I4 在 Sol 清理前为 2 failed / 7 passed，准确锁定无日期旧 current block；I2 同轮锁定测试计划版本漂移。
- 修正后：`uv run pytest tests/test_lifecycle_governance.py tests/test_project_test_governance.py -q`，26 passed。
- I3 iteration 2 Red：语义反转反例为 1 failed / 10 passed；加入列级禁止语义后，上述 focused suite 为 27 passed。反例覆盖 Spike、简单任务跳过 WorkItem/TDD/定向验证、旧输出替代和发布无需人工授权。
- 目录校验：`validate_test_documents.py --repo-root . --catalog docs/06-delivery/test-cases.md`，5 cases valid。
- 静态检查：`uv run ruff check tests/test_lifecycle_governance.py tests/test_project_test_governance.py tests/test_full_project_session_workflow_routing.py` 通过；`git diff --check` 通过。
