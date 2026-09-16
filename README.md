# sudoku-board-formatter

Sudoku puzzles that get passed around forums, chat logs, and text files are
never in the same shape twice: some use `0` for blanks, some use `.`, some
pad cells with pipes and box-drawing borders, some have one stray extra
space that throws off a single row out of nine. Before you can feed a
puzzle into a solver you usually end up writing a one-off cleanup script
for whatever format that particular copy happens to be in.

This is that cleanup script, done once. It parses loosely-formatted sudoku
text into a strict 9x9 grid and renders it back out in one of two
predictable shapes. When the input doesn't parse, it tells you exactly
which line and column broke, not just "invalid puzzle".

## Usage

```python
from sudoku_fmt import format_sudoku

messy = """
+-------+-------+-------+
| 5 3 . | . 7 . | . . . |
| 6 . . | 1 9 5 | . . . |
| . 9 8 | . . . | . 6 . |
+-------+-------+-------+
| 8 . . | . 6 . | . . 3 |
| 4 . . | 8 . 3 | . . 1 |
| 7 . . | . 2 . | . . 6 |
+-------+-------+-------+
| . 6 . | . . . | 2 8 . |
| . . . | 4 1 9 | . . 5 |
| . . . | . 8 . | . 7 9 |
+-------+-------+-------+
"""

print(format_sudoku(messy, style="compact"))
# 53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79
```

`format_sudoku` also accepts `style="pretty"` (the default), which re-renders
the grid in the same boxed layout no matter how ragged the input was.

## Error messages

The parser tracks the exact line and column of every character it reads, so
a bad cell doesn't just fail the whole puzzle with no context:

```python
>>> from sudoku_fmt import parse_grid
>>> parse_grid("53x......\n" + "........." * 8)
sudoku_fmt.errors.CellError: line 1, column 3: unexpected character 'x' (expected a digit 1-9, '.' for a blank cell, or a separator)
    53x......
      ^
```

Row-length and grid-shape problems get the same treatment: a row with 10
cells names its line number, and a puzzle with 8 or 10 rows says so instead
of guessing which row is missing.

## Accepted input

- Blank cells: `.`, `0`, or `_`
- Given digits: `1`-`9`
- Separators ignored between cells: spaces, tabs, `|`, `,`, `;`, `:`
- Decorative lines made entirely of `-`, `=`, `+`, `*` (box borders) are skipped
- Blank lines and lines starting with `#` are skipped

## Status

Early skeleton: parsing and both output styles work. See below for what's next.

## Roadmap

- validate parsed puzzles for duplicate digits in a row, column, or box
- accept a `--file` / stdin CLI entry point
- support parsing and rendering candidate/pencil-mark annotations
- add a test suite covering the error-message paths
