"""Normalize messy sudoku puzzle text into a canonical grid."""

from .errors import CellError, DuplicateError, GridError, RowError, SudokuFormatError
from .formatter import to_compact, to_pretty
from .parser import parse_grid
from .validator import validate_grid

__all__ = [
    "SudokuFormatError",
    "CellError",
    "RowError",
    "GridError",
    "DuplicateError",
    "parse_grid",
    "validate_grid",
    "to_compact",
    "to_pretty",
    "format_sudoku",
]


def format_sudoku(text, style="pretty", validate=False):
    """Parse messy puzzle text and render it in a canonical style.

    style is "pretty" (boxed 9x9 grid) or "compact" (single 81-char line).
    If validate is True, also raise DuplicateError for a repeated digit
    in a row, column, or box before rendering.
    """
    grid = parse_grid(text)
    if validate:
        validate_grid(grid)
    if style == "compact":
        return to_compact(grid)
    if style == "pretty":
        return to_pretty(grid)
    raise ValueError(f"unknown style {style!r}, expected 'pretty' or 'compact'")
