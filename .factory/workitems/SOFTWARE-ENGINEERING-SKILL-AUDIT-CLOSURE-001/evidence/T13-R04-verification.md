# T13-R04 代码形态验证

- 根因：`ShapeVisitor` 只访问命名函数，未访问 `ast.Lambda`。
- 修改：`skills/tdd-workflow/scripts/check_code_shape.py::ShapeVisitor.visit_Lambda` 在函数深度内记录精确文件和行号；模块级 lambda 不误判。
- 测试：RED 为 `1 failed`；GREEN 为 `3 passed, 0 failed`。
- 父级独立复验：`3 passed`；Ruff、checker 自检、ledger 校验和 `git diff --check` 通过。
- 代码形状：无函数套函数；未新增公共 helper。
