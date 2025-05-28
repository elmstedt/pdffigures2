"""Command line interface for the Python port of PDFFigures2."""
from argparse import ArgumentParser
import json
from pathlib import Path
from . import figure_detector, figure_renderer, pdf_parser

def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Extract figures and captions from PDFs")
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("-d", "--data-prefix", required=True, help="Output JSON prefix")
    parser.add_argument("-m", "--image-prefix", help="Optional image output prefix")
    return parser


def process_pdf(pdf_path: str, data_prefix: str, image_prefix: str | None = None) -> None:
    pages = pdf_parser.parse_pdf(pdf_path)
    figures = []
    for page in pages:
        figures.extend(figure_detector.detect_figures(page))

    out_json = Path(f"{data_prefix}.json")
    out_json.write_text(json.dumps(figures, indent=2))
    if image_prefix:
        figure_renderer.save_figure_images(figures, pdf_path, image_prefix)
    print(f"Saved {len(figures)} figures to {out_json}")


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    process_pdf(args.pdf, args.data_prefix, args.image_prefix)


if __name__ == "__main__":
    main()
