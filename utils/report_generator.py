"""
Module for generating professional PDF evaluation reports using fpdf2.
"""

from typing import Any, Dict
from fpdf import FPDF


class ResumeReportPDF(FPDF):
    """
    Custom PDF class to represent the Resume Analysis Report.
    Includes customized headers, footers, margins, and page numbering.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self) -> None:
        """
        Renders the header at the top of each page.
        """
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 41, 59)  # Dark slate gray
        self.cell(0, 10, "Semantic Resume Matcher - Analysis Report", ln=True, align="L")
        
        # Horizontal rule separator
        self.set_draw_color(99, 102, 241)  # Indigo-500
        self.set_line_width(0.8)
        self.line(10, 20, 200, 20)
        self.ln(12)

    def footer(self) -> None:
        """
        Renders the footer at the bottom of each page.
        """
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)  # Muted gray-blue
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} - Powered by Google Gemini & Antigravity", align="C")


def generate_pdf_report(analysis_data: Dict[str, Any], cosine_score: float) -> bytes:
    """
    Generates a beautifully structured PDF document based on match statistics and AI analysis.

    Args:
        analysis_data (Dict[str, Any]): Evaluated JSON dictionary.
        cosine_score (float): Mathematical similarity score.

    Returns:
        bytes: Raw PDF bytes.
    """
    pdf = ResumeReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # 1. Executive Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)  # Accent color (Indigo-600)
    pdf.cell(0, 8, "1. Executive Match Summary", ln=True)
    pdf.ln(2)

    # Metric Table/Grid
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(51, 65, 85)  # Slate-700
    pdf.set_fill_color(248, 250, 252)  # Very light gray-blue background
    
    pdf.cell(90, 10, f"  Semantic Similarity Score (Embeddings)", border=1, fill=True)
    pdf.cell(90, 10, f"  AI Qualitative Fit Score (Gemini LLM)", border=1, fill=True, ln=True)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(99, 102, 241)  # Indigo
    pdf.cell(90, 12, f"  {cosine_score:.1f}%", border=1)
    pdf.cell(90, 12, f"  {analysis_data.get('match_score', 0)}%", border=1, ln=True)
    pdf.ln(6)

    # 2. Skills Analysis
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 8, "2. Skills Alignment", ln=True)
    pdf.ln(2)

    # Matched Skills
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(22, 163, 74)  # Green-600
    pdf.cell(0, 6, "Matched Skills (Present in Resume):", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    matched_skills = analysis_data.get("matched_skills", [])
    if matched_skills:
        pdf.multi_cell(0, 5, ", ".join(matched_skills))
    else:
        pdf.cell(0, 5, "No direct matching skills identified.", ln=True)
    pdf.ln(4)

    # Missing Skills
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(220, 38, 38)  # Red-600
    pdf.cell(0, 6, "Missing Skills (Requested in Job Description but Absent/Not Stated):", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    missing_skills = analysis_data.get("missing_skills", [])
    if missing_skills:
        pdf.multi_cell(0, 5, ", ".join(missing_skills))
    else:
        pdf.cell(0, 5, "No significant skill gaps identified.", ln=True)
    pdf.ln(6)

    # 3. Strengths and Weaknesses
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 8, "3. Strengths & Weaknesses Evaluation", ln=True)
    pdf.ln(2)

    # Strengths
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, "Key Strengths:", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    for strength in analysis_data.get("strengths", []):
        pdf.multi_cell(0, 5, f"- {strength}")
        pdf.ln(1)
    pdf.ln(3)

    # Weaknesses
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, "Key Gaps or Weaknesses:", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    for weakness in analysis_data.get("weaknesses", []):
        pdf.multi_cell(0, 5, f"- {weakness}")
        pdf.ln(1)
    pdf.ln(6)

    # 4. Resume Improvements
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 8, "4. Recommended Resume Improvements", ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    for improvement in analysis_data.get("resume_improvements", []):
        pdf.multi_cell(0, 5, f"- {improvement}")
        pdf.ln(1)
    pdf.ln(6)

    # 5. Interview Preparation
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 8, "5. Recommended Interview Questions", ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    for idx, question in enumerate(analysis_data.get("interview_questions", []), 1):
        pdf.multi_cell(0, 5, f"{idx}. {question}")
        pdf.ln(1.5)
    pdf.ln(4)

    # 6. Skill Upgrades
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 8, "6. Recommended Courses & Learning Topics", ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    for course in analysis_data.get("recommended_courses", []):
        pdf.multi_cell(0, 5, f"- {course}")
        pdf.ln(1)

    # Generate raw bytes
    return bytes(pdf.output())
