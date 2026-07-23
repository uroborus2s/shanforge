# T02 独立评审输入

## 输入

- Work item：`PROJECT-ARTIFACTS-001`
- Task：`T02 OpenAPI 详细合同`
- task brief：`task-briefs/T02-openapi-contract.md`
- report：`reports/task-2.md`
- evidence：`evidence/task-2.md`
- plan：`plan.md` 及 `reviews/plan-amendment-t02-review.md`

## 评审范围

- `contracts/openapi/openapi.yaml`
- `contracts/schemas/openapi-shanforge-rules.schema.json`
- `src/domain/project_artifacts/validation.py` 的 OpenAPI 规则
- `src/runtime/project_artifacts/yaml_extractor.py`
- `src/settings/project_artifacts/source_registry.py`
- `.factory/project-knowledge/artifact-source-registry.json`
- `src/settings/composition/project_knowledge.py` 的 registry/extractor 装配
- `tests/test_project_artifact_contracts.py` OpenAPI 测试
- `tests/test_project_artifact_extractor.py`
- `docs/05-design/api-design.md`
- `docs/04-product/prd.md` 的七个新增 section marker

## 重点

1. 四条 route 是否与代码精确一致，是否有完整中文字段说明、错误响应和示例。
2. 稳定 API/需求/测试 ID 是否严格、唯一且没有悬空强关系。
3. YAML locator 是否无行号，实体与关系是否确定性。
4. 组合 registry 是否保持严格路径、缓存和 source owner 边界。
5. PRD 只增加 marker、API 文档保持候选，是否没有伪造批准事实。

只读评审，不修改文件、不运行 Git。输出 `approved | changes_requested`、评分和 findings。
