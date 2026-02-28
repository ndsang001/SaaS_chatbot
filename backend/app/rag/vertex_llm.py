from __future__ import annotations
import vertexai
from vertexai.generative_models import GenerativeModel
from google.api_core.exceptions import NotFound, PermissionDenied
from app.core.config import settings


class VertexGemini:
    def __init__(self) -> None:
        if not settings.gcp_project:
            raise RuntimeError("GCP_PROJECT is empty.")
        vertexai.init(project=settings.gcp_project, location=settings.gcp_location)
        self.model = GenerativeModel(settings.gemini_model)

    def generate(self, prompt: str, max_output_tokens: int = 1024, temperature: float = 0.2) -> str:
        try:
            resp = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": max_output_tokens,
                    "temperature": temperature,
                },
            )
            # print("LLM RAW OUTPUT:\n", resp.text)
            return (resp.text or "").strip()
        except NotFound as e:
            raise RuntimeError(
                f"Gemini model not found / no access: '{settings.gemini_model}'. "
                f"Verify the exact model name in Vertex AI Studio and that it's available in location "
                f"'{settings.gcp_location}'."
            ) from e
        except PermissionDenied as e:
            raise RuntimeError(
                "Permission denied calling Gemini. Check IAM role 'Vertex AI User' and project billing/API enablement."
            ) from e