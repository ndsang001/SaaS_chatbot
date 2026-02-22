from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Client-generated session id")
    question: str = Field(..., min_length=1)

class SourceItem(BaseModel):
    chunk_id: str
    title: str
    section: Optional[str] = None
    source: Optional[str] = None  # url or file path

class ChatResponse(BaseModel):
    turn_id: int
    answer: str
    sources: List[SourceItem]
    latency_ms: int
    not_in_kb: bool = False