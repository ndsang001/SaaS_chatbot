from __future__ import annotations
import csv
import sqlite3
from pathlib import Path
from app.core.config import settings


def export_table(conn: sqlite3.Connection, table: str, out_path: Path) -> None:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    # Grab column names
    colnames = [desc[0] for desc in cur.description]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(colnames)
        for r in rows:
            writer.writerow([r[c] for c in colnames])


def main() -> None:
    db_path = Path(settings.sqlite_path)
    if not db_path.exists():
        raise SystemExit(f"SQLite DB not found: {db_path}")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    out_dir = Path("exports")
    export_table(conn, "chat_turns", out_dir / "chat_turns.csv")
    export_table(conn, "feedback", out_dir / "feedback.csv")

    print("Export complete")
    print(f"- {out_dir / 'chat_turns.csv'}")
    print(f"- {out_dir / 'feedback.csv'}")


if __name__ == "__main__":
    main()