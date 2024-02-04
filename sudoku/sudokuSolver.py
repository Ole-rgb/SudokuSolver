import numpy as np
from typing import Union, Tuple
from sudoku.sudokuGrid import SudokuGrid

ROWS, COLUMNS = (9, 9)
DIGITS = 10


# same for rows
all_rows = [[(i, j) for j in range(9)] for i in range(9)]

# return columns' lists of cells
all_columns = [[(i, j) for i in range(9)] for j in range(9)]

# same for blocks
# this list comprehension is unreadable, but quite cool!
all_blocks = [
    [((i // 3) * 3 + j // 3, (i % 3) * 3 + j % 3) for j in range(9)] for i in range(9)
]

# combine three
all_houses = all_columns + all_rows + all_blocks


class SudokuSolver:
    """
    Sudoku class represents a Sudoku puzzle and provides methods for manipulation.

    Attributes:
    - __grid (SudokuGrid): An instance of SudokuGrid representing the Sudoku puzzle.

    Methods:
    - __init__(self, grid_str: Union[None, str] = None) -> None:
        Constructor for the Sudoku class. Initializes the Sudoku grid.

    - fill_cell(self) -> None:
        Abstract method to be implemented by subclasses. Fills a cell in the Sudoku grid.

    - fill_in_candidates(self) -> None:
        Fills in candidate values for empty cells in the Sudoku grid.

    - get_sudoku_grid(self) -> SudokuGrid:
        Returns the SudokuGrid instance representing the Sudoku puzzle.

    - get_np_grid(self) -> np.ndarray:
        Returns the NumPy array representation of the Sudoku grid.

    - __str__(self) -> str:
        Returns a string representation of the Sudoku puzzle.

    Example Usage:
    >>> sudoku = Sudoku("530070000600195000098000060800060003400803001700020006060000280000419005000080079")
    >>> sudoku.fill_in_candidates()
    >>> print(sudoku)
    5 3 0 | 0 7 0 | 0 0 0
    6 0 0 | 1 9 5 | 0 0 0
    0 9 8 | 0 0 0 | 0 6 0
    ---------------------
    8 0 0 | 0 6 0 | 0 0 3
    4 0 0 | 8 0 3 | 0 0 1
    7 0 0 | 0 2 0 | 0 0 6
    ---------------------
    0 6 0 | 0 0 0 | 2 8 0
    0 0 0 | 4 1 9 | 0 0 5
    0 0 0 | 0 8 0 | 0 7 9
    """

    def __init__(self, grid_str: Union[None, str] = None) -> None:
        """
        Constructor for the Sudoku class.

        Parameters:
        - grid_str (Union[None, str]): A string containing digits representing the initial Sudoku grid.
          If None, an empty Sudoku grid is created.

        Returns:
        - None
        """
        self.__grid = SudokuGrid(grid_str)

    def simple_elimination(self):
        grid = self.get_sudoku_grid()
        for house in all_houses:
            for cell_position in house:
                cell = grid.get_cell(cell_position)
                if len(cell) == 1:
                    value_to_remove = cell[0]
                    # remove cell value from houses
                    for cell_positions2 in house:
                        cell2_has_value_to_remove = np.any(
                            grid.get_cell(cell_positions2) == value_to_remove
                        )
                        if (
                            cell_positions2 != cell_position
                            and cell2_has_value_to_remove
                        ):
                            self.get_sudoku_grid().set_cell(
                                cell_positions2,
                                self.remove_element(
                                    grid.get_cell(cell_positions2), value_to_remove
                                ),
                            )

    def remove_element(
        self, arr: np.ndarray, value_to_remove: Union[1, 2, 3, 4, 5, 6, 7, 8, 9]
    ) -> np.ndarray:
        return arr[arr != value_to_remove]

    def get_sudoku_grid(self) -> SudokuGrid:
        """
        Returns the SudokuGrid instance representing the Sudoku puzzle.

        Returns:
        - SudokuGrid: The SudokuGrid instance.
        """
        return self.__grid

    def __str__(self) -> str:
        """
        Returns a string representation of the Sudoku puzzle.

        Returns:
        - str: The string representation of the Sudoku puzzle.
        """
        return self.get_sudoku_grid().get_grid().__str__()


if __name__ == "__main__":
    s = SudokuSolver(
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000"
    )
    s.get_sudoku_grid().fill_in_candidates()
    s.simple_elimination()

    print(s)
