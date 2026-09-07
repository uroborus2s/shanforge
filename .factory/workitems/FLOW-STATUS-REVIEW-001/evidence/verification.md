# 验证与行为试用记录

范围：本批流程合同、文档、测试和受控合成场景；不包含医院或 ita-club 产品验收。

## 首轮事实（保留，不覆盖）

- 父线程合同定向复验：77 passed；5 个相关 skill 的 quick_validate 均 exit 0。
- 全仓预检（排除尚未生成的实际响应检查）：410 passed、2 failed、1 deselected、11 subtests passed。失败为 session 模板辅助标签和 current-state 恢复字段兼容；已定位修正，等待全量重跑。
- 独立试用 v1：8 条原始输入由未参与实现的 Terra medium 在一个独立任务上下文内生成，原始回复保存在 `behavior-observations.json`；不是 8 个独立上下文，也不是真实业务项目运行。
- 消费 v1 的测试：1 failed、2 passed。SR-04 原 oracle 错把“当前批次剩余”当作“完整产品剩余”，还把进行中的 bug 修复归为未知/未开始；输入未给完整产品基线，故应保留产品剩余未知。修正测试依据原始输入，不改实际回复。
- 父线程正文检查另发现真正的合同问题：SR-01/02/03/07/08 把“状态复核”当作总体阶段，SR-04 把 bug 修复当作总体阶段；普遍缺唯一下一动作与遗漏核对正文。原测试未断言这些字段，所以结构通过不代表正文合格。
- 整改：主合同明确总体阶段与当前活动的证据边界；补足对应观察字段、负向变异。v1 原样保留；修正后以新独立上下文重新生成 v2，由另一只读 reviewer 验正文语义。

## 当前结论

第三轮回复、核心声明/变异/新鲜性绑定及全量验证通过；同一独立reviewer复审approved，唯一Important已关闭。实现已本地提交27fe2cd，未推送。本批五项要求完成，不声明其他产品完成。

## 第二轮事实（保留，不覆盖）

- 修正兼容问题后的父全仓预检：`UV_CACHE_DIR=/private/tmp/shanforge-flow-uv-cache uv run --no-sync pytest -q -k 'not real_independent_observations_match_closed_facts'`，exit 0，412 passed、1 deselected、11 subtests passed。此结果不包括二轮真实回复。
- 第二独立上下文产出 8 条回复：`behavior-observations-v2.json`，未读一轮或 oracle。阶段/活动已分开；SR-06 明确同候选新增证据揭示此前未识别泄露，而非新代码引入。
- SR-04 仍把已知本批缺口写成完整产品剩余，同时承认完整基线缺失；这是实质不一致，不能判通过。
- v2 把状态清单保存为字符串而非数组，SR-05 还含不在原正文的 delta_reason 摘录；不改原记录来通过测试。下一轮明确观察 schema 和“不存在的正文事实省略”规则。
- oracle 校准：SR-01 输入仅说明其他模块未验证，不足以断言一定未实现，应接受 incomplete 或 unknown，但必须拒绝 complete；“状态核对/状态复核”和“完成/验收完成”是允许的同义表述。严守事实，不以固定文案当语义证明。
- 测试收口：严格清单类型、错误完成/未知归零/遗漏与增项/错误阶段/缺下一动作摘录，以及重复/缺失场景；旧响应只用于明确失败边界，不能错配不同 case ID 让拒绝测试空过。

## 需求与实现映射

第三轮派发前父行为检查为 `1 failed, 4 passed`，exit 1，唯一失败是尚不存在 v3 实测文件。没有预填通过记录。第三轮输入冻结的 SHA-256：

```text
dd28b22beb99a89cc0200154cf18c7f7ef6e66db26c5cec320d44c85484b7aac  skills/using-shanforge/SKILL.md
3dff3128b05cdd48cae0d6107e214223805a7d014cfec076d503febd3e8b691c  skills/using-shanforge/references/human-readable-status.md
0dd9f5932110dc40dce992cd248dd5e137d3bfcbd43856d311a9869641f6eb4a  skills/using-shanforge/references/work-skill-return-contract.md
85a50ae108bcddce7651b9fbe7dec726fa29172bdf33394bd7f19769de61e7d0  skills/requesting-code-review/SKILL.md
7a0d247825243ea33e75d6e4ef5dc6cd46406daf5007929e83cfdee9165f5328  skills/requesting-code-review/references/review-score-rubric.md
d3752b296671afed2bb137d28db4a693232fc27aa48b613ada9678eb4cf22f55  .factory/workitems/FLOW-STATUS-REVIEW-001/task-briefs/FLOW-STATUS-REVIEW-001-T03.md
0732f99f558dc51fb73bb85848fa724856e1b1d9748c9072803543722d690850  .factory/workitems/FLOW-STATUS-REVIEW-001/evidence/raw-behavior-inputs.json
```

