from __future__ import annotations

import hashlib
from pathlib import Path

from test_remaining_skill_project_status_contract import (
    PROJECT_CONTRACT_LINK,
    STATUS_FACTS,
    WORK_SKILLS,
    read_skill,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
SHARED_CONTRACT = (
    REPO_ROOT / "skills" / "using-shanforge" / "references" / "work-skill-return-contract.md"
)

PROFESSIONAL_PREFIX_SHA256 = {
    "agent-harness-construction": (
        "b97365a4385adcab3d0a85a0240b2df406fd3beb51cebede56563263d3545c43"
    ),
    "ai-first-engineering": "22a546be3ca4e7ccb97405de71aa5594ad6b1908600cbd0818eecc96a2bc35a6",
    "ai-regression-testing": "42aa8be6d43006f4b51a7410473b7e74cce80036e131da85b23b586cb53b4652",
    "algorithmic-art": "ef87545fc2aafe4811dee1f41fdeaf28abd195c654ccb24d36b4b65a94c96d2f",
    "api-design": "0085634f9ad8898d2ef7f388fb37312a111226ada41dfb5cf9cb271a495fa4d2",
    "art-asset-pipeline": "3073885a3861284b7e207edaa6f852ad23e96b7f173698156afc56ef8770ca89",
    "article-writing": "244f51d8545284d0115bd7b93d15b45cb71d56070e1dec368914f2eaddc5f47d",
    "brainstorming": "2a9d176af74058691682c1509f07232e369abc550f68e5ed0f31d94307a01687",
    "browser-control": "363c9fb1d83714576a4d9f788c6cb19b620b49c236a2c31bdc95b824eaba2cdc",
    "crawler4j-model-project": "3e0fff07dd04b25c67e492bc5cd444db230ada45f1ed8290ba7b0780e77ec8d3",
    "doc-coauthoring": "be0834078b4081e84e006dfba245d472bab2e07fac7782cef5c59c432253e223",
    "document-templates": "8d24359ca61c6bf23aebd30168ecfa4ddca5137cf4d0d07ec56bb1e8af36eee4",
    "docx": "4c0902897179193845cd2e3e2772047bdf17ed4fa5d6f33dd58919a1626220e8",
    "frontend-patterns": "577d8a43d0f5783ff88ef30f51639db5b8c88bf64855a9902b0ba09c257aa727",
    "gitcommitzh": "f8ddcf2b910ff6a3e37118cf660ad4eb7098473943a51e0ed35f61d7a85e8751",
    "go-backend-developer": "9e7e4e7c3e598367d91ca7e10baa4be37784417d345603163f64490ee2b33da8",
    "humanizer": "2a5b0a33077aafda23e54e46577a0bf964ad22c7a7f0c939f350bdd8d2e88557",
    "java-developer": "a299f7ea659a3f1b00809835aa2affe6fa9c9346b15902a6dd9d5a5b35acfa62",
    "pdf": "9ac28dc422d7ccd697e7ef5612979b32bae6eb01e5088e9112fc66ee60107085",
    "python-uv-project": "d5543a107ec6b793aca69f84bf3fba452d31f622da9713300c7c907ae4010d69",
    "receiving-code-review": "bcb549457979f8f1297f6a1651b2bd3e6b6fe47ea2de3ab91ee2e9758169fd0f",
    "requirements-engineering": "992c25aab74397b6d6ebd78a54c7db1fb1b86fa74f1782860264e1a055898408",
    "shadcn": "0cba439d7e48e9d6f2b805379129ef06d835286bda44a2eee280578f13b07b23",
    "skill-creator": "9d26d5b7655215911732d79ca6301cbdb239c8fcfdaea82d76d66ae0fb1f8b9a",
    "stratix-admin-web": "2a35b86d6681d1c934e680fb94d8c894f80daf4060289d964df06379588f93f6",
    "stratix-service": "3e9c5ad0837a2667d574790f29367d80a93b26c4fd60bfaca1fb16ab0419c08d",
    "systematic-debugging": "d55a7d6ba2ab071f27b9502e8ef55708d615360bac1e9a79c0b9f7e690a49741",
    "tdd-workflow": "889c73ca45da361f5275311e5897010acbb39be9c53ccff60d4e508064b817c6",
    "ui-ux-pro-max": "03034d023923f4fb7448e643532af1f1f7302b55f7b00321b4e00e4dd998c2f2",
    "webapp-testing": "dfba94b7e9486c898bada2f3a85c4946ee012cb85f03560cfff2404d2e1ec03f",
    "writing-plans": "33bea287ef47b3f30e68b89445d90825d6be24b708faec3ecc1bacc64bf4474a",
    "xlsx": "109bf2bd5b00710a152d6638d0cb815c12b66afb854acec78bef52f3df6a0ca9",
}


def test_professional_prefixes_are_unchanged_for_exactly_32_work_skills() -> None:
    assert set(PROFESSIONAL_PREFIX_SHA256) == WORK_SKILLS

    # Keep the trailing newline that preceded the removed heading in the frozen prefix.
    separator = f"\n{PROJECT_CONTRACT_LINK}"
    for name in sorted(WORK_SKILLS):
        skill = read_skill(name)
        assert skill.count(separator) == 1, name
        professional_prefix = skill.split(separator, maxsplit=1)[0]
        digest = hashlib.sha256(professional_prefix.encode()).hexdigest()
        assert digest == PROFESSIONAL_PREFIX_SHA256[name], name


def test_shared_contract_separates_local_results_from_project_envelope() -> None:
    contract = SHARED_CONTRACT.read_text(encoding="utf-8")

    assert "task_id/task_type 表示正式任务身份" in contract
    assert "skill 表示执行者身份" in contract
    assert "不得统一或改写工作 Skill 的既有专业输出" in contract
    assert "工作 Skill 本职结果包" in contract
    assert "项目状态信封" in contract
    assert "direct_answer" in contract
    assert "lightweight_analysis" in contract
    for fact in STATUS_FACTS:
        assert contract.count(fact) == 1


def test_using_shanforge_is_the_project_envelope_owner() -> None:
    controller = read_skill("using-shanforge")
    section = controller.split("## 工作 skill 状态回写协议", maxsplit=1)[1]
    section = section.split("\n## ", maxsplit=1)[0]
    work_result = section.split("项目状态信封：", maxsplit=1)[0]
    project_envelope = section.split("项目状态信封：", maxsplit=1)[1]

    assert "references/work-skill-return-contract.md" in section
    assert "工作 Skill 本职结果包：" in work_result
    for field in ("project_position", "completion_level", "stop_reason", "scope_remaining"):
        assert field not in work_result
        assert field in project_envelope
    assert "next_required_action" in project_envelope


def test_local_status_and_needs_are_forwarded_without_normalization() -> None:
    controller = read_skill("using-shanforge")
    contract = SHARED_CONTRACT.read_text(encoding="utf-8")
    formal_design = (REPO_ROOT / "docs" / "05-design" / "workflow-execution-design.md").read_text(
        encoding="utf-8"
    )
    formal_package = formal_design.split("## 统一任务包", maxsplit=1)[1]
    formal_package = formal_package.split("\n## 六类任务", maxsplit=1)[0]

    for owner_contract in (controller, contract, formal_package):
        assert "status: <该 Skill 的既有本地状态>" in owner_contract
        assert "needs: <该 Skill 的既有本地 needs>" in owner_contract

    representative_local_contracts = {
        "api-design": (
            "status: passed | partial | failed | blocked",
            "none | product_decision | compatibility_review | tests | human_confirmation",
        ),
        "systematic-debugging": (
            "status: root_cause_found | blocked | needs_user_input",
            "human_confirmation | more_information | more_diagnostics | architecture_decision",
        ),
        "writing-plans": (
            "status: ready_for_review | blocked | needs_user_input",
            "plan_review | human_confirmation | none",
        ),
    }
    for name, local_fields in representative_local_contracts.items():
        skill = read_skill(name)
        for local_field in local_fields:
            assert local_field in skill


def test_shared_contract_is_markdown_not_a_runtime_skill_manager() -> None:
    assert SHARED_CONTRACT.suffix == ".md"
    assert not (REPO_ROOT / "src" / "runtime" / "skills").exists()
    assert not (REPO_ROOT / "src" / "settings" / "skills").exists()
