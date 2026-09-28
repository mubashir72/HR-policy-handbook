"""Text splitting that preserves PDF page provenance."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from src.pdf_processing import ExtractedPage


@dataclass(frozen=True)
class TextChunk:
    chunk_id: str
    document_name: str
    page_number: int
    text: str


def _split_at_boundary(text: str, limit: int) -> int:
    """Choose a readable split point no later than the requested length."""
    if len(text) <= limit:
        return len(text)
    candidates = [text.rfind("\n", 0, limit + 1), text.rfind(". ", 0, limit + 1), text.rfind(" ", 0, limit + 1)]
    boundary = max(candidates)
    return boundary + 1 if boundary >= max(1, limit // 2) else limit


def chunk_pages(
    pages: Sequence[ExtractedPage], document_name: str, chunk_size: int = 800, overlap: int = 120
) -> list[TextChunk]:
    """Create overlapping chunks per page, never joining text across pages."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be at least zero and smaller than chunk_size")

    safe_name = Path(document_name).name
    chunks: list[TextChunk] = []
    for page in pages:
        text = page.text.strip()
        start = 0
        chunk_number = 1
        while start < len(text):
            end = start + _split_at_boundary(text[start:], chunk_size)
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    TextChunk(
                        chunk_id=f"p{page.page_number}-c{chunk_number}",
                        document_name=safe_name,
                        page_number=page.page_number,
                        text=chunk_text,
                    )
                )
                chunk_number += 1
            if end >= len(text):
                break
            start = max(end - overlap, start + 1)
    if not chunks:
        raise ValueError("No usable text chunks could be created.")
    return chunks

