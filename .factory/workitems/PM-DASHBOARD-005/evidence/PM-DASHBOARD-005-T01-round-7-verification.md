# PM-DASHBOARD-005-T01 第七轮验证证据

- Work item：`PM-DASHBOARD-005`
- Task：`PM-DASHBOARD-005-T01`
- Actor：`AI_EXECUTOR`
- 日期：`2026-07-30`
- 状态：`in_progress`

## 改动前全仓前像

命令：

```bash
uv run pytest -q
```

真实结果：

```text
exit code: 1
217 passed / 7 failed
```

`pre_change_failed_nodeids`：

```text
tests/test_doc_factory_restructure.py::test_task_execution_contract_defines_six_task_types_and_gates
tests/test_doc_factory_restructure.py::test_current_workitem_has_standard_artifacts
tests/test_full_project_session_workflow_routing.py::test_flow_task_015_is_registered_as_closed_after_local_commit
tests/test_sf_sp_010_documentation_navigation.py::test_doc_factory_restructure_summary_tracks_destructive_migration
tests/test_skill_flow_process_audit.py::test_other_prompt_review_target_skills_have_work_item_status_packages
tests/test_superpowers_reference_migration.py::test_workflow_template_migration_progress_is_tracked
tests/test_work_skill_status_envelope_ownership.py::test_professional_prefixes_are_unchanged_for_exactly_31_work_skills
```

七项失败均位于本任务禁止修改范围；集合与上一轮 `217 passed / 7 failed` 数量基线一致。
本轮完成后必须重新运行并逐项比较 node ID，不能只比较数量。

## Red

命令：

```bash
uv run pytest tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest::test_plan_stages_use_explicit_parent_ids_at_arbitrary_depth tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest::test_invalid_route_tree_fails_closed -q
```

真实结果：

```text
exit code: 1
6 failed
```

失败身份：

- 显式四列表未被读取，旧解析器只错误识别到表格后的 `INSIDE-001` Markdown 标题。
- `duplicate`、`orphan`、`self`、`cycle` 四个非法父链子用例均未抛出 `SnapshotError`。
- 含孤儿父节点的 CLI 仍返回 `0 / success`，未 fail-closed。

结论：Red 精确命中 H3–H6 推断、缺少图校验和非法路线仍成功生成三个已确认根因。

## Green

### 路线树

```text
uv run pytest tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest::test_plan_stages_use_explicit_parent_ids_at_arbitrary_depth tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest::test_invalid_route_tree_fails_closed -q
exit code: 0
2 passed, 4 subtests passed
```

四列表解析、7 层父链、重复 ID、孤儿、自引用、循环和 CLI fail-closed 均通过。

### 紧凑看板与聚焦回归

```text
uv run pytest tests/test_using_shanforge_snapshot.py -q
exit code: 0
10 passed, 4 subtests passed

uv run ruff check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
exit code: 0
All checks passed!

uv run ruff format --check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py
exit code: 0
2 files already formatted
```

看板专用测试先于源修改写入，但第一次单独执行发生在共享渲染入口完成后，结果为
`1 passed`；因此本证据不虚构看板 pytest Red。旧实现的范围、30 个状态单元和 5 个
重复任务事实仍由 round-7 root-cause evidence 提供修改前失败证据。

## 回归

- 定向测试：`10 passed, 4 subtests passed`。
- 静态检查：Ruff check / format check 通过，限定范围 `git diff --check` 通过。
- 真实主线：四列表 `32` 个节点、`5` 个根节点，生成 `32/32` 个节点页。
- 真实看板：六状态汇总 `6`，业务组 `2`，非空状态段 `3`，主板任务
  `3 total / 3 unique`，空状态单元 `0`，死分组标题 `0`。
- 范围隔离：`SKILL-CLOSEOUT-001`、`STRATIX-SERVICE-GUIDE-001` 和
  `WRITING-PLANS-SIMPLE-GATE-001` 在主板命中 `0`，在“后续工作”保留入口。
- 站内导航：检查生成站点全部 `.html` 链接 `31,607` 个，缺失 `0`。
- 双生成：

```text
generation_id: a984983a4e5ca91a593383dee20cf57a1ab54fe028a21cc592a3ce17aa1b8e40
first cache_hit: false
second cache_hit: true
status: success
source_count: 273
```

### 全仓后像

```text
uv run pytest -q
exit code: 1
219 passed / 7 failed / 4 subtests passed
```

`post_change_failed_nodeids`：

```text
tests/test_doc_factory_restructure.py::test_task_execution_contract_defines_six_task_types_and_gates
tests/test_doc_factory_restructure.py::test_current_workitem_has_standard_artifacts
tests/test_full_project_session_workflow_routing.py::test_flow_task_015_is_registered_as_closed_after_local_commit
tests/test_sf_sp_010_documentation_navigation.py::test_doc_factory_restructure_summary_tracks_destructive_migration
tests/test_skill_flow_process_audit.py::test_other_prompt_review_target_skills_have_work_item_status_packages
tests/test_superpowers_reference_migration.py::test_workflow_template_migration_progress_is_tracked
tests/test_work_skill_status_envelope_ownership.py::test_professional_prefixes_are_unchanged_for_exactly_31_work_skills
```

`post_change_failed_nodeids == pre_change_failed_nodeids`。通过数增加 2 来自本轮新增两个测试
方法；七个失败身份未增加、未消失，均位于禁止修改范围。

### TEST-UI-ROUND7

- 被测 URL：
  - `file:///Users/uroborus/AiProject/shanforge/.factory/cache/site/current/work.html`
  - `file:///Users/uroborus/AiProject/shanforge/.factory/cache/site/current/roadmap.html`
- 启动命令 / 端口 / 关闭方式：`N/A`；交付物是本地静态 HTML，没有服务进程。
- 健康检查：文件存在、快照 receipt 成功、浏览器加载成功。
- 临时脚本：`/private/tmp/pm_round7_browser_check.cjs`
- `TEST-UI-ROUND7-DESKTOP-WORK`：
  `REQ-PM-SNAPSHOT-005 / PM-DASHBOARD-005-T01`；1440×900，无横向溢出，6 个状态汇总
  均可聚焦，0 空格、3 张唯一任务、2 个可点击业务组。
- `TEST-UI-ROUND7-MOBILE-WORK`：
  `REQ-PM-SNAPSHOT-005 / PM-DASHBOARD-005-T01`；390×844，无横向溢出，两个 EAD
  非空状态段纵向排列，最窄任务行 308px。
- `TEST-UI-ROUND7-MOBILE-ROUTE`：
  `REQ-PM-SNAPSHOT-003 / PM-DASHBOARD-005-T01`；根节点显示 8 个直接子节点，
  子节点与任务入口独立可点，叶节点页可达，无横向溢出。
- 控制台错误：`0`。
- 截图：
  - `/tmp/PM-DASHBOARD-005-round-7-desktop-work.png`
  - `/tmp/PM-DASHBOARD-005-round-7-mobile-work.png`
  - `/tmp/PM-DASHBOARD-005-round-7-mobile-route.png`

## 结论

`approved_pending_human_ui_acceptance`

代码、事实迁移、测试、真实生成和双视口自动浏览器验收已完成。独立任务评审为
`approved / 99 / C0-I0-M0`；用户最终 UI 验收仍是后续 Gate。未提交、未关闭。
