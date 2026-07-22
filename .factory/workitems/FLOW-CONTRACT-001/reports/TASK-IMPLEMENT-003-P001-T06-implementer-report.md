# T06 实现报告：项目知识索引与只读项目站点

## 交付结果

完成“Git 正式事实 + 可重建 SQLite 当前投影 + 多页面静态站点 cache”的完整落地。项目查看不再要求 AI 散读并计算进度：会话调用一个固定 `project snapshot --html --json` 命令，CLI 自己判断来源变化、增量刷新或直接复用最后站点。

## 关键能力

- 39 张逻辑表、2 个 FTS、137 字段 PM 映射与 10 张 PM 表。
- Markdown/JSON/JSONL/Python/Git 提取器和稳定 semantic locator。
- `index/find/show/trace/context/snapshot/sync/maintain` 单一命令面。
- source contribution 增量复用、单事务 generation、SQLite 安全原子替换。
- 只读企业项目站点：总览、需求、设计、计划、执行、质量、文档、代码、版本、项目管理、报告。
- 所有完整详情使用独立页面与返回按钮；任务和 PM 字段使用中文人类说明。
- 默认快照自动检查来源；页面指纹最小重绘；失败不覆盖最后成功站点。
- 异步项目状态同步、登记式 cache 维护和可回滚资料迁移。
- `docs/` 只保留 34 份人类 Markdown；机器 Catalog/策略迁至 `.factory/catalog/`。
- `using-shanforge`、`project-memory`、`document-templates` 已迁移到新的固定 CLI 和事实边界；旧 HTML 模板与两套 PM 模型已删除。

## SQLite rebuild 修复

按用户确认的方案 1 实施：新旧数据库在原子替换前 checkpoint、完整性检查并转换为单文件 DELETE journal；严格清理登记的 rebuild sidecar；`os.replace` 后 fsync 目录；活动 reader 返回稳定 exit 7 并保留旧 generation。根因与尝试证据见同任务 report/evidence。

## 非目标与残留

- 没有写操作 UI、远端服务、Push、PR、Merge 或部署。
- SQLite、HTML、cache 和 runtime queue 不提交 Git。
- 全仓仍有两个与本任务无关的 skill 契约回归和一个无关 format 项，已在验证证据精确列明。

作者状态：`ready_for_review`；需要整体独立 Spec/Quality/UI review。

## 独立评审整改增补

首轮独立评审给出 `changes_requested / 60` 后，已落实以下修复：

- 137 个 PM 字段除四态 `field_values_json` 外，高频字段真实写入 typed columns，首页不再把缺失完成度伪造成 `0%`。
- 需求、任务、代码和测试使用专用详情结构，显示目标、范围、非目标、验收、进度、阻塞、关联、发布与定向来源；缺失事实显式显示“未登记”。
- alias、module、document revision、memory checkpoint、render view 和 cache entry 全部接入生产写入路径。
- cache hit 验证 current/build realpath、路由全集、文件类型、属主、精确权限和元数据，并无条件重算全部页面摘要；跨 build 复用使用 APFS copy-on-write，不使用 hardlink。
- CLI 删除无实现的 `--open/--serve`；第一版合同只允许静态文件。
- contribution、SQLite、HTML 和 receipt 共用敏感值脱敏策略。
- source discovery cache 只在索引成功发布后提交；页面在渲染前使用 page-input fingerprint 跳过未变化详情。

第二轮整改把代码符号汇总到代码文件详情的稳定锚点，并为严格安全前置条件内的单 Python 来源启用事务增量投影。完整 CLI 连续五次实测 `0.69, 0.69, 0.69, 0.69, 0.70 s`，P95 `0.70 s`，每次只解析 1 个来源、重建 6 页、复用 759 页，已达到同步变化 `≤800 ms`。无变化 site service 20 次 P95 `32.884 ms`，测量包含全部页面摘要校验；10,000 artifact extractor P95 `402.268 ms`、冷 rebuild `3.00 s` 的既有证据保持。
