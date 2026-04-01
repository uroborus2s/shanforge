# docs-stratego 升级通知

- 通知时间：2026-04-01
- 发起方：shanforge / Codex
- 通知对象：`docs-stratego` 项目开发者
- 目的：使用最新的山海工枢，对 `docs-stratego` 项目自行完成升级确认

## 当前结论

- `shanforge` 已完成历史项目纳管，当前已进入软件工厂维护态。
- 最新 docs 源文档标准升级能力已落地，包括：
  - 契约文件自动索引与校验
  - 根导航合并保留
  - 单项目升级入口
  - 多项目批量升级入口
- 对 `docs-stratego` 的只读检查结果显示：当前 docs 源文档状态为 `就绪`。

## 请 `docs-stratego` 开发者执行

在 `docs-stratego` 项目根目录执行以下命令，确认项目在最新山海工枢下仍然通过升级与校验：

```bash
python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch docs-standard-upgrade --project "/Users/uroborus/AiProject/docs-stratego" --check
python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch docs-standard-upgrade --project "/Users/uroborus/AiProject/docs-stratego"
python3 /Users/uroborus/AiProject/shanforge/scripts/factory-state-doctor --project "/Users/uroborus/AiProject/docs-stratego" --owner "<docs-stratego-owner>" --scope docs
```

## 预期结果

- `docs-standard-upgrade --check` 返回：
  - 结构迁移：`无需`
  - 源文档状态：`就绪`
- 正式执行 `docs-standard-upgrade` 后，最终状态为 `就绪`
- `state-doctor --scope docs` 不再提示 docs 标准缺口

## 若出现异常

- 若提示旧 docs 结构残留，先执行同一入口的正式升级，不要手工拆步骤。
- 若提示契约文件缺失最小字段，按最新源文档标准补齐：
  - OpenAPI：`openapi`、`info.title`、`info.version`
  - MCP tools：非空 `tools`，且条目含 `name` / `description` / `inputSchema`
- 若根导航有人工包装分组，升级后请人工复核目录锚点与顺序。
