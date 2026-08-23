# SKILL-FULL-OPTIMIZATION-001 Brief

## 目标

对仓库当前 38 个 `skills/*/SKILL.md` 逐项审计、按真实问题优化、运行单项与全量验证，并由独立 reviewer 为每个 Skill 给出可追溯的 100 分制评分。

## 非目标

- 不为追求改动数量而重写已经合格的 Skill。
- 不新增中心注册表、平台运行时、第三方依赖或整文件 SHA 快照。
- 不修改历史审计快照，不执行 push、PR、merge、发布或部署。

## 用户意图

- 用户明确要求“全量逐 Skill 优化评分”。
- “全量”表示当前文件系统动态发现的全部 Skill，不复用上一轮 P0 批次分数代替单项分数。

## 方案比较

1. **分组实施、单项计分、集中独立终审（采用）**：38 个 Skill 逐项形成基线和结果，按职责分批优化，最后由同一独立 reviewer 输出 38 张单项 scorecard；既保证可比性，也避免 38 次重复 gate。
2. **每个 Skill 单独建立 WorkItem 和 reviewer**：隔离最强，但会制造大量重复 ledger、review 和 memory，违背当前批次集中收口规则。
3. **只用自动指标评分**：速度快，但行数、标题数和 validator 不能证明触发边界、工作流和错误语义正确，不能满足“独立评分”。

## 已批准方案

采用方案 1。用户已明确授权全量逐 Skill 优化评分；评分沿用项目现有独立 review 五维 100 分制，并在 Skill 语境下解释：

- 需求符合度 30：触发描述、适用/排除范围、专业任务结果是否准确。
- 架构一致性 20：skill-first、职责 owner、授权边界和 progressive disclosure 是否正确。
- 测试充分性 20：validator、行为/不变量测试和适用的 forward test 是否足够。
- 代码质量 20：指令是否简洁、可执行、无重复与投机性抽象；脚本/引用是否必要且可维护。
- 文档与记忆同步 10：引用可达、合同一致、必要项目事实和评分证据是否同步。

每个 Skill 的通过线为 `>=90 / C0-I0`。低于 90、存在 Critical/Important、validator 失败或真实行为缺口时必须整改；没有问题的 Skill 记录 `no_change_required`，不得为制造 diff 而改写。

## 成功标准

- 38/38 Skill 都有基线审计、必要优化、验证结果和独立单项评分。
- 每个 Skill 的评分包含维度分、Critical/Important/Minor、优化状态与证据路径。
- 无 Critical/Important 残留；未修改项必须记录“无需修改”的证据，而不是默认视为优化完成。
- 完整 pytest、Ruff、38 个 Skill validator、JSON/JSONL 与 Git hygiene 通过。

## 当前状态

`ready_for_commit`
