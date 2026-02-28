from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import numpy as np

from app.rag.vertex_embedder import VertexEmbedder
from app.rag.retriever_faiss import FaissRetriever, RetrievedChunk
from app.rag.prompt_builder import build_grounded_prompt
from app.rag.vertex_llm import VertexGemini


@dataclass
class RagResult:
    answer: str
    chunks: List[RetrievedChunk]
    not_in_kb: bool


class RagService:
    def __init__(self, retriever: FaissRetriever) -> None:
        self.retriever = retriever
        self.embedder = VertexEmbedder()
        self.llm = VertexGemini()

    def answer(self, question: str, top_k: int = 4, max_distance: float = 1.2) -> RagResult:
        """
        max_distance is a simple relevance guardrail for L2 distance.
        Easy to tune: higher = more results but more noise; lower = fewer results but more likely in-KB.
        """
        qvec = self.embedder.embed_texts([question])[0]  # shape (dim,)
        chunks = self.retriever.search(qvec, top_k=top_k)

        # Guardrail: if all distances are "far", treat as not-in-kb.
        good = [c for c in chunks if c.score <= max_distance]

        if not good:
            return RagResult(
                answer="I couldn't find that in the provided help articles.",
                chunks=[],
                not_in_kb=True,
            )

        prompt = build_grounded_prompt(question, good)
        answer = self.llm.generate(prompt)

        # Extra guard: if model returns empty, fallback
        if not answer.strip():
            answer = "I couldn't find that in the provided help articles."

        return RagResult(answer=answer, chunks=good, not_in_kb=False)