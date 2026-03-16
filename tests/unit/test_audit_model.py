# Copyright (c) Dario Pizzolante
import unittest

from tests.unit.base import ROOT, UnitTestCase

AUDIT_MODEL_PATH = ROOT / "AUDIT_MODEL.md"


class AuditModelTests(UnitTestCase):
    def test_audit_model_exists_and_covers_core_audit_contracts(self) -> None:
        self.assertTrue(AUDIT_MODEL_PATH.is_file(), "Missing AUDIT_MODEL.md")
        text = AUDIT_MODEL_PATH.read_text(encoding="utf-8")

        required_markers = [
            "# Audit Model",
            "`agent_run`",
            "`audit_event`",
            "`agent_runs`",
            "`audit_events`",
            "`approval.requested`",
            "`approval.decided`",
            "`tool.call.started`",
            "`tool_id`",
            "`trace_ref`",
            "`approval_id`",
            "`run_id`",
            "Langfuse",
            "TOOLS.md",
            "EVENT_MODEL.md",
        ]

        for marker in required_markers:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
