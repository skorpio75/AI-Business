from app.core.prompt_loader import PromptLoader
from app.knowledge.retrieval import RetrievalQuery, RetrievalService
from app.models.schemas import (
    KnowledgeCitation,
    KnowledgeQueryRequest,
    KnowledgeQueryResponse,
)
from app.services.model_gateway import ModelGateway


class KnowledgeQnAService:
    def __init__(self, retrieval_service: RetrievalService, model_gateway: ModelGateway) -> None:
        self.retrieval_service = retrieval_service
        self.model_gateway = model_gateway
        self.prompt_loader = PromptLoader()

    def answer(self, payload: KnowledgeQueryRequest) -> KnowledgeQueryResponse:
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
            return KnowledgeQueryResponse(
                question=payload.question,
                answer=(
                    "I could not find grounded internal documents for that question yet. "
                    "Ingest relevant documents first or ask a narrower question."
                ),
                citations=[],
                grounded=False,
                provider_used="fallback-rule",
                model_used="rules-v1",
            )

        context = "\n\n".join(
            f"Source: {item.title} ({item.source_path})\nSnippet: {item.snippet}" for item in citations
        )
        fallback_answer = self._fallback_answer(payload.question, citations)
        prompt = self.prompt_loader.render(
            "knowledge/knowledge_qna_prompt.txt",
            question=payload.question,
            context=context,
        )
        generation = self.model_gateway.generate_text(
            prompt=prompt,
            fallback_content=fallback_answer,
        )
        return KnowledgeQueryResponse(
            question=payload.question,
            answer=generation.content,
            citations=citations,
            grounded=True,
            provider_used=generation.provider_used,
            model_used=generation.model_used,
        )

    def _fallback_answer(
        self, question: str, citations: list[KnowledgeCitation]
    ) -> str:
        top_titles = ", ".join(item.title for item in citations[:2])
        top_snippets = " ".join(item.snippet for item in citations[:2])
        return (
            f"Grounded answer for '{question}': based on {top_titles}, the strongest available "
            f"context indicates that {top_snippets}"
        )
