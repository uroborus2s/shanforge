# TASK-IMPLEMENT-003 整体独立评审输入

## 评审目标

对“项目知识索引、固定查询 CLI、异步同步与只读项目站点”整体实现做 Spec / Quality / UI 独立评审。评审人只读，不修改实现。

## 规格输入

- `.factory/workitems/FLOW-CONTRACT-001/drafts/DESIGN-PROJECT-KNOWLEDGE-001.R001.md`
- `.factory/workitems/FLOW-CONTRACT-001/plans/TASK-IMPLEMENT-003-P001.md`
- `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json`

## 实现范围

- `src/{access,application,domain,runtime,settings}/project_knowledge/` 及 composition/CLI。
- `.factory/project-knowledge/*.json`、`.factory/catalog/*.json`、Catalog builder。
- `tests/test_project_knowledge_*.py`、CLI、sync 和相邻治理测试。
- 正式 PRD、需求矩阵、现有 `docs/05-design` owner、文档索引与入口。
- `using-shanforge`、`project-memory`、`document-templates` 的新入口与事实边界。

## 重点检查

1. 是否真正只有一套事实/投影/渲染链，旧 `.factory/pm` 和旧模板是否已退役。
2. 39 表、137 字段、稳定 locator、强关系、source contribution 与原子 generation 是否满足规格。
3. 标准 snapshot 是否自动判断来源变化，无变化是否零重绘；Git HEAD 是否可追溯。
4. SQLite atomic rebuild 是否在 sidecar、reader、失败点和 fsync 上失败关闭。
5. 异步 queue、fencing/retry、cache maintenance 与 migration 是否不阻塞主任务且不误提交派生物。
6. UI 是否可商用、只读、人类可读；完整详情是否为独立页面和返回按钮；十要素是否齐全。
7. 安全、HTML 转义、路径/软链接、权限画像、键盘、打印、响应式与 axe 证据是否可信。
8. 全仓剩余失败是否确为任务外既有改动，不能把它们伪报为全绿。

## 证据

- `evidence/TASK-IMPLEMENT-003-P001-T05-verification.md`
- `evidence/TASK-IMPLEMENT-003-P001-T06-verification.md`
- `evidence/TASK-IMPLEMENT-003-P001-T06-migration-activation.md`
- `evidence/TASK-IMPLEMENT-003-P001-review-remediation.md`
- `reports/TASK-IMPLEMENT-003-P001-T06-sqlite-rebuild-root-cause.md`
- `/tmp/shanforge-project-site-browser/` 当前浏览器与 axe 临时证据。

## 首轮整改后的复审重点

请逐项复核首轮 7 Important / 3 Minor，不只读取实现者结论。尤其检查 typed columns、专用详情、六类原 DDL-only 表的生产写入、统一脱敏、静态 CLI、cache fail-closed、旧 build 元数据不变和页面输入指纹复用。

第二轮整改后请重点验证两个剩余 Important：缓存命中是否对每个页面无条件重算摘要并拒绝同 size/mtime 篡改；完整单来源变化是否真实满足 `≤800 ms`。当前真实仓完整 CLI 五样本为 `0.69, 0.69, 0.69, 0.69, 0.70 s`，P95 `0.70 s`，每次只解析 1 个来源、重建 6 页并复用 759 页。代码符号改为代码文件详情内稳定锚点，不能把页数下降误判成符号不可查看。

## 输出要求

- 结论：`approved` 或 `changes_requested`。
- 评分：0–100。
- Findings 按 Critical / Important / Minor，给精确文件/行为证据。
- 开放 Critical/Important 必须为 0 才能进入提交。
- 明确区分本任务问题、工作区既有无关问题和未验证项。
