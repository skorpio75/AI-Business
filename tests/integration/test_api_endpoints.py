from app.knowledge.retrieval import RetrievalQuery, RetrievalResult
from app.services.email_workflow import EmailWorkflowService
from app.services.knowledge_qna import KnowledgeQnAService
from app.services.model_gateway import GenerationResult, TextGenerationResult
from app.services.proposal_workflow import ProposalWorkflowService
from tests.integration.base import ApiIntegrationTestCase
from tests.sample_data import (
    approval_decision_payload,
    connector_bootstrap_status_response,
    email_workflow_payload,
    knowledge_query_payload,
    proposal_generation_payload,
)


class StubWorkflowGateway:
    def generate_text(self, *, prompt: str, fallback_content: str, **kwargs) -> TextGenerationResult:
        del prompt, fallback_content, kwargs
        return TextGenerationResult(
            content="Generated content from integration stub.",
            provider_used="local",
            model_used="stub/local",
            local_llm_invoked=True,
        )

    def draft_email(self, *, sender: str, subject: str, body: str, thread_context: str | None, risk_level: str) -> GenerationResult:
        del body, thread_context, risk_level
        return GenerationResult(
            intent="general-inquiry",
            confidence=0.92,
            draft_reply=f"Draft reply to {sender} about '{subject}'.",
            provider_used="local",
            model_used="stub/local",
            local_llm_invoked=True,
        )


class StubRetrievalService:
    def search(self, query: RetrievalQuery) -> list[RetrievalResult]:
        return [
            RetrievalResult(
                source_path="docs/client-playbook.md",
                title="client-playbook",
                snippet=f"Grounded answer support for {query.text}",
                score=1.0,
            )
        ]


class RecordingInboxConnector:
    def __init__(self) -> None:
        self.replies: list[dict[str, str]] = []

    def reply_to_message(self, *, account_id: str, message_id: str, reply_body: str) -> None:
        self.replies.append(
            {"account_id": account_id, "message_id": message_id, "reply_body": reply_body}
        )


class StubPersonalAssistantContextService:
    def __init__(self, inbox_connector: RecordingInboxConnector) -> None:
        self.inbox_connector = inbox_connector


class ApiEndpointIntegrationTests(ApiIntegrationTestCase):
    def setUp(self) -> None:
        super().setUp()
        gateway = StubWorkflowGateway()
        self.patch_api_attr("email_workflow", EmailWorkflowService(model_gateway=gateway))
        self.patch_api_attr(
            "knowledge_qna",
            KnowledgeQnAService(retrieval_service=StubRetrievalService(), model_gateway=gateway),
        )
        self.patch_api_attr("proposal_workflow", ProposalWorkflowService(model_gateway=gateway))

    def test_healthz_returns_runtime_metadata(self) -> None:
        response = self.client.get("/healthz")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("app", payload)
        self.assertIn("local_model", payload)
        self.assertIn("cloud_model", payload)

    def test_email_workflow_run_and_list_endpoints_round_trip(self) -> None:
        run_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(),
        )

        self.assertEqual(run_response.status_code, 200)
        run_payload = run_response.json()
        self.assertEqual(run_payload["status"], "pending_approval")
        self.assertEqual(run_payload["provider_used"], "local")
        self.assertEqual(run_payload["send_status"], "pending")

        runs_response = self.client.get("/workflows/runs")
        approvals_response = self.client.get("/approvals/pending")

        self.assertEqual(runs_response.status_code, 200)
        self.assertEqual(approvals_response.status_code, 200)
        self.assertEqual(len(runs_response.json()), 1)
        self.assertEqual(len(approvals_response.json()), 1)
        self.assertEqual(approvals_response.json()[0]["workflow_id"], run_payload["workflow_id"])

    def test_approval_decision_approve_sends_reply_and_updates_state(self) -> None:
        run_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(
                subject="Need approval",
                body="Please send the approved follow-up.",
                source_message_id="msg-approve",
                source_thread_id="thread-approve",
            ),
        )
        approval_id = run_response.json()["approval_id"]
        inbox_connector = RecordingInboxConnector()
        self.patch_api_attr(
            "build_personal_assistant_context_service",
            lambda current_settings: StubPersonalAssistantContextService(inbox_connector),
        )

        decision_response = self.client.post(
            f"/approvals/{approval_id}/decision",
            json=approval_decision_payload(),
        )

        self.assertEqual(decision_response.status_code, 200)
        payload = decision_response.json()
        self.assertEqual(payload["status"], "approved")
        self.assertEqual(payload["send_status"], "sent")
        self.assertEqual(len(inbox_connector.replies), 1)

        runs_response = self.client.get("/workflows/runs")
        approvals_response = self.client.get("/approvals/pending")

        self.assertEqual(runs_response.json()[0]["approval_status"], "approved")
        self.assertEqual(runs_response.json()[0]["send_status"], "sent")
        self.assertEqual(approvals_response.json(), [])

    def test_knowledge_qna_endpoint_returns_grounded_payload(self) -> None:
        response = self.client.post(
            "/knowledge/qna",
            json=knowledge_query_payload(),
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["grounded"])
        self.assertEqual(payload["provider_used"], "local")
        self.assertEqual(len(payload["citations"]), 1)

    def test_proposal_generation_endpoint_returns_draft(self) -> None:
        response = self.client.post(
            "/workflows/proposal-generation/run",
            json=proposal_generation_payload(),
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["provider_used"], "local")
        self.assertIn("Proposal draft for Acme", payload["title"])
        self.assertEqual(payload["proposal_draft"], "Generated content from integration stub.")

    def test_connector_bootstrap_status_endpoint_returns_normalized_response(self) -> None:
        expected = connector_bootstrap_status_response()
        self.patch_api_attr("describe_provider_bootstrap", lambda settings: expected)

        response = self.client.get("/connectors/bootstrap-status")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["providers"][0]["provider_id"], "microsoft_graph")
        self.assertEqual(payload["providers"][0]["status"], "ready")

    def test_email_workflow_endpoint_rejects_invalid_payload(self) -> None:
        response = self.client.post(
            "/workflows/email-operations/run",
            json={"sender": "", "subject": "", "body": ""},
        )

        self.assertEqual(response.status_code, 422)
