"""Combine captions and graphics into figure regions."""
from typing import List

from .caption_builder import build_caption
from .caption_detector import find_captions
from .document_layout import compute_layout_stats
from .graphic_extractor import extract_graphics
from .text_extraction import TextLine

from .text_extraction import extract_text_lines

def detect_figures(page) -> List[dict]:
    lines = extract_text_lines(page)
    stats = compute_layout_stats(lines)
    captions = [build_caption(c, lines) for c in find_captions(lines, stats)]
    graphics = extract_graphics(page)
    figures = []
    for caption in captions:
        figures.append({
            "page": page.number,
            "caption": caption.text,
            "captionBoundary": {
                "x": caption.x,
                "y": caption.y,
                "width": caption.width,
                "height": caption.height,
            },
            "regionBoundary": {
                "x": caption.x,
                "y": caption.y - 100,
                "width": caption.width,
                "height": caption.height + 100,
            },
            "figureType": "Figure",
            "name": "",
            "text": "",
        })
    return figures
