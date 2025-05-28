"""Text extraction helpers."""
from dataclasses import dataclass
from typing import List

import fitz


@dataclass
class TextLine:
    x: float
    y: float
    width: float
    height: float
    text: str
    font_size: float


def extract_text_lines(page: fitz.Page) -> List[TextLine]:
    """Return text lines from a page."""
    lines: List[TextLine] = []
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, text, *_ = b
        if text.strip():
            lines.append(TextLine(x0, y0, x1 - x0, y1 - y0, text, y1 - y0))
    return lines
