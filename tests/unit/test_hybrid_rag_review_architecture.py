import unittest

from tests.unit.base import ROOT, UnitTestCase

DOC_PATH = ROOT / "docs" / "hybrid-rag-review-architecture.md"


class HybridRagReviewArchitectureTests(UnitTestCase):
    def test_doc_exists_and_covers_hybrid_retrieval_and_review_pattern(self) -> None:
        self.assertTrue(DOC_PATH.is_file(), "Missing hybrid RAG/review architecture doc")
        text = DOC_PATH.read_text(encoding="utf-8")

        required_markers = [
            "# Hybrid RAG and Review Architecture",
            "`internal_corpus`",
            "`client_corpus`",
            "`external_web`",
            "`shared_workspace`",
            "evidence separated into readable lanes",
            "`QA / Review Agent`",
            "`Risk / Watchdog Agent`",
            "`Mission Control Agent`",
            "`approve`",
            "`revise`",
            "`escalate`",
            "`human_review`",
        ]

        for marker in required_markers:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
