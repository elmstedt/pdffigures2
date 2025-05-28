"""Assemble multi-line captions."""
from typing import List

from .text_extraction import TextLine


def build_caption(start: TextLine, lines: List[TextLine]) -> TextLine:
    """Join subsequent lines that belong to the same caption."""
    text = [start.text]
    bottom = start.y + start.height
    for line in lines:
        if line.y > start.y and line.y - bottom < 2 and line.font_size == start.font_size:
            text.append(line.text)
            bottom = line.y + line.height
    joined = " ".join(text)
    return TextLine(start.x, start.y, start.width, bottom - start.y, joined, start.font_size)
