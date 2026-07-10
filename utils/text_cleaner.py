"""
Module for cleaning and normalizing text extracted from resumes and job descriptions.
"""

import re


def clean_text(text: str) -> str:
    """
    Cleans and normalizes raw text to make it suitable for embedding and LLM analysis.
    
    Preserves case, punctuation, and sentence structures, but removes control
    characters, multiple consecutive spaces, and excessive blank lines.

    Args:
        text (str): Raw input text.

    Returns:
        str: Cleaned, single-spaced and formatted text.
    """
    if not text:
        return ""
    
    # Remove ASCII control characters (excluding tab and newlines)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # Replace multiple consecutive spaces or tabs with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Replace three or more consecutive newlines with exactly two newlines (to preserve paragraphs)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip trailing/leading spaces on each line
    lines = [line.strip() for line in text.splitlines()]
    
    # Reassemble and strip overall leading/trailing whitespace
    return "\n".join(line for line in lines if line).strip()
