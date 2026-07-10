"""
Service for performing LLM analysis of resumes and job descriptions using Google Gemini.
"""

import logging
from typing import Any, Dict, Optional
import google.generativeai as genai

from models.response_models import ResumeAnalysisResponse
from prompts.prompt import SYSTEM_PROMPT, generate_analysis_prompt
from utils.helper import safe_parse_json

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Manages semantic analysis of resumes against job descriptions.
    
    Uses gemini-2.5-flash with structured JSON output and Pydantic validation.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initializes the service. If an API key is provided, configures the genai library.

        Args:
            api_key (Optional[str]): Google Gemini API Key.
        """
        if api_key:
            genai.configure(api_key=api_key)

    def analyze_resume_vs_jd(
        self, resume_text: str, jd_text: str, model_name: str = "gemini-2.5-flash"
    ) -> Dict[str, Any]:
        """
        Sends the resume and job description to Gemini 2.5 Flash for deep parsing.
        
        Tries to enforce structured JSON using a Pydantic schema config. Falls back 
        to general JSON MIME configuration if schema configuration fails.

        Args:
            resume_text (str): Extracted resume text.
            jd_text (str): Target job description text.
            model_name (str): The Gemini model. Defaults to 'gemini-2.5-flash'.

        Returns:
            Dict[str, Any]: Structured and validated analysis report.

        Raises:
            ValueError: If inputs are invalid.
            RuntimeError: If API call or validation fails.
        """
        if not resume_text.strip() or not jd_text.strip():
            raise ValueError("Resume text and job description text must not be empty.")

        prompt_content = generate_analysis_prompt(resume_text, jd_text)
        
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=SYSTEM_PROMPT
            )

            # Step 1: Attempt structured generation using the Pydantic schema directly
            try:
                generation_config = genai.types.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=ResumeAnalysisResponse,
                    temperature=0.2,
                )
                response = model.generate_content(
                    prompt_content,
                    generation_config=generation_config
                )
            except Exception as config_err:
                logger.warning(
                    "Pydantic schema generation configuration failed, falling back to default JSON mime type. Error: %s",
                    str(config_err)
                )
                # Step 2: Fallback to plain JSON MIME type
                generation_config = genai.types.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                )
                response = model.generate_content(
                    prompt_content,
                    generation_config=generation_config
                )

            raw_response_text = response.text
            if not raw_response_text:
                raise RuntimeError("Empty response received from Gemini API.")

            # Parse and clean output
            parsed_json = safe_parse_json(raw_response_text)

            # Validate against our Pydantic schema
            validated_response = ResumeAnalysisResponse(**parsed_json)
            
            # Return as serializable dictionary
            return validated_response.model_dump()

        except Exception as e:
            logger.exception("Failed to analyze resume vs job description via Gemini API")
            raise RuntimeError(
                f"Gemini Analysis Failure: {str(e)}"
            ) from e
            
    def verify_api_connection(self) -> bool:
        """
        Verifies if the configured API key can authenticate and talk to the API.

        Returns:
            bool: True if key is valid, False otherwise.
        """
        try:
            # Try a lightweight model list call to verify auth
            genai.list_models()
            return True
        except Exception:
            return False
