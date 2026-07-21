# 任务简报

## 工作项

- 工作项：`PM-DASHBOARD-002`
- 任务：`PM-DASHBOARD-002-T01` Excel 十模块项目状态查看契约
- 状态：`approved_ready_for_commit`
- 上游计划：`.factory/workitems/PM-DASHBOARD-002/plan.md`
- 流水账：`.factory/workitems/PM-DASHBOARD-002/ledger.jsonl`

## 目标

把旧 PM 查看入口校准到正式 `WF-CTL-010`：会话请求经一次注册查询消费同一固定 H 获授权快照，固定代码计算并渲染事实，HTML 以总览加 Excel 十模块展示，AI 只做意图识别和有证据的专业检查。

## 输入

- 正式需求/设计：`docs/04-product/prd.md`、`docs/05-design/frontend-design.md`。
- 必读：`skills/using-shanforge/SKILL.md`、`skills/using-shanforge/references/pm-dashboard-rendering.md`、`skills/using-shanforge/references/status-dashboard-template.html`。
- 可选参考：原始 Excel 十一张 sheet 的只读结构检查结果。

## 允许修改

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/pm-dashboard-rendering.md`
- `skills/using-shanforge/references/status-dashboard-template.html`
- `tests/test_pm_dashboard_template_contract.py`
- `tests/test_pm_dashboard_template_browser.py`
- `.factory/workitems/PM-DASHBOARD-002/`

## 禁止修改

- 用户已有未归属本任务的脏改动。
- `src/`、正式 PRD/设计、PM 事实文件、现有 `.factory/memory/` 和 `FLOW-CONTRACT-001/ledger.jsonl`。
- 模板脚本中的事实读取、网络访问、业务派生或项目写入。
- 查询时重新读取或解析原始 Excel 样例；样例结构已经固化进 HTML 模板。

## 实施步骤

1. Preflight 三份目标文件并保存全工作区状态快照/摘要/路径集合，发现目标冲突则停止。
2. 按计划精确 slot 和 11 页顺序写静态红灯测试。
3. 写真实 Chrome 固定 fixture 红灯，覆盖五视口与三类只读交互。
4. 更新 skill 快速查询入口、渲染 reference 和 HTML 模板。
5. 运行静态与浏览器单测，生成五张截图。
6. 运行 PM/project-memory 与会话/project-status 两组相邻回归。
7. 比较全工作区前后状态，确认新增变化只在允许路径；再检查允许路径 diff 和 `git diff --check`。
8. 写 evidence、report、review input 和本工作项 ledger。
9. 进入独立任务 Spec/Quality review；实现者不得自批 `approved`。

## 验证命令

```bash
uv run pytest tests/test_pm_dashboard_template_contract.py -q
PM_DASHBOARD_SCREENSHOT_DIR=.factory/workitems/PM-DASHBOARD-002/evidence/screenshots uv run pytest tests/test_pm_dashboard_template_browser.py -q
uv run pytest tests/test_project_management_control_plane.py tests/test_project_memory_skill.py -q
uv run pytest tests/test_full_project_session_workflow_routing.py tests/test_project_control_response.py -q
```

期望：静态契约不少于 8 项、五视口浏览器断言、筛选/排序/来源展开和两组相邻回归全部通过；浏览器证据包含五张截图。

Chrome 按任务环境变量、PATH 中 Chrome/Chromium、macOS 应用路径顺序发现；缺失必须失败而非 skip。截图还要通过尺寸、非空、至少两色和通道极差检查，独立 reviewer 查看 1440、768、320 三张首屏截图。

## 输出

- evidence：`.factory/workitems/PM-DASHBOARD-002/evidence/PM-DASHBOARD-002-T01-verification.md`
- report：`.factory/workitems/PM-DASHBOARD-002/reports/PM-DASHBOARD-002-T01-implementation.md`
- review input：`.factory/workitems/PM-DASHBOARD-002/reviews/PM-DASHBOARD-002-T01-review-input.md`
- ledger：`.factory/workitems/PM-DASHBOARD-002/ledger.jsonl`

## 完成口径

实现者只能写 `ready_for_review`。`approved` 必须来自独立评审。
