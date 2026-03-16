# Copyright (c) Dario Pizzolante
import unittest

from tests.unit.base import ROOT, UnitTestCase

DOC_PATH = ROOT / "docs" / "agent-instance-portfolio-model.md"
PLATFORM_MODEL_PATH = ROOT / "PLATFORM_MODEL.md"
ARCHITECTURE_PATH = ROOT / "ARCHITECTURE.md"
ROADMAP_PATH = ROOT / "ROADMAP.md"
DECISIONS_PATH = ROOT / "DECISIONS.md"


class AgentInstancePortfolioModelTests(UnitTestCase):
    def test_doc_exists_and_covers_instance_binding_and_portfolio_visibility(self) -> None:
        self.assertTrue(DOC_PATH.is_file(), "Missing agent instance portfolio doc")
        text = DOC_PATH.read_text(encoding="utf-8")

        required_markers = [
            "# Agent Instance and Portfolio Model",
            "`family`",
            "`mode`",
            "`instance`",
            "`client`",
            "`engagement`",
            "`mission`",
            "`agent_instance`",
            "`agent_assignment`",
            "Track A Mission Control",
            "`agents_dispatched`",
            "AI-Business_IDE_Handoff.md",
        ]

        for marker in required_markers:
            self.assertIn(marker, text)

    def test_core_governance_docs_reference_portfolio_instance_model(self) -> None:
        platform_text = PLATFORM_MODEL_PATH.read_text(encoding="utf-8")
        architecture_text = ARCHITECTURE_PATH.read_text(encoding="utf-8")
        roadmap_text = ROADMAP_PATH.read_text(encoding="utf-8")
        decisions_text = DECISIONS_PATH.read_text(encoding="utf-8")

        for marker in ["`AgentInstance`", "`AgentAssignment`", "`Engagement`", "`Mission`"]:
            self.assertIn(marker, platform_text)

        self.assertIn("portfolio cockpit", architecture_text)
        self.assertIn("docs/agent-instance-portfolio-model.md", architecture_text)

        for marker in ["B-T47", "B-T48", "B-T49", "B-T50"]:
            self.assertIn(marker, roadmap_text)

        for marker in ["ADR-048", "ADR-049", "client, engagement, and mission"]:
            self.assertIn(marker, decisions_text)


if __name__ == "__main__":
    unittest.main()
