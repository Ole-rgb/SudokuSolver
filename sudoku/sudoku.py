import numpy as np
from typing import Union

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
        The string gets parsed so that the first number is placed in the left top corner
        and the second number in placed in the first column second row.

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
                if row + 1 == ROWS:
                    column += 1
                    row = 0
                else:
                    row += 1
        except ValueError:
            raise InvalidSudokuInput(
                "Parsed sudoku contains character that is not a digit"
            )

        return grid

    def get_grid(self) -> np.ndarray:
        return self.__grid

    def __str__(self) -> str:
        """
        Returns a string representation of the Sudoku grid.

        Returns:
        - str: A string representation of the Sudoku grid.
        """
        return self.__grid.__str__()


class SudokuUtils:
    @staticmethod
    def valid_houses(sudoku, row, column):
        """
        Check if the row, column, and 3x3 square in the Sudoku grid are valid.

        Parameters:
        - sudoku: The Sudoku grid.
        - row: The row index.
        - column: The column index.

        Returns:
        - bool: True if the row, column, and square are valid, False otherwise.
        """
        return (
            SudokuUtils.is_valid_row(sudoku, row)
            and SudokuUtils.is_valid_column(sudoku, column)
            and SudokuUtils.is_valid_block(sudoku, row, column)
        )

    @staticmethod
    def is_valid_row(sudoku, row):
        raise NotImplementedError()

    @staticmethod
    def is_valid_column(sudoku, column):
        raise NotImplementedError()

    @staticmethod
    def is_valid_block():
        raise NotImplementedError()


class LogicChecker:
    @staticmethod
    def simple_elemination(grid: SudokuGrid):
        for index, cell in grid:
            if len(cell) == 1:
                continue
            for candidate in cell:
                if LogicChecker.candidate_in_houses(candidate, index):
                    not NotImplementedError("todo remove candidate from array ")

    @staticmethod
    def candidate_in_houses(candidate, position):
        print(position)


class Sudoku:
    def __init__(self, grid_str: Union[None, str] = None) -> None:
        self.__grid = SudokuGrid(grid_str)

    def fill_cell(self) -> None:
        raise NotImplementedError()

    def fill_in_candidates(self) -> None:
        grid = self.get_np_grid()
        for row in range(grid.shape[0]):
            for column in range(grid.shape[1]):
                cell = grid[row][column]
                if cell == [0]:
                    candidates = list(range(1, DIGITS))
                    grid[row][column] = np.array(candidates, dtype=np.uint8)

    def get_sudoku_grid(self) -> SudokuGrid:
        return self.__grid

    def get_np_grid(self) -> np.ndarray:
        return self.get_sudoku_grid().get_grid()

    def __str__(self) -> str:
        return self.get_np_grid().__str__()


if __name__ == "__main__":
    # Todo
    # grid = SudokuGrid("")
    # LogicChecker.simple_elemination()
    grid_string = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

    sudoku = Sudoku(grid_string)

    print(sudoku)
    sudoku.fill_in_candidates()
    print(sudoku)
