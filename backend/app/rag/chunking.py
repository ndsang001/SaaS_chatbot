from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class Chunk:
    chunk_id: str
    text: str
    title: str
    section: str | None
    source: str  # filename or path


def normalize_text(s: str) -> str:
    # Minimal cleanup; keep deterministic
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in s.split("\n")).strip()


def split_into_chunks(
    text: str,
    chunk_size: int = 800,
    overlap: int = 120,
) -> List[str]:
    """
    Simple character-based chunking.
    - predictable
    - easy to explain in thesis
    """
    text = normalize_text(text)
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        start = max(0, end - overlap)

    return chunks