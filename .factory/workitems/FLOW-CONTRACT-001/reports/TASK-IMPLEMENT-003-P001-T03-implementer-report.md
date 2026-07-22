# T03 实现者报告

## 产出

- `find/show/trace/context/index check|refresh|rebuild` application 用例与 composition 入口。
- Access 只解析参数和输出 `ProjectCommandReceipt/v1`，不直读 SQLite/文件。
- alias 最多 8 跳并检测环；trace 默认 2 层/100 节点/200 边；同边多来源不合并。
- context 只返回 4 文件/32 KiB 读取计划，现时重新校验 locator 恰好命中一次，不返回正文。
- 固定退出码 0/2/4/6/8 已在当前命令路径生效；权限/并发/异步类退出码待 T05/T06 对应路径。

## 范围自检

- CLI 未提供 TUI，未实现站内编辑。
- 未修改冻结 system-task 候选。
- 实仓 SQLite 只是可删除运行投影。
