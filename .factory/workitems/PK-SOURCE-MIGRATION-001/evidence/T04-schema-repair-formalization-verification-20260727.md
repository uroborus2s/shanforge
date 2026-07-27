# PK T04 Schema 修复正式化验证

- 时间：`2026-07-27T20:44:19+08:00`
- 状态：`passed`
- completion_level：`work_item`

## 人工确认

- data-design 候选 SHA-256：
  `1684d359f928a4a155dfa3ba8ec4a712154182939703f7467ff97d036bf72f60`
- frontend-design 候选 SHA-256：
  `f2cbff2f090530b7dde04d101acd95e4b18616def44f2ae0f4f94a0d66b654b4`
- 用户已精确确认两项候选并授权正式化、关闭和精确本地提交。

## 正式化

- `docs/05-design/data-design.md`：正式版本 `v1.4.0`
- `docs/05-design/frontend-design.md`：正式版本 `v1.6.0`
- 正式化后 SHA-256：
  - data-design：
    `a3074024fd695a3497bb9c8f53847c6f61d0b2c95807f21f8f642feb77b90595`
  - frontend-design：
    `a157cfd6fc175a26a3874b49cb2eaf02c8fbeb3e71d6bbebbfb3101235253f4e`

## 新鲜验证

```text
项目知识五文件：67 passed in 1.00s
Ruff format：2 files already formatted
Ruff lint：All checks passed!
Mypy：Success: no issues found in 290 source files
docs-stratego：exit 0
```

固定快照：

```text
status=success
cache_hit=false
generation=generation:8f6481166c22bf392f45e63ae3b9e836098780770e0ae8a4aeff3069108f78b3
parsed=9
rendered_pages=21
reused_pages=2262
source_count=644
```

Chrome 在该快照上检查 5 页 × 390/1440 两视口，共 `10/10` 通过；语义区块、返回
链接、横向溢出和控制台错误检查全部通过。

## N/A

- API / SQLite schema：未改。
- 远端 / 部署：未执行。
