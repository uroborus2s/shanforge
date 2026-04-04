# 变更摘要

## 2026-04-04

- 修复文档站点告警：
  - 将 `docs/04-project-development/04-design/evaluation-summary-and-approval-reporting.md` 中指向 `config/`、`scripts/` 的 Markdown 相对链接改为仓库路径说明
  - 避免 MkDocs 将仓库非文档文件误判为站内文档目标并输出 warning / info
  - 复查 `docs/` 后，未发现同类指向 `config/`、`scripts/` 的 Markdown 文档链接残留
- 全量扫描无效链接：
  - 使用 PyPI 发布版 `docs-stratego` CLI 在聚合站点工作区执行 `dev --build-only`
  - 当前未再出现 `shanforge` 文档的无效链接或未识别相对链接告警
  - 当前构建输出仅剩 Material for MkDocs 的上游公告，不属于本仓库文档缺陷

## 2026-04-03

- 重构 `skills/document-templates/`：
  - 默认文档结构切换为 `01-getting-started / 02-user-guide / 03-developer-guide / 04-project-development`
  - 明确根 `docs/index.md` 是唯一导航与权限事实源
  - 补充 docs 标准升级、历史项目纳管和旧目录迁移的正式流程说明
  - 新增根索引与模块首页模板，补齐新结构的入口模板缺口
- 补齐 Python / uv 工程基线：
  - 新增 `.python-version`，固定仓库默认 Python 为 `3.14`
  - 新增 `pyproject.toml`，声明 `requires-python = ">=3.14"` 与 `uv` 开发工具链
  - 保留 `uv.lock` 作为仓库锁文件；当前环境里的 Homebrew `uv` 仍需另行修复后再重新生成
  - 正式文档继续推荐使用 `uv run python scripts/...` 执行本仓库脚本
- 重构 docs 流程：
  - 文档内容维护统一改走 `document-templates` skill
  - PyPI 已发布的 `docs-stratego` CLI 成为唯一正式的源仓校验、接入、同步、构建和预览入口
  - 删除 `factory-docs-*` 旧 docs 处理链的正式入口定位
