# Review Response

## STRATIX-GUIDE-I002

- disposition：Fixed
- 修改：
  - 删除 `references/source-locations.md`。
  - `SKILL.md` 改为业务项目直接遵循 bundled norms，不读取框架源码。
  - 从 application、runtime、CLI 和 OpenAI metadata 移除本机源码路径及回源要求。
  - 回归测试新增运行时材料不得泄漏源码调查流程的断言。
  - 保留标准工作 Skill 回写合同句，并同步 `stratix-service` 候选哈希。
- 验证：见 `../evidence/review-fix-verification.md`。

## Independent Review I1

- disposition：Fixed
- 修改：源码泄漏检查改为递归扫描全部运行时 skill 材料，并覆盖全部已知框架源码、模板、指南路径类别和旧回源指令。
- 验证：`19 passed`；Ruff、skill validator、diff check 通过。

## STRATIX-GUIDE-I003

- disposition：Fixed
- 修改：
  - 删除 `stratix-service` 的通用工作 Skill 回写合同尾注。
  - 将维护过程说明替换为五个框架包的精确适用版本。
  - 共享测试不再强制专业 Skill 内嵌治理尾注，但仍禁止重复引用，并保留项目状态信封唯一 owner 与专业内容哈希检查。
- 验证：`28 passed`；独立复审 `approved / 100 / C0-I0-M0`。
