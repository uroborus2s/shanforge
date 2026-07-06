from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_CREATOR = REPO_ROOT / "skills" / "skill-creator" / "SKILL.md"


def test_skill_creator_requires_chinese_skill_authoring_principles() -> None:
    content = SKILL_CREATOR.read_text(encoding="utf-8")

    for phrase in (
        "所有项目内 skill 默认使用中文",
        "用户可见文本必须中文",
        "丰富经验的中文语言专家和 prompt 专家",
        "中文表达使用短句",
        "完整保留原文所有含义",
        "不得为了省 token 删除流程控制语义",
        "含义保留清单",
        "工具名、命令名、路径、文件名、API 名和代码标识符保留原文",
    ):
        assert phrase in content


def test_skill_creator_requires_isolated_review_loop() -> None:
    content = SKILL_CREATOR.read_text(encoding="utf-8")

    for phrase in (
        "改写者不能批准自己的 skill",
        "作者自检只能把状态推进到 `ready_for_review`",
        "交给独立 reviewer",
        "`approved` / `changes_requested`",
        "直到评审和验证通过",
        "评估时必须保持“作者 / 裁判”隔离",
    ):
        assert phrase in content


def test_skill_creator_keeps_references_and_helper_code_boundaries() -> None:
    content = SKILL_CREATOR.read_text(encoding="utf-8")

    for phrase in (
        "helper code 可以放入该 skill 自己的 `scripts/`",
        "`SKILL.md` 必须写清输入、输出、触发、失败语义和风险边界",
        "文档模板、schema、rubric、评审表和长背景放入 `references/`",
        "禁止把全局中心脚本、隐藏执行器或仓库级 CLI 当成 skill 流程主控",
        "skill 是流程入口，helper code 只是 skill 内部工具",
    ):
        assert phrase in content
