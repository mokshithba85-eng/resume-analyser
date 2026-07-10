"""
General helper utilities for file validation and robust JSON parsing.
"""

import json
import re
from typing import Any, Dict


def clean_json_string(raw_json_str: str) -> str:
    """
    Strips markdown code block formatting (like ```json ... ```) from a string.

    Args:
        raw_json_str (str): The raw string output from the LLM.

    Returns:
        str: A cleaned JSON string ready for parsing.
    """
    if not raw_json_str:
        return "{}"
        
    raw_json_str = raw_json_str.strip()
    
    # Regular expression to extract JSON from code blocks if they are present
    code_block_pattern = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
    match = code_block_pattern.search(raw_json_str)
    
    if match:
        return match.group(1).strip()
        
    # If no standard markdown code blocks, try to find any first open brace to last close brace
    brace_pattern = re.compile(r"(\{.*?\})", re.DOTALL)
    match = brace_pattern.search(raw_json_str)
    if match:
        return match.group(1).strip()
        
    return raw_json_str


def safe_parse_json(raw_json_str: str) -> Dict[str, Any]:
    """
    Parses LLM response string to JSON dictionary safely, handling markdown decorators.

    Args:
        raw_json_str (str): The raw model response.

    Returns:
        Dict[str, Any]: The parsed JSON data.

    Raises:
        ValueError: If JSON is invalid and cannot be parsed.
    """
    cleaned = clean_json_string(raw_json_str)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse model output into JSON: {str(e)}. "
            f"Cleaned output was: {cleaned[:300]}..."
        ) from e


def validate_file_extension(filename: str, allowed_extensions: tuple = (".pdf",)) -> bool:
    """
    Validates if a file extension is in the allowed list.

    Args:
        filename (str): Name of the file.
        allowed_extensions (tuple): Allowed extensions. Defaults to ('.pdf',).

    Returns:
        bool: True if allowed, False otherwise.
    """
    return filename.lower().endswith(allowed_extensions)


def validate_file_size(file_size_bytes: int, max_size_mb: float = 10.0) -> bool:
    """
    Validates if a file size is within the acceptable limit.

    Args:
        file_size_bytes (int): Size of the file in bytes.
        max_size_mb (float): Maximum allowed file size in Megabytes. Defaults to 10.0.

    Returns:
        bool: True if within size limits, False otherwise.
    """
    max_bytes = max_size_mb * 1024 * 1024
    return file_size_bytes <= max_bytes
