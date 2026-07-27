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
