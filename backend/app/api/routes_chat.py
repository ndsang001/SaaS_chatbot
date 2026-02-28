import time
import json
from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse, SourceItem
from app.core.config import settings
from app.storage.sqlite import get_conn
from app.rag.service import RagService
from app.rag.retriever_faiss import FaissRetriever

router = APIRouter()

# Create singletons (simple + demo-friendly)
_retriever = None
_rag = None

def get_rag() -> RagService:
    global _retriever, _rag
    if _rag is None:
        _retriever = FaissRetriever(settings.faiss_index_path, settings.meta_path)
        _rag = RagService(_retriever)
    return _rag

def db_conn():
    return get_conn(settings.sqlite_path)

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, conn=Depends(db_conn)):
    start = time.perf_counter()

    rag = get_rag()
    rag_result = rag.answer(req.question, top_k=4)

    latency_ms = int((time.perf_counter() - start) * 1000)

    retrieved_ids = [c.chunk_id for c in rag_result.chunks]
    sources = [
        SourceItem(
            chunk_id=c.chunk_id,
            title=c.title,
            section=c.section,
            source=c.source,
        )
        for c in rag_result.chunks
    ]

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO chat_turns (session_id, user_question, retrieved_chunk_ids, model_answer, latency_ms, not_in_kb)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (req.session_id, req.question, json.dumps(retrieved_ids), rag_result.answer, latency_ms, int(rag_result.not_in_kb))
    )
    conn.commit()
    turn_id = cur.lastrowid

    return ChatResponse(
        turn_id=turn_id,
        answer=rag_result.answer,
        sources=sources,
        latency_ms=latency_ms,
        not_in_kb=rag_result.not_in_kb
    )