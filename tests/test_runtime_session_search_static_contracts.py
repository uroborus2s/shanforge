from __future__ import annotations

import unittest
from typing import Any, Mapping

from runtime.capability.contracts import CapabilityInvocationContext
from runtime.session_search.service import SessionSearchService


class _MalformedScoreSearchIndex:
    def search(
        self,
        namespace: str,
        query_text: str,
        limit: int = 20,
        filters: Mapping[str, Any] | None = None,
    ) -> tuple[Mapping[str, Any], ...]:
        del namespace, query_text, limit, filters
        return (
            {
                "session_id": "session-malformed-score",
                "summary": "Malformed persisted search hit",
                "score": object(),
            },
        )


class RuntimeSessionSearchStaticContractTests(unittest.TestCase):
    def test_artifact_search_rejects_non_numeric_limit_with_diagnostic(self) -> None:
        service = SessionSearchService()

        with self.assertRaisesRegex(ValueError, "limit must be numeric"):
            service.search_session_artifacts(
                {"limit": object()},
                CapabilityInvocationContext(session_id="session-static-contract"),
            )

    def test_archive_search_rejects_non_numeric_persisted_score_with_diagnostic(
        self,
    ) -> None:
        service = SessionSearchService(search_index=_MalformedScoreSearchIndex())

        with self.assertRaisesRegex(ValueError, "score must be numeric"):
            service.search_session_archive(
                "persisted hit",
                profile_id=None,
                limit=5,
                context=CapabilityInvocationContext(session_id="session-static-contract"),
            )


if __name__ == "__main__":
    unittest.main()
