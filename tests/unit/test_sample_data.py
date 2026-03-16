import unittest
from pathlib import Path

from app.models.schemas import EmailWorkflowRequest
from tests.sample_data import (
    chief_ai_analysis_payload,
    cto_cio_analysis_payload,
    DEFAULT_CONNECTOR_BOOTSTRAP_PROVIDER,
    DEFAULT_EMAIL_SOURCE_METADATA,
    approval_decision_payload,
    connector_bootstrap_status_response,
    email_workflow_payload,
    email_workflow_request,
    knowledge_query_payload,
    proposal_generation_payload,
    track_b_runtime_paths,
    track_b_settings_kwargs,
)


class SampleDataTests(unittest.TestCase):
    def test_email_workflow_payload_includes_source_metadata_by_default(self) -> None:
        payload = email_workflow_payload()

        self.assertEqual(payload["sender"], "client@example.com")
        self.assertEqual(payload["source_provider"], "microsoft_graph")
        self.assertEqual(payload["source_message_id"], DEFAULT_EMAIL_SOURCE_METADATA["source_message_id"])

    def test_email_workflow_payload_can_omit_source_metadata(self) -> None:
        payload = email_workflow_payload(include_source_metadata=False)

        self.assertNotIn("source_account_id", payload)
        self.assertNotIn("source_message_id", payload)
        self.assertNotIn("source_thread_id", payload)

    def test_email_workflow_request_builds_schema_object(self) -> None:
        request = email_workflow_request(subject="Need confirmation")

        self.assertIsInstance(request, EmailWorkflowRequest)
        self.assertEqual(request.subject, "Need confirmation")

    def test_approval_decision_payload_applies_defaults_and_overrides(self) -> None:
        payload = approval_decision_payload("edit", edited_reply="Rewritten draft")

        self.assertEqual(payload["decision"], "edit")
        self.assertEqual(payload["note"], "Revise it")
        self.assertEqual(payload["edited_reply"], "Rewritten draft")

    def test_other_payload_builders_clone_defaults(self) -> None:
        knowledge_payload = knowledge_query_payload(limit=5)
        proposal_payload = proposal_generation_payload(client_name="Beta Corp")
        cto_payload = cto_cio_analysis_payload(engagement_name="ERP Reset")
        chief_ai_payload = chief_ai_analysis_payload(engagement_name="AI Service Desk")

        self.assertEqual(knowledge_payload["limit"], 5)
        self.assertEqual(proposal_payload["client_name"], "Beta Corp")
        self.assertEqual(cto_payload["engagement_name"], "ERP Reset")
        self.assertEqual(chief_ai_payload["engagement_name"], "AI Service Desk")

    def test_connector_bootstrap_status_builder_returns_normalized_model(self) -> None:
        response = connector_bootstrap_status_response(status="degraded", detail="Needs refresh.")

        self.assertEqual(len(response.providers), 1)
        self.assertEqual(response.providers[0].provider_id, DEFAULT_CONNECTOR_BOOTSTRAP_PROVIDER["provider_id"])
        self.assertEqual(response.providers[0].status, "degraded")
        self.assertEqual(response.providers[0].detail, "Needs refresh.")

    def test_track_b_runtime_helpers_return_expected_paths_and_settings(self) -> None:
        root = Path("C:/repo")
        paths = track_b_runtime_paths(root, "acme")
        settings_kwargs = track_b_settings_kwargs(root, "acme")

        self.assertEqual(paths["env_path"], root / "config" / "clients" / "acme.env")
        self.assertEqual(paths["documents_dir"], root / "data" / "clients" / "acme" / "documents")
        self.assertEqual(settings_kwargs["tenant_id"], "acme")
        self.assertEqual(settings_kwargs["runtime_env_file"], str(paths["env_path"]))
        self.assertEqual(settings_kwargs["microsoft_graph_secrets_path"], str(paths["microsoft_secret_path"]))


if __name__ == "__main__":
    unittest.main()
