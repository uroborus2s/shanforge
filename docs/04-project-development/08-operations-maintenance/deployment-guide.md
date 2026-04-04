# 部署手册

## 1. 文档目标

说明如何把当前仓库的共享脚本和文档能力分发给自身或目标项目使用。

## 2. 当前部署方式

当前项目没有独立运行服务，主要部署动作是：

- 在当前仓库更新脚本与文档
- 在目标项目中调用共享脚本执行初始化、迁移、刷新和检查

### 2.1 前置条件

- 本地可执行 `python3`
- 能访问当前仓库 `scripts/`
- 目标项目具备可读写 `docs/` 和 `.factory/` 的权限

### 2.2 部署步骤

1. 在当前仓库完成脚本和文档修改。
2. 运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
uvx --from docs-stratego docs-stratego source validate --repo-path .
```

3. 在目标项目中按需执行：

```bash
使用 `document-templates` skill 重构目标项目 `docs/`
uvx --from docs-stratego docs-stratego source validate --repo-path "."
```

### 2.3 验证步骤

- 目标项目 `docs/` 已为 4 大模块结构
- 根 `docs/index.md` 能被章略·墨衡读取
- `docs-stratego source validate` 返回 `就绪`

### 2.4 回滚步骤

- 回退当前仓库的脚本或文档改动
- 回退目标项目的 `docs/` 迁移结果
- 重新执行回归测试和 `--check`

### 2.5 常见故障排查

- 若 `--check` 报旧结构异常，先执行迁移，不要直接刷新
- 若目标项目已有定制目录页，确认脚本版本已包含“保留人工正文”逻辑
- 若链接失效，检查迁移后 Markdown 相对路径是否已重写

## 3. 推荐表格

| 步骤 | 操作 | 预期结果 | 失败处理 |
|---|---|---|---|
| 1 | 当前仓库运行 `unittest` | 全部通过 | 回退代码并修复 |
| 2 | 当前仓库运行 docs 检查 | 返回 `就绪` | 修正导航或结构 |
| 3 | 目标项目执行迁移 | 旧结构升级完成 | 回退目标项目改动 |
| 4 | 目标项目执行检查 | 返回 `就绪` | 修正文档结构或路径 |
