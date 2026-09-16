"""Normalize messy sudoku puzzle text into a canonical grid."""

from .errors import CellError, GridError, RowError, SudokuFormatError
from .formatter import to_compact, to_pretty
from .parser import parse_grid

__all__ = [
    "SudokuFormatError",
    "CellError",
    "RowError",
    "GridError",
    "parse_grid",
    "to_compact",
    "to_pretty",
    "format_sudoku",
]


def format_sudoku(text, style="pretty"):
    """Parse messy puzzle text and render it in a canonical style.

    style is "pretty" (boxed 9x9 grid) or "compact" (single 81-char line).
    """
    grid = parse_grid(text)
    if style == "compact":
        return to_compact(grid)
    if style == "pretty":
        return to_pretty(grid)
    raise ValueError(f"unknown style {style!r}, expected 'pretty' or 'compact'")
