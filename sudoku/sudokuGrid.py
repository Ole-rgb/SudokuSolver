from typing import Union, Tuple
import numpy as np

ROWS, COLUMNS = (9, 9)
DIGITS = 10


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
