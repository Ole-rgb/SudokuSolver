import numpy as np
import matplotlib.pyplot as plt
from sudoku import Sudoku


def display_sudoku(grid):
    """
    Display the Sudoku grid as an image.
    """

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.matshow(np.ones_like(np.zeros((9, 9))) * -1, cmap="Blues", vmin=-2, vmax=2)

    for i in range(9):
        for j in range(9):
            if len(grid[i][j]) == 1 and grid[i][j] != 0:
                number = grid[i][j][0]
                ax.text(
                    j,
                    i,
                    str(number),
                    ha="center",
                    va="center",
                    fontsize=12,
                    color="black",
                )
            elif len(grid[i][j]) > 1:
                display_candidates = ""

                for index, candidate in enumerate(grid[i][j]):
                    if index % 3 == 0:
                        display_candidates += "\n"

                    display_candidates += "{} ".format(candidate)

                ax.text(
                    j,
                    i,
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
    sudoku = Sudoku(
        "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    )
    sudoku.fill_in_candidates()
    display_sudoku(sudoku.get_np_grid())
