"""
Module containing Pydantic models for parsing and validating the Gemini AI
resume analysis response.
"""

from typing import List
from pydantic import BaseModel, Field


class ResumeAnalysisResponse(BaseModel):
    """
    Pydantic model representing the structured response from the Gemini AI analysis.
    
    This enforces a strict schema for downstream usage in the dashboard
    and report generator, reducing parsing errors and handling potential API drifts.
    """
    match_score: int = Field(
        ...,
        description="A qualitative assessment score from 0 to 100 indicating how well the candidate's resume fits the job requirements.",
        ge=0,
        le=100
    )
    matched_skills: List[str] = Field(
        ...,
        description="Skills and technologies from the resume that directly align with the job description."
    )
    missing_skills: List[str] = Field(
        ...,
        description="Required or preferred skills from the job description that are not mentioned in the resume."
    )
    strengths: List[str] = Field(
        ...,
        description="Notable strengths, projects, or background qualifications that make the candidate a strong fit."
    )
    weaknesses: List[str] = Field(
        ...,
        description="Critical gaps, lack of depth, or experiences that are missing or weak relative to the role."
    )
    resume_improvements: List[str] = Field(
        ...,
        description="Specific, actionable feedback on how to improve the resume (e.g., phrasing, formatting, adding missing keywords)."
    )
    interview_questions: List[str] = Field(
        ...,
        description="Custom-tailored, realistic interview questions (technical or behavioral) designed to test the candidate on the role requirements and their stated background."
    )
    recommended_courses: List[str] = Field(
        ...,
        description="Targeted courses, certifications, or topics to help the candidate learn the missing skills and close background gaps."
    )
