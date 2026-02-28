# Knowledge-Grounded AI Customer Support Chatbot (RAG Prototype)

## Master's Thesis Project

**Title:**\
Design and Evaluation of a Knowledge-Grounded AI-Powered Customer
Support Chatbot for Web Applications

**Author:**\
Sang Nguyen\
MSc Web, Cloud and Software Engineering\
Tampere University

------------------------------------------------------------------------

## 1. Project Overview

This project implements a minimal, runnable prototype of a
knowledge-grounded AI chatbot for SaaS-style web application customer
support.

The system:

-   Uses Retrieval-Augmented Generation (RAG)
-   Grounds responses strictly in FAQ/help documentation
-   Returns source citations for transparency
-   Logs response time and retrieval metadata
-   Collects user feedback (thumbs up/down + optional comment)

The implementation is intentionally simple and modular to align with
thesis scope constraints.

------------------------------------------------------------------------

## 2. System Architecture

The system follows a clean, modular RAG architecture:

### Ingestion Pipeline

1.  FAQ / Help Articles (Markdown files)
2.  Chunking + Metadata
3.  Vertex AI Text Embeddings
4.  FAISS Vector Index

### Runtime Flow

1.  User question (Frontend)
2.  FastAPI `/chat` endpoint
3.  Query embedding (Vertex AI)
4.  FAISS top‑k retrieval
5.  Prompt builder (strict grounding)
6.  Vertex AI Gemini model
7.  Response + sources + latency returned
8.  Interaction logged to SQLite

------------------------------------------------------------------------

## 3. Technology Stack

### Backend

-   FastAPI
-   Vertex AI Gemini
-   Vertex AI Text Embeddings
-   FAISS (vector search)
-   SQLite (evaluation logging)

### Frontend

-   React + Vite
-   MUI
-   Zustand

------------------------------------------------------------------------

## 4. Project Structure

SaaS_chatbot/ ├── backend/ │ ├── app/ │ │ ├── api/ │ │ ├── rag/ │ │ ├──
storage/ │ │ ├── scripts/ │ │ └── data/ │ └── logs.db ├── frontend/ └──
README.md

------------------------------------------------------------------------

## 5. Backend Setup

### 5.1 Create Virtual Environment

``` bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5.2 Environment Configuration

Create `backend/.env`:

``` env
GCP_PROJECT="your-project-id"
GCP_LOCATION="us-central1"
GEMINI_MODEL="your-vertex-gemini-model"
EMBEDDING_MODEL="text-embedding-004"
DATA_DIR="app/data"
FAISS_INDEX_PATH="app/data/index.faiss"
META_PATH="app/data/meta.json"
SQLITE_PATH="logs.db"
```

Export service account credentials:

``` bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/service-account.json"
```

------------------------------------------------------------------------

### 5.3 Build Vector Index

Place 5--10 FAQ `.md` files in:

backend/app/data/docs/

Then run:

``` bash
python -m app.scripts.ingest
```

------------------------------------------------------------------------

### 5.4 Run Backend

``` bash
uvicorn app.main:app --reload
```

Health check:

``` bash
curl http://127.0.0.1:8000/health
```

------------------------------------------------------------------------

## 6. Frontend Setup

``` bash
cd frontend
npm install
npm run dev
```

Open:

http://localhost:5173

------------------------------------------------------------------------

## 7. API Endpoints

### POST /chat

``` json
{
  "session_id": "demo1",
  "question": "How long does the password reset link last?"
}
```

### POST /feedback

``` json
{
  "turn_id": 1,
  "rating": "up",
  "comment": "Helpful answer"
}
```

------------------------------------------------------------------------

## 8. Evaluation Logging

All interactions are stored in SQLite:

-   chat_turns
-   feedback

Export logs:

``` bash
python -m app.scripts.export_logs
```

Generates:

-   exports/chat_turns.csv
-   exports/feedback.csv

------------------------------------------------------------------------

## 9. Scope Limitations

This prototype intentionally does NOT include:

-   Authentication
-   Account modification actions
-   Ticketing systems
-   Payment integration
-   Conversation memory
-   Production deployment automation

The focus is on evaluating knowledge grounding and response quality.

------------------------------------------------------------------------

## 10. Demo Questions

-   How long does the password reset link last?
-   What are your support hours?
-   Can I downgrade my subscription?
-   Do you store passwords in plain text?
-   Can you access my account and change my email?

------------------------------------------------------------------------

## 11. License

Academic prototype for Master's thesis purposes only.
