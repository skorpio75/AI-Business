# Copyright (c) Dario Pizzolante
from app.knowledge.retrieval import RetrievalQuery, RetrievalResult
from app.services.email_workflow import EmailWorkflowService
from app.services.knowledge_qna import KnowledgeQnAService
from app.services.model_gateway import GenerationResult, ModelGateway, TextGenerationResult
from app.services.proposal_workflow import ProposalWorkflowService
from tests.integration.base import ApiIntegrationTestCase
from tests.sample_data import approval_decision_payload, email_workflow_payload
from tests.unit.base import UnitTestCase


class StubWorkflowGateway:
    def generate_text(self, *, prompt: str, fallback_content: str, **kwargs) -> TextGenerationResult:
        del prompt, fallback_content, kwargs
        return TextGenerationResult(
            content="Generated content from workflow-branch stub.",
            provider_used="local",
            model_used="stub/local",
            local_llm_invoked=True,
        )

    def draft_email(
        self,
        *,
        sender: str,
        subject: str,
        body: str,
        thread_context: str | None,
        risk_level: str,
    ) -> GenerationResult:
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


class StubPersonalAssistantContextService:
    def __init__(self) -> None:
        self.inbox_connector = self
        self.replies: list[dict[str, str]] = []

    def reply_to_message(self, *, account_id: str, message_id: str, reply_body: str) -> None:
        self.replies.append(
            {"account_id": account_id, "message_id": message_id, "reply_body": reply_body}
        )


class EmailRoutingBranchTests(UnitTestCase):
    def test_draft_email_marks_cloud_unconfigured_when_escalation_is_needed(self) -> None:
        gateway = ModelGateway(
            settings=self.build_settings(
                force_local_only=False,
                openrouter_api_key=None,
                local_confidence_threshold=0.8,
            )
        )
        gateway._call_local_ollama_structured = lambda **kwargs: (  # type: ignore[method-assign]
            GenerationResult(
                intent="urgent-request",
                confidence=0.41,
                draft_reply="Local draft",
                provider_used="local",
                model_used="ollama/test-local",
                local_llm_invoked=True,
            ),
            True,
            None,
            None,
        )

        result = gateway.draft_email(
            sender="client@example.com",
            subject="Urgent help needed",
            body="Please respond quickly.",
            thread_context=None,
            risk_level="high",
        )

        self.assertEqual(result.provider_used, "local")
        self.assertEqual(result.escalation_reason, "cloud_unconfigured_used_local")
        self.assertEqual(result.llm_diagnostic_code, "cloud_unconfigured")
        self.assertTrue(result.local_llm_invoked)

    def test_draft_email_marks_cloud_unavailable_when_cloud_call_fails(self) -> None:
        gateway = ModelGateway(
            settings=self.build_settings(
                force_local_only=False,
                openrouter_api_key="test-key",
                local_confidence_threshold=0.8,
            )
        )
        gateway._call_local_ollama_structured = lambda **kwargs: (  # type: ignore[method-assign]
            GenerationResult(
                intent="general-inquiry",
                confidence=0.44,
                draft_reply="Local draft",
                provider_used="local",
                model_used="ollama/test-local",
                local_llm_invoked=True,
            ),
            True,
            None,
            None,
        )
        gateway._call_model = lambda **kwargs: (None, True, "cloud_llm_request_failed", "Cloud request failed.")  # type: ignore[method-assign]

        result = gateway.draft_email(
            sender="client@example.com",
            subject="Need review",
            body="Please review the attached plan.",
            thread_context=None,
            risk_level="medium",
        )

        self.assertEqual(result.provider_used, "local")
        self.assertEqual(result.escalation_reason, "cloud_unavailable_used_local")
        self.assertEqual(result.llm_diagnostic_code, "cloud_llm_request_failed")
        self.assertTrue(result.cloud_llm_invoked)

    def test_draft_email_routes_to_cloud_when_cloud_result_is_available(self) -> None:
        gateway = ModelGateway(
            settings=self.build_settings(
                force_local_only=False,
                openrouter_api_key="test-key",
                local_confidence_threshold=0.8,
            )
        )
        gateway._call_local_ollama_structured = lambda **kwargs: (  # type: ignore[method-assign]
            GenerationResult(
                intent="general-inquiry",
                confidence=0.40,
                draft_reply="Local draft",
                provider_used="local",
                model_used="ollama/test-local",
                local_llm_invoked=True,
            ),
            True,
            None,
            None,
        )
        gateway._call_model = lambda **kwargs: (  # type: ignore[method-assign]
            GenerationResult(
                intent="general-inquiry",
                confidence=0.95,
                draft_reply="Cloud draft",
                provider_used="cloud",
                model_used="openrouter/test-cloud",
                cloud_llm_invoked=True,
            ),
            True,
            None,
            None,
        )

        result = gateway.draft_email(
            sender="client@example.com",
            subject="Need strategy",
            body="Please provide a careful response.",
            thread_context=None,
            risk_level="medium",
        )

        self.assertEqual(result.provider_used, "cloud")
        self.assertEqual(result.escalation_reason, "routed_to_cloud")
        self.assertEqual(result.model_used, "openrouter/test-cloud")
        self.assertTrue(result.local_llm_invoked)
        self.assertTrue(result.cloud_llm_invoked)


