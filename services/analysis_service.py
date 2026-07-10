"""
Coordinator service that manages the end-to-end execution of the resume matching pipeline.
"""

import logging
from typing import Any, Dict, Optional, Tuple
from services.embedding_service import EmbeddingService
from services.gemini_service import GeminiService
from services.similarity_service import SimilarityService
from utils.text_cleaner import clean_text

logger = logging.getLogger(__name__)


class AnalysisService:
    """
    Orchestrates semantic matching and AI resume-job description analysis.
    
    Acts as the single point of entry for the execution pipeline, connecting
    text cleaners, vector similarity metrics, and LLM evaluations.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initializes the service with individual pipeline component services.

        Args:
            api_key (Optional[str]): Google Gemini API Key.
        """
        self.embedding_service = EmbeddingService(api_key=api_key)
        self.gemini_service = GeminiService(api_key=api_key)
        self.similarity_service = SimilarityService()

    def run_analysis(self, raw_resume_text: str, raw_jd_text: str) -> Tuple[float, Dict[str, Any]]:
        """
        Runs the full semantic matching and qualitative review pipeline.

        Args:
            raw_resume_text (str): Extracted raw resume text.
            raw_jd_text (str): Raw job description text.

        Returns:
            Tuple[float, Dict[str, Any]]: 
                - Mathematical match score (cosine similarity percentage, 0-100).
                - Dictionary containing Gemini structured analysis results.

        Raises:
            ValueError: If inputs are invalid or empty.
            RuntimeError: If any pipeline stage fails.
        """
        if not raw_resume_text.strip():
            raise ValueError("Resume content cannot be empty.")
        if not raw_jd_text.strip():
            raise ValueError("Job description content cannot be empty.")

        # Step 1: Preprocess and clean text
        logger.info("Starting text preprocessing...")
        cleaned_resume = clean_text(raw_resume_text)
        cleaned_jd = clean_text(raw_jd_text)

        # Step 2: Compute mathematical semantic similarity
        logger.info("Generating embeddings and calculating cosine similarity...")
        resume_emb = self.embedding_service.generate_embedding(cleaned_resume)
        jd_emb = self.embedding_service.generate_embedding(cleaned_jd)
        cosine_score = self.similarity_service.calculate_cosine_similarity(resume_emb, jd_emb)

        # Step 3: Run Qualitative LLM Analysis
        logger.info("Running qualitative AI gap analysis via Gemini...")
        analysis_data = self.gemini_service.analyze_resume_vs_jd(cleaned_resume, cleaned_jd)

        return cosine_score, analysis_data
