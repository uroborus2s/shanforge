# T01-T08 整改实现摘要

## 已完成的用户可见变化

1. 项目回复可定位 WBS、TaskCard、当前 Gate 和唯一下一动作。
2. `review_status=approved` 不再被计作任务或产品完成。
3. worker `DONE` 只代表当前 TaskCard 实现结束；批次完成另需集中证据。
4. 开发、测试、Bug、修复使用不同事实正文；测试保留完整八态计数和逐项失败原因。
5. Go/Python 普通修改使用定向验证；批次、高风险和发布使用全量验证。
6. 外部工具不可用时返回 blocked、缺失能力和一个解决动作。
7. Crawler4j/Stratix 版本未知或不兼容时停止并报告版本差异。

## 精确修改位置

| 任务 | 文件与符号/章节 | 改动与原因 |
|---|---|---|
| T01 | `skills/writing-plans/SKILL.md` 的运行时路由、默认流程、任务身份；三个 writing-plans 模板；两个 project-memory 模板 | 删除临时 ID；固定 WBS 四列表和 TaskCard/ledger/session 恢复字段，使快照能一致读取。 |
| T02 | `project_snapshot.py::_category`、`_effective_event`、`_plan_stages`；TaskCard/review 模板；PM dashboard 合同 | 分离 review、任务生命周期和产品完成，防止 approved 冒充完成。 |
| T03 | `subagent-driven-development/SKILL.md` 的 worker 映射；verification 主文/checklist；共享回写合同 | 统一四种 worker 回执和三层 evidence 规则。 |
| T04 | `humanizer` 的 Shanforge 例外；`brainstorming` 的确认门；human-readable-status 四类示例；共享合并合同 | 保留三段式状态事实，开发/测试/Bug/修复分别说明必要事实。 |
| T05 | `go-developer`、`python-uv-project` 的验证范围 | 按风险选择定向/全量检查，明确未运行范围。 |
| T06 | art asset、browser、DOCX、PDF、XLSX 的能力探测与 blocked 回执 | 删除不存在脚本承诺；只展示真实可用命令。 |
| T07 | Crawler4j、Stratix service/admin 的版本兼容门 | 只有实际版本兼容才继续；未知/不匹配 fail closed。 |
| T08 | `using-shanforge/SKILL.md` 的无损测试基线规则；`writing-plans/SKILL.md` 的状态信封所有权修复 | 根据全量测试和黑盒失败修复真实回归；固定八标签统计、基线/定向分层和逐用例 owner。 |

## 测试代码

- 新增 `tests/test_human_response_contract_integration.py`。
- 新增 `tests/test_external_tool_skill_fallbacks.py`。
- 新增 `tests/test_runtime_skill_verification_scope.py`。
- 扩展 WBS/快照、review、worker、verification、Go、Crawler4j 和 Stratix 现有测试。

## 代码形态

- 未在函数或方法内部新增命名函数。
- 未抽取只有一个调用点且无独立职责的公共函数。
- 无新增依赖、运行时、schema 或中心控制脚本。
