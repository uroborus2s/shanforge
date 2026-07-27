# Review Feedback Triage

## STRATIX-GUIDE-I001

- 反馈来源：human
- severity：Important
- 反馈要求：从真实 Stratix 框架指南和源码重建 skill，覆盖配置、环境、模块和 API 到 Kysely 的完整组织方式。
- 是否清楚：yes
- 是否技术正确：yes
- 证据：
  - 现有 `scaffolds.md` 使用已从配置 schema 移除的 `applicationAutoDI`。
  - 现有配置命令使用源码不支持的 `--key`。
  - 当前 Core 已统一支持原始文本、hex、base64 32-byte key，旧兼容性警告已过期。
  - 现有 Repository 示例没有按 `BaseRepository.query()` 的 `Either` 返回契约解包。
- 处理决定：Fixed
- 验证：`19 passed`；TypeScript syntax/type contract 0 错误；独立评审 `approved / 98 / C0-I0-M0`。

## STRATIX-GUIDE-I002

- 反馈来源：human
- severity：Important
- 反馈要求：框架源码只用于编制统一规范，不能要求每个业务项目读取框架代码。
- 是否清楚：yes
- 是否技术正确：yes
- 证据：
  - `SKILL.md` 把 `source-locations.md` 设为所有任务的首个必读文件。
  - `source-locations.md` 要求业务开发按任务读取框架源码和指南。
  - CLI、runtime、application reference 和 metadata 暴露本机框架路径。
- 处理决定：Fixed（待独立复审）
- 修复：删除 `source-locations.md`；业务项目直接执行已提炼规范；源码调查仅属于 skill 维护 evidence。
- 验证：`19 passed`；Ruff、skill validator、diff check 通过；运行时材料源码路径扫描 0 命中。

### 独立复审 Iteration 1

- 结论：`changes_requested / 92 / C0-I1-M0`
- Finding：测试只扫描顶层 Markdown 和部分源码目录，无法防止嵌套 reference 或其他框架源码路径回归。
- 处理：Fixed
- 修复：递归扫描 `SKILL.md`、`agents/**`、`references/**`，禁止 create/core/forge/database/testing 的 source/template 路径、正式指南路径、本机用户路径和旧回源指令。
- 验证：`19 passed`；Ruff、skill validator、diff check 通过。
- Iteration 2：`approved / 100 / C0-I0-M0`。
