from pydantic import BaseModel, Field
from typing import Optional, Literal

class FeedbackRequest(BaseModel):
    turn_id: int
    rating: Literal["up", "down"]
    comment: Optional[str] = Field(default=None, max_length=500)

class FeedbackResponse(BaseModel):
    ok: bool = True