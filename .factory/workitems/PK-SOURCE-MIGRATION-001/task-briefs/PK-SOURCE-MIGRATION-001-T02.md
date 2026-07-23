# 实施任务简报

## 工作项

- 任务：`PK-SOURCE-MIGRATION-001-T02` SQLite 绑定与 R009 当前来源退役
- 目标：删除数据库后只依赖正式 PRD即可重建当前需求。
- 设计：复用 `pk_requirement.source_section_key`，不新增表；R009 文件保留但不参与 source discovery。
- 接口：SQLite schema 和 CLI 不变。
- UI：N/A；本任务只改变投影来源。
- 测试：冷重建与现有 R009 owner 数据库 warm refresh；逐 ID 验证章节、AC parent/order/status、locator，并比较 after-image。
- 完成条件：缺章节绑定、unknown AC、R009 requirement contract 当前来源均为 0；warm/cold after-image 等价，manifest 与 PM map 仍登记。
