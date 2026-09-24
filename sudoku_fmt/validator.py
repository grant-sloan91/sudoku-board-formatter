"""Checking a parsed grid for duplicate digits, since parsing alone only
guarantees the shape of the puzzle, not that it's a legal one to solve.
"""

from .errors import DuplicateError


def _check_unit(values, positions, unit_type, unit_index):
    seen = {}
    for value, pos in zip(values, positions):
        if value == 0:
            continue
        if value in seen:
            raise DuplicateError(value, unit_type, unit_index, seen[value], pos)
        seen[value] = pos


def validate_grid(grid):
    """Check a parsed 9x9 grid for duplicate digits in any row, column, or box.

    Raises DuplicateError on the first conflict found (rows are checked
    before columns, columns before boxes), naming the two clashing cells
    by their 1-based row and column. Blank cells (0) never conflict.
    """
    for r, row in enumerate(grid, start=1):
        positions = [(r, c) for c in range(1, 10)]
        _check_unit(row, positions, "row", r)

    for c in range(9):
        column = [grid[r][c] for r in range(9)]
        positions = [(r, c + 1) for r in range(1, 10)]
        _check_unit(column, positions, "column", c + 1)

    box_index = 0
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_index += 1
            values = []
            positions = []
            for dr in range(3):
                for dc in range(3):
                    values.append(grid[box_row + dr][box_col + dc])
                    positions.append((box_row + dr + 1, box_col + dc + 1))
            _check_unit(values, positions, "box", box_index)

    return grid
