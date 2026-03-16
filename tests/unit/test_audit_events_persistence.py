# Copyright (c) Dario Pizzolante
from types import SimpleNamespace
from unittest.mock import patch

from app.db.repository import list_audit_events
from app.knowledge.retrieval import RetrievalQuery, RetrievalResult
from app.models.schemas import KnowledgeQueryRequest
from app.services.email_workflow import EmailWorkflowService
from app.services.knowledge_qna import KnowledgeQnAService
from app.services.model_gateway import GenerationResult, TextGenerationResult
from tests.sample_data import email_workflow_request, knowledge_query_payload
from tests.unit.base import UnitTestCase


class StubEmailGateway:
    def draft_email(self, *, sender: str, subject: str, body: str, thread_context: str | None, risk_level: str) -> GenerationResult:
        del body, thread_context, risk_level
        return GenerationResult(
            intent="general-inquiry",
            confidence=0.88,
            draft_reply=f"Draft reply to {sender} about '{subject}'.",
            provider_used="local",
            model_used="stub/local",
            local_llm_invoked=True,
        )


class StubKnowledgeGateway:
    def __init__(self, track: str) -> None:
        self.settings = SimpleNamespace(primary_track=track)

    def generate_text(self, *, prompt: str, fallback_content: str, **kwargs) -> TextGenerationResult:
        del prompt, fallback_content, kwargs
        return TextGenerationResult(
            content="Grounded answer from stub.",
            provider_used="local",
            model_used="stub/local",
            local_llm_invoked=True,
        )


class StubRetrievalService:
    def search(self, query: RetrievalQuery) -> list[RetrievalResult]:
        return [
            RetrievalResult(
                source_path="docs/runbook.md",
                title="runbook",
                snippet=f"Grounding for {query.text}",
                score=1.0,
            )
        ]


class AuditEventsPersistenceTests(UnitTestCase):
    def test_email_workflow_persists_step_route_and_approval_events(self) -> None:
        service = EmailWorkflowService(model_gateway=StubEmailGateway())

        with self.sqlite_session() as db:
            with patch(
                "app.services.agent_run_logger.get_settings",
                return_value=SimpleNamespace(tenant_id="internal", primary_track="track_a_internal"),
            ), patch(
                "app.services.audit_event_logger.get_settings",
                return_value=SimpleNamespace(tenant_id="internal", primary_track="track_a_internal"),
            ):
                response = service.run(email_workflow_request(), db=db)
                audit_events = list_audit_events(db, workflow_id=response.workflow_id)

        self.assertEqual(
            {item.event_name for item in audit_events},
            {"workflow.step.completed", "model.route.selected", "approval.requested"},
        )
        self.assertTrue(any(item.step_id == "draft_email" for item in audit_events))
        self.assertTrue(any(item.step_id == "route_approval" for item in audit_events))
        self.assertTrue(any(item.approval_id == response.approval_id for item in audit_events))

    def test_knowledge_qna_persists_tool_and_step_events(self) -> None:
        service = KnowledgeQnAService(
            retrieval_service=StubRetrievalService(),
            model_gateway=StubKnowledgeGateway(track="track_b_client"),
        )

        with self.sqlite_session() as db:
            with patch(
                "app.services.agent_run_logger.get_settings",
                return_value=SimpleNamespace(tenant_id="acme", primary_track="track_b_client"),
            ), patch(
                "app.services.audit_event_logger.get_settings",
                return_value=SimpleNamespace(tenant_id="acme", primary_track="track_b_client"),
            ):
                service.answer(
                    payload=KnowledgeQueryRequest(**knowledge_query_payload()),
                    db=db,
                )
                audit_events = list_audit_events(db)

        self.assertEqual(
            {item.event_name for item in audit_events},
            {"tool.call.completed", "model.route.selected", "workflow.step.completed"},
        )
        self.assertTrue(any(item.tool_id == "memory.search" for item in audit_events))
        self.assertTrue(any(item.step_id == "answer_question" for item in audit_events))

