import sqlite3
from typing import Optional

_conn: Optional[sqlite3.Connection] = None

def get_conn(sqlite_path: str) -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(sqlite_path, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
    return _conn