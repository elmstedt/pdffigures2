from pdffigures2_python import caption_detector, document_layout
from pdffigures2_python.text_extraction import TextLine


def test_simple_caption_line():
    line = TextLine(0, 0, 100, 10, "Figure 1: Test", 8)
    stats = document_layout.DocumentStats(avg_font_size=12, median_font_size=12)
    captions = caption_detector.find_captions([line], stats)
    assert len(captions) == 1
