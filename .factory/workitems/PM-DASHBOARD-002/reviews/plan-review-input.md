# PM-DASHBOARD-002 计划复审输入

## 输入

- 计划：`.factory/workitems/PM-DASHBOARD-002/plan.md`
- 正式需求：`docs/04-product/prd.md` 的 `WF-CTL-010`
- 正式设计：`docs/05-design/frontend-design.md` §26.6
- 简报：`.factory/workitems/PM-DASHBOARD-002/task-briefs/PM-DASHBOARD-002-T01.md`

## 文件与测试

- 修改 `skills/using-shanforge/SKILL.md` 和两份 reference。
- 新建静态契约与真实 Chrome 固定 fixture 两份测试。
- 红灯锁定固定 H、完整 slot、十模块顺序、AI/代码边界、权限/错误处置和只读交互。
- 绿灯在五视口运行几何、焦点、对比度、筛选、排序、来源展开和截图验证。
- 证据、报告、评审和 ledger 只写 `.factory/workitems/PM-DASHBOARD-002/`。

## 首轮 Finding 关闭声明

- 浏览器验证：增加系统 Chrome 固定 fixture、五视口 DOM 几何/可访问性断言和五张截图。
- 精确 slot：计划列出总览全部 slot、11 页顺序、十模块共同后缀及三种 render disposition。
- 交互边界：本任务实现只读筛选/排序/来源展开；生产数据接入和事实派生明确排除。
- 负向断言：覆盖禁止第二事实源、AI 计算/拼装、错误态业务值、权限过滤后明文、网络和事实写入。
- 工作区隔离：增加执行前目标 diff preflight 和执行后允许路径检查。

## 第二轮 Finding 关闭声明

- 固定 H 与规则：新增 `AS_OF_H`、`PROJECT_TIMEZONE`、`RULE_VERSION`；定义 scalar、enum 和固定 renderer 生成 fragment 的类型/转义边界。
- conflict 处置：明确 `conflict|stale|failed -> ERROR_ONLY`；可见业务模块的 `CONFLICT_COUNT` 必须为 0。
- 全工作区隔离：preflight/收尾保存并比较全状态快照、摘要和路径集合；新增变化只能落在允许清单。
- 截图有效性：定义尺寸、非空、至少两色、通道极差和 reviewer 三视口人工查看。
- Chrome 发现：定义任务环境变量、PATH、macOS 固定候选顺序和缺失诊断。

## 复审重点

- 首轮五个和第二轮三个 Important 是否全部关闭。
- 是否仍误把 `.factory/pm` 写成全部事实源。
- 是否清楚区分模板/入口校准与尚未实现的生产 renderer。
- 是否能由未参与作者工作的执行者直接实施和验证。
