# PM-DASHBOARD-003-T01：移动端横向溢出修复

- 父工作项：`PM-DASHBOARD-003`
- 状态：`closed`
- 来源：已确认的移动端溢出根因报告

## 目标

让 390px 移动视口不再出现页面级横向溢出，同时保留横向导航自身的滚动能力。

## 修复范围

- 只修改
  `.factory/workitems/PM-DASHBOARD-003/design-assets/prototype/status-dashboard-prototype.html`。
- 在 `max-width: 900px` 断点把 `.app-shell` 的
  `grid-template-columns: 1fr` 改为 `grid-template-columns: minmax(0, 1fr)`。

## 非范围

- 不修改生产 renderer、服务、数据或事实源。
- 不新增依赖、组件或响应式抽象。
- 不执行远端 Git、发布或部署。

## 验收标准

1. 390px 视口下 `document.documentElement.scrollWidth <= window.innerWidth`。
2. 十个管理要素、五个移动 lane 和详情抽屉仍可用。
3. 桌面视口不产生横向溢出，控制台错误为 0。
4. 原型静态验证脚本通过。

## Baseline 影响

仅修正当前视觉原型的响应式 CSS，不改变正式 UI baseline、领域边界、数据库、API 或架构。

## 人工确认对象

批准上述单行 CSS 修复和验收口径后，才实施并执行桌面、移动端浏览器回归。

## 关闭证据

- 人工批准：ledger
  `PM-DASHBOARD-003:mobile-overflow-fix-requirement-confirmation:20260727:v1`
- 独立评审：
  `reviews/PM-DASHBOARD-003-T01-independent-review-20260727.md`
- 关闭验证：
  `evidence/mobile-overflow-fix-closeout-verification-20260727.md`
