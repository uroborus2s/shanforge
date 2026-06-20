from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path

from domain.session.delegation_models import SubAgentDigest
from settings.shared.jsonl import JsonlStore


def _deserialize_digest(payload: dict[str, object]) -> SubAgentDigest:
    normalized = dict(payload)
    normalized.pop("id", None)
    return SubAgentDigest.from_mapping(normalized)


@dataclass(slots=True)
class InMemoryDelegationDigestStore:
    """Simple in-memory store for child-session digests."""

    digests_by_session: dict[str, tuple[SubAgentDigest, ...]] = field(default_factory=dict)

    def save(self, digest: SubAgentDigest) -> None:
        current = list(self.digests_by_session.get(digest.parent_session_id, ()))
        for index, existing in enumerate(current):
            if existing.child_session_id == digest.child_session_id:
                current[index] = copy.deepcopy(digest)
                break
        else:
            current.append(copy.deepcopy(digest))
        self.digests_by_session[digest.parent_session_id] = tuple(current)

    def list_by_session(self, session_id: str) -> tuple[SubAgentDigest, ...]:
        return tuple(copy.deepcopy(item) for item in self.digests_by_session.get(session_id, ()))


class JsonlDelegationDigestStore(JsonlStore):
    """JSONL-backed store for child-session digests."""

    def __init__(self, root: str | Path) -> None:
        super().__init__(root=root, filename="delegation-digests.jsonl")

    def save(self, digest: SubAgentDigest) -> None:
        record_id = f"{digest.parent_session_id}:{digest.child_session_id}"
        payload = {"id": record_id, **digest.to_mapping()}
        self.replace_or_append(record_id, payload)

    def list_by_session(self, session_id: str) -> tuple[SubAgentDigest, ...]:
        return tuple(
            digest
            for digest in self.read_all(_deserialize_digest)
            if digest.parent_session_id == session_id
        )
