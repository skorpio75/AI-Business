# Copyright (c) Dario Pizzolante
from app.db.repository import get_public_lead_submission, list_agent_runs, list_audit_events
from app.knowledge.retrieval import RetrievalQuery, RetrievalResult
from app.services.chief_ai_panel import ChiefAIPanelService
from app.services.cto_cio_panel import CTOCIOPanelService
from app.services.email_workflow import EmailWorkflowService
from app.services.knowledge_qna import KnowledgeQnAService
from app.services.model_gateway import GenerationResult, TextGenerationResult
from app.services.proposal_workflow import ProposalWorkflowService
from tests.integration.base import ApiIntegrationTestCase
from tests.sample_data import (
    approval_decision_payload,
    chief_ai_analysis_payload,
    connector_bootstrap_status_response,
    cto_cio_analysis_payload,
    email_workflow_payload,
    knowledge_query_payload,
    proposal_generation_payload,
    public_booking_payload,
)


class StubWorkflowGateway:
    def __init__(self) -> None:
        self.settings = type("StubSettings", (), {"primary_track": "track_a_internal"})()

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

    def generate_structured_json(self, *, prompt: str, fallback_payload: dict):
        del prompt
        return type(
            "StubStructuredResult",
            (),
            {
                "content": fallback_payload,
                "provider_used": "fallback-rule",
                "model_used": "rules-test",
                "local_llm_invoked": False,
                "cloud_llm_invoked": False,
                "llm_diagnostic_code": None,
                "llm_diagnostic_detail": None,
            },
        )()


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
        self.patch_api_attr("cto_cio_panel", CTOCIOPanelService(model_gateway=gateway))
        self.patch_api_attr("chief_ai_panel", ChiefAIPanelService(model_gateway=gateway))

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

    def test_agents_endpoint_exposes_governed_metadata_labels(self) -> None:
        response = self.client.get("/agents")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        cto_agent = next(item for item in payload if item["agent_id"] == "cto-cio-agent")
        self.assertEqual(cto_agent["governed_metadata"]["routing_posture"], "DO-C")
        self.assertIn("Direct Ollama", cto_agent["governed_metadata"]["routing_posture_label"])
        self.assertGreaterEqual(len(cto_agent["governed_metadata"]["tool_profiles"]), 1)

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

    def test_public_booking_endpoint_materializes_private_lead_submission(self) -> None:
        response = self.client.post(
            "/public/booking-requests",
            json=public_booking_payload(),
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "received")
        self.assertEqual(payload["source_class"], "website_form")
        self.assertEqual(payload["submission_kind"], "booking_request")

        with self._session_factory() as db:
            stored = get_public_lead_submission(db, payload["submission_id"])
            audit_events = list_audit_events(db)

        self.assertIsNotNone(stored)
        assert stored is not None
        self.assertEqual(stored.lead_id, payload["lead_id"])
        self.assertEqual(stored.status, "received")
        event_names = [item.event_name for item in audit_events if item.entity_id == payload["submission_id"]]
        self.assertIn("agent.run.started", event_names)
        self.assertIn("agent.run.completed", event_names)

    def test_agent_runs_are_persisted_for_workflows_and_specialist_analyses(self) -> None:
        email_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(),
        )
        knowledge_response = self.client.post(
            "/knowledge/qna",
            json=knowledge_query_payload(),
        )
        proposal_response = self.client.post(
            "/workflows/proposal-generation/run",
            json=proposal_generation_payload(),
        )
        cto_response = self.client.post(
            "/specialists/cto-cio/analyze",
            json=cto_cio_analysis_payload(),
        )
        chief_ai_response = self.client.post(
            "/specialists/chief-ai-digital-strategy/analyze",
            json=chief_ai_analysis_payload(),
        )

        self.assertEqual(email_response.status_code, 200)
        self.assertEqual(knowledge_response.status_code, 200)
        self.assertEqual(proposal_response.status_code, 200)
        self.assertEqual(cto_response.status_code, 200)
        self.assertEqual(chief_ai_response.status_code, 200)

        with self._session_factory() as db:
            agent_runs = list_agent_runs(db)

        self.assertEqual(len(agent_runs), 5)
        self.assertEqual(
            {item.agent_id for item in agent_runs},
            {
                "email-agent",
                "knowledge-agent",
                "proposal-sow-agent",
                "cto-cio-agent",
                "chief-ai-digital-strategy-agent",
            },
        )
        self.assertEqual(
            {item.mode for item in agent_runs if item.agent_id in {"cto-cio-agent", "chief-ai-digital-strategy-agent"}},
            {"client_facing_service"},
        )
        self.assertTrue(
            any(item.workflow_id == email_response.json()["workflow_id"] for item in agent_runs if item.agent_id == "email-agent")
        )
        self.assertTrue(
            any(item.workflow_id == proposal_response.json()["workflow_id"] for item in agent_runs if item.agent_id == "proposal-sow-agent")
        )

    def test_audit_events_capture_approval_and_tool_timeline(self) -> None:
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
        workflow_id = run_response.json()["workflow_id"]
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

        with self._session_factory() as db:
            audit_events = list_audit_events(db, workflow_id=workflow_id)

        event_names = [item.event_name for item in audit_events]
        self.assertIn("approval.requested", event_names)
        self.assertIn("approval.decided", event_names)
        self.assertIn("outbound.action.requested", event_names)
        self.assertIn("tool.call.completed", event_names)
        self.assertTrue(any(item.tool_id == "email.send_external" for item in audit_events))
        self.assertTrue(any(item.approval_id == approval_id for item in audit_events))

    def test_workflow_trace_endpoint_returns_run_approval_and_event_bundle(self) -> None:
        run_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(),
        )

        self.assertEqual(run_response.status_code, 200)
        workflow_id = run_response.json()["workflow_id"]

        trace_response = self.client.get(f"/audit/workflows/{workflow_id}")

        self.assertEqual(trace_response.status_code, 200)
        payload = trace_response.json()
        self.assertEqual(payload["workflow_id"], workflow_id)
        self.assertEqual(payload["workflow_run"]["workflow_id"], workflow_id)
        self.assertEqual(payload["approval"]["workflow_id"], workflow_id)
        self.assertGreaterEqual(len(payload["agent_runs"]), 1)
        self.assertGreaterEqual(len(payload["audit_events"]), 1)

    def test_specialist_panel_endpoints_include_governed_metadata(self) -> None:
        cto_response = self.client.get("/specialists/cto-cio/panel")
        chief_ai_response = self.client.get("/specialists/chief-ai-digital-strategy/panel")
        finance_response = self.client.get("/specialists/finance/panel")

        self.assertEqual(cto_response.status_code, 200)
        self.assertEqual(chief_ai_response.status_code, 200)
        self.assertEqual(finance_response.status_code, 200)
        self.assertEqual(cto_response.json()["governed_metadata"]["routing_posture"], "DO-C")
        self.assertEqual(chief_ai_response.json()["governed_metadata"]["routing_posture"], "DO-C")
        self.assertTrue(all("governed_metadata" in item for item in finance_response.json()["agents"]))

    def test_approval_trace_endpoint_returns_decision_timeline(self) -> None:
        run_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(
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
        decide_response = self.client.post(
            f"/approvals/{approval_id}/decision",
            json=approval_decision_payload(),
        )

        self.assertEqual(decide_response.status_code, 200)

        trace_response = self.client.get(f"/audit/approvals/{approval_id}")

        self.assertEqual(trace_response.status_code, 200)
        payload = trace_response.json()
        self.assertEqual(payload["approval_id"], approval_id)
        self.assertEqual(payload["approval"]["status"], "approved")
        self.assertTrue(any(item["event_name"] == "approval.decided" for item in payload["audit_events"]))

    def test_agent_trace_endpoint_returns_runs_and_events_for_one_agent(self) -> None:
        response = self.client.post(
            "/specialists/cto-cio/analyze",
            json=cto_cio_analysis_payload(),
        )

        self.assertEqual(response.status_code, 200)

        trace_response = self.client.get("/audit/agents/cto-cio-agent?limit=5")

        self.assertEqual(trace_response.status_code, 200)
        payload = trace_response.json()
        self.assertEqual(payload["agent"]["agent_id"], "cto-cio-agent")
        self.assertGreaterEqual(len(payload["agent_runs"]), 1)
        self.assertGreaterEqual(len(payload["audit_events"]), 1)
        self.assertTrue(all(item["agent_id"] == "cto-cio-agent" for item in payload["agent_runs"]))

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
