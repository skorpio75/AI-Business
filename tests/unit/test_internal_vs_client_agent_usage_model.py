# Copyright (c) Dario Pizzolante
import unittest

from tests.unit.base import ROOT, UnitTestCase

DOC_PATH = ROOT / "docs" / "internal-vs-client-agent-usage-model.md"
AGENTS_PATH = ROOT / "AGENTS.md"
PLATFORM_MODEL_PATH = ROOT / "PLATFORM_MODEL.md"
CONSULTING_LIFECYCLE_PATH = ROOT / "docs" / "consulting-engagement-lifecycle-model.md"
ARCHITECTURE_PATH = ROOT / "ARCHITECTURE.md"
DECISIONS_PATH = ROOT / "DECISIONS.md"


class InternalVsClientAgentUsageModelTests(UnitTestCase):
    def test_doc_exists_and_covers_mode_selection_rule(self) -> None:
        self.assertTrue(DOC_PATH.is_file(), "Missing internal vs client agent usage doc")
        text = DOC_PATH.read_text(encoding="utf-8")

        required_markers = [
            "# Internal vs Client Agent Usage Model",
            "`internal_operating`",
            "`client_delivery`",
            "`client_facing_service`",
            "Track A is where `internal_operating` agents live",
            "Track B is where `client_delivery`",
            "Track A decides, shapes, approves, bills, and oversees",
            "Track B executes, evidences, and delivers",
        ]

        for marker in required_markers:
            self.assertIn(marker, text)

    def test_related_docs_reference_internal_vs_client_usage_rule(self) -> None:
        agents_text = AGENTS_PATH.read_text(encoding="utf-8")
        platform_text = PLATFORM_MODEL_PATH.read_text(encoding="utf-8")
        lifecycle_text = CONSULTING_LIFECYCLE_PATH.read_text(encoding="utf-8")
        architecture_text = ARCHITECTURE_PATH.read_text(encoding="utf-8")
        decisions_text = DECISIONS_PATH.read_text(encoding="utf-8")

        self.assertIn("Mode Selection Rule", agents_text)
        self.assertIn("Mode Usage Rule", platform_text)
        self.assertIn("Agent Usage Rule", lifecycle_text)
        self.assertIn("docs/internal-vs-client-agent-usage-model.md", architecture_text)

        for marker in ["ADR-054", "`internal_operating`", "`client_delivery`"]:
            self.assertIn(marker, decisions_text)


if __name__ == "__main__":
    unittest.main()
