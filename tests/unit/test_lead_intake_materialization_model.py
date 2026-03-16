import unittest

from tests.unit.base import ROOT, UnitTestCase

DOC_PATH = ROOT / "docs" / "lead-intake-materialization-model.md"
WORKFLOWS_PATH = ROOT / "WORKFLOWS.md"
EVENT_MODEL_PATH = ROOT / "EVENT_MODEL.md"
ROADMAP_PATH = ROOT / "ROADMAP.md"
DECISIONS_PATH = ROOT / "DECISIONS.md"


class LeadIntakeMaterializationModelTests(UnitTestCase):
    def test_doc_exists_and_covers_source_and_materialization_model(self) -> None:
        self.assertTrue(DOC_PATH.is_file(), "Missing lead intake materialization doc")
        text = DOC_PATH.read_text(encoding="utf-8")

        required_markers = [
            "# Lead Intake and Materialization Model",
            "`lead_signal`",
            "`lead_candidate`",
            "`lead`",
            "`manual_entry`",
            "`inbound_email`",
            "`website_form`",
            "`calendar_booking`",
            "`web_research`",
            "`lead.signal.detected`",
            "`lead.materialized`",
            "`lead.received`",
            "Track A",
        ]

        for marker in required_markers:
            self.assertIn(marker, text)

    def test_related_governance_docs_reference_lead_materialization(self) -> None:
        workflows_text = WORKFLOWS_PATH.read_text(encoding="utf-8")
        event_text = EVENT_MODEL_PATH.read_text(encoding="utf-8")
        roadmap_text = ROADMAP_PATH.read_text(encoding="utf-8")
        decisions_text = DECISIONS_PATH.read_text(encoding="utf-8")

        for marker in [
            "`lead.signal.detected`",
            "`lead.candidate.created`",
            "`lead.review.requested`",
            "`lead.materialized`",
        ]:
            self.assertIn(marker, workflows_text)
            self.assertIn(marker, event_text)

        self.assertIn("Lead Signal to Opportunity Intake", workflows_text)

        for marker in ["B-T51", "B-T52", "B-T53", "B-T54"]:
            self.assertIn(marker, roadmap_text)

        for marker in ["ADR-050", "lead_signal", "lead.received"]:
            self.assertIn(marker, decisions_text)


if __name__ == "__main__":
    unittest.main()
