from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SettingsCapabilityEntry:
    """Stable capability-level fact for the base settings layer."""

    capability_id: str
    description: str
    modules: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SettingsDomainEntry:
    """Stable domain-level fact for the base settings layer."""

    domain_id: str
    responsibility: str
    modules: tuple[str, ...]
    capabilities: tuple[SettingsCapabilityEntry, ...]


SETTINGS_LAYER_NAME = "base_settings"

SETTINGS_DOMAINS: tuple[SettingsDomainEntry, ...] = (
    SettingsDomainEntry(
        domain_id="model",
        responsibility="模型与向量供应商适配、模型策略解析支撑。",
        modules=(
            "src/settings/model/mock_provider.py",
            "src/settings/model/openai_provider.py",
            "src/settings/model/anthropic_provider.py",
            "src/settings/model/embedding_provider.py",
            "src/settings/model/registry.py",
        ),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="llm_provider",
                description="封装真实模型供应商差异。",
                modules=(
                    "src/settings/model/mock_provider.py",
                    "src/settings/model/openai_provider.py",
                    "src/settings/model/anthropic_provider.py",
                ),
            ),
            SettingsCapabilityEntry(
                capability_id="embedding_provider",
                description="为后续向量索引和召回能力预留 embedding provider 骨架。",
                modules=("src/settings/model/embedding_provider.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="model_registry",
                description="提供默认模型策略解析与注册表。",
                modules=("src/settings/model/registry.py",),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="memory",
        responsibility=(
            "记忆、证据、蒸馏样本的真实持久化实现，"
            "以及 external augmentation provider。"
        ),
        modules=(
            "src/settings/memory/store.py",
            "src/settings/memory/evidence_store.py",
            "src/settings/memory/dataset_store.py",
            "src/settings/memory/lifecycle_audit_store.py",
            "src/settings/memory/lifecycle_queue_store.py",
            "src/settings/memory/remote_http_metadata.py",
            "src/settings/memory/provider.py",
        ),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="memory_store",
                description="持久化长期记忆记录。",
                modules=("src/settings/memory/store.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="evidence_store",
                description="持久化证据投影。",
                modules=("src/settings/memory/evidence_store.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="memory_dataset_store",
                description="持久化蒸馏样本与晋升决策。",
                modules=("src/settings/memory/dataset_store.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="memory_lifecycle_audit_store",
                description="持久化 lifecycle review/apply 的审计轨迹。",
                modules=("src/settings/memory/lifecycle_audit_store.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="memory_lifecycle_queue_store",
                description="持久化 lifecycle review queue 的 durable 状态。",
                modules=("src/settings/memory/lifecycle_queue_store.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="memory_provider",
                description=(
                    "提供 single external memory augmentation provider "
                    "的本地实现与占位实现。"
                ),
                modules=(
                    "src/settings/memory/remote_http_metadata.py",
                    "src/settings/memory/provider.py",
                ),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="session",
        responsibility="session、artifact、archive、assembly 与检索索引支撑。",
        modules=(
            "src/settings/session/store.py",
            "src/settings/session/artifact_store.py",
            "src/settings/session/blob_store.py",
            "src/settings/session/archive.py",
            "src/settings/session/search_index.py",
            "src/settings/session/vector_index.py",
            "src/settings/session/assembly_store.py",
        ),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="session_store",
                description="持久化会话与事件第一事实源。",
                modules=("src/settings/session/store.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="artifact_store",
                description="持久化会话产物与引用。",
                modules=("src/settings/session/artifact_store.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="blob_store",
                description="为二进制 artifact 与后续附件存储预留 blob store 骨架。",
                modules=("src/settings/session/blob_store.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="session_archive",
                description="聚合 session、event、artifact、assembly explain 的 archive provider。",
                modules=("src/settings/session/archive.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="search_index",
                description="提供 token-based search index 骨架和 archive-backed 入口。",
                modules=("src/settings/session/search_index.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="vector_index",
                description="提供向量索引空实现骨架。",
                modules=("src/settings/session/vector_index.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="assembly_store",
                description="持久化 session assembly snapshot。",
                modules=("src/settings/session/assembly_store.py",),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="skills",
        responsibility="技能目录发现、加载、安装与启停管理。",
        modules=("src/settings/skills/local_provider.py",),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="skill_source",
                description="发现与加载技能文档。",
                modules=("src/settings/skills/local_provider.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="skill_management",
                description="安装、启停和移除技能。",
                modules=("src/settings/skills/local_provider.py",),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="workspace",
        responsibility="工作区、本地文件、shell、git、profile 与 rule source。",
        modules=(
            "src/settings/workspace/local_provider.py",
            "src/settings/workspace/command_provider.py",
            "src/settings/workspace/profile_catalog.py",
            "src/settings/workspace/backend_catalog.py",
            "src/settings/workspace/provider_catalog.py",
            "src/settings/workspace/secret_catalog.py",
            "src/settings/workspace/source_provider.py",
        ),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="workspace_provider",
                description="解析工作区根目录并提供文件系统访问。",
                modules=("src/settings/workspace/local_provider.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="shell_command",
                description="本地 shell 命令执行后端。",
                modules=("src/settings/workspace/command_provider.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="git",
                description="本地 git 执行后端。",
                modules=("src/settings/workspace/command_provider.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="profile_source",
                description="本地 profile source provider。",
                modules=(
                    "src/settings/workspace/profile_catalog.py",
                    "src/settings/workspace/backend_catalog.py",
                    "src/settings/workspace/provider_catalog.py",
                    "src/settings/workspace/source_provider.py",
                ),
            ),
            SettingsCapabilityEntry(
                capability_id="rule_source",
                description="本地 rule source provider。",
                modules=(
                    "src/settings/workspace/profile_catalog.py",
                    "src/settings/workspace/backend_catalog.py",
                    "src/settings/workspace/provider_catalog.py",
                    "src/settings/workspace/source_provider.py",
                ),
            ),
            SettingsCapabilityEntry(
                capability_id="secret_catalog",
                description=(
                    "durable secret catalog 的加载、"
                    "key rotation 与 selection-source 审计。"
                ),
                modules=("src/settings/workspace/secret_catalog.py",),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="approval",
        responsibility="审批后端与 Hermes-backed approval 适配。",
        modules=("src/settings/approval/hermes_policy.py",),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="approval_backend",
                description="审批后端与策略桥接实现。",
                modules=("src/settings/approval/hermes_policy.py",),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="delegation",
        responsibility="委派后端、child digest 持久化与 Hermes-backed transport。",
        modules=(
            "src/settings/delegation/hermes_transport.py",
            "src/settings/delegation/digest_store.py",
        ),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="delegation_backend",
                description="委派 transport/backends 适配。",
                modules=("src/settings/delegation/hermes_transport.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="delegation_digest_store",
                description="子任务 digest 持久化。",
                modules=("src/settings/delegation/digest_store.py",),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="gateway",
        responsibility="外部宿主网关适配和 HTTP client 骨架。",
        modules=(
            "src/settings/gateway/local_gateway.py",
            "src/settings/gateway/hermes_gateway.py",
            "src/settings/gateway/http_client.py",
        ),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="gateway_adapter",
                description="接入外部宿主请求并输出统一响应。",
                modules=(
                    "src/settings/gateway/local_gateway.py",
                    "src/settings/gateway/hermes_gateway.py",
                ),
            ),
            SettingsCapabilityEntry(
                capability_id="http_client",
                description="为外部 HTTP 调用预留 provider 骨架。",
                modules=("src/settings/gateway/http_client.py",),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="capability_registry",
        responsibility="能力注册表与 Hermes-backed registry 适配。",
        modules=(
            "src/settings/capability_registry/registry.py",
            "src/settings/capability_registry/hermes_registry.py",
        ),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="capability_registry",
                description="能力声明、处理器与 Hermes registry 适配。",
                modules=(
                    "src/settings/capability_registry/registry.py",
                    "src/settings/capability_registry/hermes_registry.py",
                ),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="hermes",
        responsibility="Hermes repo bridge 与受控能力探测。",
        modules=("src/settings/hermes/bridge.py",),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="hermes_bridge",
                description="为 Hermes-backed adapters 提供受控文件桥接。",
                modules=("src/settings/hermes/bridge.py",),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="composition",
        responsibility="环境 settings、business bindings 与唯一 composition root。",
        modules=(
            "src/settings/composition/settings.py",
            "src/settings/composition/component_bindings.py",
            "src/settings/composition/container.py",
        ),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="runtime_settings",
                description="解析环境变量和装配配置。",
                modules=("src/settings/composition/settings.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="business_bindings",
                description="业务 ID 到实现对象的绑定层。",
                modules=("src/settings/composition/component_bindings.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="default_container",
                description="唯一默认容器与 composition root。",
                modules=("src/settings/composition/container.py",),
            ),
        ),
    ),
    SettingsDomainEntry(
        domain_id="shared",
        responsibility="层内共享 JSONL、web/browser local bridge、clock 与 id generator。",
        modules=(
            "src/settings/shared/jsonl.py",
            "src/settings/shared/web_provider.py",
            "src/settings/shared/browser_provider.py",
            "src/settings/shared/system_identity.py",
        ),
        capabilities=(
            SettingsCapabilityEntry(
                capability_id="jsonl_shared",
                description="层内共享 JSONL 读写基座。",
                modules=("src/settings/shared/jsonl.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="web_bridge",
                description="本地 web search/document provider。",
                modules=("src/settings/shared/web_provider.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="browser_automation",
                description="本地 browser automation provider。",
                modules=("src/settings/shared/browser_provider.py",),
            ),
            SettingsCapabilityEntry(
                capability_id="clock_identity",
                description="系统时钟和 ID generator provider。",
                modules=("src/settings/shared/system_identity.py",),
            ),
        ),
    ),
)


def list_settings_domains() -> tuple[SettingsDomainEntry, ...]:
    """Return the stable domain list for the base settings layer."""

    return SETTINGS_DOMAINS


def list_settings_capabilities() -> tuple[SettingsCapabilityEntry, ...]:
    """Return the flattened capability list for the base settings layer."""

    return tuple(
        capability
        for domain in SETTINGS_DOMAINS
        for capability in domain.capabilities
    )
