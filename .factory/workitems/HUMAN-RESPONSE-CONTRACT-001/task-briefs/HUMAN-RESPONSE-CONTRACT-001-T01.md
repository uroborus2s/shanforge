# HUMAN-RESPONSE-CONTRACT-001-T01 三段式响应合同

## 状态

`approved_for_implementation`

## 目标

以最小改动把用户批准的三段式人类响应合同写入流程主控，并用静态契约测试锁定“无需回复继续执行”的语义。

## 输入

- 用户批准：三段式人类响应合同作为下一项正式修改实施。
- 工作项简报：`.factory/workitems/HUMAN-RESPONSE-CONTRACT-001/brief.md`

## 允许修改

- `skills/using-shanforge/SKILL.md`
- `tests/test_skill_progress_visibility_and_continuation.py`
- `.factory/workitems/HUMAN-RESPONSE-CONTRACT-001/**`

## 禁止修改

- `skills/project-memory/SKILL.md`
- PM 页面和 SQLite 投影实现。
- 其他工作项及用户已有脏改动。
- Git 远端、部署和外部系统。

## 验证

```bash
uv run pytest -q tests/test_skill_progress_visibility_and_continuation.py
uv run ruff check tests/test_skill_progress_visibility_and_continuation.py
git diff --check -- skills/using-shanforge/SKILL.md tests/test_skill_progress_visibility_and_continuation.py .factory/workitems/HUMAN-RESPONSE-CONTRACT-001
```

## 完成口径

- 实现者只能推进到 `ready_for_review`。
- 独立评审和关闭前新鲜验证通过后才能关闭。
