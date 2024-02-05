import numpy as np
from typing import Union, Tuple
from sudoku.sudokuGrid import SudokuGrid

ROWS, COLUMNS = (9, 9)
DIGITS = 10

# same for rows
all_rows = [[(row, column) for column in range(COLUMNS)] for row in range(ROWS)]

# return columns' lists of cells
all_columns = [[(row, column) for row in range(ROWS)] for column in range(COLUMNS)]

# same for blocks
# this list comprehension is unreadable, but quite cool!
all_blocks = [
    [
        ((row // 3) * 3 + column // 3, (row % 3) * 3 + column % 3)
        for column in range(COLUMNS)
    ]
    for row in range(ROWS)
]

# combine three
all_houses = all_columns + all_rows + all_blocks


class SudokuSolver:
    """
    SudokuSolver class represents a Sudoku puzzle solver.

    Attributes:
    - __grid (SudokuGrid): An instance of SudokuGrid representing the Sudoku puzzle.

    Methods:
    - __init__(self, grid_str: Union[None, str] = None) -> None:
        Constructor for the SudokuSolver class. Initializes the Sudoku grid.

    - simple_elimination(self) -> None:
        Applies simple elimination technique to fill in candidates for empty cells.

    - remove_element(self, arr: np.ndarray, value_to_remove: int) -> np.ndarray:
        Removes a specified value from the given NumPy array.

    - get_sudoku_grid(self) -> SudokuGrid:
        Returns the SudokuGrid instance representing the Sudoku puzzle.

    - __str__(self) -> str:
        Returns a string representation of the Sudoku puzzle.

    Example Usage:
    >>> sudoku_solver = SudokuSolver("530070000600195000098000060800060003400803001700020006060000280000419005000080079")
    >>> sudoku_solver.simple_elimination()
    >>> print(sudoku_solver)
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
        Constructor for the SudokuSolver class.

        Parameters:
        - grid_str (Union[None, str]): A string containing digits representing the initial Sudoku grid.
          If None, an empty Sudoku grid is created. The string has to be of length 9x9=81

        Returns:
        - None
        """
        self.__grid = SudokuGrid(grid_str)

    def simple_elimination(self):
        """
        Applies the simple elimination technique to remove candidates for unassigned cells.
        If there is one number in a cell - remove it from the candidates of the other cells in the house

        Returns:
        - None
        """
        grid = self.get_sudoku_grid()
        for house in all_houses:
            for cell_position in house:
                cell = grid.get_cell(cell_position)
                if len(cell) == 1:
                    value_to_remove = cell[0]
                    self.remove_candidate_from_house(
                        house, cell_position, value_to_remove
                    )

    def fill_in_candidates(self) -> None:
        """
        Fills in candidate values for empty cells in the Sudoku grid.

        Returns:
        - None
        """
        grid = self.get_sudoku_grid()
        rows, columns = grid.get_shape()
        for row in range(rows):
            for column in range(columns):
                cell = grid.get_cell((row, column))
                if cell == [0]:
                    candidates = list(range(1, DIGITS))
                    grid.set_cell((row, column), np.array(candidates, dtype=np.uint8))

    def remove_candidate_from_house(
        self,
        house: list(Tuple[int, int]),
        cell_position: Tuple[int, int],
        value_to_remove: int,
    ):
        """
        Removes the specified value from the candidates of other cells in the given house.

        Parameters:
        - house (list): The list of cell positions representing a house (row, column, or block).
        - cell_position (tuple): The position of the cell containing the value to be removed.
        - value_to_remove (int): The value to be removed from other cells in the house.

        Returns:
        - None
        """
        for other_cell_position in house:
            if (
                other_cell_position != cell_position
                and value_to_remove
                in self.get_sudoku_grid().get_cell(other_cell_position)
            ):
                updated_candidates = self.remove_element(
                    self.get_sudoku_grid().get_cell(other_cell_position),
                    value_to_remove,
                )
                self.get_sudoku_grid().set_cell(other_cell_position, updated_candidates)

    def remove_element(
        self, arr: np.ndarray, value_to_remove: Union[1, 2, 3, 4, 5, 6, 7, 8, 9]
    ) -> np.ndarray:
        """
        Removes a specified value from the given NumPy array.

        Parameters:
        - arr (np.ndarray): The NumPy array from which to remove the value.
        - value_to_remove (int): The value to be removed.

        Returns:
        - np.ndarray: The modified NumPy array.
        """
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
        return self.get_sudoku_grid().__str__()


if __name__ == "__main__":
    s = SudokuSolver(
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000"
    )
    s.get_sudoku_grid()  # .fill_in_candidates()
    # s.simple_elimination()

    print(s)
