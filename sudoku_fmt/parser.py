"""Parsing of loosely-formatted sudoku puzzle text into a strict 9x9 grid."""

from .errors import CellError, GridError, RowError

# '0' means blank as well as '.', since plenty of dumped puzzles use 0
# for an empty cell instead of a dot.
_BLANK_CHARS = frozenset(".0_")
_SEPARATOR_CHARS = frozenset(" \t|,;:")
_DECORATIVE_CHARS = frozenset("-=+*")


def _is_decorative(stripped_line):
    return bool(stripped_line) and all(c in _DECORATIVE_CHARS for c in stripped_line)


def _parse_row(raw_line, line_no):
    cells = []
    for col, ch in enumerate(raw_line, start=1):
        if ch in _SEPARATOR_CHARS:
            continue
        if ch in _BLANK_CHARS:
            cells.append(0)
        elif ch.isdigit():
            # '0' was already handled above, so this is '1'-'9'.
            cells.append(int(ch))
        else:
            raise CellError(
                f"unexpected character {ch!r} (expected a digit 1-9, "
                "'.' for a blank cell, or a separator)",
                line_no,
                col,
                raw_line,
            )

    if len(cells) != 9:
        raise RowError(
            f"expected 9 cells in this row, found {len(cells)}",
            line_no,
            raw_line,
        )
    return cells


def parse_grid(text):
    """Parse messy sudoku puzzle text into a 9x9 list of ints (0 = blank).

    Accepts extra whitespace, `|`/`,`/`;`/`:` separators between cells,
    decorative border lines made of `-`, `=`, `+`, `*`, blank lines, and
    `#` comment lines. Raises CellError, RowError, or GridError with the
    exact line (and, for bad characters, column) that didn't parse.
    """
    rows = []
    row_lines = []

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if _is_decorative(stripped):
            continue

        rows.append(_parse_row(raw_line, line_no))
        row_lines.append(line_no)

    if len(rows) != 9:
        where = ", ".join(str(n) for n in row_lines) if row_lines else "none"
        raise GridError(
            f"expected 9 rows of puzzle data, found {len(rows)} (lines used: {where})"
        )

    return rows
