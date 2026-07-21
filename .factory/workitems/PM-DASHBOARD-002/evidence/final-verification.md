# PM-DASHBOARD-002-T01 Completion Evidence

## 基本信息

- Work item：`PM-DASHBOARD-002`
- Task：`PM-DASHBOARD-002-T01`
- Actor：AI_EXECUTOR
- 时间：2026-07-21T12:48:00+08:00
- 验证声明：Excel 样例信息架构已一次性固化进 HTML；查询/渲染合同、十模块模板、负向安全合同和五视口行为达到任务验收口径。
- 结论：passed

## 新鲜验证命令与真实结果

```text
PM_DASHBOARD_SCREENSHOT_DIR=.factory/workitems/PM-DASHBOARD-002/evidence/screenshots \
uv run pytest tests/test_pm_dashboard_template_contract.py \
tests/test_pm_dashboard_template_browser.py -q

.......................                                                  [100%]
23 passed in 3.10s
exit code: 0
```

```text
uv run pytest tests/test_project_management_control_plane.py \
tests/test_project_memory_skill.py -q

11 passed in 0.02s
exit code: 0
```

```text
uv run pytest tests/test_full_project_session_workflow_routing.py \
tests/test_project_control_response.py -q

42 passed in 0.12s
exit code: 0
```

```text
uv run ruff check tests/test_pm_dashboard_template_contract.py \
tests/test_pm_dashboard_template_browser.py

All checks passed!
exit code: 0
```

- 失败：0
- 错误：0
- 跳过：0

## 截图像素检查

工作区依赖 Python + Pillow 对五张图进行新鲜检查，exit code 0：

| 文件 | 尺寸 | 颜色数 | 最大通道极差 |
|---|---:|---:|---:|
| `dashboard-1440x900.png` | 1440×900 | 2209 | 255 |
| `dashboard-1024x768.png` | 1024×768 | 1938 | 255 |
| `dashboard-768x1024.png` | 768×1024 | 2190 | 255 |
| `dashboard-390x844.png` | 390×844 | 1873 | 255 |
| `dashboard-320x568.png` | 320×568 | 1537 | 255 |

独立 reviewer 和主执行者均查看 1440、768、320 代表截图；无页面级横向溢出、首屏重叠或空白图。

## 需求核对

- Excel：只作为一次性设计参考；skill/reference/测试明确运行时不得回读。
- 事实源：`.factory/pm` 只是一类 PM 管理事实，另有正式文档、work item、evidence 和 deployment 来源。
- 快速路径：AI 意图候选 → 确定性计划 → 固定 H → 注册查询 → 权限过滤 → 固定渲染 → 核对 → AI 检查 → 会话装配。
- 模板：总览 + 固定十模块；精确 slot、FULL/PARTIAL/ERROR_ONLY、转义/权限/失败关闭合同齐备。
- 浏览器：五个精确 CSS 视口；十模块布局、焦点、对比度、筛选、排序、来源展开通过。
- review：独立复审 `approved / 99 / C0-I0-M0`。
- memory：只追加旁路历史索引与 review 事件，不覆盖主工作项当前焦点。

## Red-Green

- Red：初始同一测试命令 14 failed，exit 1；失败原因符合旧模板缺固定 H、slot、十模块、处置和交互合同。
- Green：最终 23 passed，exit 0。

## 偏离与残余范围

- 未运行全仓测试：批准计划明确排除；仓库存在大量其他工作项并行脏改，本任务运行定向和相邻回归。
- 未实现生产快照、生产 HTML/XLSX renderer、完整投影、注册会话工具和跨格式核对器：这些是明确非目标，也是项目后续剩余范围。
- 本结论只覆盖 `PM-DASHBOARD-002-T01` 任务，不代表整个 Shanforge 项目完成。
