from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from settings.workspace.secret_catalog import (
    DurableSecretSelection,
    LocalSecretCatalogProvider,
)


@dataclass(frozen=True, slots=True)
class RemoteHttpRequestGovernance:
    """One normalized request-governance view for remote_http."""

    request_kind: str
    endpoint_url: str | None = None
    request_options: dict[str, Any] = field(default_factory=dict)
    response_contract: str = ""
    response_contract_source: str = "built-in"
    response_validation_mode: str = "ignore"
    failure_policy: str | None = None


@dataclass(slots=True)
class RemoteHttpMetadataResolver:
    """Normalizes remote_http binding metadata into canonical request options."""

    def resolve_prefetch_governance(
        self,
        metadata: Mapping[str, Any],
        *,
        default_endpoint_url: str | None,
        default_contract: str,
        secret_catalog_provider: LocalSecretCatalogProvider,
    ) -> RemoteHttpRequestGovernance:
        response_contract, response_contract_source = self.resolve_prefetch_response_contract(
            metadata,
            default_contract=default_contract,
        )
        return RemoteHttpRequestGovernance(
            request_kind="recall",
            endpoint_url=self.resolve_endpoint_url(
                metadata,
                request_kind="recall",
                default=default_endpoint_url,
            ),
            request_options=self.resolve_request_options(
                metadata=metadata,
                request_kind="recall",
                secret_catalog_provider=secret_catalog_provider,
            ),
            response_contract=response_contract,
            response_contract_source=response_contract_source,
            response_validation_mode=self.resolve_prefetch_response_validation_mode(metadata),
        )

    def resolve_writeback_governance(
        self,
        metadata: Mapping[str, Any],
        *,
        request_kind: str,
        default_endpoint_url: str | None,
        default_contract: str,
        secret_catalog_provider: LocalSecretCatalogProvider,
    ) -> RemoteHttpRequestGovernance:
        response_contract, response_contract_source = self.resolve_writeback_response_contract(
            metadata,
            request_kind=request_kind,
            default_contract=default_contract,
        )
        return RemoteHttpRequestGovernance(
            request_kind=request_kind,
            endpoint_url=self.resolve_endpoint_url(
                metadata,
                request_kind=request_kind,
                default=default_endpoint_url,
            ),
            request_options=self.resolve_request_options(
                metadata=metadata,
                request_kind=request_kind,
                secret_catalog_provider=secret_catalog_provider,
            ),
            response_contract=response_contract,
            response_contract_source=response_contract_source,
            response_validation_mode=self.resolve_writeback_response_validation_mode(
                metadata,
                request_kind=request_kind,
            ),
            failure_policy=self.resolve_writeback_failure_policy(
                metadata,
                request_kind=request_kind,
            ),
        )

    def resolve_endpoint_url(
        self,
        metadata: Mapping[str, Any],
        *,
        request_kind: str,
        default: str | None,
    ) -> str | None:
        legacy_keys: tuple[str, ...] = ("endpoint_url",) if request_kind == "recall" else ()
        value = self._first_value(
            metadata,
            f"{request_kind}_endpoint_url",
            *legacy_keys,
        )
        if value is None:
            value = default
        normalized = str(value or "").strip()
        return normalized or None

    def writeback_enabled(
        self,
        metadata: Mapping[str, Any],
        *,
        default_sync_endpoint_url: str | None,
        default_session_end_endpoint_url: str | None,
        default_lifecycle_apply_endpoint_url: str | None,
        default_delegation_endpoint_url: str | None,
    ) -> bool:
        return any(
            (
                self.resolve_endpoint_url(
                    metadata,
                    request_kind="sync",
                    default=default_sync_endpoint_url,
                ),
                self.resolve_endpoint_url(
                    metadata,
                    request_kind="session_end",
                    default=default_session_end_endpoint_url,
                ),
                self.resolve_endpoint_url(
                    metadata,
                    request_kind="lifecycle_apply",
                    default=default_lifecycle_apply_endpoint_url,
                ),
                self.resolve_endpoint_url(
                    metadata,
                    request_kind="delegation",
                    default=default_delegation_endpoint_url,
                ),
            )
        )

    def resolve_prefetch_response_contract(
        self,
        metadata: Mapping[str, Any],
        *,
        default_contract: str,
    ) -> tuple[str, str]:
        return self._response_contract(
            metadata,
            canonical_key="recall_response_contract",
            legacy_keys=("prefetch_response_contract", "response_contract"),
            default_contract=default_contract,
        )

    def resolve_writeback_response_contract(
        self,
        metadata: Mapping[str, Any],
        *,
        request_kind: str,
        default_contract: str,
    ) -> tuple[str, str]:
        return self._response_contract(
            metadata,
            canonical_key=f"{request_kind}_response_contract",
            legacy_keys=("writeback_response_contract",),
            default_contract=default_contract,
        )

    def resolve_request_options(
        self,
        *,
        metadata: Mapping[str, Any],
        request_kind: str,
        secret_catalog_provider: LocalSecretCatalogProvider,
    ) -> dict[str, Any]:
        secret_catalog, secret_catalog_source_path = secret_catalog_provider.load_catalog(metadata)
        headers = self._merge_headers(
            metadata.get("request_headers"),
            metadata.get(f"{request_kind}_headers"),
        )
        options: dict[str, Any] = {"headers": headers} if headers else {}
        if secret_catalog_source_path is not None:
            options["secret_catalog_source_path"] = secret_catalog_source_path

        for key in (
            "timeout_seconds",
            "max_retries",
            "retry_status_codes",
            "retry_backoff_seconds",
        ):
            value = self._request_value(metadata, request_kind=request_kind, canonical_key=key)
            if value is None or value == "":
                continue
            options[key] = value

        self._resolve_bearer_options(
            options,
            metadata=metadata,
            request_kind=request_kind,
            secret_catalog=secret_catalog,
            secret_catalog_source_path=secret_catalog_source_path,
            secret_catalog_provider=secret_catalog_provider,
        )
        self._resolve_signature_options(
            options,
            metadata=metadata,
            request_kind=request_kind,
            secret_catalog=secret_catalog,
            secret_catalog_source_path=secret_catalog_source_path,
            secret_catalog_provider=secret_catalog_provider,
        )
        signature_algorithm = self._request_value(
            metadata,
            request_kind=request_kind,
            canonical_key="signature_algorithm",
        )
        if signature_algorithm not in {None, ""}:
            options["signature_algorithm"] = signature_algorithm
        return options

    def resolve_prefetch_response_validation_mode(self, metadata: Mapping[str, Any]) -> str:
        raw_mode = self._first_value(
            metadata,
            "recall_response_validation",
            "prefetch_response_validation",
            "response_validation",
        )
        return self._normalized_validation_mode(raw_mode)

    def resolve_writeback_failure_policy(
        self,
        metadata: Mapping[str, Any],
        *,
        request_kind: str,
    ) -> str:
        policy = self._first_value(
            metadata,
            f"{request_kind}_failure_policy",
            "writeback_failure_policy",
        )
        normalized = str(policy or "raise").strip().lower()
        return normalized or "raise"

    def resolve_writeback_response_validation_mode(
        self,
        metadata: Mapping[str, Any],
        *,
        request_kind: str,
    ) -> str:
        raw_mode = self._first_value(
            metadata,
            f"{request_kind}_response_validation",
            "writeback_response_validation",
            "response_validation",
        )
        return self._normalized_validation_mode(raw_mode)

    def _resolve_bearer_options(
        self,
        options: dict[str, Any],
        *,
        metadata: Mapping[str, Any],
        request_kind: str,
        secret_catalog: Mapping[str, Any],
        secret_catalog_source_path: str | None,
        secret_catalog_provider: LocalSecretCatalogProvider,
    ) -> None:
        selection = secret_catalog_provider.resolve_secret_selection(
            secret_catalog=secret_catalog,
            metadata=metadata,
            secret_family="bearer_tokens",
            requested_id_key=f"{request_kind}_bearer_token_id",
            fallback_id_key="bearer_token_id",
            default_id_key="default_bearer_token_id",
            source_path=secret_catalog_source_path,
        )
        bearer_token = self._request_value(
            metadata,
            request_kind=request_kind,
            canonical_key="bearer_token",
            legacy_generic_keys=("auth_bearer_token",),
        )
        if bearer_token in {None, ""}:
            bearer_token = selection.get("bearer_token")
        if bearer_token not in {None, ""}:
            options["bearer_token"] = bearer_token

        bearer_token_env = self._request_value(
            metadata,
            request_kind=request_kind,
            canonical_key="bearer_token_env",
            legacy_generic_keys=("auth_bearer_token_env",),
        )
        if bearer_token_env in {None, ""}:
            bearer_token_env = selection.get("bearer_token_env")
        if bearer_token_env not in {None, ""}:
            options["bearer_token_env"] = bearer_token_env

        bearer_token_file = self._request_value(
            metadata,
            request_kind=request_kind,
            canonical_key="bearer_token_file",
            legacy_generic_keys=("auth_bearer_token_file",),
        )
        if bearer_token_file in {None, ""}:
            bearer_token_file = selection.get("bearer_token_file")
        if bearer_token_file not in {None, ""}:
            options["bearer_token_file"] = bearer_token_file

        if any(
            value not in {None, ""}
            for value in (bearer_token, bearer_token_env, bearer_token_file)
        ):
            self._apply_secret_selection(
                options,
                selection,
                secret_family="bearer_tokens",
            )

    def _resolve_signature_options(
        self,
        options: dict[str, Any],
        *,
        metadata: Mapping[str, Any],
        request_kind: str,
        secret_catalog: Mapping[str, Any],
        secret_catalog_source_path: str | None,
        secret_catalog_provider: LocalSecretCatalogProvider,
    ) -> None:
        selection = secret_catalog_provider.resolve_secret_selection(
            secret_catalog=secret_catalog,
            metadata=metadata,
            secret_family="signature_keys",
            requested_id_key=f"{request_kind}_signature_key_id",
            fallback_id_key="signature_key_id",
            default_id_key="default_signature_key_id",
            source_path=secret_catalog_source_path,
        )
        signature_secret = self._request_value(
            metadata,
            request_kind=request_kind,
            canonical_key="signature_secret",
        )
        if signature_secret in {None, ""}:
            signature_secret = selection.get("signature_secret")
        if signature_secret not in {None, ""}:
            options["signature_secret"] = signature_secret

        signature_secret_env = self._request_value(
            metadata,
            request_kind=request_kind,
            canonical_key="signature_secret_env",
        )
        if signature_secret_env in {None, ""}:
            signature_secret_env = selection.get("signature_secret_env")
        if signature_secret_env not in {None, ""}:
            options["signature_secret_env"] = signature_secret_env

        signature_secret_file = self._request_value(
            metadata,
            request_kind=request_kind,
            canonical_key="signature_secret_file",
        )
        if signature_secret_file in {None, ""}:
            signature_secret_file = selection.get("signature_secret_file")
        if signature_secret_file not in {None, ""}:
            options["signature_secret_file"] = signature_secret_file

        if any(
            value not in {None, ""}
            for value in (signature_secret, signature_secret_env, signature_secret_file)
        ):
            self._apply_secret_selection(
                options,
                selection,
                secret_family="signature_keys",
            )

    @staticmethod
    def _normalized_validation_mode(raw_mode: object) -> str:
        normalized = str(raw_mode or "ignore").strip().lower()
        if normalized == "strict":
            return "raise"
        if normalized not in {"ignore", "record", "raise"}:
            return "ignore"
        return normalized

    @staticmethod
    def _request_value(
        metadata: Mapping[str, Any],
        *,
        request_kind: str,
        canonical_key: str,
        legacy_generic_keys: tuple[str, ...] = (),
    ) -> Any:
        return RemoteHttpMetadataResolver._first_value(
            metadata,
            f"{request_kind}_{canonical_key}",
            canonical_key,
            *legacy_generic_keys,
        )

    @staticmethod
    def _response_contract(
        metadata: Mapping[str, Any],
        *,
        canonical_key: str,
        legacy_keys: tuple[str, ...],
        default_contract: str,
    ) -> tuple[str, str]:
        for key in (canonical_key, *legacy_keys):
            if key not in metadata:
                continue
            value = metadata.get(key)
            if value is None or value == "":
                continue
            return str(value), f"metadata:{key}"
        return default_contract, "built-in"

    @staticmethod
    def _first_value(metadata: Mapping[str, Any], *keys: str) -> Any:
        for key in keys:
            if key not in metadata:
                continue
            value = metadata.get(key)
            if value is None or value == "":
                continue
            return value
        return None

    @staticmethod
    def _merge_headers(*payloads: object) -> dict[str, str]:
        merged: dict[str, str] = {}
        for payload in payloads:
            if not isinstance(payload, dict):
                continue
            for key, value in payload.items():
                header_name = str(key).strip()
                if not header_name or value is None:
                    continue
                merged[header_name] = str(value)
        return merged

    @staticmethod
    def _apply_secret_selection(
        options: dict[str, Any],
        selection: DurableSecretSelection,
        *,
        secret_family: str,
    ) -> None:
        if selection.secret_id in {None, ""}:
            return
        if secret_family == "signature_keys":
            options["signature_key_id"] = selection.secret_id
            if selection.selection_source is not None:
                options["signature_key_selection_source"] = selection.selection_source
            return
        if secret_family == "bearer_tokens":
            options["bearer_token_id"] = selection.secret_id
            if selection.selection_source is not None:
                options["bearer_token_selection_source"] = selection.selection_source
