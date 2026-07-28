# SKILL-FIRST-PM-001-T01 实现报告

## 结果

`using-shanforge` 现在直接携带标准库 PM 快照脚本。目标项目只需把项目根目录传给已加载
skill 的脚本，不安装 Shanforge 包、不调用 Shanforge 仓库 CLI，也不读取 Shanforge `src/`。

ITA Club 已完成真实快照和缓存命中验证。旧平台 `src/`、只服务于该 runtime 的测试及依赖已
删除，`PM-DASHBOARD-004` 已登记为被本任务取代。

## 最小实现

- 单文件脚本读取 `.factory/project.json`、会话卡和 work item brief/ledger。
- 单文件行为测试覆盖外部项目、缓存、共享相对路径和无 `src` 边界。
- 使用 Python 标准库；没有新增依赖、服务、SQLite 投影或通用框架。

## 已知非本任务失败

全仓剩余 7 个失败分别来自：

1. `workflow-execution-design.md` 的旧版本表断言；
2. 当前 work item actor 列表包含 `AI_EXECUTOR`；
3. 当前会话事实不是 `FLOW-CONTRACT-001 closed`；
4. 当前会话未登记 `DOC-FACTORY-RESTRUCTURE-001`；
5. `ui-ux-pro-max` 的既有短语断言；
6. workflow 文档缺少既有 subagent 文本；
7. `document-templates` 的已登记 hash 与脏工作区不一致。

这些文件在本任务开始前已经修改或属于其他 work item，未为追求全绿而越界修复。

## 首轮审查响应

首轮 reviewer 给出 `changes_requested / C0-I7-M0`。当前已：

- 以 `--relative-paths` 取代名不副实的 restricted profile；
- 为运行时 I/O/编码失败返回结构化 receipt；
- 拒绝任何解析到目标项目外的输入和缓存路径；
- 把 task brief 补入正式读取合同；
- 重写 ITA Club 的旧执行计划；
- 重写当前数据设计和运维入口，并把旧平台设计明确降为历史；
- 重新运行 ITA Club 快照并验证缓存命中。

最终独立复审和 project-memory 增量复审均为 `approved / C0-I0-M0`。

## 看板重新验收

- 页面先显示当前重点、为什么做、当前任务和下一步，再展开技术状态。
- 任务卡显示层级、优先级、需求关系、目标和完成标准；无效分组目录被过滤。
- 旧 `PM-DASHBOARD-004` 显示为“已由新方案替代”，不再继续 T04/T05 runtime 实现。
- Shanforge 与 ITA Club 在 390×844、1440×900 下共 4/4 通过：无横向溢出、
  无控制台错误，跳转链接和归档区可用键盘操作。
- 最终 generation：Shanforge `a545bfac...230bd6`，ITA Club
  `86a2c1f9...ca4951`；第二次运行均为 `cache_hit=true`。
