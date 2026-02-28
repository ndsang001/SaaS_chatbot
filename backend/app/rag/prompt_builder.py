from __future__ import annotations
from typing import List
from app.rag.retriever_faiss import RetrievedChunk


def build_grounded_prompt(question: str, chunks: List[RetrievedChunk]) -> str:
    """
    Strict grounding rules:
    - Answer ONLY using the provided context.
    - If not enough info, say don't know / not in KB.
    - Cite sources with [chunk_id].
    """
    context_blocks = []
    for c in chunks:
        context_blocks.append(
            f"Source [{c.chunk_id}] ({c.title}; {c.source}):\n{c.text}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    return f"""You are a customer support assistant for a SaaS web application.

Rules (must follow):
1) Use ONLY the information in the Context. Do not use outside knowledge.
2) If the answer is not clearly found in the Context, say: "I couldn't find that in the provided help articles."
3) When you use information from a source, cite it using [chunk_id] (example: [c00012]).
4) Provide a complete but concise answer (2-4 sentences).

User question:
{question}

Context:
{context}

Answer:
"""