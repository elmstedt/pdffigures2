"""Classify text lines using a pre-trained model."""
from typing import List

import joblib

from .document_layout import DocumentStats
from .text_extraction import TextLine

_model = None


def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(
            __import__("pkgutil").get_data(__package__, "models/region_classifier_model.pkl")
        )
    return _model


def classify_text_lines(lines: List[TextLine], stats: DocumentStats) -> List[str]:
    """Return labels for each line (e.g., 'BodyText' or 'Other')."""
    model = _load_model()
    # Placeholder feature: font size ratio
    features = [[line.font_size / stats.avg_font_size if stats.avg_font_size else 0] for line in lines]
    return model.predict(features)  # type: ignore
