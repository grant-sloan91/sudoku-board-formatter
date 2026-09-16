"""Rendering a parsed sudoku grid back into a canonical, predictable shape."""


def to_compact(grid):
    """Render the grid as a single 81-character line, '.' for blanks."""
    return "".join(str(cell) if cell else "." for row in grid for cell in row)


def to_pretty(grid):
    """Render the grid as a boxed 9x9 layout, grouped into 3x3 blocks."""
    horizontal = "+-------+-------+-------+"
    lines = [horizontal]
    for r, row in enumerate(grid):
        groups = []
        for start in range(0, 9, 3):
            chunk = row[start:start + 3]
            groups.append(" ".join(str(cell) if cell else "." for cell in chunk))
        lines.append("| " + " | ".join(groups) + " |")
        if r % 3 == 2:
            lines.append(horizontal)
    return "\n".join(lines)
