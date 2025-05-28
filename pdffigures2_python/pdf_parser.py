"""PDF parsing utilities using PyMuPDF."""
from typing import List

import fitz


def parse_pdf(path: str) -> List[fitz.Page]:
    """Open a PDF and return list of pages."""
    doc = fitz.open(path)
    return [page for page in doc]
