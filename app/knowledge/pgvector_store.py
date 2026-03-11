import hashlib
import math

from sqlalchemy import text

from app.core.settings import get_settings
from app.db.session import engine
from app.knowledge.ingestion import IngestedDocument
from app.knowledge.retrieval import RetrievalQuery, RetrievalResult, RetrievalService


def embed_text(text_value: str, dimensions: int) -> list[float]:
    vector = [0.0] * dimensions
    tokens = [token.lower() for token in text_value.split() if token.strip()]
    if not tokens:
        return vector

    for token in tokens:
        digest = hashlib.md5(token.encode("utf-8")).digest()
        bucket = int.from_bytes(digest[:2], "big") % dimensions
        sign = 1.0 if digest[2] % 2 == 0 else -1.0
        vector[bucket] += sign

    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return vector
    return [value / magnitude for value in vector]


def to_vector_literal(values: list[float]) -> str:
    return "[" + ",".join(f"{value:.8f}" for value in values) + "]"


class PgVectorRetrievalService(RetrievalService):
    def __init__(self) -> None:
        self.settings = get_settings()
        self.dimensions = self.settings.knowledge_vector_dimensions

    def upsert_documents(self, documents: list[IngestedDocument]) -> int:
        upsert_sql = text(
            """
            INSERT INTO knowledge_documents (source_path, title, content, content_length, embedding)
            VALUES (:source_path, :title, :content, :content_length, CAST(:embedding AS vector))
            ON CONFLICT (source_path) DO UPDATE
            SET title = EXCLUDED.title,
                content = EXCLUDED.content,
                content_length = EXCLUDED.content_length,
                embedding = EXCLUDED.embedding
            """
        )
        count = 0
        with engine.begin() as conn:
            for document in documents:
                embedding = embed_text(document.content, self.dimensions)
                conn.execute(
                    upsert_sql,
                    {
                        "source_path": document.source_path,
                        "title": document.title,
                        "content": document.content,
                        "content_length": document.content_length,
                        "embedding": to_vector_literal(embedding),
                    },
                )
                count += 1
        return count

    def search(self, query: RetrievalQuery) -> list[RetrievalResult]:
        vector = embed_text(query.text, self.dimensions)
        sql = text(
            """
            SELECT
                source_path,
                title,
                LEFT(REPLACE(content, E'\n', ' '), 180) AS snippet,
                1 - (embedding <=> CAST(:embedding AS vector)) AS score
            FROM knowledge_documents
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
            """
        )
        with engine.begin() as conn:
            rows = conn.execute(
                sql,
                {"embedding": to_vector_literal(vector), "limit": query.limit},
            ).mappings()
            return [
                RetrievalResult(
                    source_path=row["source_path"],
                    title=row["title"],
                    snippet=row["snippet"],
                    score=float(row["score"]),
                )
                for row in rows
            ]
