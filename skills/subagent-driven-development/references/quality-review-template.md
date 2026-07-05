# Quality Review

只在 Spec Review 通过后执行。目标是确认实现质量、测试、架构和维护性。

## Inputs

- Task brief：
- Spec Review：
- Implementer report：
- evidence：
- diff：
- 测试结果：

## 检查项

- 测试是否覆盖行为，而不是只覆盖 mock。
- 是否遵守 TDD 和任务验证要求。
- 是否符合分层、接口 owner 和禁止耦合规则。
- 是否每个文件职责清晰，接口明确。
- 是否有不必要抽象、过度设计或未请求功能。
- 是否存在错误处理、边界条件或可维护性风险。
- 是否需要补文档或 `.factory/memory/`。

## Severity

- `Critical`：会导致错误行为、数据风险、安全风险或任务不能用。
- `Important`：会带来明显维护、测试、架构或回归风险。
- `Minor`：不阻塞，但值得记录。

## 输出格式

```markdown
## Quality Review

**Assessment:** approved | changes_requested

**Strengths:**
- <真实优点>

**Issues:**
- [Critical][file:line] <问题> - <影响>
- [Important][file:line] <问题> - <影响>
- [Minor][file:line] <问题> - <影响>
```

有 `Critical` 或 `Important` 时必须 `changes_requested`。修复后重新 review。
