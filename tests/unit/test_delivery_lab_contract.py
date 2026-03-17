# Copyright (c) Dario Pizzolante
import unittest

import yaml

from app.models.delivery_lab import (
    DEFAULT_DELIVERY_LAB_CONTRACT_REGISTRY,
    ActivationRequest,
    AdHocSession,
    AgentInvokeRequest,
    CreateHandoverPackRequest,
    HandoverPack,
    LabMission,
    ReadinessGateResult,
)
from app.models.operating_state import DEFAULT_STATE_REGISTRY
from tests.unit.base import ROOT, UnitTestCase

DELIVERY_LAB_CONFIG_PATH = ROOT / "config" / "base" / "delivery_lab.yaml"
STATE_REGISTRY_CONFIG_PATH = ROOT / "config" / "base" / "state_registry.yaml"
DOC_PATH = ROOT / "docs" / "delivery-lab-operating-model.md"
HANDOVER_DOC_PATH = ROOT / "docs" / "handover-pack-schema.md"


class DeliveryLabContractTests(UnitTestCase):
    def test_default_delivery_lab_registry_defines_expected_objects(self) -> None:
        object_ids = {item.object_id for item in DEFAULT_DELIVERY_LAB_CONTRACT_REGISTRY.objects}
        self.assertEqual(
            object_ids,
            {
                "ad_hoc_session",
                "lab_mission",
                "handover_pack",
                "readiness_gate_result",
                "activation_request",
            },
        )

    def test_runtime_payload_models_accept_the_planned_contract_shapes(self) -> None:
        invoke_request = AgentInvokeRequest(
            family_id="project-management-delivery-coordination",
            scope_kind="ad_hoc_session",
            task_template_id="generate-project-plan",
            title="CRM rollout planning draft",
            goal="Draft a practical first-pass project plan for a CRM rollout.",
            inputs={"project_name": "CRM rollout"},
            output_schema_id="project-plan-v1",
        )
        self.assertEqual(invoke_request.scope_kind, "ad_hoc_session")
        self.assertEqual(invoke_request.mode, "internal_operating")

        session = AdHocSession(
            session_id="lab-session-001",
            tenant_id="internal",
            family_id="project-management-delivery-coordination",
            title="CRM rollout planning draft",
            goal="Draft a practical first-pass project plan.",
            task_template_id="generate-project-plan",
            output_schema_id="project-plan-v1",
        )
        self.assertEqual(session.track, "track_a_internal")

        lab_mission = LabMission(
            lab_mission_id="lab-crm-rollout-001",
            tenant_id="internal",
            title="Internal CRM rollout rehearsal",
            goal="Rehearse the CRM rollout delivery motion before client activation.",
            mission_brief="Rehearse project planning and handover preparation for a CRM rollout.",
            owner_role="CEO",
            assigned_family_ids=["project-management-delivery-coordination", "qa-review"],
        )
        self.assertEqual(lab_mission.last_readiness_posture, "not_started")

        handover_request = CreateHandoverPackRequest(
            target_client_id="acme",
            target_engagement_id="acme-crm-rollout",
            target_mission_name="Discovery Mission",
            approved_roster_ref="artifact://roster/acme-crm-rollout.json",
        )
        self.assertEqual(handover_request.target_client_id, "acme")

        handover_pack = HandoverPack(
            handover_pack_id="hp-acme-crm-rollout-001",
            tenant_id="internal",
            source_lab_mission_id="lab-crm-rollout-001",
            target_client_id="acme",
            target_engagement_id="acme-crm-rollout",
            target_mission_name="Discovery Mission",
            mission_brief_ref="artifact://handover/hp-acme-crm-rollout-001/mission-brief.md",
            approved_roster_ref="artifact://handover/hp-acme-crm-rollout-001/roster.json",
        )
        self.assertEqual(handover_pack.readiness_status, "not_started")

        readiness_result = ReadinessGateResult(
            readiness_gate_result_id="rg-001",
            handover_pack_id="hp-acme-crm-rollout-001",
            status="ready",
            review_summary="Pack is ready for activation.",
            rubric_version="track-b-activation-readiness-v1",
        )
        self.assertEqual(readiness_result.status, "ready")

        activation = ActivationRequest(
            activation_request_id="act-001",
            handover_pack_id="hp-acme-crm-rollout-001",
            tenant_id="internal",
            target_tenant_id="acme",
            runtime_env_ref="config/clients/acme.env",
            activation_mode="seed_and_start",
        )
        self.assertEqual(activation.status, "queued")

    def test_state_registry_and_yaml_include_delivery_lab_states(self) -> None:
        ownership_ids = {item.state_id for item in DEFAULT_STATE_REGISTRY.ownership}
        persistence_ids = {item.state_id for item in DEFAULT_STATE_REGISTRY.persistence}
        expected_ids = {
            "ad_hoc_session_state",
            "lab_mission_state",
            "handover_pack_state",
            "readiness_gate_result_state",
            "activation_request_state",
        }
        self.assertTrue(expected_ids.issubset(ownership_ids))
        self.assertTrue(expected_ids.issubset(persistence_ids))

        yaml_registry = yaml.safe_load(STATE_REGISTRY_CONFIG_PATH.read_text(encoding="utf-8"))["state_registry"]
        yaml_ownership_ids = {item["state_id"] for item in yaml_registry["ownership"]}
        yaml_persistence_ids = {item["state_id"] for item in yaml_registry["persistence"]}
        self.assertTrue(expected_ids.issubset(yaml_ownership_ids))
        self.assertTrue(expected_ids.issubset(yaml_persistence_ids))

    def test_delivery_lab_yaml_registry_aligns_with_backend_contract(self) -> None:
        yaml_registry = yaml.safe_load(DELIVERY_LAB_CONFIG_PATH.read_text(encoding="utf-8"))
        yaml_object_ids = {item["object_id"] for item in yaml_registry["delivery_lab_registry"]["objects"]}
        backend_object_ids = {item.object_id for item in DEFAULT_DELIVERY_LAB_CONTRACT_REGISTRY.objects}
        self.assertEqual(yaml_object_ids, backend_object_ids)

    def test_related_docs_exist_for_delivery_lab_and_handover_contracts(self) -> None:
        self.assertTrue(DOC_PATH.is_file(), "Missing delivery lab operating model doc")
        self.assertTrue(HANDOVER_DOC_PATH.is_file(), "Missing handover pack schema doc")
        self.assertIn("`ad_hoc_session`", DOC_PATH.read_text(encoding="utf-8"))
        self.assertIn("`handover_pack`", HANDOVER_DOC_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
