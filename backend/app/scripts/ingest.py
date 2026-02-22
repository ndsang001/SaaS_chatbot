from __future__ import annotations
import os
import json
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import faiss

from app.core.config import settings
from app.rag.chunking import split_into_chunks
from app.rag.vertex_embedder import VertexEmbedder


def load_docs(docs_dir: Path) -> List[dict]:
    docs = []
    for p in sorted(docs_dir.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        title = p.stem.replace("_", " ").strip()
        docs.append({"path": str(p), "title": title, "text": text})
    return docs


def main() -> None:
    docs_dir = Path(settings.data_dir) / "docs"
    out_index = Path(settings.faiss_index_path)
    out_meta = Path(settings.meta_path)

    if not docs_dir.exists():
        raise SystemExit(f"Docs folder not found: {docs_dir} (create it and add .md files)")

    docs = load_docs(docs_dir)
    if len(docs) < 5:
        print(f"WARNING: Only {len(docs)} docs found. Target is 5–10 for the demo.")

    embedder = VertexEmbedder()

    meta: Dict[str, Dict[str, Any]] = {}
    all_vecs: List[np.ndarray] = []
    all_ids: List[str] = []

    chunk_counter = 0
    for doc in docs:
        chunks = split_into_chunks(doc["text"], chunk_size=800, overlap=120)
        if not chunks:
            continue

        # Embed in a single batch per doc (simple and fast)
        vecs = embedder.embed_texts(chunks)

        for i, chunk_text in enumerate(chunks):
            chunk_id = f"c{chunk_counter:05d}"
            chunk_counter += 1

            meta[chunk_id] = {
                "title": doc["title"],
                "section": None,          # keep minimal; can extend later if needed
                "source": os.path.basename(doc["path"]),
                "text": chunk_text,
            }
            all_ids.append(chunk_id)
            all_vecs.append(vecs[i])

    if not all_vecs:
        raise SystemExit("No chunks produced. Check docs content.")

    mat = np.vstack(all_vecs).astype(np.float32)
    dim = mat.shape[1]

    # FAISS: simple L2 flat index (minimal + thesis-friendly)
    index = faiss.IndexFlatL2(dim)
    index.add(mat)

    out_index.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(out_index))

    out_meta.parent.mkdir(parents=True, exist_ok=True)
    out_meta.write_text(json.dumps({"chunk_ids": all_ids, "meta": meta}, ensure_ascii=False, indent=2), encoding="utf-8")

    print("✅ Ingestion complete")
    print(f"- chunks: {len(all_ids)}")
    print(f"- index:  {out_index}")
    print(f"- meta:   {out_meta}")


if __name__ == "__main__":
    main()