from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings
from app.storage.sqlite import get_conn
from app.storage.models import init_db

from app.api.routes_chat import router as chat_router
from app.api.routes_feedback import router as feedback_router
from app.api.routes_health import router as health_router



app = FastAPI(title="Thesis RAG Chatbot API", version="0.1")

# CORS (allow Vite dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    conn = get_conn(settings.sqlite_path)
    init_db(conn)

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(feedback_router)