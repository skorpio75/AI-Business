# Copyright (c) Dario Pizzolante
from dataclasses import dataclass
from typing import Protocol

from app.knowledge.ingestion import IngestedDocument


@dataclass
class RetrievalQuery:
    text: str
    limit: int = 5


@dataclass
class RetrievalResult:
    source_path: str
    title: str
    snippet: str
    score: float


class RetrievalService(Protocol):
    def search(self, query: RetrievalQuery) -> list[RetrievalResult]:
        ...


class KeywordRetrievalService:
    def __init__(self, documents: list[IngestedDocument]) -> None:
        self.documents = documents

    def search(self, query: RetrievalQuery) -> list[RetrievalResult]:
        terms = [term.lower() for term in query.text.split() if term.strip()]
        if not terms:
            return []

        scored: list[RetrievalResult] = []
        for document in self.documents:
            content_lower = document.content.lower()
            score = float(sum(content_lower.count(term) for term in terms))
            if score <= 0:
                continue
            snippet = self._build_snippet(document.content, terms)
            scored.append(
                RetrievalResult(
                    source_path=document.source_path,
                    title=document.title,
                    snippet=snippet,
                    score=score,
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[: query.limit]

    def _build_snippet(self, content: str, terms: list[str], width: int = 180) -> str:
        content_lower = content.lower()
        for term in terms:
            idx = content_lower.find(term)
            if idx >= 0:
                start = max(0, idx - width // 3)
                end = min(len(content), start + width)
                return content[start:end].replace("\n", " ").strip()
        return content[:width].replace("\n", " ").strip()
