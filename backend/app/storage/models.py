import sqlite3

def init_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    # Matches the architecture doc schema (chat_turns + feedback). :contentReference[oaicite:12]{index=12}
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_turns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        user_question TEXT NOT NULL,
        retrieved_chunk_ids TEXT NOT NULL,
        model_answer TEXT NOT NULL,
        latency_ms INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # If table already exists, add column safely
    try:
        cur.execute("ALTER TABLE chat_turns ADD COLUMN not_in_kb INTEGER DEFAULT 0")
    except Exception:
        pass

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        turn_id INTEGER NOT NULL,
        rating TEXT NOT NULL,
        comment TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(turn_id) REFERENCES chat_turns(id)
    )
    """)

    conn.commit()