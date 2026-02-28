from pydantic import BaseModel
import os
# from dotenv import load_dotenv
# load_dotenv()

class Settings(BaseModel):
    # Google Cloud / Vertex AI
    gcp_project: str = os.getenv("GCP_PROJECT", "")
    gcp_location: str = os.getenv("GCP_LOCATION", "us-central1")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-004")

    # Local data paths
    data_dir: str = os.getenv("DATA_DIR", "app/data")
    faiss_index_path: str = os.getenv("FAISS_INDEX_PATH", "app/data/index.faiss")
    meta_path: str = os.getenv("META_PATH", "app/data/meta.json")

    # SQLite (logs only)
    sqlite_path: str = os.getenv("SQLITE_PATH", "logs.db")

settings = Settings()