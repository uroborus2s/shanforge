# T10 可执行验证闭环

## 结论

- status: `completed`
- finding closure: `7/7`
- independent pytest: `69 passed, 4 subtests passed`
- failed: `0`
- skipped: `0`
- Ruff: `passed`
- `git diff --check`: `passed`
- code shape: `passed`；无局部命名函数，无本轮新增且未经解释的单调用公共 helper

## 问题与修复位置

| Finding | 原问题 | 修复文件与符号/章节 | 修复内容 |
|---|---|---|---|
| ZH-I06 | 不知道何时允许局部替代完整验证 | `skills/verification-before-completion/SKILL.md`“默认流程”第 3 步 | 只允许外部服务、受限硬件、不可获得凭据或明确无影响时替代；必须记录原因、命令、退出码、未覆盖范围和风险。 |
| ZH-M04 | 资源清理要求重复 | `skills/art-asset-pipeline/SKILL.md`“默认流程”“通过标准” | 清理 owner 收敛到收尾规则；流程和通过标准不再重复列同一动作。 |
| SE-I05 | 版本门只有 Markdown 关键词测试 | `skills/crawler4j-model-project/scripts/check_compatibility.py::main`；`skills/stratix-service/scripts/check_compatibility.py::main` | 新增真实可执行版本/协议检查入口；兼容和不兼容临时项目均直接执行入口。缺 CLI 或非法 package 输入清晰失败，不输出 traceback。 |
| SE-M01 | manifest 依赖人工检查 | `skills/art-asset-pipeline/scripts/validate_manifest.py::main` | 校验 pack type、assets 字段、相对路径、临时目录、文件存在性和 approved 来源；Skill 给出准确命令。 |
| SE-M02 | `code_shape_check` 只能自报 | `skills/tdd-workflow/scripts/check_code_shape.py::ShapeVisitor/main` | AST 拒绝函数/方法内部命名函数，并报告单调用 helper 候选供职责判断。 |
| SE-M03 | DOCX/XLSX 没有真实往返 | 两个 Skill 的 `scripts/office/{pack.py,unpack.py,validate.py::main}`；`tests/test_office_skill_roundtrip.py` | 最小 OOXML 执行 unpack→pack→unpack→package validation；生产脚本保留 `defusedxml`，测试只用隔离 shim。 |
| PM-I05 | 正式模板没有贯通 PM 快照 | `tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest.test_plan_template_task_card_ledger_and_snapshot_are_connected` | 从正式计划模板生成 plan，连接 TaskCard/ledger 后执行真实 snapshot 并检查计划页和任务页。 |

## 失败与根因记录

1. 第一版虽有 `67 passed + 6 subtests`，但独立检查拒绝关闭：版本测试只比较手写字符串、manifest 逻辑只存在测试中、Office 把安全解析器回退为标准解析器、存在新增单调用公共函数。
2. 第二版先得到 `3 failed`，原因是真实脚本尚未创建和测试遗漏导入；修复后 `67 passed + 4 subtests`。
3. 第二版边界复现发现缺少 `crawler4j` 时 `subprocess.run()` 未捕获 `FileNotFoundError`；第三版新增两项 RED，分别复现缺 CLI traceback 和非法 Stratix dependency map `TypeError`。
4. 最终 GREEN 为 `69 passed + 4 subtests`；直接运行缺 CLI 场景输出 `module.yaml is missing`、`cli_version detected=unknown required=0.4.0`、`runtime_api detected=unknown required=core-native-v2`，退出非零且无 traceback。

## 已知边界

- Office `--package-only` 证明 ZIP/XML 良构和往返，不替代 Word/Excel 语义与视觉验收。
- 兼容性脚本验证版本与协议事实；通过后仍要在真实目标项目执行 Crawler4j/Stratix CLI smoke。
- 代码形状检查报告的 `validate_xlsx` 等候选属于本轮前既有入口；本轮没有新增未经判断的单调用公共 helper。
