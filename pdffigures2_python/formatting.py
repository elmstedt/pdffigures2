"""Utilities for cleaning extracted text."""
from typing import List

from .text_extraction import TextLine


def filter_text_blocks(text_blocks: List[TextLine]) -> List[TextLine]:
    """Remove headers, footers, and page numbers."""
    cleaned = []
    for line in text_blocks:
        lower = line.text.lower().strip()
        if lower.isdigit():
            continue
        cleaned.append(line)
    return cleaned
