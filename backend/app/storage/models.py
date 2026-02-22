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