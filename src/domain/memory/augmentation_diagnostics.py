from __future__ import annotations

from typing import Any, Mapping

_CANONICAL_AUGMENTATION_INPUT_KEYS = frozenset(
    {
        "provider_id",
        "memory_provider_id",
        "namespace",
        "writable",
        "memory_provider_writable",
        "prefetch_present",
        "prefetch_chars",
        "external_memory_block_present",
        "query_terms",
        "source_breakdown",
        "result_truncated",
        "budget_trace",
        "rank_trace",
        "hit_provenance",
        "contract_trace",
        "access_trace",
        "writeback_trace",
    }
)

_LEGACY_AUGMENTATION_INPUT_KEYS = frozenset(
    {
        "state_root",
        "hit_count",
        "hit_ids",
        "query_text_present",
        "request_header_names",
        "auth_kind",
        "response_keys",
        "signature_key_id",
        "signature_key_selection_source",
        "bearer_token_id",
        "bearer_token_selection_source",
        "secret_catalog_source_path",
        "timeout_seconds",
        "max_retries",
        "retry_status_codes",
        "retry_backoff_seconds",
        "attempt_count",
        "status_code",
        "response_validation_error",
        "writeback_enabled",
        "writeback_reports",
    }
)

_STORED_AUGMENTATION_INPUT_KEYS = (
    _CANONICAL_AUGMENTATION_INPUT_KEYS | _LEGACY_AUGMENTATION_INPUT_KEYS
)


def normalize_augmentation_diagnostics(
    diagnostics: Mapping[str, Any] | None,
    *,
    contract_metadata: Mapping[str, Any] | None = None,
    backfill_legacy_aliases: bool = True,
) -> dict[str, Any]:
    """Normalize augmentation diagnostics around trace-first explainability."""

    normalized = dict(diagnostics or {})
    metadata = dict(contract_metadata or {})

    contract_trace = _merge_trace(
        normalized.get("contract_trace"),
        _synthesize_contract_trace(normalized, metadata),
    )
    if contract_trace:
        normalized["contract_trace"] = contract_trace

    access_trace = _merge_trace(
        normalized.get("access_trace"),
        _synthesize_access_trace(normalized),
    )
    if access_trace:
        normalized["access_trace"] = access_trace

    writeback_trace = _merge_trace(
        normalized.get("writeback_trace"),
        _synthesize_writeback_trace(normalized),
    )
    writeback_trace = _normalize_writeback_trace_fields(writeback_trace)
    if writeback_trace:
        normalized["writeback_trace"] = writeback_trace

    budget_trace = _merge_trace(
        normalized.get("budget_trace"),
        _synthesize_budget_trace(normalized),
    )
    if budget_trace:
        normalized["budget_trace"] = budget_trace

    if backfill_legacy_aliases:
        _backfill_contract_aliases(normalized, contract_trace)
        _backfill_access_aliases(normalized, access_trace)
        _backfill_writeback_aliases(normalized, writeback_trace)
        _backfill_budget_aliases(normalized, budget_trace)
    return normalized


