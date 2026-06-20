from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory

from domain.memory.models import (
    MemoryDistillationSample,
    MemoryKind,
    MemoryLifecycleAuditAction,
    MemoryLifecycleAuditEntry,
    MemoryLifecycleQueueEntry,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleReviewResolution,
    MemoryRecord,
    MemoryScope,
    MemoryStatus,
)
from domain.session.models import SessionArtifact
from settings.memory import (
    JsonlEvidenceStore,
    JsonlMemoryDatasetStore,
    JsonlMemoryLifecycleAuditStore,
    JsonlMemoryLifecycleQueueStore,
    JsonlMemoryStore,
)


class SettingsMemoryStoreTests(unittest.TestCase):
    def test_jsonl_stores_round_trip_memory_evidence_and_dataset(self) -> None:
        with TemporaryDirectory() as temp_dir:
            memory_store = JsonlMemoryStore(temp_dir)
            evidence_store = JsonlEvidenceStore(temp_dir)
            dataset_store = JsonlMemoryDatasetStore(temp_dir)
            lifecycle_queue_store = JsonlMemoryLifecycleQueueStore(temp_dir)
            lifecycle_audit_store = JsonlMemoryLifecycleAuditStore(temp_dir)

            record = MemoryRecord(
                id="memory-file",
                kind=MemoryKind.EPISODIC,
                scope=MemoryScope.APP,
                scope_key="demo.writer",
                title="File-backed memory",
                body="Persisted to jsonl.",
                status=MemoryStatus.ACCEPTED,
                confidence=0.77,
                supporting_refs=("event://1",),
            )
            artifact = SessionArtifact(
                id="artifact-file",
                kind="capability",
                uri="capability://context.inspect",
                summary="Persisted artifact.",
            )
            sample = MemoryDistillationSample(
                id="sample-file",
                session_id="session-file",
                candidate_id="candidate-file",
                candidate_kind=MemoryKind.EPISODIC,
                candidate_scope=MemoryScope.APP,
                candidate_scope_key="demo.writer",
                decision_status=MemoryStatus.ACCEPTED,
                decision_reason="Accepted for training corpus.",
                supporting_refs=("event://1",),
            )
            queue_entry = MemoryLifecycleQueueEntry(
                id="queue-session-file:memory-file",
                session_id="session-file",
                record_id="memory-file",
                scope=MemoryScope.APP,
                scope_key="demo.writer",
                current_status=MemoryStatus.ACCEPTED,
                effective_status=MemoryStatus.SUPERSEDED,
                reason="conflict_superseded",
                allowed=True,
                hidden=False,
                action_required=True,
                selected_by_default=False,
                review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
                reviewed_by="memory-reviewer",
                review_note="keep for manual review",
                review_resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
            )
            audit_entry = MemoryLifecycleAuditEntry(
                id="audit-session-file:memory-file:1",
                session_id="session-file",
                record_id="memory-file",
                actor="memory-reviewer",
                action=MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,
                current_status=MemoryStatus.ACCEPTED,
                effective_status=MemoryStatus.SUPERSEDED,
                queue_review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
                resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
                reason="conflict_superseded",
                note="keep for manual review",
            )

            memory_store.save(record)
            evidence_store.save_evidence_from_artifact("session-file", artifact)
            dataset_store.save_entry(sample)
            lifecycle_queue_store.replace_lifecycle_queue_entries(
                "session-file",
                (queue_entry,),
            )
            lifecycle_audit_store.append_lifecycle_audit_entries(
                "session-file",
                (audit_entry,),
            )

            self.assertEqual(
                memory_store.list_by_scope(MemoryScope.APP, "demo.writer")[0].id,
                "memory-file",
            )
            self.assertEqual(
                evidence_store.list_by_session("session-file")[0].source_id,
                "artifact-file",
            )
            self.assertEqual(dataset_store.list_by_session("session-file")[0].id, "sample-file")
            self.assertEqual(
                lifecycle_queue_store.list_lifecycle_queue_entries("session-file")[0].review_status,
                MemoryLifecycleQueueReviewStatus.DISMISSED,
            )
            self.assertEqual(
                lifecycle_queue_store.list_lifecycle_queue_entries("session-file")[
                    0
                ].review_resolution,
                MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
            )
            self.assertEqual(
                lifecycle_audit_store.list_lifecycle_audit_entries("session-file")[0].action,
                MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,
            )
            self.assertEqual(
                lifecycle_audit_store.list_lifecycle_audit_entries("session-file")[
                    0
                ].resolution,
                MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
            )


if __name__ == "__main__":
    unittest.main()
