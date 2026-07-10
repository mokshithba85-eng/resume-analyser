"""
Module for extracting raw text from PDF files using pdfplumber.
"""

import logging
from typing import BinaryIO, Union
from pathlib import Path
import pdfplumber

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_file: Union[str, Path, BinaryIO]) -> str:
    """
    Extracts text from a PDF file (supports path strings, Path objects, and file-like objects).

    Args:
        pdf_file (Union[str, Path, BinaryIO]): Path to the PDF or a file-like object (BytesIO).

    Returns:
        str: Clean, joined text content of the PDF.

    Raises:
        ValueError: If the file is invalid, corrupted, empty, or image-only.
    """
    text_pages = []
    
    try:
        with pdfplumber.open(pdf_file) as pdf:
            if not pdf.pages:
                raise ValueError("The PDF file contains no pages.")
            
            for index, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(page_text)
                else:
                    logger.warning("No extractable text found on page %d", index + 1)
                    
    except Exception as e:
        if isinstance(e, ValueError):
            raise e
        logger.exception("Failed to parse PDF file")
        raise ValueError(f"Unable to read PDF file. It might be corrupted or password-protected. Error: {str(e)}") from e

    full_text = "\n".join(text_pages).strip()
    
    if not full_text:
        raise ValueError(
            "No extractable text was found in the PDF. "
            "Please ensure it is not a scanned document (image-only) and is readable."
        )
        
    return full_text
