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


class RecordingPromptLoader:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def render_composition(self, composition_id: str, *, template_context: dict | None = None, injected_context: dict | None = None) -> str:
        self.calls.append(
            {
                "composition_id": composition_id,
                "template_context": template_context or {},
                "injected_context": injected_context or {},
            }
        )
        return f"prompt:{composition_id}"


class EmailRoutingBranchTests(UnitTestCase):
    def test_draft_email_uses_email_specific_model_and_richer_prompt_context(self) -> None:
        gateway = ModelGateway(settings=self.build_settings())
        prompt_loader = RecordingPromptLoader()
        gateway.prompt_loader = prompt_loader
        text_calls: list[dict] = []

        def fake_text(**kwargs):
            text_calls.append(kwargs)
            return (
                TextGenerationResult(
                    content="I am reviewing the next checkpoint and any current blockers, and I will confirm timing today.",
                    provider_used="local",
                    model_used="ollama/test-email",
                    local_llm_invoked=True,
                ),
                True,
                None,
                None,
            )

        gateway._call_local_ollama_text = fake_text  # type: ignore[method-assign]

        result = gateway.draft_email(
            sender="client@example.com",
            subject="Need a delivery update",
            body="Can you confirm the next checkpoint and whether anything is blocked?",
            thread_context="Previous note: the plan was under review.",
            risk_level="medium",
        )

        self.assertEqual(result.provider_used, "local")
        self.assertEqual(text_calls[0]["local_model_override"], "llama3.2:3b")
        self.assertEqual(text_calls[0]["timeout_seconds"], 30)
        self.assertEqual(text_calls[0]["num_predict"], 180)
        self.assertEqual(
            {call["composition_id"] for call in prompt_loader.calls},
            {"email-operations.draft-reply"},
        )
        draft_call = next(call for call in prompt_loader.calls if call["composition_id"] == "email-operations.draft-reply")
        self.assertEqual(draft_call["injected_context"]["track"], "track_a_internal")
        self.assertEqual(draft_call["injected_context"]["operating_mode"], "internal_operating")
        self.assertIn("risk=medium", draft_call["injected_context"]["state_summary"])
        self.assertIn("Previous note", draft_call["injected_context"]["memory_context"])
        self.assertEqual(draft_call["template_context"]["sender"], "client@example.com")
        self.assertEqual(draft_call["template_context"]["risk_level"], "medium")
        self.assertIn("solo consulting CEO support", draft_call["injected_context"]["tenant_context"])

    def test_draft_email_retries_on_stronger_local_model_when_first_draft_is_generic(self) -> None:
        gateway = ModelGateway(settings=self.build_settings())
        text_calls: list[dict] = []

        def fake_text(**kwargs):
            text_calls.append(kwargs)
            if kwargs["local_model_override"] == "llama3.2:3b":
                return (
                    TextGenerationResult(
                        content="Thanks for your message. I reviewed your request and prepared a draft response.",
                        provider_used="local",
                        model_used="ollama/llama3.2:3b",
                        local_llm_invoked=True,
                    ),
                    True,
                    None,
                    None,
                )
            return (
                TextGenerationResult(
                    content="I am reviewing the next checkpoint, current blockers, and revised timing, and I will confirm the next step shortly.",
                    provider_used="local",
                    model_used="ollama/qwen2.5:1.5b-instruct-q4_K_M",
                    local_llm_invoked=True,
                ),
                True,
                None,
                None,
            )

        gateway._call_local_ollama_text = fake_text  # type: ignore[method-assign]

        result = gateway.draft_email(
            sender="client@example.com",
            subject="Need a delivery update",
            body="Can you confirm the next checkpoint and whether anything is blocked?",
            thread_context="Previous note: the plan was under review.",
            risk_level="medium",
        )

        self.assertEqual(len(text_calls), 2)
        self.assertEqual(text_calls[0]["local_model_override"], "llama3.2:3b")
        self.assertEqual(text_calls[1]["local_model_override"], "qwen2.5:1.5b-instruct-q4_K_M")
        self.assertEqual(result.provider_used, "local")
        self.assertEqual(result.model_used, "ollama/qwen2.5:1.5b-instruct-q4_K_M")
        self.assertEqual(result.escalation_reason, "routed_to_stronger_local")
        self.assertIn("next checkpoint", result.draft_reply)

    def test_draft_email_replaces_placeholder_heavy_output_with_guardrailed_fallback(self) -> None:
        gateway = ModelGateway(settings=self.build_settings())
        gateway._call_local_ollama_text = lambda **kwargs: (  # type: ignore[method-assign]
            TextGenerationResult(
                content=(
                    "Subject: Confirmation of Next Checkpoint\n\n"
                    "Dear [Client's Name],\n\n"
                    "The next milestone is scheduled for [Date].\n\n"
                    "Best regards,\n[Your Name]"
                ),
                provider_used="local",
                model_used="ollama/test-email",
                local_llm_invoked=True,
            ),
            True,
            None,
            None,
        )

        result = gateway.draft_email(
            sender="client@example.com",
            subject="Need a delivery update",
            body="Can you confirm the next checkpoint and whether anything is blocked?",
            thread_context="Previous note: the plan was under review.",
            risk_level="medium",
        )

        self.assertEqual(result.provider_used, "fallback-rule")
        self.assertEqual(result.model_used, "rules-v2-email-guardrail")
        self.assertIn(result.llm_diagnostic_code, {"email_draft_placeholder_detected", "multiple_llm_failures"})
        self.assertNotIn("[Client's Name]", result.draft_reply)
        self.assertNotIn("[Date]", result.draft_reply)
        self.assertIn("Need a delivery update", result.draft_reply)
        self.assertIn("next checkpoint", result.draft_reply)

    def test_draft_email_uses_fallback_local_model_before_cloud_when_primary_local_fails(self) -> None:
        gateway = ModelGateway(
            settings=self.build_settings(
                force_local_only=False,
                openrouter_api_key="test-key",
            )
        )
        text_calls: list[dict] = []

        def fake_text(**kwargs):
            text_calls.append(kwargs)
            if kwargs["local_model_override"] == "llama3.2:3b":
                return None, True, "local_ollama_timeout", "Primary local timed out."
            return (
                TextGenerationResult(
                    content="I am reviewing the next checkpoint and any current blockers, and I will confirm the next step shortly.",
                    provider_used="local",
                    model_used="ollama/qwen2.5:1.5b-instruct-q4_K_M",
                    local_llm_invoked=True,
                ),
                True,
                None,
                None,
            )

        gateway._call_local_ollama_text = fake_text  # type: ignore[method-assign]
        gateway._call_text_model = lambda **kwargs: self.fail("cloud should not be used when fallback local succeeds")  # type: ignore[method-assign]

        result = gateway.draft_email(
            sender="client@example.com",
            subject="Need a delivery update",
            body="Can you confirm the next checkpoint and whether anything is blocked?",
            thread_context="Previous note: the plan was under review.",
            risk_level="medium",
        )

        self.assertEqual(len(text_calls), 2)
        self.assertEqual(text_calls[0]["local_model_override"], "llama3.2:3b")
        self.assertEqual(text_calls[1]["local_model_override"], "qwen2.5:1.5b-instruct-q4_K_M")
        self.assertEqual(result.provider_used, "local")
        self.assertEqual(result.model_used, "ollama/qwen2.5:1.5b-instruct-q4_K_M")
        self.assertEqual(result.escalation_reason, "routed_to_fallback_local")
        self.assertIn(result.llm_diagnostic_code, {"local_ollama_timeout", "multiple_llm_failures"})

    def test_draft_email_marks_cloud_unconfigured_when_escalation_is_needed(self) -> None:
        gateway = ModelGateway(
            settings=self.build_settings(
                force_local_only=False,
                openrouter_api_key=None,
                local_confidence_threshold=0.9,
            )
        )
        gateway._call_local_ollama_text = lambda **kwargs: (  # type: ignore[method-assign]
            TextGenerationResult(
                content="Local draft",
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
                local_confidence_threshold=0.9,
            )
        )
        gateway._call_local_ollama_text = lambda **kwargs: (  # type: ignore[method-assign]
            TextGenerationResult(
                content="Local draft",
                provider_used="local",
                model_used="ollama/test-local",
                local_llm_invoked=True,
            ),
            True,
            None,
            None,
        )
        gateway._call_text_model = lambda **kwargs: (None, True, "cloud_llm_request_failed", "Cloud request failed.")  # type: ignore[method-assign]

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
                local_confidence_threshold=0.9,
            )
        )
        gateway._call_local_ollama_text = lambda **kwargs: (  # type: ignore[method-assign]
            TextGenerationResult(
                content="Local draft",
                provider_used="local",
                model_used="ollama/test-local",
                local_llm_invoked=True,
            ),
            True,
            None,
            None,
        )
        gateway._call_text_model = lambda **kwargs: (  # type: ignore[method-assign]
            TextGenerationResult(
                content="Cloud draft",
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
