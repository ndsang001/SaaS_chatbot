import time
import json
from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse, SourceItem
from app.core.config import settings
from app.storage.sqlite import get_conn

router = APIRouter()

def db_conn():
    return get_conn(settings.sqlite_path)

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, conn=Depends(db_conn)):
    start = time.perf_counter()

    # Phase 1 placeholder: no retrieval, no LLM call yet.
    answer = "Prototype backend is running. RAG will be enabled in Phase 3."
    sources = []

    latency_ms = int((time.perf_counter() - start) * 1000)

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO chat_turns (session_id, user_question, retrieved_chunk_ids, model_answer, latency_ms)
        VALUES (?, ?, ?, ?, ?)
        """,
        (req.session_id, req.question, json.dumps([]), answer, latency_ms)
    )
    conn.commit()
    turn_id = cur.lastrowid

    return ChatResponse(
        turn_id=turn_id,
        answer=answer,
        sources=[SourceItem(**s) for s in sources],
        latency_ms=latency_ms,
        not_in_kb=True
    )