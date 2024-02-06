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
            for row in range(ROWS):
                for column in range(COLUMNS):
                    grid[row, column] = [0]

            self.__grid = grid

    def __parse_sudoku(self, grid: np.ndarray, grid_str: str) -> np.ndarray:
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
                grid[row][column] = [int(cell_char)]

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

    def get_cell(self, position: Tuple[int, int]) -> []:
        row, column = position
        if row < 0 or column < 0:
            raise IndexError("out of bounds for position ({},{})".format(row, column))

        return self.__get_grid()[row][column]

    def set_cell(self, position: Tuple[int, int], new_value: list) -> None:
        row, column = position
        if row < 0 or column < 0:
            raise IndexError("out of bounds for position ({},{})".format(row, column))

        self.__get_grid()[row][column] = new_value

    def __get_grid(self) -> np.ndarray:
        return self.__grid

    def get_shape(self) -> tuple([int, int]):
        return self.__get_grid().shape

    def __iter__(self):
        self.__iterator = (0, 0)
        return self

    def __next__(self) -> np.ndarray:
        rows, columns = self.__iterator

        if rows == ROWS or columns == COLUMNS:
            raise StopIteration

        cell = self.get_cell(self.__iterator)

        self.__increase_iterator()
        return cell

    def __increase_iterator(self) -> None:
        rows, columns = self.__iterator
        if rows == ROWS or columns == COLUMNS:
            raise IndexError(
                "Index: {} out of range for size: {}", self.__iterator, self.get_shape()
            )

        if columns == COLUMNS - 1:
            rows += 1
            self.__iterator = (rows, 0)
            return

        columns += 1
        self.__iterator = (rows, columns)

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the Sudoku puzzle.

        Returns:
        - str: The formatted string representation of the Sudoku puzzle.
        """

        result = ""
        for index, cell in enumerate(self):
            if index % (COLUMNS / 3) == 0 and index != 0 and index % 9 != 0:
                result += "| "
            if index % COLUMNS == 0 and index != 0:
                result += "\n"
            if index % (ROWS * 3) == 0 and index != 0:
                result += "-" * 39 + "\n"
            result += f"{cell} "

        return result.strip()


if __name__ == "__main__":
    grid = SudokuGrid(
        "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    )

    # for cell in grid:
    #     print("cell with value:{}".format(cell))
    print(grid)
