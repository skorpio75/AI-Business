# Copyright (c) Dario Pizzolante
import unittest

from tests.unit.base import ROOT, UnitTestCase

DOC_PATH = ROOT / "docs" / "delivery-quality-gate-model.md"
WORKFLOWS_PATH = ROOT / "WORKFLOWS.md"
ROADMAP_PATH = ROOT / "ROADMAP.md"
DECISIONS_PATH = ROOT / "DECISIONS.md"
ARCHITECTURE_PATH = ROOT / "ARCHITECTURE.md"


class DeliveryQualityGateModelTests(UnitTestCase):
    def test_doc_exists_and_covers_phase_aware_quality_gates(self) -> None:
        self.assertTrue(DOC_PATH.is_file(), "Missing delivery quality gate doc")
        text = DOC_PATH.read_text(encoding="utf-8")

        required_markers = [
            "# Delivery Quality Gate Model",
            "`quality_gate_plan`",
            "`quality_gate_checkpoint`",
            "`quality_gate_result`",
            "`document_review_gate`",
            "`implementation_review_gate`",
            "`handover_readiness_gate`",
            "`QA / Review Agent`",
            "`Testing / QA Agent`",
            "`Documentation Agent`",
            "`approve`",
            "`revise`",
            "`blocked`",
        ]

        for marker in required_markers:
            self.assertIn(marker, text)

    def test_related_docs_reference_delivery_quality_gate_pattern(self) -> None:
        workflows_text = WORKFLOWS_PATH.read_text(encoding="utf-8")
        roadmap_text = ROADMAP_PATH.read_text(encoding="utf-8")
        decisions_text = DECISIONS_PATH.read_text(encoding="utf-8")
        architecture_text = ARCHITECTURE_PATH.read_text(encoding="utf-8")

        for marker in [
            "mission-specific `quality_gate_plan`",
            "Quality and Testing Gate",
            "handover-readiness gate",
        ]:
            self.assertIn(marker, workflows_text)

        for marker in ["B-T62", "B-T63", "B-T64", "B-T65", "B-T66"]:
            self.assertIn(marker, roadmap_text)

        for marker in ["ADR-053", "`quality_gate_plan`", "phase-aware"]:
            self.assertIn(marker, decisions_text)

        self.assertIn("docs/delivery-quality-gate-model.md", architecture_text)


if __name__ == "__main__":
    unittest.main()
