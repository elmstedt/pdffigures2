"""Command line interface for the Python port of PDFFigures2."""
from argparse import ArgumentParser


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Extract figures and captions from PDFs")
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("-d", "--data-prefix", required=True, help="Output JSON prefix")
    parser.add_argument("-m", "--image-prefix", help="Optional image output prefix")
    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    # TODO: invoke pipeline once modules are implemented
    print(f"Would process {args.pdf} -> {args.data_prefix}")


if __name__ == "__main__":
    main()
