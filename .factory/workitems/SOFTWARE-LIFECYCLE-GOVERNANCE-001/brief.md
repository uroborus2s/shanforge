# SOFTWARE-LIFECYCLE-GOVERNANCE-001

## 目标

统一 Shanforge 当前 Skill-first 正式设计事实，删除已废止 Python 平台在现行设计、接口、UI 和机器附件中的执行资格；补齐一张可执行的生命周期输入、活动、输出、保存位置、负责人、验证、退出 Gate 与回流矩阵，并用跨文档测试阻止版本、状态和废止路径再次漂移。

## 验收标准

- 所有当前生效的架构、模块、API、前端、UI、记忆、接口矩阵和流程设计只描述仓库真实存在的 Skill-first 交付面。
- 已废止的 `src/` 平台、HTTP/OpenAPI 运行时和未投入使用的 Penpot 机器附件不再具有当前正式资格；历史仅由 Git 与归档 WorkItem 回源。
- 正式流程明确何时使用阶段门、Spike/原型、TDD、定向回归和发布质量门。
- 生命周期矩阵逐阶段声明触发、权威输入、准入、活动、输出、保存位置、owner/模型、验证、退出 Gate 和回流。
- `docs/document-index.md` 的版本与文档控制一致，`REQ-SF-008` 与已关闭模型调度 WorkItem 状态一致。
- 自动测试覆盖废止路径、版本索引、需求状态、生命周期矩阵和机器附件资格。
- 当前工作区和提交后的干净克隆通过完整 pytest、Ruff、Skill validator、JSON/JSONL/TOML 与 Git 卫生检查。

## 范围

- `docs/05-design/` 当前设计基线、`docs/document-index.md`、`docs/04-product/requirements-matrix.md`。
- 当前接口/UI 机器附件及其来源登记。
- `docs/06-delivery/` 测试登记和跨文档治理测试。
- 本 WorkItem 的计划、ledger、evidence、report、review 和必要 memory 摘要。

## 非目标

- 不新增仓内 `src/`、服务、数据库、API runtime、UI 编辑器集成或新依赖。
- 不恢复旧 Catalog 平台流程或批量迁移历史 WorkItem。
- 不执行 push、PR、merge、发布或部署。

## 状态

`closed`
