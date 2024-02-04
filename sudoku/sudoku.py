import numpy as np
from typing import Union, Tuple

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


class InvalidSudokuInput(Exception):
    pass


class SudokuGrid:
    """
    Represents a Sudoku grid using a 2D NumPy array.

    Attributes:
    - grid (np.array): A 2D NumPy array representing the Sudoku grid.

    Methods:
    - __init__(sudoku_str: Union[None, str] = None) -> None:
        Initializes a SudokuGrid object. If a Sudoku string is provided, it is parsed into the grid.

    - __parse_sudoku(grid_str: str) -> np.array:
        Parses a string representing a Sudoku grid into a 2D NumPy array.

    - __str__() -> str:
        Returns a string representation of the Sudoku grid.

    Raises:
    - InvalidSudokuInput: If the length of the input string is not equal to ROWS * COLUMNS,
      or if the input string contains a character that is not a digit.
    """

    def __init__(self, sudoku_str: Union[None, str] = None) -> None:
        """
        Initializes a SudokuGrid object.

        Parameters:
        - sudoku_str (Union[None, str]): Optional. If provided, a string containing digits representing the Sudoku grid.
          If None, the grid will be initialized with zeros.

        Raises:
        - InvalidSudokuInput: If the provided sudoku string has an invalid length or contains a character that is not a digit.
        """
        grid = np.empty((ROWS, COLUMNS), dtype=np.ndarray)

        if type(sudoku_str) is str:
            self.__grid = self.__parse_sudoku(grid, sudoku_str)
        else:
            for i in range(9):
                for j in range(9):
                    grid[i, j] = np.array([0], dtype=np.uint8)

            self.__grid = grid

    def __parse_sudoku(self, grid, grid_str: str) -> np.ndarray:
        """
        Parse a string representing a Sudoku grid into a 2D NumPy array.

        Parameters:
        - grid (np.ndarray): The 2D NumPy array to be filled with parsed values.
        - grid_str (str): A string containing digits representing the Sudoku grid.

        Returns:
        - np.ndarray: A 2D NumPy array representing the parsed Sudoku grid.

        Raises:
        - InvalidSudokuInput: If the length of the input string is not equal to ROWS * COLUMNS,
          or if the input string contains a character that is not a digit.
        """
        if len(grid_str) != ROWS * COLUMNS:
            raise InvalidSudokuInput(
                "Length or parsed sudoku needs to be {}, but is {}".format(
                    ROWS * COLUMNS, len(grid_str)
                )
            )

        row, column = 0, 0
        try:
            for cell_char in grid_str:
                grid[row][column] = np.array([int(cell_char)], dtype=np.uint8)

                if column + 1 == COLUMNS:
                    row += 1
                    column = 0
                else:
                    column += 1

        except ValueError:
            raise InvalidSudokuInput(
                "Parsed sudoku contains character that is not a digit"
            )

        return grid

    def fill_in_candidates(self) -> None:
        """
        Fills in candidate values for empty cells in the Sudoku grid.

        Returns:
        - None
        """
        grid = self.get_grid()
        rows, columns = grid.shape
        for row in range(rows):
            for column in range(columns):
                cell = self.get_cell((row, column))
                if cell == [0]:
                    candidates = list(range(1, DIGITS))
                    self.set_cell((row, column), np.array(candidates, dtype=np.uint8))

    def get_cell(self, position: Tuple[int, int]) -> np.ndarray:
        row, column = position
        if row < 0 or column < 0:
            raise IndexError("out of bounds for position ({},{})".format(row, column))

        return self.get_grid()[row][column]

    def set_cell(self, position: Tuple[int, int], new_value: np.ndarray) -> None:
        row, column = position
        if row < 0 or column < 0:
            raise IndexError("out of bounds for position ({},{})".format(row, column))

        self.get_grid()[row][column] = new_value

    def get_grid(self) -> np.ndarray:
        return self.__grid

    def __str__(self) -> str:
        """
        Returns a string representation of the Sudoku grid.

        Returns:
        - str: A string representation of the Sudoku grid.
        """
        return self.__grid.__str__()


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
