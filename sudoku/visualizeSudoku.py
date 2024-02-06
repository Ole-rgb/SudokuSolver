import numpy as np
import matplotlib.pyplot as plt
from sudoku.sudokuSolver import SudokuSolver, SudokuGrid, ROWS, COLUMNS


def display_sudoku(grid: SudokuGrid):
    """
    Display the Sudoku grid as an image.
    """

    _, ax = plt.subplots(figsize=(6, 6))
    ax.matshow(
        np.ones_like(np.zeros((ROWS, COLUMNS))) * -1, cmap="Blues", vmin=-2, vmax=2
    )

    for row in range(ROWS):
        for column in range(COLUMNS):
            if (
                len(grid.get_cell((row, column))) == 1
                and grid.get_cell((row, column)) != 0
            ):
                # Displays fixed numbers
                number = grid.get_cell((row, column))[0]
                ax.text(
                    column,
                    row,
                    str(number),
                    ha="center",
                    va="center",
                    fontsize=12,
                    color="black",
                )
            elif len(grid.get_cell((row, column))) > 1:
                # Displays candidates
                display_candidates = ""
                for index, candidate in enumerate(grid.get_cell((row, column))):
                    if index % 3 == 0:
                        display_candidates += "\n"
                    display_candidates += "{} ".format(candidate)
                ax.text(
                    column,
                    row,
                    display_candidates,
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="black",
                )

    for i in range(1, 9):
        linewidth = 2 if i % 3 == 0 else 0.5
        ax.axhline(i - 0.5, color="black", linewidth=linewidth)
        ax.axvline(i - 0.5, color="black", linewidth=linewidth)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


if __name__ == "__main__":

    s = SudokuSolver(
        "100000050006000007000000090000004000000000000030000000000080000000000000000000200"
    )
    s.get_sudoku_grid()
    s.fill_in_candidates()
    s.simple_elimination()

    display_sudoku(s.get_sudoku_grid())
