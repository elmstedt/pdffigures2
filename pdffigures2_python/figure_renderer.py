"""Render detected figures to image files."""
from pathlib import Path
from typing import List, Dict

import fitz


def save_figure_images(figures: List[Dict], pdf_path: str, prefix: str) -> None:
    doc = fitz.open(pdf_path)
    for idx, fig in enumerate(figures):
        page = doc.load_page(fig["page"])
        rect = fitz.Rect(
            fig["regionBoundary"]["x"],
            fig["regionBoundary"]["y"],
            fig["regionBoundary"]["x"] + fig["regionBoundary"]["width"],
            fig["regionBoundary"]["y"] + fig["regionBoundary"]["height"],
        )
        pix = page.get_pixmap(clip=rect)
        out = Path(f"{prefix}_{idx}.png")
        pix.save(out)
