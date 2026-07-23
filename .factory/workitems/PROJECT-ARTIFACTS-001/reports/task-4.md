# T04 实施报告

## 结果

项目站点现在只有一个“项目文档”入口。设计、UX/UI、API、测试、部署和运维都按
文档分类展示，不再维护“设计”和“文档”两个重复入口。

## 文档详情

每个详情页按以下顺序阅读：

1. 返回上一列表；
2. 中文名称、文档分类、适合谁看、负责人、当前状态和源文件；
3. Markdown 正文；
4. 章节索引；
5. SQLite 当前关系绑定的机器附件。

机器附件卡展示中文标题、用途、状态、稳定 ID 和必要追踪。Penpot 文件未连接时明确
显示“等待在 Penpot 打开文件并连接插件”，不生成伪文件或假链接。OpenAPI 显示
method/path；测试 catalog 只显示“测试定义已登记 · 尚未执行”。

## 缓存

wrapper 以独立 renderer version 包装已有静态 renderer，并对 source token 加版本。
事实未变化时，CLI 在加载 SQLite DTO 和渲染前直接返回最后站点；事实变化时，
publisher 仍按页面 fingerprint 只写变化页面。

SQLite、HTML 和缓存保持 `.factory` 派生状态，不进入 Git。
