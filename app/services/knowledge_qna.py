from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.prompt_loader import PromptLoader
from app.knowledge.retrieval import RetrievalQuery, RetrievalService
from app.models.schemas import (
    KnowledgeCitation,
    KnowledgeQueryRequest,
    KnowledgeQueryResponse,
)
from app.services.agent_run_logger import record_agent_run, subject_from_identity
from app.services.model_gateway import ModelGateway
from app.services.observability import NullObservabilityService

KNOWLEDGE_AGENT_INTERNAL_SUBJECT = subject_from_identity(
    agent_id="knowledge-agent",
    agent_family="knowledge-agent",
    mode="internal_operating",
    autonomy_class="assistant",
    approval_class="bounded",
)
KNOWLEDGE_AGENT_CLIENT_SUBJECT = subject_from_identity(
    agent_id="knowledge-agent",
    agent_family="knowledge-agent",
    mode="client_delivery",
    autonomy_class="assistant",
    approval_class="bounded",
)


class KnowledgeQnAService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        model_gateway: ModelGateway,
        observability: NullObservabilityService | None = None,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.model_gateway = model_gateway
        self.prompt_loader = PromptLoader()
        self.observability = observability or getattr(model_gateway, "observability", NullObservabilityService())

    def answer(self, payload: KnowledgeQueryRequest, db: Session | None = None) -> KnowledgeQueryResponse:
        started_at = datetime.now(timezone.utc)
        try:
            with self.observability.start_span(
                name="workflow.knowledge-qna.answer",
                input={"question": payload.question, "limit": payload.limit},
                metadata={"workflow_type": "knowledge-qna"},
            ) as observation:
                matches = self.retrieval_service.search(RetrievalQuery(text=payload.question, limit=payload.limit))
                citations = [
                    KnowledgeCitation(
                        title=match.title,
                        source_path=match.source_path,
                        snippet=match.snippet,
                        score=match.score,
                    )
                    for match in matches
                ]

                if not citations:
                    response = KnowledgeQueryResponse(
                        question=payload.question,
                        answer=(
                            "I could not find grounded internal documents for that question yet. "
                            "Ingest relevant documents first or ask a narrower question."
                        ),
                        citations=[],
                        grounded=False,
                        provider_used="fallback-rule",
                        model_used="rules-v1",
                        local_llm_invoked=False,
                        cloud_llm_invoked=False,
                        llm_diagnostic_code="knowledge_context_missing",
                        llm_diagnostic_detail=(
                            "No grounded citations were available for this question, so the service returned the built-in non-LLM fallback answer."
                        ),
                    )
                    if db is not None:
                        record_agent_run(
                            db,
                            subject=self._subject_for_current_track(),
                            status="completed",
                            started_at=started_at,
                            ended_at=datetime.now(timezone.utc),
                            trigger_event_name="knowledge.retrieved",
                            input_ref="knowledge_query_request",
                            provider_used=response.provider_used,
                            model_used=response.model_used,
                        )
                        db.commit()
                    observation.update(
                        output=response.model_dump(mode="json"),
                        metadata={"grounded": False, "citation_count": 0},
                    )
                    return response

                context = "\n\n".join(
                    f"Source: {item.title} ({item.source_path})\nSnippet: {item.snippet}" for item in citations
                )
                fallback_answer = self._fallback_answer(payload.question, citations)
                prompt = self.prompt_loader.render_composition(
                    "knowledge-qna.answer-question",
                    template_context={
                        "question": payload.question,
                        "context": context,
                    },
                    injected_context={
                        "memory_context": "Use only retrieved internal document evidence as grounding context.",
                        "output_schema": "plain_text_answer_with_supporting_grounding",
                        "tool_profile": "memory.search + docs.read only; no unstated external sources",
                    },
                )
                generation = self.model_gateway.generate_text(
                    prompt=prompt,
                    fallback_content=fallback_answer,
                )
                response = KnowledgeQueryResponse(
                    question=payload.question,
                    answer=generation.content,
                    citations=citations,
                    grounded=True,
                    provider_used=generation.provider_used,
                    model_used=generation.model_used,
                    local_llm_invoked=generation.local_llm_invoked,
                    cloud_llm_invoked=generation.cloud_llm_invoked,
                    llm_diagnostic_code=generation.llm_diagnostic_code,
                    llm_diagnostic_detail=generation.llm_diagnostic_detail,
                )
                if db is not None:
                    record_agent_run(
                        db,
                        subject=self._subject_for_current_track(),
                        status="completed",
                        started_at=started_at,
                        ended_at=datetime.now(timezone.utc),
                        trigger_event_name="knowledge.retrieved",
                        input_ref="knowledge_query_request",
                        provider_used=response.provider_used,
                        model_used=response.model_used,
                    )
                    db.commit()
                observation.update(
                    output=response.model_dump(mode="json"),
                    metadata={
                        "grounded": True,
                        "citation_count": len(citations),
                        "provider_used": response.provider_used,
                        "model_used": response.model_used,
                    },
                )
                return response
        except Exception as exc:
            if db is not None:
                db.rollback()
                try:
                    record_agent_run(
                        db,
                        subject=self._subject_for_current_track(),
                        status="failed",
                        started_at=started_at,
                        ended_at=datetime.now(timezone.utc),
                        trigger_event_name="knowledge.retrieved",
                        input_ref="knowledge_query_request",
                        error_code=exc.__class__.__name__,
                        error_detail=str(exc),
                    )
                    db.commit()
                except Exception:
                    db.rollback()
            raise

    def _fallback_answer(
        self, question: str, citations: list[KnowledgeCitation]
    ) -> str:
        top_titles = ", ".join(item.title for item in citations[:2])
        top_snippets = " ".join(item.snippet for item in citations[:2])
        return (
            f"Grounded answer for '{question}': based on {top_titles}, the strongest available "
            f"context indicates that {top_snippets}"
        )

    def _subject_for_current_track(self):
        if getattr(self.model_gateway.settings, "primary_track", "track_a_internal") == "track_b_client":
            return KNOWLEDGE_AGENT_CLIENT_SUBJECT
        return KNOWLEDGE_AGENT_INTERNAL_SUBJECT
