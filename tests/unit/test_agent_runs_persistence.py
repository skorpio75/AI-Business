from types import SimpleNamespace
from unittest.mock import patch

from app.db.repository import list_agent_runs
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


class AgentRunsPersistenceTests(UnitTestCase):
    def test_email_workflow_persists_agent_run_with_workflow_linkage(self) -> None:
        service = EmailWorkflowService(model_gateway=StubEmailGateway())

        with self.sqlite_session() as db:
            with patch(
                "app.services.agent_run_logger.get_settings",
                return_value=SimpleNamespace(tenant_id="internal", primary_track="track_a_internal"),
            ):
                response = service.run(email_workflow_request(), db=db)
                agent_runs = list_agent_runs(db, workflow_id=response.workflow_id)

        self.assertEqual(len(agent_runs), 1)
        agent_run = agent_runs[0]
        self.assertEqual(agent_run.agent_id, "email-agent")
        self.assertEqual(agent_run.workflow_id, response.workflow_id)
        self.assertEqual(agent_run.run_id, response.workflow_id)
        self.assertEqual(agent_run.step_id, "draft_email")
        self.assertEqual(agent_run.status, "completed")
        self.assertEqual(agent_run.provider_used, "local")

    def test_knowledge_qna_uses_client_delivery_mode_for_track_b_runs(self) -> None:
        service = KnowledgeQnAService(
            retrieval_service=StubRetrievalService(),
            model_gateway=StubKnowledgeGateway(track="track_b_client"),
        )

        with self.sqlite_session() as db:
            with patch(
                "app.services.agent_run_logger.get_settings",
                return_value=SimpleNamespace(tenant_id="acme", primary_track="track_b_client"),
            ):
                response = service.answer(
                    payload=KnowledgeQueryRequest(**knowledge_query_payload()),
                    db=db,
                )
                agent_runs = list_agent_runs(db)

        self.assertTrue(response.grounded)
        self.assertEqual(len(agent_runs), 1)
        agent_run = agent_runs[0]
        self.assertEqual(agent_run.agent_id, "knowledge-agent")
        self.assertEqual(agent_run.mode, "client_delivery")
        self.assertEqual(agent_run.tenant_id, "acme")
        self.assertEqual(agent_run.track, "track_b_client")
