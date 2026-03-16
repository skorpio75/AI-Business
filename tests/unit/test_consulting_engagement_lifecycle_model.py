# Copyright (c) Dario Pizzolante
import unittest

from tests.unit.base import ROOT, UnitTestCase

DOC_PATH = ROOT / "docs" / "consulting-engagement-lifecycle-model.md"
WORKFLOWS_PATH = ROOT / "WORKFLOWS.md"
EVENT_MODEL_PATH = ROOT / "EVENT_MODEL.md"
ROADMAP_PATH = ROOT / "ROADMAP.md"
DECISIONS_PATH = ROOT / "DECISIONS.md"
ARCHITECTURE_PATH = ROOT / "ARCHITECTURE.md"


class ConsultingEngagementLifecycleModelTests(UnitTestCase):
    def test_doc_exists_and_covers_dispatch_billing_and_closeout(self) -> None:
        self.assertTrue(DOC_PATH.is_file(), "Missing consulting engagement lifecycle doc")
        text = DOC_PATH.read_text(encoding="utf-8")

        required_markers = [
            "# Consulting Engagement Lifecycle Model",
            "Track A is the control plane",
            "Track B is the delivery plane",
            "`dispatch_candidate_plan`",
            "`approved_consultant_roster`",
            "`billing_plan`",
            "`milestone.accepted`",
            "`contract.signed`",
            "`dispatch.plan.approved`",
            "`mission_closeout`",
        ]

        for marker in required_markers:
            self.assertIn(marker, text)

    def test_related_docs_reference_lifecycle_contracts(self) -> None:
        workflows_text = WORKFLOWS_PATH.read_text(encoding="utf-8")
        event_text = EVENT_MODEL_PATH.read_text(encoding="utf-8")
        roadmap_text = ROADMAP_PATH.read_text(encoding="utf-8")
        decisions_text = DECISIONS_PATH.read_text(encoding="utf-8")
        architecture_text = ARCHITECTURE_PATH.read_text(encoding="utf-8")

        for marker in [
            "Signed Scope to Mission Startup",
            "Milestone Acceptance to Billing",
            "Mission Closeout",
        ]:
            self.assertIn(marker, workflows_text)

        for marker in [
            "`contract.signed`",
            "`dispatch.plan.proposed`",
            "`dispatch.plan.approved`",
            "`mission.approved`",
            "`milestone.acceptance.requested`",
            "`milestone.accepted`",
            "`mission.closed`",
        ]:
            self.assertIn(marker, event_text)

        for marker in ["B-T55", "B-T56", "B-T57", "B-T58", "B-T59", "B-T60", "B-T61"]:
            self.assertIn(marker, roadmap_text)

        for marker in ["ADR-051", "ADR-052", "`dispatch_candidate_plan`", "`billing_plan`"]:
            self.assertIn(marker, decisions_text)

        self.assertIn("docs/consulting-engagement-lifecycle-model.md", architecture_text)


if __name__ == "__main__":
    unittest.main()
