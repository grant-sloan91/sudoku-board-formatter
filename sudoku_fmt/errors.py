"""Exceptions raised while parsing sudoku puzzle text.

Every error here carries enough position information to point a reader
at the exact character that broke, because "invalid puzzle" on its own
is useless once the input is more than a few lines long.
"""


class SudokuFormatError(Exception):
    """Base class for all parsing errors in this package."""


class CellError(SudokuFormatError):
    """A single character couldn't be read as a digit, blank, or separator."""

    def __init__(self, message, line, column, source_line=None):
        self.line = line
        self.column = column
        self.source_line = source_line
        located = f"line {line}, column {column}: {message}"
        if source_line is not None:
            pointer = " " * (column - 1) + "^"
            located += f"\n    {source_line}\n    {pointer}"
        super().__init__(located)


class RowError(SudokuFormatError):
    """A row didn't contain exactly nine cells."""

    def __init__(self, message, line, source_line=None):
        self.line = line
        self.source_line = source_line
        located = f"line {line}: {message}"
        if source_line is not None:
            located += f"\n    {source_line}"
        super().__init__(located)


class GridError(SudokuFormatError):
    """The puzzle as a whole didn't have exactly nine rows."""

    def __init__(self, message):
        super().__init__(message)


class DuplicateError(SudokuFormatError):
    """The same digit appears twice in a row, column, or 3x3 box."""

    def __init__(self, digit, unit_type, unit_index, first_cell, second_cell):
        self.digit = digit
        self.unit_type = unit_type
        self.unit_index = unit_index
        self.first_cell = first_cell
        self.second_cell = second_cell
        r1, c1 = first_cell
        r2, c2 = second_cell
        super().__init__(
            f"digit {digit} appears twice in {unit_type} {unit_index}: "
            f"row {r1} column {c1} and row {r2} column {c2}"
        )
