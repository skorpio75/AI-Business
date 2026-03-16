import unittest

import yaml

from app.models.delivery_quality import DEFAULT_QUALITY_GATE_REGISTRY, QUALITY_GATE_TEMPLATE_BY_ID
from app.models.operating_state import ProjectState
from tests.unit.base import ROOT, UnitTestCase

QUALITY_GATE_CONFIG_PATH = ROOT / "config" / "base" / "quality_gates.yaml"
CLIENT_TEMPLATE_PATH = ROOT / "config" / "client-template" / "client.yaml"


class DeliveryQualityContractTests(UnitTestCase):
    def test_default_registry_defines_expected_templates_and_checkpoint_shapes(self) -> None:
        template_ids = {template.template_id for template in DEFAULT_QUALITY_GATE_REGISTRY.templates}
        self.assertEqual(template_ids, {"advisory_light", "delivery_standard", "implementation_heavy"})
        self.assertIn("delivery_standard", QUALITY_GATE_TEMPLATE_BY_ID)

        implementation_template = QUALITY_GATE_TEMPLATE_BY_ID["implementation_heavy"]
        self.assertTrue(any(checkpoint.phase == "implementation" for checkpoint in implementation_template.checkpoints))
        self.assertTrue(any(checkpoint.gate_type == "milestone_release_gate" for checkpoint in implementation_template.checkpoints))

    def test_project_state_supports_quality_gate_plan_linkage(self) -> None:
        project_state = ProjectState(
            id="mission-001",
            tenant_id="client-template",
            client_id="client-template",
            status="active",
            project_manager="pmo-project-control-agent",
            current_phase="implementation",
            risk_level="medium",
            quality_gate_plan_id="qgp-001",
            active_quality_gate_ids=["implementation-artifact-review"],
            quality_gate_status="in_review",
            quality_gate_result_refs=["gate-result-001"],
        )

        self.assertEqual(project_state.quality_gate_plan_id, "qgp-001")
        self.assertEqual(project_state.active_quality_gate_ids, ["implementation-artifact-review"])
        self.assertEqual(project_state.quality_gate_status, "in_review")
        self.assertEqual(project_state.quality_gate_result_refs, ["gate-result-001"])

    def test_yaml_registry_and_client_template_default_align_with_backend_contract(self) -> None:
        yaml_registry = yaml.safe_load(QUALITY_GATE_CONFIG_PATH.read_text(encoding="utf-8"))
        template_ids = {
            template["template_id"] for template in yaml_registry["quality_gate_registry"]["templates"]
        }
        self.assertEqual(template_ids, {"advisory_light", "delivery_standard", "implementation_heavy"})

        client_config = yaml.safe_load(CLIENT_TEMPLATE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(client_config["runtime_defaults"]["default_quality_gate_template"], "delivery_standard")
        self.assertIn(
            client_config["runtime_defaults"]["default_quality_gate_template"],
            template_ids,
        )


if __name__ == "__main__":
    unittest.main()
