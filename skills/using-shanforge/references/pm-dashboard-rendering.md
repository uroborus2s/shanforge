# 项目状态查询与只读站点

本文件供 `using-shanforge` 在用户要求查看项目状态、进度、PM 看板、需求、设计、任务、风险、变更或交付详情时读取。它定义会话调用合同，不保存项目事实，也不替代固定 CLI 和 renderer。

## 核心合同

- 正式产品事实在 Git 管理的 `docs/`、代码和测试中；执行事实在 work item ledger、evidence、report 和 review 中。
- `.factory/index/project-knowledge.sqlite3` 是当前知识投影；`.factory/cache/site/current/` 是最后有效的只读站点。两者可删除重建，均不提交 Git。
- AI 只识别用户要看的范围和授权画像。AI 不临时扫描文件计算进度，不计算完成率、状态、风险、权限或上线结论，不拼装 HTML。
- 固定代码按 source registry 刷新索引、投影 PM 十要素、生成多页面静态站点并返回 `ProjectCommandReceipt/v1`。
- 输入指纹未变化时必须复用最后有效站点；不得为了“看一下项目”重复生成相同 HTML。
- 索引、权限、来源或定位异常时失败关闭；不得回退到 AI 手工汇总后声称“实时”。

## 标准会话调用

在仓库根目录执行：

```bash
PYTHONPATH=src uv run python -m settings.composition.project_knowledge project snapshot --html --json
```

返回数据至少包括：

- `site_path`：最后有效入口，标准位置为 `.factory/cache/site/current/index.html`。
- `cache_hit`：`true` 表示输入没有变化，直接复用；`false` 表示发布了新 build。
- `generation_id` 或等价代次标识。
- `input_token`、页面数、授权画像和只读标志。
- 索引检查、重建或失败诊断。

可选参数：

| 参数 | 使用条件 | 作用 |
|---|---|---|
| `--profile local-owner` | 默认本地项目负责人 | 生成本地 owner 只读视图 |
| `--profile shared-restricted` | 用户明确要求共享脱敏视图 | 只输出该画像允许的字段 |
| `--check` | 怀疑索引不完整、损坏或过期 | 在生成前执行只读完整性检查 |
| `--rebuild` | 用户明确要求冷重建，或诊断证明当前索引需要重建 | 从登记事实原子替换 SQLite，再生成站点 |

普通查看不得默认使用 `--rebuild`。第一版 CLI 不提供 `--open` 或 `--serve`；会话直接返回本地 `index.html` 链接即可。

## 定向查询

只有用户需要解释某个具体对象，或站点摘要不足以回答时，才按需调用：

```bash
PYTHONPATH=src uv run python -m settings.composition.project_knowledge project find '<关键词>' --json
PYTHONPATH=src uv run python -m settings.composition.project_knowledge project show '<entity_id>' --json
PYTHONPATH=src uv run python -m settings.composition.project_knowledge project trace '<entity_id>' --depth 2 --json
PYTHONPATH=src uv run python -m settings.composition.project_knowledge project context '<entity_id>' --max-files 4 --max-bytes 32768 --json
```

- `find` 找稳定实体 ID，不把文件名或标题文本当主键。
- `show` 返回单个实体、来源和 semantic locator。
- `trace` 返回已声明的强关系，不用标题相似度猜依赖。
- `context` 按 locator 精确切片，受 4 文件、32 KiB 预算约束；定位不唯一时零文件失败。

AI 先查索引，再按需读取 receipt 指向的最小原文。不得先散读 `docs/` 或 `.factory/workitems/`。

## 来源与更新边界

source registry 是允许读取的来源清单。固定提取器支持：

- Markdown：文档控制字段、稳定标题路径、章节内容 Hash。
- JSON：JSON Pointer 和声明关系。
- JSONL：稳定事件 UID；缺 UID 记录诊断，不用行号充当身份。
- Python：AST 模块、类、函数和代码位置。
- Git：当前提交与受控文件身份。

当正式文档、代码、测试、ledger 或受控 memory 发生变化时，可以通过同一快照命令增量更新索引和页面。SQLite 不保存第二份业务历史；历史仍由 Git 与权威 ledger 管理。

## 页面信息架构

静态站点至少提供：

- 项目总览。
- 需求、设计、任务、缺陷、代码、文档、质量、版本和报告。
- PM 十要素：项目章程、团队与干系人、范围/WBS/进度、风险、沟通、会议/决策、行动项、状态报告、变更、交付/收尾。

所有业务对象采用稳定列表页和独立详情页。详情页必须有清晰返回按钮；不得使用 drawer、modal 或侧边详情栏承载完整详情。任务说明优先使用人类可读的目标、当前状态、下一步、来源和关系，不直接把内部事件码当正文。

## 只读与安全

- 页面不得提供新增、编辑、删除、审批、状态切换、提交或发布入口。这些变更只能通过用户与 AI 会话进入正式 workflow。
- renderer 只消费 SQLite 的已验证页面 DTO；不读取 cookie、local storage、网络或原始 Excel。
- 业务值必须 HTML 转义；站点不得包含越权明文、密钥或未登记来源。
- `shared-restricted` 页面只能包含已脱敏字段。权限不明时不得生成宽松结果。
- 查看、查询和渲染不得创建 WorkItem、修改正式事实、同步 memory 或提交 Git。

## PM 十要素的实现

十要素不是十份手工维护文档，也不是 `.factory/pm/` 第二套事实。它们由固定 137 字段映射从同一代次投影到 10 张 SQLite PM 表，再由 renderer 生成列表和详情页。

字段只有四种显式状态：`known`、`unknown`、`not_registered`、`not_applicable`。页面只展示投影结果，不在浏览器中推导业务值。没有来源的要素显示“未登记”或“不适用”及原因，不创建空文档补位。

## 缓存与维护

- `current` 永远指向最后成功发布的 build；失败构建不得覆盖它。
- 页面按 fingerprint 增量复用；静态文件只保留当前 build、一个回滚 build和 legal hold 项。
- 清理前运行 `project maintain --dry-run --json`；只有已登记 cache 才能执行 `--apply`。
- `.factory/index/`、`.factory/cache/`、`.factory/runtime/project-state-sync.sqlite3*` 由 `.gitignore` 排除。
- 未授权 Git 提交时，后台同步以 `commit_not_authorized` 正常收口，不把派生物提交到仓库。

## 失败语义

| 情况 | 行为 |
|---|---|
| 输入未变化 | 返回 `cache_hit=true` 和最后有效入口，不重写页面 |
| 首次使用且无索引 | 自动冷重建并发布第一版站点 |
| 索引损坏或原子替换存在活动 reader | 返回稳定失败码；保留旧索引和旧站点 |
| locator 为 0 个或多个候选 | 定向读取失败，读取文件数为 0 |
| source registry 越界、软链接越界或来源 Hash 不一致 | 拒绝读取并记录诊断 |
| 构建中途失败 | 不切换 `current`，继续返回最后成功版本并报告 stale/failed |
| 授权画像未知 | 失败关闭，不生成 owner 全量视图 |

不新增单独的 `project-management` skill。项目状态页是 `using-shanforge` 的按需只读输出，固定代码负责事实计算与 HTML，工作 skill 仍只处理各自专业任务。
