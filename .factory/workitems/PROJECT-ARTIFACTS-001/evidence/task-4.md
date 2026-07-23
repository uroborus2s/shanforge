# T04 验证证据

## 渲染回归

```bash
uv run pytest -q \
  tests/test_project_artifact_site_renderer.py \
  tests/test_project_site_renderer.py
```

结果：exit `0`，`21 passed`。

覆盖：

- 导航只有一个“项目文档”，不生成 `design/` 页面；
- 文档按 7 类分组；
- 正文、章节和索引关系绑定的机器附件在同一详情页；
- 任务/关系中的旧设计链接统一指向文档详情；
- 测试 catalog 显示“测试定义已登记 · 尚未执行”；
- 版本化 token 使旧 renderer 缓存失效，同一事实第二次直接 cache hit；
- 未变化文档页面的内容 hash 保持不变。

T03/T04 联合回归结果：`85 passed`；Ruff 与 Mypy 均通过。

## 正式静态快照

第一次：

- `cache_hit=false`
- `rendered_pages=51`
- `reused_pages=2119`
- 当前入口：`.factory/cache/site/current/index.html`

第二次：

- `cache_hit=true`
- `rendered_pages=0`
- `reused_pages=2170`

HTML 与 SQLite 是派生缓存，未加入 Git 候选。

## TEST-UI-DOCUMENTS-001 桌面文档目录

- 需求：单一项目文档入口，按用途分类，中文名称可读
- 任务：`PROJECT-ARTIFACTS-001 / T04`
- 被测 URL：`http://127.0.0.1:64712/documents/index.html`
- 临时启动：`python3 -m http.server 0 --bind 127.0.0.1 --directory <current-site>`
- 实际端口：`64712`
- 健康检查：页面、样式和快照脚本返回 200
- 关闭：验收后 `Ctrl-C`，服务已退出
- 断言：
  - “项目文档”导航恰好 1 个；
  - “设计”导航 0 个；
  - 文档分类 7 个；
  - API 设计详情链接存在；
  - 横向溢出 0；
  - console error 0。
- 截图：`evidence/TEST-UI-DOCUMENTS-001-desktop.png`

## TEST-UI-DOCUMENTS-002 移动端文档详情

- 需求：详情使用独立页面和返回按钮，正文与机器附件同页
- 任务：`PROJECT-ARTIFACTS-001 / T04`
- 被测 URL：`http://127.0.0.1:64712/documents/DESIGN-API-001.html`
- viewport：`390 × 844`
- 断言：
  - 返回按钮存在；
  - 关联机器附件 8 个；
  - `POST /apps/{app_id}/run` 可读；
  - “测试定义已登记 · 尚未执行”可读；
  - 人类文档摘要恰好 1 个，内部 definition grid 0 个；
  - 横向溢出 0；
  - console error 0。
- 截图：`evidence/TEST-UI-DOCUMENTS-002-mobile.png`

静态文件无需常驻应用服务；临时 HTTP server 只为内置浏览器绕过 `file://` 限制，
没有写操作或应用数据。
