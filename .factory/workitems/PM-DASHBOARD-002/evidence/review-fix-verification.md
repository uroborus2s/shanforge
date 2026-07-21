# PM-DASHBOARD-002-T01 Review Fix Verification

## 定向合同、安全与浏览器

```text
PM_DASHBOARD_SCREENSHOT_DIR=.factory/workitems/PM-DASHBOARD-002/evidence/screenshots \
uv run pytest tests/test_pm_dashboard_template_contract.py \
tests/test_pm_dashboard_template_browser.py -q

.......................                                                  [100%]
23 passed in 3.31s
exit code: 0
```

覆盖：Excel 样例仅设计时读取且运行时不回读、精确 slot、AI/策略边界、FULL/PARTIAL/ERROR_ONLY、冲突/过期/失败关闭、scalar 转义、fragment allowlist、权限字段省略、总览与十模块、筛选/稳定排序/来源展开、五视口几何/焦点/对比度/截图。

## Python 静态质量

```text
uv run ruff check tests/test_pm_dashboard_template_contract.py \
tests/test_pm_dashboard_template_browser.py

All checks passed!
exit code: 0
```

## 相邻回归

```text
uv run pytest tests/test_project_management_control_plane.py \
tests/test_project_memory_skill.py -q

11 passed in 0.02s
exit code: 0
```

```text
uv run pytest tests/test_full_project_session_workflow_routing.py \
tests/test_project_control_response.py -q

42 passed in 0.14s
exit code: 0
```

## 浏览器与截图

- executable：`/Users/uroborus/Library/Caches/ms-playwright/chromium-1228/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`
- version：`149.0.7827.55`
- 视口：1440×900、1024×768、768×1024、390×844、320×568；探针断言 CSS viewport 与目标完全相等。
- 五张 PNG 颜色数：1537–2209。
- RGB 通道最大极差：全部 255。
- 人工查看：1440、768、320 均无页面级横向溢出、首屏关键区重叠或空白截图；窄屏模块导航在自身容器内横向滚动。
