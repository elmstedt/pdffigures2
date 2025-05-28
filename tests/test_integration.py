import os


def test_sample_pdf_exists():
    assert os.path.exists(os.path.join(os.path.dirname(__file__), "sample_papers", "test1.pdf"))
