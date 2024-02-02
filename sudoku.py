import numpy as np
from typing import Union

ROWS, COLUMNS = (9,9)
DIGITS=10

class InvalidSudokuInput(Exception):
    pass

class SudokuGrid():
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
    def __init__(self, sudoku_str:Union[None,str]=None) -> None:
        """
        Initializes a SudokuGrid object.

        Parameters:
        - sudoku_str (Union[None, str]): Optional. If provided, a string containing digits representing the Sudoku grid.
          If None, the grid will be initialized with zeros.

        Raises:
        - InvalidSudokuInput: If the provided sudoku string has an invalid length or contains a character that is not a digit.
        """
        if type(sudoku_str) is str:
            self.__grid = self.__parse_sudoku(sudoku_str)
        else:
            self.__grid = np.full((ROWS, COLUMNS), fill_value=np.array([0]), dtype=np.uint8)


    def __parse_sudoku(self, grid_str:str) -> np.array:
        """
        Parse a string representing a Sudoku grid into a 2D NumPy array.

        Parameters:
        - grid_str (str): A string containing digits representing the Sudoku grid.
        
        Returns:
        - np.array: A 2D NumPy array representing the parsed Sudoku grid.
        
        Raises:
        - InvalidSudokuInput: If the length of the input string is not equal to ROWS * COLUMNS,
          or if the input string contains a character that is not a digit.
        """
        if len(grid_str) != ROWS*COLUMNS:
            raise InvalidSudokuInput("Length or parsed sudoku needs to be {}, but is {}".format(ROWS*COLUMNS, len(grid_str)))

        sudoku_grid = np.zeros((ROWS, COLUMNS), dtype=np.uint8)
        row, column = 0,0
        try:
            for cell_char in grid_str:
                sudoku_grid[row][column] = int(cell_char)

                if row+1 == ROWS:
                    column += 1
                    row = 0
                else:
                    row += 1
        except:
            raise InvalidSudokuInput("Parsed sudoku contains character that is not a digit")
            
        return sudoku_grid
    
    def get_grid(self) -> np.array:
        return self.__grid
    def __str__(self) -> str:
        """
        Returns a string representation of the Sudoku grid.

        Returns:
        - str: A string representation of the Sudoku grid.
        """
        return self.__grid.__str__()
    

    
    
class Sudoku():
    def __init__(self, grid_str:Union[None,str]=None) -> None:
        self.grid = SudokuGrid(grid_str)
        
        
if __name__ == "__main__":
    pass