class ApprovalWorkflowBranchTests(ApiIntegrationTestCase):
    def setUp(self) -> None:
        super().setUp()
        gateway = StubWorkflowGateway()
        self.patch_api_attr("email_workflow", EmailWorkflowService(model_gateway=gateway))
        self.patch_api_attr(
            "knowledge_qna",
            KnowledgeQnAService(retrieval_service=StubRetrievalService(), model_gateway=gateway),
        )
        self.patch_api_attr("proposal_workflow", ProposalWorkflowService(model_gateway=gateway))

    def test_approval_reject_marks_workflow_completed_and_clears_pending_queue(self) -> None:
        run_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(
                subject="Need rejection",
                body="Please reject this draft.",
                source_message_id="msg-reject",
                source_thread_id="thread-reject",
            ),
        )
        approval_id = run_response.json()["approval_id"]

        decision_response = self.client.post(
            f"/approvals/{approval_id}/decision",
            json=approval_decision_payload("reject"),
        )

        self.assertEqual(decision_response.status_code, 200)
        payload = decision_response.json()
        self.assertEqual(payload["status"], "rejected")
        self.assertEqual(payload["send_status"], "not_applicable")

        runs_response = self.client.get("/workflows/runs")
        approvals_response = self.client.get("/approvals/pending")

        self.assertEqual(runs_response.json()[0]["status"], "completed")
        self.assertEqual(runs_response.json()[0]["approval_status"], "rejected")
        self.assertEqual(runs_response.json()[0]["send_status"], "not_applicable")
        self.assertEqual(approvals_response.json(), [])

    def test_approval_edit_requires_reply_body(self) -> None:
        run_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(
                subject="Need edit",
                body="Please revise this draft.",
                source_message_id="msg-edit-missing",
                source_thread_id="thread-edit-missing",
            ),
        )
        approval_id = run_response.json()["approval_id"]

        decision_response = self.client.post(
            f"/approvals/{approval_id}/decision",
            json=approval_decision_payload("edit"),
        )

        self.assertEqual(decision_response.status_code, 400)
        self.assertEqual(decision_response.json()["detail"], "edited_reply_required")

    def test_approval_edit_keeps_item_pending_and_updates_draft(self) -> None:
        run_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(
                subject="Need edit branch",
                body="Please revise this draft.",
                source_message_id="msg-edit",
                source_thread_id="thread-edit",
            ),
        )
        approval_id = run_response.json()["approval_id"]
        edited_reply = "Updated draft kept pending for approval."

        decision_response = self.client.post(
            f"/approvals/{approval_id}/decision",
            json=approval_decision_payload(
                "edit",
                edited_reply=edited_reply,
                note="Reworded",
            ),
        )

        self.assertEqual(decision_response.status_code, 200)
        payload = decision_response.json()
        self.assertEqual(payload["status"], "pending")
        self.assertEqual(payload["draft_reply"], edited_reply)
        self.assertEqual(payload["send_status"], "pending")

        runs_response = self.client.get("/workflows/runs")
        approvals_response = self.client.get("/approvals/pending")

        self.assertEqual(runs_response.json()[0]["status"], "pending_approval")
        self.assertEqual(runs_response.json()[0]["approval_status"], "pending")
        self.assertEqual(runs_response.json()[0]["send_status"], "pending")
        self.assertEqual(approvals_response.json()[0]["draft_reply"], edited_reply)

    def test_approval_approve_without_source_message_sets_not_applicable_send_status(self) -> None:
        run_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(
                include_source_metadata=False,
                subject="Approve without source",
                body="There is no source message metadata on this item.",
            ),
        )
        approval_id = run_response.json()["approval_id"]
        assistant_context = StubPersonalAssistantContextService()
        self.patch_api_attr(
            "build_personal_assistant_context_service",
            lambda current_settings: assistant_context,
        )

        decision_response = self.client.post(
            f"/approvals/{approval_id}/decision",
            json=approval_decision_payload(
                "approve",
                note="Approved without outbound send",
            ),
        )

        self.assertEqual(decision_response.status_code, 200)
        payload = decision_response.json()
        self.assertEqual(payload["status"], "approved")
        self.assertEqual(payload["send_status"], "not_applicable")
        self.assertEqual(assistant_context.replies, [])

        runs_response = self.client.get("/workflows/runs")
        approvals_response = self.client.get("/approvals/pending")

        self.assertEqual(runs_response.json()[0]["status"], "completed")
        self.assertEqual(runs_response.json()[0]["approval_status"], "approved")
        self.assertEqual(runs_response.json()[0]["send_status"], "not_applicable")
        self.assertEqual(approvals_response.json(), [])

    def test_workflow_endpoint_records_cloud_escalation_metadata(self) -> None:
        class EscalationGateway(StubWorkflowGateway):
            def draft_email(
                self,
                *,
                sender: str,
                subject: str,
                body: str,
                thread_context: str | None,
                risk_level: str,
            ) -> GenerationResult:
                del sender, subject, body, thread_context, risk_level
                return GenerationResult(
                    intent="urgent-request",
                    confidence=0.55,
                    draft_reply="Escalated cloud-backed draft.",
                    provider_used="cloud",
                    model_used="openrouter/test-cloud",
                    escalation_reason="routed_to_cloud",
                    local_llm_invoked=True,
                    cloud_llm_invoked=True,
                    llm_diagnostic_code="local_llm_invalid_schema",
                    llm_diagnostic_detail="Local structured output failed schema validation before cloud escalation.",
                )

        self.patch_api_attr("email_workflow", EmailWorkflowService(model_gateway=EscalationGateway()))

        run_response = self.client.post(
            "/workflows/email-operations/run",
            json=email_workflow_payload(
                include_source_metadata=False,
                subject="Need escalated handling",
                body="This should be routed to the cloud path.",
            ),
        )

        self.assertEqual(run_response.status_code, 200)
        payload = run_response.json()
        self.assertEqual(payload["provider_used"], "cloud")
        self.assertEqual(payload["escalation_reason"], "routed_to_cloud")
        self.assertEqual(payload["llm_diagnostic_code"], "local_llm_invalid_schema")
