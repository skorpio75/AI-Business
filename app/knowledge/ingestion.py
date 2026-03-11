from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SUPPORTED_EXTENSIONS = {".md", ".txt"}


@dataclass
class IngestedDocument:
    source_path: str
    title: str
    content: str
    content_length: int


class DocumentIngestionService:
    def __init__(self, supported_extensions: set[str] | None = None) -> None:
        self.supported_extensions = supported_extensions or SUPPORTED_EXTENSIONS

    def collect_files(self, root: Path) -> list[Path]:
        if root.is_file():
            return [root] if root.suffix.lower() in self.supported_extensions else []
        return sorted(
            path
            for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in self.supported_extensions
        )

    def ingest_paths(self, paths: Iterable[Path]) -> list[IngestedDocument]:
        documents: list[IngestedDocument] = []
        for path in paths:
            content = path.read_text(encoding="utf-8")
            documents.append(
                IngestedDocument(
                    source_path=str(path),
                    title=path.stem,
                    content=content,
                    content_length=len(content),
                )
            )
        return documents

    def ingest(self, source: str) -> list[IngestedDocument]:
        root = Path(source)
        if not root.exists():
            raise FileNotFoundError(f"source_not_found:{source}")
        paths = self.collect_files(root)
        return self.ingest_paths(paths)
