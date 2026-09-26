"""Command-line entry point: read messy puzzle text, print the canonical form."""

import argparse
import sys

from .errors import SudokuFormatError
from . import format_sudoku


def _read_input(path):
    if path is None or path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def build_parser():
    parser = argparse.ArgumentParser(
        prog="sudoku-fmt",
        description="Normalize messy sudoku puzzle text into a canonical grid.",
    )
    parser.add_argument(
        "--file",
        metavar="PATH",
        help="path to the puzzle text to read; defaults to stdin, '-' also means stdin",
    )
    parser.add_argument(
        "--style",
        choices=("pretty", "compact"),
        default="pretty",
        help="output shape (default: pretty)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="also check for duplicate digits in a row, column, or box",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    text = _read_input(args.file)

    try:
        result = format_sudoku(text, style=args.style, validate=args.validate)
    except SudokuFormatError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
