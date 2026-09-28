"""Local embedding and FAISS retrieval services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from src.chunking import TextChunk

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@dataclass(frozen=True)
class RetrievalResult:
    chunk: TextChunk
    score: float


class PolicyIndex:
    """A session-scoped FAISS index and its position-aligned chunk metadata."""

    def __init__(self, index: faiss.Index, chunks: Sequence[TextChunk]) -> None:
        self._index = index
        self._chunks = list(chunks)

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)

    @classmethod
    def build(cls, chunks: Sequence[TextChunk], model: SentenceTransformer) -> "PolicyIndex":
        if not chunks:
            raise ValueError("Cannot build an index without chunks.")
        vectors = model.encode(
            [chunk.text for chunk in chunks],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        vectors = np.ascontiguousarray(vectors, dtype=np.float32)
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)
        return cls(index, chunks)

    def search(self, question: str, model: SentenceTransformer, top_k: int) -> list[RetrievalResult]:
        if not question.strip():
            return []
        query = model.encode(
            [question], convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False
        )
        scores, positions = self._index.search(np.ascontiguousarray(query, dtype=np.float32), min(top_k, self.chunk_count))
        return [
            RetrievalResult(chunk=self._chunks[position], score=float(score))
            for score, position in zip(scores[0], positions[0])
            if position >= 0
        ]

