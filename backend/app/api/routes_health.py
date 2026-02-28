from fastapi import APIRouter
from app.core.config import settings
import os
import vertexai

router = APIRouter()

@router.get("/health")
def health():
    index_loaded = os.path.exists(settings.faiss_index_path) and os.path.exists(settings.meta_path)

    vertex_ok = False
    try:
        if settings.gcp_project:
            vertexai.init(project=settings.gcp_project, location=settings.gcp_location)
            vertex_ok = True
    except Exception:
        vertex_ok = False

    return {
        "status": "ok",
        "index_loaded": index_loaded,
        "vertex_reachable": vertex_ok,
    }