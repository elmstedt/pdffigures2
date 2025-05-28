"""Extract images and drawings from a page."""
from typing import List, Tuple

import fitz


BBox = Tuple[float, float, float, float]


def extract_graphics(page: fitz.Page) -> List[BBox]:
    boxes = []
    for img in page.get_images(full=True):
        for rect in page.get_image_rects(img[0]):
            boxes.append((rect.x0, rect.y0, rect.x1, rect.y1))
    for drawing in page.get_drawings():
        rect = drawing.get("rect")
        if rect is not None:
            boxes.append((rect.x0, rect.y0, rect.x1, rect.y1))
    return boxes
