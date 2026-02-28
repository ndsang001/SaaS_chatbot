from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple
import json
import numpy as np
import faiss


@dataclass
class RetrievedChunk:
    chunk_id: str
    score: float          # smaller is better for L2 distance
    text: str
    title: str
    section: str | None
    source: str | None


class FaissRetriever:
    def __init__(self, index_path: str, meta_path: str) -> None:
        self.index = faiss.read_index(index_path)

        payload = json.loads(open(meta_path, "r", encoding="utf-8").read())
        self.chunk_ids: List[str] = payload["chunk_ids"]
        self.meta: Dict[str, Dict[str, Any]] = payload["meta"]

        if self.index.ntotal != len(self.chunk_ids):
            raise RuntimeError(
                f"FAISS ntotal={self.index.ntotal} but meta chunk_ids={len(self.chunk_ids)}"
            )

    def search(self, query_vec: np.ndarray, top_k: int = 4) -> List[RetrievedChunk]:
        """
        query_vec: shape (dim,) or (1, dim)
        Returns: top_k chunks by L2 distance (lower is more similar).
        """
        if query_vec.ndim == 1:
            query_vec = query_vec.reshape(1, -1)

        distances, indices = self.index.search(query_vec.astype(np.float32), top_k)
        d0 = distances[0].tolist()
        i0 = indices[0].tolist()

        results: List[RetrievedChunk] = []
        for dist, idx in zip(d0, i0):
            if idx == -1:
                continue
            chunk_id = self.chunk_ids[idx]
            m = self.meta[chunk_id]
            results.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    score=float(dist),
                    text=m["text"],
                    title=m.get("title", ""),
                    section=m.get("section"),
                    source=m.get("source"),
                )
            )
        return results