def compact_augmentation_diagnostics(
    diagnostics: Mapping[str, Any] | None,
    *,
    contract_metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Drop legacy top-level aliases when the same facts already live in traces."""

    compacted = normalize_augmentation_diagnostics(
        diagnostics,
        contract_metadata=contract_metadata,
        backfill_legacy_aliases=False,
    )
    _drop_contract_aliases(compacted, compacted.get("contract_trace"))
    _drop_access_aliases(compacted, compacted.get("access_trace"))
    _drop_writeback_aliases(compacted, compacted.get("writeback_trace"))
    _drop_budget_aliases(compacted, compacted.get("budget_trace"))
    return compacted


def project_preview_augmentation_diagnostics(
    diagnostics: Mapping[str, Any] | None,
    *,
    contract_metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Project preview diagnostics as canonical trace-first fields only."""

    projected = compact_augmentation_diagnostics(
        diagnostics,
        contract_metadata=contract_metadata,
    )
    projected.pop("legacy_aliases", None)
    return projected


def project_stored_augmentation_diagnostics(
    diagnostics: Mapping[str, Any] | None,
    *,
    contract_metadata: Mapping[str, Any] | None = None,
    provider_id: str | None = None,
    binding_metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Project stored diagnostics into a compact canonical form for replay."""

    if not isinstance(diagnostics, Mapping):
        return {}
    resolved_provider_id = (
        str(
            provider_id
            or diagnostics.get("provider_id")
            or diagnostics.get("memory_provider_id")
            or ""
        )
        or None
    )
    projected = {
        str(key): value
        for key, value in diagnostics.items()
        if str(key) in _STORED_AUGMENTATION_INPUT_KEYS
    }
    if resolved_provider_id is not None and "provider_id" not in projected:
        projected["provider_id"] = resolved_provider_id
    projected = _merge_access_defaults(
        projected,
        provider_id=resolved_provider_id,
        binding_metadata=binding_metadata,
    )
    projected_contract_metadata = _merge_contract_metadata(
        _provider_contract_defaults(resolved_provider_id),
        contract_metadata,
    )
    normalized = normalize_augmentation_diagnostics(
        projected,
        contract_metadata=projected_contract_metadata,
    )
    return compact_augmentation_diagnostics(
        normalized,
        contract_metadata=projected_contract_metadata,
    )


def _synthesize_contract_trace(
    diagnostics: Mapping[str, Any],
    contract_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    trace = {
        "bridge_kind": contract_metadata.get("bridge_kind") or diagnostics.get("bridge_kind"),
        "provider_kind": contract_metadata.get("provider_kind")
        or diagnostics.get("provider_kind"),
        "storage_kind": contract_metadata.get("storage_kind") or diagnostics.get("storage_kind"),
        "retrieval_kind": contract_metadata.get("retrieval_kind")
        or diagnostics.get("retrieval_kind"),
        "contract_ready": contract_metadata.get("contract_ready")
        if contract_metadata.get("contract_ready") is not None
        else diagnostics.get("contract_ready"),
        "response_contract": contract_metadata.get("response_contract")
        or diagnostics.get("response_contract"),
        "response_contract_source": contract_metadata.get("response_contract_source")
        or diagnostics.get("response_contract_source"),
        "response_keys": diagnostics.get("response_keys"),
        "response_validation_error": diagnostics.get("response_validation_error"),
    }
    return _compact_trace_mapping(trace)


def _provider_contract_defaults(provider_id: str | None) -> dict[str, Any]:
    provider_text = str(provider_id or "").strip()
    if provider_text == "none":
        return {
            "bridge_kind": "local",
            "contract_ready": True,
            "provider_kind": "null",
        }
    if provider_text == "in_memory":
        return {
            "bridge_kind": "local",
            "contract_ready": True,
            "provider_kind": "augmentation",
        }
    if provider_text == "jsonl":
        return {
            "bridge_kind": "local",
            "contract_ready": True,
            "provider_kind": "augmentation",
            "storage_kind": "jsonl",
            "retrieval_kind": "snapshot",
        }
    if provider_text == "jsonl_vector":
        return {
            "bridge_kind": "local",
            "contract_ready": True,
            "provider_kind": "augmentation",
            "storage_kind": "jsonl",
            "retrieval_kind": "vector",
        }
    if provider_text == "remote_http":
        return {
            "bridge_kind": "remote",
            "contract_ready": True,
            "provider_kind": "augmentation",
            "retrieval_kind": "remote_http",
            "response_contract": "remote_memory_prefetch_v1",
            "response_contract_source": "built-in",
        }
    return {}


def _merge_contract_metadata(
    defaults: Mapping[str, Any],
    overrides: Mapping[str, Any] | None,
) -> dict[str, Any]:
    merged = dict(defaults)
    for key, value in dict(overrides or {}).items():
        merged[str(key)] = value
    return merged


def _merge_access_defaults(
    diagnostics: dict[str, Any],
    *,
    provider_id: str | None,
    binding_metadata: Mapping[str, Any] | None,
) -> dict[str, Any]:
    merged = dict(diagnostics)
    metadata = dict(binding_metadata or {})
    provider_text = str(provider_id or "").strip()
    if provider_text == "remote_http" and "endpoint_url" not in merged:
        endpoint_url = metadata.get("recall_endpoint_url") or metadata.get("endpoint_url")
        if endpoint_url not in (None, ""):
            merged["endpoint_url"] = endpoint_url
    return merged


def _synthesize_access_trace(diagnostics: Mapping[str, Any]) -> dict[str, Any]:
    access_ref = diagnostics.get("endpoint_url") or diagnostics.get("state_root")
    if access_ref in (None, ""):
        return {}
    access_kind = (
        "endpoint_url"
        if diagnostics.get("endpoint_url") not in (None, "")
        else "state_root"
    )
    trace = {
        "access_kind": access_kind,
        "access_ref": access_ref,
        "attempt_count": diagnostics.get("attempt_count"),
        "auth_kind": diagnostics.get("auth_kind"),
        "request_header_names": diagnostics.get("request_header_names"),
        "signature_key_id": diagnostics.get("signature_key_id"),
        "signature_key_selection_source": diagnostics.get("signature_key_selection_source"),
        "bearer_token_id": diagnostics.get("bearer_token_id"),
        "bearer_token_selection_source": diagnostics.get("bearer_token_selection_source"),
        "secret_catalog_source_path": diagnostics.get("secret_catalog_source_path"),
        "timeout_seconds": diagnostics.get("timeout_seconds"),
        "max_retries": diagnostics.get("max_retries"),
        "retry_status_codes": diagnostics.get("retry_status_codes"),
        "retry_backoff_seconds": diagnostics.get("retry_backoff_seconds"),
        "status_code": diagnostics.get("status_code"),
    }
    return _compact_trace_mapping(trace)


def _synthesize_writeback_trace(diagnostics: Mapping[str, Any]) -> dict[str, Any]:
    existing_trace = diagnostics.get("writeback_trace")
    reports = diagnostics.get("writeback_reports")
    if not isinstance(reports, Mapping) and isinstance(existing_trace, Mapping):
        reports = existing_trace.get("detail_reports")
    if not isinstance(reports, Mapping) and isinstance(existing_trace, Mapping):
        reports = existing_trace.get("reports")
    enabled = diagnostics.get("writeback_enabled")
    if enabled is None and isinstance(existing_trace, Mapping):
        enabled = existing_trace.get("enabled")
    configured = diagnostics.get("writeback_enabled")
    if configured is None and isinstance(existing_trace, Mapping):
        configured = existing_trace.get("configured")
    session_writable = diagnostics.get("writable")
    if session_writable is None and isinstance(existing_trace, Mapping):
        session_writable = existing_trace.get("session_writable")
    supported = True
    if isinstance(existing_trace, Mapping) and "supported" in existing_trace:
        supported = bool(existing_trace.get("supported"))
    if not isinstance(reports, Mapping) and enabled is None and not isinstance(
        existing_trace,
        Mapping,
    ):
        return {}
    trace = {
        "supported": supported,
        "configured": configured,
        "session_writable": session_writable,
        "enabled": enabled,
        "detail_reports": dict(reports) if isinstance(reports, Mapping) else {},
        "successes": _writeback_report_field_map(reports, "success"),
        "failure_policies": _writeback_report_field_map(reports, "failure_policy"),
        "response_oks": _writeback_report_field_map(reports, "response_ok"),
        "response_statuses": _writeback_report_field_map(reports, "response_status"),
        "response_messages": _writeback_report_field_map(reports, "response_message"),
        "response_report_ids": _writeback_report_field_map(
            reports,
            "response_report_id",
        ),
        "response_validation_errors": _writeback_report_field_map(
            reports,
            "response_validation_error",
        ),
    }
    return _compact_trace_mapping(trace)


def _synthesize_budget_trace(diagnostics: Mapping[str, Any]) -> dict[str, Any]:
    hit_ids = diagnostics.get("hit_ids")
    if isinstance(hit_ids, tuple):
        selected_hit_ids = tuple(str(hit_id) for hit_id in hit_ids)
    elif isinstance(hit_ids, list):
        selected_hit_ids = tuple(str(hit_id) for hit_id in hit_ids)
    else:
        selected_hit_ids = ()
    selected_hit_count = diagnostics.get("hit_count")
    if selected_hit_count is None and selected_hit_ids:
        selected_hit_count = len(selected_hit_ids)
    trace = {
        "selected_hit_count": selected_hit_count,
        "selected_hit_ids": selected_hit_ids,
        "query_text_present": diagnostics.get("query_text_present"),
    }
    return _compact_trace_mapping(trace)


def _backfill_contract_aliases(
    diagnostics: dict[str, Any],
    contract_trace: Mapping[str, Any] | object,
) -> None:
    if not isinstance(contract_trace, Mapping):
        return
    for key in (
        "bridge_kind",
        "provider_kind",
        "storage_kind",
        "retrieval_kind",
        "response_contract",
        "response_contract_source",
        "response_keys",
        "response_validation_error",
    ):
        if key not in diagnostics and key in contract_trace:
            diagnostics[key] = contract_trace[key]


def _backfill_access_aliases(
    diagnostics: dict[str, Any],
    access_trace: Mapping[str, Any] | object,
) -> None:
    if not isinstance(access_trace, Mapping):
        return
    access_kind = str(access_trace.get("access_kind") or "")
    access_ref = access_trace.get("access_ref")
    if (
        access_kind == "endpoint_url"
        and "endpoint_url" not in diagnostics
        and access_ref is not None
    ):
        diagnostics["endpoint_url"] = access_ref
    if access_kind == "state_root" and "state_root" not in diagnostics and access_ref is not None:
        diagnostics["state_root"] = access_ref
    for key in (
        "attempt_count",
        "auth_kind",
        "request_header_names",
        "signature_key_id",
        "signature_key_selection_source",
        "bearer_token_id",
        "bearer_token_selection_source",
        "secret_catalog_source_path",
        "timeout_seconds",
        "max_retries",
        "retry_status_codes",
        "retry_backoff_seconds",
        "status_code",
    ):
        if key not in diagnostics and key in access_trace:
            diagnostics[key] = access_trace[key]


def _backfill_writeback_aliases(
    diagnostics: dict[str, Any],
    writeback_trace: Mapping[str, Any] | object,
) -> None:
    if not isinstance(writeback_trace, Mapping):
        return
    if "writeback_enabled" not in diagnostics and "enabled" in writeback_trace:
        diagnostics["writeback_enabled"] = writeback_trace["enabled"]
    if "writeback_reports" not in diagnostics:
        if "detail_reports" in writeback_trace:
            diagnostics["writeback_reports"] = writeback_trace["detail_reports"]
        elif "reports" in writeback_trace:
            diagnostics["writeback_reports"] = writeback_trace["reports"]


def _backfill_budget_aliases(
    diagnostics: dict[str, Any],
    budget_trace: Mapping[str, Any] | object,
) -> None:
    if not isinstance(budget_trace, Mapping):
        return
    if "hit_count" not in diagnostics and "selected_hit_count" in budget_trace:
        diagnostics["hit_count"] = budget_trace["selected_hit_count"]
    if "hit_ids" not in diagnostics and "selected_hit_ids" in budget_trace:
        diagnostics["hit_ids"] = budget_trace["selected_hit_ids"]
    if "query_text_present" not in diagnostics and "query_text_present" in budget_trace:
        diagnostics["query_text_present"] = budget_trace["query_text_present"]


def _drop_contract_aliases(
    diagnostics: dict[str, Any],
    contract_trace: Mapping[str, Any] | object,
) -> None:
    if not isinstance(contract_trace, Mapping):
        return
    for key in (
        "bridge_kind",
        "provider_kind",
        "storage_kind",
        "retrieval_kind",
        "response_contract",
        "response_contract_source",
        "response_keys",
        "response_validation_error",
    ):
        if key in diagnostics and diagnostics.get(key) == contract_trace.get(key):
            diagnostics.pop(key, None)


def _drop_access_aliases(
    diagnostics: dict[str, Any],
    access_trace: Mapping[str, Any] | object,
) -> None:
    if not isinstance(access_trace, Mapping):
        return
    access_kind = str(access_trace.get("access_kind") or "")
    access_ref = access_trace.get("access_ref")
    if access_kind == "endpoint_url" and diagnostics.get("endpoint_url") == access_ref:
        diagnostics.pop("endpoint_url", None)
    if access_kind == "state_root" and diagnostics.get("state_root") == access_ref:
        diagnostics.pop("state_root", None)
    for key in (
        "attempt_count",
        "auth_kind",
        "request_header_names",
        "signature_key_id",
        "signature_key_selection_source",
        "bearer_token_id",
        "bearer_token_selection_source",
        "secret_catalog_source_path",
        "timeout_seconds",
        "max_retries",
        "retry_status_codes",
        "retry_backoff_seconds",
        "status_code",
    ):
        if key in diagnostics and diagnostics.get(key) == access_trace.get(key):
            diagnostics.pop(key, None)


def _drop_writeback_aliases(
    diagnostics: dict[str, Any],
    writeback_trace: Mapping[str, Any] | object,
) -> None:
    if not isinstance(writeback_trace, Mapping):
        return
    if diagnostics.get("writeback_enabled") == writeback_trace.get("enabled"):
        diagnostics.pop("writeback_enabled", None)
    detail_reports = writeback_trace.get("detail_reports", writeback_trace.get("reports"))
    if diagnostics.get("writeback_reports") == detail_reports:
        diagnostics.pop("writeback_reports", None)


def _drop_budget_aliases(
    diagnostics: dict[str, Any],
    budget_trace: Mapping[str, Any] | object,
) -> None:
    if not isinstance(budget_trace, Mapping):
        return
    if diagnostics.get("hit_count") == budget_trace.get("selected_hit_count"):
        diagnostics.pop("hit_count", None)
    if diagnostics.get("hit_ids") == budget_trace.get("selected_hit_ids"):
        diagnostics.pop("hit_ids", None)
    if diagnostics.get("query_text_present") == budget_trace.get("query_text_present"):
        diagnostics.pop("query_text_present", None)


def _compact_trace_mapping(trace: Mapping[str, Any]) -> dict[str, Any]:
    return {
        str(key): value for key, value in trace.items() if value not in (None, "", (), {})
    }


def _merge_trace(
    existing: Mapping[str, Any] | object,
    synthesized: Mapping[str, Any],
    *,
    preserve_empty_keys: tuple[str, ...] = (),
) -> dict[str, Any]:
    merged = dict(existing) if isinstance(existing, Mapping) else {}
    for key, value in synthesized.items():
        merged.setdefault(str(key), value)
    compacted = _compact_trace_mapping(merged)
    for key in preserve_empty_keys:
        if key not in merged or key in compacted:
            continue
        value = merged[key]
        if isinstance(value, Mapping):
            compacted[key] = dict(value)
        else:
            compacted[key] = value
    return compacted


def _writeback_report_field_map(
    reports: Mapping[str, Any] | object,
    field: str,
) -> dict[str, Any]:
    if not isinstance(reports, Mapping):
        return {}
    values: dict[str, Any] = {}
    for request_kind, report in reports.items():
        if not isinstance(report, Mapping):
            continue
        value = report.get(field)
        if value not in (None, "", (), {}):
            values[str(request_kind)] = value
    return values


def _normalize_writeback_trace_fields(
    writeback_trace: Mapping[str, Any] | object,
) -> dict[str, Any]:
    if not isinstance(writeback_trace, Mapping):
        return {}
    normalized = dict(writeback_trace)
    if "detail_reports" not in normalized and "reports" in normalized:
        normalized["detail_reports"] = normalized["reports"]
    normalized.pop("reports", None)
    return _compact_trace_mapping(normalized)
