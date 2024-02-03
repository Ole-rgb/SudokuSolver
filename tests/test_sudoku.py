import pytest
from sudoku.sudoku import SudokuGrid, InvalidSudokuInput, Sudoku
import numpy as np

ROWS, COLUMNS = 9, 9


def test_fill_in_candidates():
    """
    Every 0 gets replaces with the numbers from 1 to 9
    Every numbers that is not 0 is a filled in number and therefore immutable
    """
    grid_string = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

    sudoku = Sudoku(grid_string)

    sudoku.fill_in_candidates()

    assert np.array_equal(
        sudoku.get_np_grid()[0][0], np.array([5])
    ), "first element in the first row is 5"
    assert np.array_equal(
        sudoku.get_np_grid()[1][0], np.array([3])
    ), "first entry in the second row is 3"
    assert np.array_equal(
        sudoku.get_np_grid()[2][0], np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "first element in the third row is 0 -> [0,...,9]"
    assert np.array_equal(
        sudoku.get_np_grid()[0][1], np.array([6])
    ), "second element in the first row is 6"
    assert np.array_equal(
        sudoku.get_np_grid()[1][1], np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "second element in the second row is 0 -> [0,...,9]"