| 批准需求 | 现有资产变更 | 验证边界 |
|---|---|---|
| REQ-FLOW-01 | using-shanforge 状态/回写合同、project-memory 会话模板 | 合同测试 + 实际状态回复；独立复审通过 |
| REQ-FLOW-02 | 原需求矩阵增加版本、页面/接口/任务/测试和设计/实现/集成/验收证据；completion checklist | 不新建并行需求台账；不核验其他产品 |
| REQ-FLOW-03 | requesting-code-review 默认无总分，明确本范围结论/未检查范围 | 权限缺陷受控案例；没有实际产品安全评审 |
| REQ-FLOW-04 | 候选指纹、标准版本、稳定 Finding 与复审差异 | 同候选新增日志案例；正文仍需独立复核 |
| REQ-FLOW-05 | raw/oracle 分离、独立真实回复、结构与变异测试 | 合成场景非真实软件全流程验收，不保证长期零漏检 |

## 第三轮事实

- 新独立上下文生成 `behavior-observations-v3.json`，只读已冻结技能与原始输入；自检类型/8个唯一ID/逐字摘录通过。v3 不被实现者改写。
- 父初次消费为 `1 failed, 4 passed`（测试在首个不匹配处停止）；逐案例诊断显示 SR-02..07 的6项匹配，SR-01 和 SR-08 不匹配。
- SR-01 已列出三个未验证领域，并称完整产品剩余未知；输入只提供基线存在，没有完整范围对账，保守写未知没有隐藏已知缺口。oracle 应允许未知或已知三项清单，但拒绝空清单。
- SR-08 已有完整产品验收通过，“交付收口”是合理阶段描述，不等于已发布；纳入终态同义表达，仍拒绝设计、开发或已发布。
- 此次只校准测试预期，不改技能或v3正文。该判断及所有正文需独立 reviewer 审核，不能以调整后测试绿代替独立结论。
- 冻结后的全仓预检（不含v3消费）为414 passed、1 deselected、11 subtests passed，exit 0；变更 Python Ruff、代码形状与 diff check 均 exit 0。代码形状报告两个既有单调用 helper 建议，无禁止形态错误。

## 最终候选父验证（2026-09-07）

- `UV_CACHE_DIR=/private/tmp/shanforge-flow-uv-cache uv run --no-sync pytest -q`：exit 0，416 passed、0 failed、0 skipped、11 subtests passed，10.23s。
- `UV_CACHE_DIR=/private/tmp/shanforge-flow-uv-cache uv run --no-sync pytest tests/test_delivery_status_review_behavior.py -q`：exit 0，6 passed，0.01s；包含8案例事实回放、字段/集合变异、v1明确拒绝和当前技能/原始输入/v3回复哈希绑定。
- 同环境的 `uv run --no-sync ruff check` 与 `python skills/tdd-workflow/scripts/check_code_shape.py` 覆盖本批5个变更 Python 测试文件，均 exit 0。形状检查只报告2个范围外既有 helper 建议，无错误。
- `shasum -a 256 -c .factory/workitems/FLOW-STATUS-REVIEW-001/evidence/candidate-sha256.txt`：exit 0，25个绑定文件全部 OK；清单指纹见 review-brief.md。
- `git diff --check`：exit 0。5个修改的skill入口 quick_validate 均 exit 0。没有新增依赖/运行时。
- 新鲜性测试首次因manifest缺raw与v3哈希而RED；父按实际文件补齐后通过，没有修改实际回复。
- 以上不是自由正文语义的最终批准；由未参与实现/试用的独立 reviewer 判断。历史完整workflow的逐场景前向回归、真实项目长周期验收、发布部署均未运行。

## 首轮评审整改后父复验

独立review认可8份正文，但发现FLOW-SR-REV-I-01核心声明摘录错配。仅修改行为测试，未修改skill、oracle或实际v3。已补删除/反转完成声明、本批/产品作用域混用及自然否定伪肯定的拒绝检查；该有限语料断言不代替独立语义判断。

- 完整pytest：exit0，416 passed、11 subtests passed，10.45s；行为6 passed（0.01s）。命令同上，重新实际运行。
- 变更5个Python文件的Ruff、代码形状、git diff --check：exit0；25文件shasum全部OK。
- 复审候选指纹：3e86f667d21da7aac61aaa388fd9f642a233e3d12714ae47ea7a761c074ae4dc。原候选bea7cc...及首轮Important留在原review历史。
- 当前宿主5个相关skill的readlink均指向本仓库，未安装或修改全局配置。
- 等待同一独立reviewer复审；不得由父或worker关闭Finding。

最终独立回执：同reviewer确认FLOW-SR-REV-I-01 fixed并approved，本范围通过、无人工Gate；独立重跑完整416 passed / 11 subtests passed及行为6 passed。该回执不代替本地提交，也不替代其他产品验收。

提交前memory同步后父再次运行完整pytest：416 passed / 11 subtests passed（10.22s，exit0）；staged diff检查通过，暂存范围46文件均属本批。首次沙箱git add被拒绝，按已授权精确范围提权后成功。实现提交27fe2cd的实际message与预先展示一致，提交后工作树干净；未推送，未变更Git全局身份。
