# T13-R03 lock 与 CLI smoke 验证

- Crawler4j `check_compatibility.py::main`：manifest lock 只要求存在、合法 JSON object，不猜测未证明的顶层 schema；协议来自 `module.yaml.runtime_api`，版本来自实际 `crawler4j --version`，内容由 `crawler4j module check structure` 判定。
- Stratix `check_compatibility.py::main`：读取 `pnpm-lock.yaml` 固定矩阵；兼容后执行 `pnpm exec stratix --help` 与 `doctor`。
- 两者均证明不兼容时不执行后续 smoke；CLI 失败立即非零退出。
- RED：`5 failed, 22 passed`；GREEN：父级新鲜复验 `27 passed, 7 subtests passed`。
- Ruff、代码形态与 `git diff --check` 通过；无函数套函数或无职责单调用公共 helper。
