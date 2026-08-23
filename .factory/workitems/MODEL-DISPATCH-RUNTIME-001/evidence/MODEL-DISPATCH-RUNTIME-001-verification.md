# MODEL-DISPATCH-RUNTIME-001 验证证据

## 基本信息

- Actor：`gpt-5.6-sol`
- 时间：`2026-08-24T01:22:36+08:00`
- 验证声明：当前批次候选具备真实、确定性、失败关闭的 Sol/Terra/Luna 派发合同，并通过仓库完整质量门。
- 结论：`passed`

## Red / Green

- Red：Terra T03 把候选测试覆盖到 `git archive HEAD` 基线临时树，`5 failed / 1 passed`，exit code `1`；失败原因是基线缺少 `.codex` 模型配置、本 WorkItem 父回执和新派发合同，与预期一致。
- Green：首轮 `6 passed`；reviewer I1–I3 整改后结构化回归 `9 passed`，exit code `0`。
- Review remediation Red：整改后的测试覆盖到 `git archive HEAD` 基线临时树，`8 failed / 1 passed`，exit code `1`；失败原因与缺模型配置、双分支合同、task brief 和父回执一致。
- Iteration 2 Green：严格互斥派发表、冲突失败关闭和四张 brief 合同为 `9 passed`，exit code `0`。
- 定向 Ruff：`uv run ruff check tests/test_model_tier_routing.py`，exit code `0`。

## 当前候选完整验证

| 检查 | 真实结果 | exit code |
|---|---|---|
| `uv run pytest -p no:cacheprovider` | Iteration 2 根因整改后 `273 passed in 2.47s`，failed/error/skipped/not_run 均为 0 | `0` |
| `uv run ruff check .` | `All checks passed!` | `0` |
| 全部 Skill `quick_validate.py`（项目 uv/PyYAML 环境） | `38/38 skills valid` | `0` |
| Python `tomllib` 配置检查 | `6 个项目 TOML valid`；Sol/high、Luna/low、Terra/medium、reviewer/high/read-only | `0` |
| Python JSON/JSONL 解析 | `.factory` 内 `160 JSON / 45 JSONL valid` | `0` |
| `git diff --check` | 无 whitespace error | `0` |

## 派发事实

- Luna：父 Sol 以 `model=gpt-5.6-luna`、`reasoning_effort=low`、`fork_turns=none` 派发 T01；工具接受 canonical task `/root/model_dispatch_luna_config`。
- Terra：父 Sol 以 `model=gpt-5.6-terra`、`reasoning_effort=medium`、`fork_turns=none` 派发 T02/T03；工具接受 canonical task `/root/model_dispatch_terra_contract`、`/root/model_dispatch_terra_tests`。
- 三条调用均由父会话生成稳定 `dispatch_id` 并记录 `source=parent_tool_receipt`；子代理自报模型没有被当作绑定证据。
- 可证明的是显式请求参数和工具接受事实；仓内不能读取或证明模型内部身份。

## 偏离与未运行项

- 首次用系统 Python 执行 Skill validator 因缺少 PyYAML 失败；随后使用项目锁定的 `uv` 环境完整重跑 38/38 并通过。失败尝试未计为通过证据。
- Iteration 2 首次 validator 重跑因沙箱禁止读取 uv 缓存而 exit `1`；在获准的沙箱外以同一命令重跑为 `38/38`、exit `0`，不把环境失败写成通过。
- 首次 review 整改后的完整 pytest 暴露 `subagent-driven-development` 点名相邻 review Skill 的边界回归；直接原因和根源原因定位后由原 Terra worker 删除跨 Skill 点名，失败节点 `1 passed`，完整回归再为 `273 passed`。该失败没有被写成通过。
- UI、API、服务、E2E、安全和性能测试未运行：本次变更只涉及 Codex 项目配置、Markdown Skill 合同、正式说明和 pytest 治理守卫，没有对应运行面。
- 干净克隆验证尚未运行；该门在精确本地提交后执行，当前结论只覆盖未提交候选。

## 需求核对

- Sol 总体设计与控制：`.codex/config.toml`、`AGENTS.md`、`using-shanforge`。
- 确定性 Luna/Terra 派发：模型矩阵、任务简报字段、Codex spawn 合同和结构化测试。
- 真实父回执：WorkItem ledger 的 T01/T02/T03 `subagent_dispatch_accepted` 事件与测试解析。
- 失败关闭：工具/模型/回执异常和模型不一致均返回 `dispatch_failed` 或 `worker_unavailable`；旧换模型/主线程 fallback 已移除。
- 质量状态：`passed`；第二轮独立评审 `changes_requested / 58 / C0-I4-M0` 的四项根因已整改并完成新鲜全量验证，待同一 reviewer 终审和提交后干净克隆复验。
- 独立终审：同一 reviewer Iteration 3 为 `approved / 96 / C0-I0-M0`，新鲜复验模型路由 `9 passed`、完整 pytest `273 passed`、Ruff、解析和 diff check 全绿。

## 实现提交干净克隆

- 实现提交：`b270ae4`，分支：`v2`。
- 从该提交建立无 hardlink 的新临时克隆；克隆内 `uv run pytest -p no:cacheprovider` 为 `273 passed in 2.70s`，exit `0`。
- 克隆内 Ruff 为 `All checks passed!`，38 个 Skill validator 为 `38/38 skills valid`，均 exit `0`。
- 克隆内 `6 TOML / 25 JSON / 40 JSONL` 全部可解析；`git diff --check` 与 `git status --short` 无输出，HEAD 回读为 `b270ae4`，均 exit `0`。
