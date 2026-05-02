# Skill Updates Summary

## 2026-05-02

- `skills/crawler4j-model-project/` 已对齐 `crawler4j 0.4.0` 的 `core-native-v2` 模块协议。
- skill 主体、references 与 `agents/openai.yaml` 现统一切到：
  - `crawler4j module init`
  - `interface/component/workflow/page-action/data/candidate/cleanup/page create`
  - `.crawler4j/manifest.lock.json`
  - `check structure/release/full`
  - `package build/verify`
  - `host devlink/install/debug config`
- 已显式标记旧叙事为迁移对象或禁用项：
  - `TaskScript`
  - `TaskFlow`
  - `TaskSpec`
  - `WorkflowSpec`
  - `module_runtime.py`
  - `env_selectors/`
  - `ui_extension`
  - `config_schema.json`
  - `crawler4j init-model`
  - `crawler4j new`
  - `crawler4j add-workflow`
  - `crawler4j add-ui`
- 新版 skill 也补上了宿主边界：目录源码只能走 `host devlink`，正式安装只走 ZIP 或 GitHub `owner/repo`，不把 `.whl` 当模块安装格式。
