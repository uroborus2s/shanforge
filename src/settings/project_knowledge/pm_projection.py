"""R009 field-map driven current PM projection."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import stat
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

from domain.project_knowledge.models import ValueState, canonical_json
from runtime.project_knowledge.site_renderer import site_input_token
from settings.project_knowledge.schema import PM_TABLES, validate_pm_field_map

_TypedSelector = str | tuple[str, ...] | None

# R009 keeps all 134 persisted contract fields in field_values_json.  This
# registry promotes the subset used for joins, filtering, sorting and the site
# header into the typed columns declared by the physical schema.  A field has
# one typed owner per row model; JSON remains the state/provenance carrier.
PM_TYPED_FIELD_PROJECTIONS: dict[tuple[str, str], tuple[tuple[str, _TypedSelector], ...]] = {
    ("project_profile", "common.project_name"): (("project_name", None),),
    ("project_profile", "common.project_manager"): (("manager_party_id", None),),
    ("member_party", "member.name"): (("display_name", None),),
    ("member_party", "member.project_role"): (("role_name", None),),
    ("member_party", "member.department"): (("department", None),),
    ("member_party", "member.responsibility"): (("responsibility", None),),
    ("stakeholder_party", "charter.stakeholder.name"): (("display_name", None),),
    ("stakeholder_party", "charter.stakeholder.title"): (("role_name", None),),
    ("stakeholder_party", "charter.stakeholder.department"): (("department", None),),
    ("wbs_item", "wbs.task_name"): (("title", None),),
    ("wbs_item", "wbs.raw_status"): (("task_status", None),),
    ("schedule_item", "schedule.item_name"): (("title", None),),
    ("schedule_item", "schedule.owner"): (("owner_party_id", None),),
    ("schedule_item", "schedule.planned_start"): (("planned_start", None),),
    ("schedule_item", "schedule.planned_finish"): (("planned_end", None),),
    ("schedule_item", "schedule.actual_start"): (("actual_start", None),),
    ("schedule_item", "schedule.actual_finish"): (("actual_end", None),),
    ("schedule_item", "schedule.variance"): (("schedule_variance", None),),
    ("risk", "risk.description"): (("description", None),),
    ("risk", "risk.probability"): (("probability", None),),
    ("risk", "risk.impact"): (("impact", None),),
    ("risk", "risk.level"): (("risk_level", None),),
    ("risk", "risk.response"): (("response_strategy", None),),
    ("risk", "risk.owner"): (("owner_party_id", None),),
    ("risk", "risk.status"): (("risk_status", None),),
    ("communication", "communication.stakeholder"): (("stakeholder_party_id", None),),
    ("communication", "communication.required_information"): (("information_need", None),),
    ("communication", "communication.frequency"): (("frequency", None),),
    ("communication", "communication.method"): (("channel", None),),
    ("communication", "communication.owner"): (("owner_party_id", None),),
    ("communication", "communication.next_at"): (("next_at", None),),
    ("meeting", "meeting.name"): (("title", None),),
    ("meeting", "meeting.convener"): (("chair_party_id", None),),
    ("meeting", "meeting.date"): (("scheduled_at", None),),
    ("meeting", "meeting.resolutions"): (("decision_summary", None),),
    ("action_item", "meeting.action"): (
        ("title", ("description", "title")),
        ("owner_party_id", ("owner", "owner_id")),
        ("due_at", ("due_at", "due")),
        ("action_status", ("status",)),
        ("completion_note", ("completion_note", "result")),
    ),
    ("status_report", "status.overall"): (("overall_status", None),),
    ("status_report", "status.period"): (
        ("period_start", ("start", "start_at", "period_start")),
        ("period_end", ("end", "end_at", "period_end")),
    ),
    ("status_report", "status.current_deliverables"): (("highlights", None),),
    ("status_report", "status.next_plan"): (("next_steps", None),),
    ("status_report", "status.current_issues"): (("help_needed", None),),
    ("change_request", "change.request"): (("title", None),),
    ("change_request", "change.reason"): (("reason", None),),
    ("change_request", "change.affected_baselines"): (("change_type", None),),
    ("change_request", "change.requester_signature"): (("requester_party_id", None),),
    ("change_request", "change.approver_signature"): (("approver_party_id", None),),
    ("change_request", "change.approval_opinion"): (("decision", None),),
    ("change_request", "change.requested_at"): (("requested_at", None),),
    ("change_request", "change.approved_at"): (("decided_at", None),),
    ("project_summary", "summary.planned_results"): (("scope_result", None),),
    ("project_summary", "summary.time_variance"): (("schedule_result", None),),
    ("project_summary", "summary.cost_variance"): (("cost_result", None),),
    ("project_summary", "summary.actual_results"): (("delivery_result", None),),
    ("project_summary", "summary.lessons"): (("lessons_learned", None),),
    ("project_summary", "summary.actual_finish"): (("closed_at", None),),
}

_DISCRIMINATOR_COLUMNS = {
    "member_party": ("party_kind", "member"),
    "stakeholder_party": ("party_kind", "stakeholder"),
    "wbs_item": ("plan_kind", "wbs"),
    "schedule_item": ("plan_kind", "schedule"),
}

_PARTY_REFERENCE_COLUMNS = {
    "manager_party_id",
    "owner_party_id",
    "stakeholder_party_id",
    "chair_party_id",
    "requester_party_id",
    "approver_party_id",
}


@dataclass(frozen=True, slots=True)
class ProjectionResult:
    field_count: int
    row_model_count: int
    row_count: int
    projection_sha256: str
    value_state_counts: dict[str, int]
    missing_row_models: tuple[str, ...]
    render_dtos: tuple[dict[str, Any], ...]


@dataclass(slots=True)
class _ProjectedRow:
    row_model: str
    table: str
    primary_key: str
    key: str
    values: dict[str, Any]
    field_values: dict[str, Any]


def _tokens(path: str) -> list[str]:
    if path == "/":
        return []
    if not path.startswith("/"):
        return [path]
    return [token.replace("~1", "/").replace("~0", "~") for token in path[1:].split("/")]


def _enumerate_collection(
    snapshot: Any, path: str
) -> list[tuple[Any, tuple[int, ...], tuple[Any, ...]]]:
    tokens = _tokens(path)
    if tokens and not path.startswith("/"):
        return []
    rows: list[tuple[Any, tuple[int, ...], tuple[Any, ...]]] = []

    def walk(
        current: Any,
        position: int,
        captures: tuple[int, ...],
        contexts: tuple[Any, ...],
    ) -> None:
        if position == len(tokens):
            rows.append((current, captures, contexts))
            return
        token = tokens[position]
        if token == "*":
            if not isinstance(current, list):
                return
            for index, item in enumerate(current):
                walk(item, position + 1, (*captures, index), (*contexts, item))
            return
        if not isinstance(current, dict) or token not in current:
            return
        walk(current[token], position + 1, captures, contexts)

    walk(snapshot, 0, (), ())
    return rows


def _explicit_state(value: Any) -> tuple[ValueState, Any] | None:
    if isinstance(value, dict) and set(value) <= {"$state", "value"} and "$state" in value:
        state = ValueState(str(value["$state"]))
        return state, value.get("value") if state is ValueState.KNOWN else None
    return None


def _resolve(
    snapshot: Any,
    path: str,
    captures: tuple[int, ...],
) -> tuple[ValueState, Any]:
    tokens = _tokens(path)
    if tokens and not path.startswith("/"):
        return ValueState.NOT_REGISTERED, None
    capture_position = 0

    def walk(current: Any, position: int) -> tuple[ValueState, Any]:
        nonlocal capture_position
        if position == len(tokens):
            if current is None:
                return ValueState.UNKNOWN, None
            explicit = _explicit_state(current)
            return explicit if explicit is not None else (ValueState.KNOWN, current)
        token = tokens[position]
        if token == "*":
            if capture_position < len(captures):
                index = captures[capture_position]
                capture_position += 1
                if not isinstance(current, list) or index >= len(current):
                    return ValueState.NOT_REGISTERED, None
                return walk(current[index], position + 1)
            if not isinstance(current, list) or not current:
                return ValueState.NOT_REGISTERED, None
            values: list[Any] = []
            states: list[ValueState] = []
            for item in current:
                saved = capture_position
                state, value = walk(item, position + 1)
                capture_position = saved
                states.append(state)
                if state is ValueState.KNOWN:
                    values.append(value)
            if values:
                return ValueState.KNOWN, values
            if ValueState.UNKNOWN in states:
                return ValueState.UNKNOWN, None
            return ValueState.NOT_REGISTERED, None
        brace = re.fullmatch(r"\{([^}]+)\}", token)
        if brace:
            if not isinstance(current, dict):
                return ValueState.NOT_REGISTERED, None
            result = {name: current.get(name) for name in brace.group(1).split(",")}
            if all(value is None for value in result.values()):
                return ValueState.UNKNOWN, None
            return ValueState.KNOWN, result
        if not isinstance(current, dict) or token not in current:
            state = ValueState.UNKNOWN if position == len(tokens) - 1 else ValueState.NOT_REGISTERED
            return state, None
        return walk(current[token], position + 1)

    return walk(snapshot, 0)


def _normalize_id(value: Any) -> str:
    if not isinstance(value, (str, int)) or str(value).strip() != str(value) or not str(value):
        raise ValueError("required source identity must be a non-empty string or integer")
    normalized = unicodedata.normalize("NFC", str(value))
    return quote(normalized, safe="-._~")


def _context_value(name: str, snapshot: dict[str, Any], contexts: tuple[Any, ...]) -> Any:
    if name == "project_id":
        return snapshot.get("project_id")
    for context in reversed(contexts):
        if isinstance(context, dict) and name in context:
            return context[name]
    return None


_PLACEHOLDER = re.compile(r"<normalized_([^>]+)>")


def _target_key(
    formula: str,
    record_id: Any,
    snapshot: dict[str, Any],
    contexts: tuple[Any, ...],
) -> str:
    if formula == "preserve_project_id":
        return str(record_id)

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        value = _context_value(name, snapshot, contexts)
        if value is None:
            value = record_id
        return _normalize_id(value)

    result = _PLACEHOLDER.sub(replace, formula)
    if "<" in result or ">" in result:
        raise ValueError(f"unresolved target key formula: {formula}")
    return result


def _validate_known_type(field_id: str, source_type: str, value: Any) -> None:
    if source_type == "string" and not isinstance(value, str):
        raise ValueError(f"{field_id} expects string")
    if source_type == "integer" and (type(value) is not int):
        raise ValueError(f"{field_id} expects integer")
    if source_type == "boolean" and type(value) is not bool:
        raise ValueError(f"{field_id} expects boolean")
    if source_type in {"decimal", "duration_minutes"} and (type(value) not in {int, float}):
        raise ValueError(f"{field_id} expects numeric value")
    if source_type.endswith("_list") and not isinstance(value, list):
        raise ValueError(f"{field_id} expects list")
    if source_type.startswith("enum:") and not isinstance(value, str):
        raise ValueError(f"{field_id} expects enum string")


def _typed_value(value: Any, selector: _TypedSelector) -> Any:
    selected = value
    if selector is not None:
        if not isinstance(value, dict):
            return None
        names = (selector,) if isinstance(selector, str) else selector
        selected = next((value[name] for name in names if value.get(name) is not None), None)
    if isinstance(selected, bool):
        return int(selected)
    if selected is None or isinstance(selected, (str, int, float)):
        return selected
    return canonical_json(selected)


def _party_reference(value: Any, party_keys: set[str]) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        raw = value
    elif isinstance(value, dict):
        raw_value = next(
            (
                value[key]
                for key in ("party_id", "member_id", "stakeholder_id", "actor_id", "id")
                if value.get(key) is not None
            ),
            None,
        )
        if raw_value is None:
            return None
        raw = str(raw_value)
    else:
        return None
    if raw in party_keys:
        return raw
    normalized = _normalize_id(raw)
    for prefix in ("pm-party:member:", "pm-party:stakeholder:"):
        candidate = prefix + normalized
        if candidate in party_keys:
            return candidate
    return None


class ProjectManagementProjector:
    def __init__(self, field_map_path: Path) -> None:
        self._path = field_map_path
        self._validated = validate_pm_field_map(field_map_path)
        self._payload = json.loads(field_map_path.read_text(encoding="utf-8"))

    def project(
        self,
        snapshot: dict[str, Any],
        connection: sqlite3.Connection,
        *,
        generation_id: str,
        source_manifest_sha256: str,
        not_applicable_fields: frozenset[str] = frozenset(),
    ) -> ProjectionResult:
        if snapshot.get("schema_id") != "ProjectProgressSnapshot/v2":
            raise ValueError("PM projection requires ProjectProgressSnapshot/v2")
        mappings = self._payload["mappings"]
        mappings_by_model: dict[str, list[dict[str, Any]]] = {}
        for mapping in mappings:
            mappings_by_model.setdefault(str(mapping["row_model"]), []).append(mapping)
        rows: list[_ProjectedRow] = []
        missing_models: list[str] = []
        render_dtos: list[dict[str, Any]] = []
        state_counts: Counter[str] = Counter({state.value: 0 for state in ValueState})
        seen_keys: set[tuple[str, str]] = set()
        row_models = self._payload["row_models"]
        for model_id, model in row_models.items():
            collections = _enumerate_collection(snapshot, str(model["source_collection_path"]))
            if not collections:
                missing_models.append(model_id)
                if model["target_kind"] == "render_dto":
                    render_dtos.append(
                        {
                            "row_model": model_id,
                            "state": ValueState.NOT_REGISTERED.value,
                            "field_values": {
                                mapping["field_id"]: {
                                    "state": ValueState.NOT_REGISTERED.value,
                                    "value": None,
                                    "label": mapping["label"],
                                    "source_path": mapping["source_snapshot_path"],
                                }
                                for mapping in mappings_by_model.get(model_id, [])
                            },
                        }
                    )
                continue
            for _, captures, contexts in collections:
                id_state, record_id = _resolve(
                    snapshot, str(model["source_record_id_path"]), captures
                )
                if id_state is not ValueState.KNOWN:
                    raise ValueError(f"row model {model_id} required source identity is missing")
                key = _target_key(str(model["target_key_formula"]), record_id, snapshot, contexts)
                target_name = str(model.get("table") or model.get("owner"))
                identity = (target_name, key)
                if identity in seen_keys:
                    raise ValueError(f"target key collision: {target_name}/{key}")
                seen_keys.add(identity)
                field_values: dict[str, Any] = {}
                typed_values: dict[str, Any] = {}
                for mapping in mappings_by_model.get(model_id, []):
                    field_id = str(mapping["field_id"])
                    if field_id in not_applicable_fields:
                        state, value = ValueState.NOT_APPLICABLE, None
                    else:
                        state, value = _resolve(
                            snapshot, str(mapping["source_snapshot_path"]), captures
                        )
                    if state is ValueState.KNOWN:
                        _validate_known_type(field_id, str(mapping["source_type"]), value)
                    state_counts[state.value] += 1
                    field_values[field_id] = {
                        "state": state.value,
                        "value": value if state is ValueState.KNOWN else None,
                        "label": mapping["label"],
                        "source_path": mapping["source_snapshot_path"],
                        "source_type": mapping["source_type"],
                        "history_policy": mapping["history_policy"],
                    }
                    for column, selector in PM_TYPED_FIELD_PROJECTIONS.get(
                        (model_id, field_id), ()
                    ):
                        typed_values[column] = (
                            _typed_value(value, selector) if state is ValueState.KNOWN else None
                        )
                if model["target_kind"] == "render_dto":
                    render_dtos.append(
                        {"row_model": model_id, "record_id": key, "field_values": field_values}
                    )
                    continue
                values: dict[str, Any] = {
                    str(model["primary_key"][0]): key,
                    "generation_id": generation_id,
                    "source_manifest_sha256": source_manifest_sha256,
                    "field_values_json": canonical_json(field_values),
                }
                values.update(typed_values)
                discriminator = _DISCRIMINATOR_COLUMNS.get(model_id)
                if discriminator is not None:
                    values[discriminator[0]] = discriminator[1]
                for parent in model["parent_keys"]:
                    parent_state, parent_value = _resolve(
                        snapshot, str(parent["source_path"]), captures
                    )
                    if parent_state is not ValueState.KNOWN:
                        if parent["required"]:
                            raise ValueError(
                                f"row model {model_id} required parent "
                                f"{parent['target']} is missing"
                            )
                        values[str(parent["target"])] = None
                        continue
                    transform = str(parent["transform"])
                    values[str(parent["target"])] = (
                        parent_value
                        if transform == "preserve"
                        else _target_key(transform, parent_value, snapshot, contexts)
                    )
                row_sha = hashlib.sha256(
                    canonical_json([model_id, key, field_values, values]).encode("utf-8")
                ).hexdigest()
                values["row_sha256"] = row_sha
                rows.append(
                    _ProjectedRow(
                        row_model=model_id,
                        table=str(model["table"]),
                        primary_key=str(model["primary_key"][0]),
                        key=key,
                        values=values,
                        field_values=field_values,
                    )
                )
        self._resolve_party_references(rows)
        self._validate_parent_targets(rows)
        self._refresh_row_hashes(rows)
        self._replace_rows(connection, rows)
        projection_payload = [
            [row.table, row.key, row.values["row_sha256"]]
            for row in sorted(rows, key=lambda item: (item.table, item.key))
        ]
        return ProjectionResult(
            field_count=self._validated.field_count,
            row_model_count=self._validated.row_model_count,
            row_count=len(rows),
            projection_sha256=hashlib.sha256(
                canonical_json(projection_payload).encode("utf-8")
            ).hexdigest(),
            value_state_counts=dict(state_counts),
            missing_row_models=tuple(missing_models),
            render_dtos=tuple(render_dtos),
        )

    @staticmethod
    def _resolve_party_references(rows: list[_ProjectedRow]) -> None:
        party_keys = {row.key for row in rows if row.table == "pm_party"}
        for row in rows:
            for column in _PARTY_REFERENCE_COLUMNS:
                if column in row.values:
                    row.values[column] = _party_reference(row.values[column], party_keys)

    @staticmethod
    def _validate_parent_targets(rows: list[_ProjectedRow]) -> None:
        plan_keys = {row.key for row in rows if row.table == "pm_work_plan"}
        meeting_keys = {row.key for row in rows if row.table == "pm_meeting"}
        for row in rows:
            parent_plan = row.values.get("parent_plan_item_id")
            if parent_plan is not None and parent_plan not in plan_keys:
                row.values["parent_plan_item_id"] = None
            meeting = row.values.get("meeting_id")
            if row.table == "pm_action_item" and meeting not in meeting_keys:
                raise ValueError(f"row model {row.row_model} required parent meeting_id is missing")

    @staticmethod
    def _refresh_row_hashes(rows: list[_ProjectedRow]) -> None:
        for row in rows:
            values_without_hash = {
                key: value for key, value in row.values.items() if key != "row_sha256"
            }
            row.values["row_sha256"] = hashlib.sha256(
                canonical_json(
                    [row.row_model, row.key, row.field_values, values_without_hash]
                ).encode("utf-8")
            ).hexdigest()

    @staticmethod
    def _replace_rows(connection: sqlite3.Connection, rows: list[_ProjectedRow]) -> None:
        order = (
            "pm_action_item",
            "pm_project_summary",
            "pm_change_request",
            "pm_status_report",
            "pm_meeting",
            "pm_communication",
            "pm_risk",
            "pm_work_plan",
            "pm_party",
            "pm_project_profile",
        )
        try:
            connection.execute("SAVEPOINT pm_projection")
            for table in order:
                connection.execute(f"DELETE FROM {table}")
            insert_order = tuple(reversed(order))
            for table in insert_order:
                columns_available = {
                    str(info[1]) for info in connection.execute(f"PRAGMA table_info({table})")
                }
                for row in (item for item in rows if item.table == table):
                    values = {
                        key: value for key, value in row.values.items() if key in columns_available
                    }
                    columns = tuple(values)
                    placeholders = ",".join("?" for _ in columns)
                    connection.execute(
                        f"INSERT INTO {table}({','.join(columns)}) VALUES ({placeholders})",
                        tuple(values[column] for column in columns),
                    )
            connection.execute("RELEASE SAVEPOINT pm_projection")
        except BaseException:
            connection.execute("ROLLBACK TO SAVEPOINT pm_projection")
            connection.execute("RELEASE SAVEPOINT pm_projection")
            raise


class SQLiteSiteDataStore:
    """Read-only DTO assembly for the site renderer."""

    _PRIMARY_KEYS = {
        "pm_project_profile": "project_id",
        "pm_party": "party_id",
        "pm_work_plan": "plan_item_id",
        "pm_risk": "risk_id",
        "pm_communication": "communication_id",
        "pm_meeting": "meeting_id",
        "pm_action_item": "action_item_id",
        "pm_status_report": "status_report_id",
        "pm_change_request": "change_request_id",
        "pm_project_summary": "summary_id",
    }

    def __init__(
        self,
        database_path: Path,
        *,
        project_name: str = "Shanforge",
        project_root: Path | None = None,
    ) -> None:
        self._path = database_path
        self._project_name = project_name
        self._project_root = None if project_root is None else project_root.resolve()

    def _document_markdown(self, relative_path: str, expected_sha256: str) -> str | None:
        if self._project_root is None:
            return None
        relative = Path(relative_path)
        if (
            relative.is_absolute()
            or len(relative.parts) < 2
            or relative.parts[0] != "docs"
            or any(part in {"", ".", ".."} for part in relative.parts)
        ):
            return None
        directory_flags = os.O_RDONLY | os.O_DIRECTORY
        no_follow = getattr(os, "O_NOFOLLOW", 0)
        open_fds: list[int] = []
        try:
            current_fd = os.open(self._project_root, directory_flags)
            open_fds.append(current_fd)
            for part in relative.parts[:-1]:
                current_fd = os.open(
                    part,
                    directory_flags | no_follow,
                    dir_fd=current_fd,
                )
                open_fds.append(current_fd)
            file_fd = os.open(
                relative.parts[-1],
                os.O_RDONLY | no_follow,
                dir_fd=current_fd,
            )
            open_fds.append(file_fd)
            file_status = os.fstat(file_fd)
            if not stat.S_ISREG(file_status.st_mode) or file_status.st_size > 2_097_152:
                return None
            chunks: list[bytes] = []
            remaining = 2_097_153
            while remaining:
                chunk = os.read(file_fd, min(65_536, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            content = b"".join(chunks)
            if len(content) > 2_097_152:
                return None
        except OSError:
            return None
        finally:
            for descriptor in reversed(open_fds):
                os.close(descriptor)
        if hashlib.sha256(content).hexdigest() != expected_sha256:
            return None
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return None

    @staticmethod
    def _pm_digest(connection: sqlite3.Connection) -> str:
        values: list[tuple[str, str, str]] = []
        for table in PM_TABLES:
            key = SQLiteSiteDataStore._PRIMARY_KEYS[table]
            values.extend(
                (table, str(row[0]), str(row[1] or ""))
                for row in connection.execute(
                    f"SELECT {key},row_sha256 FROM {table} ORDER BY {key}"
                )
            )
        return hashlib.sha256(canonical_json(values).encode("utf-8")).hexdigest()

    def load(self, *, profile: str = "local-owner") -> dict[str, Any]:
        if profile not in {"local-owner", "shared-restricted"}:
            raise ValueError("unsupported site profile")
        connection = sqlite3.connect(self._path)
        connection.row_factory = sqlite3.Row
        try:
            current = connection.execute(
                "SELECT * FROM pk_generation WHERE status='current'"
            ).fetchone()
            entity_access = "" if profile == "local-owner" else " AND a.access_class='public'"
            entities = [
                dict(row)
                for row in connection.execute(
                    "SELECT e.entity_id,e.entity_kind,e.display_name,e.summary,e.lifecycle_status,"
                    "e.detail_json "
                    "FROM pk_entity e LEFT JOIN pk_artifact a "
                    "ON a.artifact_id=e.primary_artifact_id WHERE 1=1"
                    + entity_access
                    + " ORDER BY e.entity_kind,e.display_name"
                )
            ]
            for entity in entities:
                entity["details"] = json.loads(str(entity.pop("detail_json") or "{}"))
            visible_entity_ids = {str(item["entity_id"]) for item in entities}
            test_entity_ids = {
                str(row[0]) for row in connection.execute("SELECT entity_id FROM pk_test")
            }
            code_symbol_parents = {
                str(row["entity_id"]): str(row["file_entity_id"])
                for row in connection.execute(
                    """
                    SELECT s.entity_id,cf.entity_id AS file_entity_id
                      FROM pk_code_symbol s
                      JOIN pk_code_file cf ON cf.code_file_id=s.code_file_id
                    """
                )
            }
            edges = [
                dict(row)
                for row in connection.execute("SELECT * FROM pk_edge")
                if str(row["from_entity_id"]) in visible_entity_ids
                and str(row["to_entity_id"]) in visible_entity_ids
            ]
            entity_by_id = {str(item["entity_id"]): item for item in entities}
            for entity_id in test_entity_ids & visible_entity_ids:
                entity_by_id[entity_id]["entity_kind"] = "test"

            def relation_target(entity_id: str) -> dict[str, Any]:
                target = {
                    "entity_id": entity_id,
                    "entity_kind": entity_by_id[entity_id]["entity_kind"],
                    "display_name": entity_by_id[entity_id]["display_name"],
                }
                if entity_id in code_symbol_parents and entity_id not in test_entity_ids:
                    target["route_entity_id"] = code_symbol_parents[entity_id]
                return target

            for entity in entities:
                entity["relations"] = []
                entity["locators"] = []
            for edge in edges:
                from_id = str(edge["from_entity_id"])
                to_id = str(edge["to_entity_id"])
                entity_by_id[from_id]["relations"].append(
                    {
                        "direction": "outgoing",
                        "relation_type": edge["relation_type"],
                        "strength": edge["strength"],
                        **relation_target(to_id),
                    }
                )
                entity_by_id[to_id]["relations"].append(
                    {
                        "direction": "incoming",
                        "relation_type": edge["relation_type"],
                        "strength": edge["strength"],
                        **relation_target(from_id),
                    }
                )
            for row in connection.execute(
                """
                SELECT el.entity_id,l.locator_kind,l.selector_json,s.relative_path
                  FROM pk_entity_locator el
                  JOIN pk_locator l ON l.locator_id=el.locator_id
                  JOIN pk_source s ON s.source_id=l.source_id
                 WHERE el.is_primary=1
                """
            ):
                entity_id = str(row["entity_id"])
                if entity_id not in entity_by_id:
                    continue
                entity_by_id[entity_id]["locators"].append(
                    {
                        "locator_kind": row["locator_kind"],
                        "selector": json.loads(str(row["selector_json"])),
                        "relative_path": row["relative_path"],
                    }
                )
            for row in connection.execute("SELECT * FROM pk_code_file"):
                entity_id = str(row["entity_id"])
                if entity_id in entity_by_id:
                    entity_by_id[entity_id]["code_file"] = dict(row)
                    entity_by_id[entity_id]["symbols"] = []
            for row in connection.execute(
                """
                SELECT cf.entity_id AS file_entity_id,s.entity_id,s.symbol_kind,
                       s.qualified_name,s.signature_text,s.visibility,e.display_name,
                       e.summary,e.lifecycle_status
                  FROM pk_code_symbol s
                  JOIN pk_code_file cf ON cf.code_file_id=s.code_file_id
                  JOIN pk_entity e ON e.entity_id=s.entity_id
                 ORDER BY cf.entity_id,s.qualified_name,s.symbol_id
                """
            ):
                file_entity_id = str(row["file_entity_id"])
                if file_entity_id not in entity_by_id:
                    continue
                symbol = dict(row)
                symbol.pop("file_entity_id", None)
                symbol_entity = entity_by_id.get(str(symbol["entity_id"]))
                symbol["locators"] = [] if symbol_entity is None else symbol_entity["locators"]
                entity_by_id[file_entity_id]["symbols"].append(symbol)
            for row in connection.execute("SELECT * FROM pk_requirement"):
                entity_id = str(row["entity_id"])
                if entity_id not in entity_by_id:
                    continue
                requirement = dict(row)
                requirement["acceptance_criteria"] = [
                    dict(criterion)
                    for criterion in connection.execute(
                        "SELECT acceptance_id,display_order,statement,criterion_status "
                        "FROM pk_acceptance_criterion WHERE requirement_id=? "
                        "ORDER BY display_order,acceptance_id",
                        (row["requirement_id"],),
                    )
                ]
                entity_by_id[entity_id]["requirement"] = requirement
            for table, key in (
                ("pk_work_item", "work_item"),
                ("pk_code_symbol", "code_symbol"),
                ("pk_test", "test"),
            ):
                for row in connection.execute(f"SELECT * FROM {table}"):
                    entity_id = str(row["entity_id"])
                    if entity_id in entity_by_id:
                        entity_by_id[entity_id][key] = dict(row)
            documents: list[dict[str, Any]] = []
            for row in connection.execute(
                """
                SELECT d.*,a.relative_path,a.access_class,a.content_sha256
                  FROM pk_document d JOIN pk_artifact a ON a.artifact_id=d.artifact_id
                 WHERE (? = 'local-owner' OR a.access_class = 'public')
                 ORDER BY d.title
                """,
                (profile,),
            ):
                document = dict(row)
                document["sections"] = [
                    dict(section)
                    for section in connection.execute(
                        "SELECT section_id,display_title,display_order FROM pk_document_section "
                        "WHERE document_id=? ORDER BY display_order",
                        (row["document_id"],),
                    )
                ]
                content_markdown = self._document_markdown(
                    str(row["relative_path"]), str(row["content_sha256"])
                )
                if content_markdown is not None:
                    document["content_markdown"] = content_markdown
                documents.append(document)
            diagnostics = (
                [
                    dict(row)
                    for row in connection.execute(
                        "SELECT * FROM pk_diagnostic ORDER BY severity,code"
                    )
                ]
                if profile == "local-owner"
                else []
            )
            versions = [
                dict(row)
                for row in connection.execute(
                    "SELECT generation_id,status,git_commit,as_of,source_root_sha256 "
                    "FROM pk_generation ORDER BY created_at DESC LIMIT 20"
                )
            ]
            pm: dict[str, list[dict[str, Any]]] = {}
            for table in PM_TABLES:
                key = self._PRIMARY_KEYS[table]
                records: list[dict[str, Any]] = []
                rows = (
                    connection.execute(f"SELECT * FROM {table} ORDER BY {key}")
                    if profile == "local-owner"
                    else ()
                )
                for row in rows:
                    record = dict(row)
                    record["record_id"] = record[key]
                    record["field_values"] = json.loads(record.pop("field_values_json"))
                    records.append(record)
                pm[table] = records
            pm_digest = self._pm_digest(connection) if profile == "local-owner" else "redacted"
        finally:
            connection.close()
        generation = dict(current) if current is not None else {}
        generation["source_manifest_sha256"] = generation.get("source_root_sha256", "")
        generation["pm_projection_sha256"] = pm_digest
        profile_records = pm.get("pm_project_profile", [])
        project = {
            "name": self._project_name if profile == "local-owner" else "受限项目视图",
            "status": "unknown",
            "completion": None,
        }
        if profile_records:
            project["name"] = profile_records[0].get("project_name") or self._project_name
            project["status"] = profile_records[0].get("project_status") or "unknown"
            project["completion"] = profile_records[0].get("completion_ratio")
        return {
            "project": project,
            "generation": generation,
            "entities": entities,
            "edges": edges,
            "documents": documents,
            "diagnostics": diagnostics,
            "versions": versions,
            "pm": pm,
        }

    def current_input_token(self, *, profile: str) -> str:
        connection = sqlite3.connect(self._path)
        connection.row_factory = sqlite3.Row
        try:
            current = connection.execute(
                "SELECT generation_id,source_root_sha256 FROM pk_generation WHERE status='current'"
            ).fetchone()
            pm_digest = self._pm_digest(connection) if profile == "local-owner" else "redacted"
        finally:
            connection.close()
        if current is None:
            raise ValueError("project knowledge index has no current generation")
        generation = dict(current)
        generation["source_manifest_sha256"] = generation["source_root_sha256"]
        generation["pm_projection_sha256"] = pm_digest
        return site_input_token(generation, profile)
