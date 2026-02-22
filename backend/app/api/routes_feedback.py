from fastapi import APIRouter, Depends, HTTPException
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.core.config import settings
from app.storage.sqlite import get_conn

router = APIRouter()

def db_conn():
    return get_conn(settings.sqlite_path)

@router.post("/feedback", response_model=FeedbackResponse)
def feedback(req: FeedbackRequest, conn=Depends(db_conn)):
    cur = conn.cursor()

    # Ensure chat_turn exists
    cur.execute("SELECT id FROM chat_turns WHERE id = ?", (req.turn_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="turn_id not found")

    cur.execute(
        "INSERT INTO feedback (turn_id, rating, comment) VALUES (?, ?, ?)",
        (req.turn_id, req.rating, req.comment)
    )
    conn.commit()
    return FeedbackResponse(ok=True)