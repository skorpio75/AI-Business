# Copyright (c) Dario Pizzolante
"""Document ingestion entrypoint for local knowledge files."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.knowledge.ingestion import DocumentIngestionService
from app.knowledge.pgvector_store import PgVectorRetrievalService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest local markdown/text documents.")
    parser.add_argument("source", help="File or directory to ingest")
    parser.add_argument(
        "--persist-db",
        action="store_true",
        help="Persist ingested documents into PostgreSQL with pgvector embeddings",
    )
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    service = DocumentIngestionService()
    documents = service.ingest(args.source)
    print(f"ingested_count={len(documents)}")
    for document in documents:
        print(f"{document.source_path}|{document.content_length}")
    if args.persist_db:
        stored = PgVectorRetrievalService().upsert_documents(documents)
        print(f"persisted_count={stored}")
