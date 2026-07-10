"""
Service for generating vector embeddings using Gemini's text-embedding-004.
"""

import time
import logging
from typing import List, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Manages embedding generation for resumes and job descriptions.
    
    Includes robust error handling and exponential backoff retry mechanisms
    for rate limiting (429 ResourceExhausted).
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initializes the service. If an API key is provided, configures the genai library.

        Args:
            api_key (Optional[str]): Google Gemini API Key.
        """
        if api_key:
            genai.configure(api_key=api_key)

    def generate_embedding(
        self, text: str, model: str = "models/text-embedding-004", retries: int = 3
    ) -> List[float]:
        """
        Generates a 768-dimension vector embedding for the input text.

        Args:
            text (str): The cleaned text to embed.
            model (str): The Gemini embedding model name. Defaults to 'models/text-embedding-004'.
            retries (int): Number of retries on network or rate limit failure.

        Returns:
            List[float]: The float vector embedding.

        Raises:
            ValueError: If text is empty.
            RuntimeError: If embedding generation fails after retries.
        """
        if not text.strip():
            raise ValueError("Cannot generate embedding for empty or whitespace-only text.")

        backoff_sec = 2.0
        for attempt in range(retries):
            try:
                response = genai.embed_content(
                    model=model,
                    content=text,
                    task_type="retrieval_document"
                )
                if "embedding" in response:
                    return response["embedding"]
                raise KeyError("Response does not contain 'embedding' key.")
                
            except Exception as e:
                err_msg = str(e)
                logger.warning(
                    "Embedding generation attempt %d failed: %s",
                    attempt + 1,
                    err_msg
                )
                
                # Check for rate-limiting or server failures
                if "429" in err_msg or "ResourceExhausted" in err_msg or "503" in err_msg:
                    if attempt < retries - 1:
                        time.sleep(backoff_sec)
                        backoff_sec *= 2.0
                        continue
                raise RuntimeError(
                    f"Gemini Embedding API Error: {err_msg}"
                ) from e

        raise RuntimeError("Embedding generation failed after maximum retries.")
