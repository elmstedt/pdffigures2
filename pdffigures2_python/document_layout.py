"""Document layout statistics."""
from dataclasses import dataclass
from statistics import mean
from typing import List

from .text_extraction import TextLine


@dataclass
class DocumentStats:
    avg_font_size: float
    median_font_size: float


def compute_layout_stats(lines: List[TextLine]) -> DocumentStats:
    sizes = [l.font_size for l in lines]
    avg = mean(sizes) if sizes else 0
    median = sorted(sizes)[len(sizes)//2] if sizes else 0
    return DocumentStats(avg, median)
