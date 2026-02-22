from __future__ import annotations
from typing import List
import numpy as np

from app.core.config import settings

# Vertex AI Python SDK
import vertexai
from vertexai.language_models import TextEmbeddingModel


class VertexEmbedder:
    def __init__(self) -> None:
        if not settings.gcp_project:
            raise RuntimeError("GCP_PROJECT is empty. Set it in environment.")
        vertexai.init(project=settings.gcp_project, location=settings.gcp_location)
        self.model = TextEmbeddingModel.from_pretrained(settings.embedding_model)

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Returns shape: (len(texts), dim)
        """
        if not texts:
            return np.zeros((0, 0), dtype=np.float32)

        # Vertex returns objects with .values
        embeddings = self.model.get_embeddings(texts)
        vecs = np.array([e.values for e in embeddings], dtype=np.float32)
        return vecs