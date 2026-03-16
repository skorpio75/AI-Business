# Copyright (c) Dario Pizzolante
import unittest

from tests.unit.base import ROOT, UnitTestCase

README_PATH = ROOT / "README.md"


class ReadmeTestingInstructionsTests(UnitTestCase):
    def test_readme_includes_current_test_execution_commands(self) -> None:
        self.assertTrue(README_PATH.is_file(), "Missing README.md")
        text = README_PATH.read_text(encoding="utf-8")

        required_markers = [
            "## Test Execution",
            ".\\.venv\\Scripts\\python.exe -m pytest -q",
            "tests\\unit",
            "tests\\integration",
            "tests\\workflow",
            "tests\\unit\\test_sample_data.py",
            "tests\\integration\\test_api_endpoints.py",
            "tests\\workflow\\test_email_workflow_branches.py",
            "tests\\sample_data.py",
            "docs/testing-strategy.md",
        ]

        for marker in required_markers:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
