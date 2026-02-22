from fastapi import APIRouter
from app.core.config import settings
import os

router = APIRouter()

@router.get("/health")
def health():
    # Minimal demo checks required by the architecture doc. :contentReference[oaicite:13]{index=13}
    index_loaded = os.path.exists(settings.faiss_index_path) and os.path.exists(settings.meta_path)

    # Vertex reachability check will be added in Phase 3 (real API call).
    return {
        "status": "ok",
        "index_loaded": index_loaded,
        "vertex_reachable": "unknown (phase 3)",
    }