# Review Fix Verification

## RED

```text
.venv/bin/pytest -q tests/test_stratix_service_framework_guide.py tests/test_stratix_service_skill.py
4 failed, 15 passed
```

失败项覆盖源码清单仍存在、CLI 暴露框架仓库、主 skill 要求回源和 metadata 依赖 installed sources。

## GREEN

```text
.venv/bin/pytest -q \
  tests/test_stratix_service_framework_guide.py \
  tests/test_stratix_service_skill.py \
  tests/test_remaining_skill_project_status_contract.py::test_all_work_skills_reference_the_shared_return_contract_once
20 passed in 0.03s

.venv/bin/ruff check tests/test_stratix_service_framework_guide.py tests/test_stratix_service_skill.py
All checks passed!

.venv/bin/python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/stratix-service
Skill is valid!
```

运行时 `SKILL.md`、metadata 和 references 扫描本机框架路径、`source-locations.md` 及框架源码目录：0 命中。`git diff --check` 通过。

复审前补充诊断发现主 Skill 末行被缩短后不再匹配共享回写合同；恢复标准完整句并同步
冻结专业前缀哈希后，共享合同节点通过。

## 独立复审修复

Iteration 1 为 `changes_requested / 92 / C0-I1-M0`：原测试未递归扫描，也未覆盖全部框架源码类别。

修复后递归扫描 `SKILL.md`、`agents/**`、`references/**`，并禁止：

- 任意 `/Users/` 路径。
- create/core/forge/database/testing 的 `src` 或 `templates` 路径。
- 框架开发指南路径。
- 旧 source-locations 和业务回源指令。

定向回归仍为 `19 passed`，Ruff、skill validator、diff check 通过。

独立复审 Iteration 2：`approved / 100 / C0-I0-M0`。

## 相邻合同

- `stratix-service` professional prefix SHA-256 已更新并精确校验为 `0e19177531b04f8d56fd19756fa3b18bf3cdee91822620e351ca7aa62dc89c55`。
- `tests/test_work_skill_status_envelope_ownership.py` 全文件仍有 2 个范围外失败：`receiving-code-review` 的并行 hash 漂移、`writing-plans` 的并行本地状态契约漂移；本任务未修改这两个 skill。

## STRATIX-GUIDE-I003

RED：

```text
.venv/bin/pytest -q tests/test_stratix_service_framework_guide.py tests/test_stratix_service_skill.py
2 failed, 17 passed
```

GREEN：

```text
.venv/bin/pytest -q \
  tests/test_stratix_service_framework_guide.py \
  tests/test_stratix_service_skill.py \
  tests/test_remaining_skill_project_status_contract.py \
  tests/test_work_skill_status_envelope_ownership.py
28 passed
```

- Skill validator：通过。
- Ruff：通过。
- 独立复审：`approved / 100 / C0-I0-M0`。
- `stratix-service` 专业内容 SHA-256：`c19274fd17d0fc04f992e64679fe7fee9369f1dd6d24e41169353b5ec3b1630c`。
- 通用治理尾注、维护期源码说明和 `work item evidence` 在 `stratix-service/SKILL.md` 中均为 0 命中。
