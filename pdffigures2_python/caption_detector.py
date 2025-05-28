"""Caption detection logic."""
import re
from typing import List

from .document_layout import DocumentStats
from .text_extraction import TextLine

CAPTION_PATTERNS = [re.compile(r"^(figure|fig|table)\b", re.IGNORECASE)]


def find_captions(lines: List[TextLine], stats: DocumentStats) -> List[TextLine]:
    """Return lines that look like captions."""
    results = []
    for line in lines:
        if any(pat.match(line.text) for pat in CAPTION_PATTERNS):
            if line.font_size <= stats.median_font_size:
                results.append(line)
    return results
