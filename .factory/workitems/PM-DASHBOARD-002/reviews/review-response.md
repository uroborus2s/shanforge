# PM-DASHBOARD-002-T01 Review Response

## Fixed

### I-1 AI/策略边界

Fixed. reference 现在只允许 AI 形成意图候选；确定性策略系统负责选择和授权注册工具。

Verified:

- `uv run pytest tests/test_pm_dashboard_template_contract.py::test_rendering_contract_keeps_ai_out_of_fact_computation -q`：1 passed。

### I-2 安全、权限与失败关闭

Fixed. 测试 renderer 现在校验精确 slot、封闭枚举和 disposition 组合；scalar 统一转义；fragment 只接受 allowlist；ERROR_ONLY 从 HTML 源码移除旧业务值；权限投影不暴露被拒字段。

Verified:

- `uv run pytest tests/test_pm_dashboard_template_browser.py -q -k 'fixture or error_only or non_eligible'`：8 passed，5 deselected。
- 完整套件：22 passed。

### I-3 十模块浏览器验证

Fixed. 五个精确 CSS 视口现在逐模块检查标题/元数据/工具栏/表格/来源区/返回链接的边界、重叠、裁切、对比度和焦点。

Verified:

- `PM_DASHBOARD_SCREENSHOT_DIR=.factory/workitems/PM-DASHBOARD-002/evidence/screenshots uv run pytest tests/test_pm_dashboard_template_contract.py tests/test_pm_dashboard_template_browser.py -q`：22 passed in 3.31s。

### M-1 / M-2 浏览器与截图证据

Fixed. 实际浏览器路径和版本进入探针结果；五张截图通过 Pillow 像素检查，并已人工检查桌面、会话和移动三档。

Verified:

- Chrome for Testing：`149.0.7827.55`。
- 五张 PNG 尺寸匹配；颜色数 1537–2209；最大通道极差均为 255。

### U-1 Excel 一次性参考边界

Fixed. Excel 样例只在模板设计时读取一次；页面结构已经写入 HTML 和 slot 合同。标准项目状态查询不打开或解析原始 `.xls` / `.xlsx`，HTML 也不再向最终用户显示“对应 Excel”。

Verified:

- 新增 `test_excel_example_is_design_time_only_and_never_a_runtime_input`。
- 完整套件：23 passed in 3.31s。

## Remaining

- 无未处理 review finding。
- 生产 `ProjectProgressSnapshot/v2`、HTML/XLSX renderer 和跨格式核对器仍是计划明确的非目标，未宣称交付。
