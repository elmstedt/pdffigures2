from pdffigures2_python import region_classifier, document_layout
from pdffigures2_python.text_extraction import TextLine


def test_model_load(monkeypatch):
    class DummyModel:
        def predict(self, X):
            return ["BodyText" for _ in X]

    monkeypatch.setattr(region_classifier, "_load_model", lambda: DummyModel())
    line = TextLine(0, 0, 100, 10, "Sample", 12)
    stats = document_layout.DocumentStats(avg_font_size=12, median_font_size=12)
    labels = region_classifier.classify_text_lines([line], stats)
    assert labels == ["BodyText"]
