# PK T04 任务简报共享 Schema 修复验证

- Work item：`PK-SOURCE-MIGRATION-001`
- Task：`PK-SOURCE-MIGRATION-001-T04-SCHEMA-REPAIR`
- 时间：`2026-07-27T20:10:24+08:00`
- 状态：`green`
- completion_level：`task`

## TEST-UNIT-PK-TASK-BRIEF-SCHEMA-001

RED：

```text
3 failed, 1 passed
```

- 同行别名缺少 `goal`。
- 空值 `- 目标：` 后的缩进列表缺少 `goal`。
- Registry 真实语料仍有 5 份缺少正式任务语义。
- 未知字段不生成语义的负例按预期通过。

GREEN：

```text
4 passed in 0.20s
```

共享 `_TASK_BRIEF_SECTION_KEYS` 现在是唯一别名表；通用字段行解析支持同行值和
空值后的缩进列表，未知字段继续被映射层拒绝。

## TEST-CONTRACT-PK-TASK-BRIEF-REGISTRY-001

五文件完整回归：

```text
67 passed in 0.94s
```

覆盖 extractor、SQLite index、site renderer、security 和 PM 投影。原有 4 份失败
简报及执行中新增的 `STRATIX-SERVICE-GUIDE-001-T01` 均产生真实任务语义；
`STATE-RECONCILIATION-001-T01` 补入唯一真实缺失目标。

质量门：

- Ruff：`All checks passed!`
- Ruff format：`2 files already formatted`
- Mypy：`Success: no issues found in 290 source files`
- Registry JSON、WorkItem/review ledger JSONL：解析通过
- 限定 `git diff --check`：通过
- docs-stratego：exit code `0`

## 固定快照

`markdown-v4` 首次全量失效验证：

```text
status=success
cache_hit=false
generation=generation:9135f76c34d9ebf4120c7b943f6842467fcc6e68d27b4ab3993894ed0939d6f4
parsed=190
rendered_pages=152
reused_pages=2129
```

格式化与文档同步后的最终当前快照：

```text
status=success
cache_hit=false
generation=generation:9c83133d5329179c2e018011bc53d0659b47f58d7e0f709ea27c01ef38ba6b2e
parsed=5
rendered_pages=13
reused_pages=2269
source_count=644
```

任务简报 Registry extractor 已从 `markdown-v3` 升为 `markdown-v4`，首次快照证明旧贡献
未被复用；最终快照绑定当前格式化后的候选。

## TEST-UI-PK-TASK-BRIEF-SCHEMA-001

- 静态入口：`.factory/cache/site/current/plans/*.html`
- 启动命令 / 端口 / 关闭方式：N/A；直接读取 CLI 生成的静态 `file://` 页面。
- 健康检查：5 个目标页面存在且可加载。
- 浏览器：本机 Chrome，无头模式。
- 视口：`390 × 844`、`1440 × 900`。
- 页面：SKILL cleanup、状态对账、Stratix guide、移动高保真、Iteration 6 决策。
- 10/10 页面运行均满足：语义文本存在、四个任务详情区块存在、返回链接存在、
  `scrollWidth=viewport`、控制台错误为 0。

## N/A

- API：N/A；未改 API、数据表或服务契约。
- 发布：N/A；只刷新本地派生快照，正式设计候选未发布。

## 候选哈希

- `docs/05-design/data-design.md`：
  `1684d359f928a4a155dfa3ba8ec4a712154182939703f7467ff97d036bf72f60`
- `docs/05-design/frontend-design.md`：
  `f2cbff2f090530b7dde04d101acd95e4b18616def44f2ae0f4f94a0d66b654b4`

## 结论

`approved_pending_candidate_hash_confirmation`
