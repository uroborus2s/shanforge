# T06 Penpot 连接检查

- 时间：`2026-07-27T18:49:56+08:00`
- skill：`browser-control`
- status：`needs_user_input`

## 事实

- 本机已安装 `@penpot/mcp@2.15.4`，配置端点为
  `http://127.0.0.1:4401/mcp`。
- 直接启动已构建的 MCP server 后，`initialize`、`tools/list` 和
  `high_level_overview` 均成功。
- 只读调用 `execute_code` 查询页面时返回：
  `No Penpot plugin instances are currently connected.`
- 已正常停止本轮临时启动的 MCP server；未写入 Penpot。

## 下一步

用户需在目标 Penpot 文件中打开 MCP 插件并点击 Connect。连接后重新启动
server，执行移动端高保真同步及管理后台组件标注，再验证页面、画板和导出。

```text
工作结果：
- work_item: UI-UX-FULL-EXAMPLE-001
- skill: browser-control
- status: needs_user_input
- outputs:
  - none
- evidence:
  - execute_code returned no connected plugin instances
- ledger_event: UI-UX-FULL-EXAMPLE-001-E020
- needs:
  - user_input
```
