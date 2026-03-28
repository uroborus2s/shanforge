# 安装说明

## 1. 前置条件

- 已安装可用的 `Codex` 或 `Gemini CLI`
- 拥有当前仓库的读写权限
- 本地可运行 `python3`

## 2. 仓库准备

1. 获取本仓库代码。
2. 进入仓库根目录。
3. 检查 `scripts/`、`skills/`、`docs/` 是否齐全。

## 3. 可选初始化动作

如果需要把当前仓库里的共享 skills 同步到本地：

```bash
python3 scripts/sync-codex-skills
```

## 4. 安装校验

- 可以读取 `docs/index.md`
- 可以执行 `scripts/factory-dispatch --help`
- 可以在 AI 会话里引用仓库内 `skills/` 和 `docs/`
