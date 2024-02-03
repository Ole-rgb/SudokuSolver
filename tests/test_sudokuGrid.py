import pytest
from sudoku.sudoku import SudokuGrid, InvalidSudokuInput
import numpy as np

ROWS, COLUMNS = 9, 9

"""
Testing the SudokuGrid() class
"""


def test_grid_size():
    grid = SudokuGrid()
    assert grid.get_grid().size == ROWS * COLUMNS, "Should have the size 81 aka 9*9"
    assert grid.get_grid().shape == (
        ROWS,
        COLUMNS,
    ), "Should be an array of form 9x9 with all zeros"


def test_grid_values():
    grid = SudokuGrid()
    assert type(grid.get_grid()[0][0]) == np.ndarray, "Should have the type of array"
    # assert grid.get_grid().shape == (ROWS, COLUMNS), "Should be an array of form 9x9 with all zeros"


def test_default_grid_values():
    grid = SudokuGrid()
    for column in range(1, COLUMNS):
        for row in range(1, ROWS):
            assert grid.get_grid()[row][column] == [0], "every entry should be zero"


def test_parsed_sudoku_values_all_ones():
    sudoku = "111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    grid = SudokuGrid(sudoku)

    assert len(sudoku) == ROWS * COLUMNS, "Sudoku field has 81 cells"
    for column in range(1, COLUMNS):
        for row in range(1, ROWS):
            assert grid.get_grid()[row][column] == [1], "every entry should be one"


def test_parsed_sudoku_values_asc_in_row():
    sudoku = "123456789123456789123456789123456789123456789123456789123456789123456789123456789"
    grid = SudokuGrid(sudoku)

    assert len(sudoku) == ROWS * COLUMNS, "Sudoku field has 81 cells"
    assert (
        grid.get_grid()[0][0] == [1]
        and grid.get_grid()[0][1] == [2]
        and grid.get_grid()[0][2] == [3]
        and grid.get_grid()[0][8] == [9]
    ), "first row should have the values 1,2,...,9"
    assert (
        grid.get_grid()[0][0] == [1]
        and grid.get_grid()[1][0] == [1]
        and grid.get_grid()[2][0] == [1]
        and grid.get_grid()[8][0] == [1]
    ), "first column should have the value 1"


def test_parsed_sudoku_short_string():
    sudoku_to_short = "1234567891234567891234567891234567891234567891234567891234567891234567891234567"
    assert (
        len(sudoku_to_short) == 79
    ), "Sudoku string should have 79 cells, because its to short"

    with pytest.raises(
        InvalidSudokuInput,
        match="Length or parsed sudoku needs to be {}, but is {}".format(
            ROWS * COLUMNS, len(sudoku_to_short)
        ),
    ):
        SudokuGrid(sudoku_to_short)


def test_parsed_sudoku_long_string():
    sudoku_to_long = "1234567891234567891234567891234567891234567891234567891234567891234567891234567223"
    assert (
        len(sudoku_to_long) == 82
    ), "Sudoku string should have 82 cells, because its to short"

    with pytest.raises(
        InvalidSudokuInput,
        match="Length or parsed sudoku needs to be {}, but is {}".format(
            ROWS * COLUMNS, len(sudoku_to_long)
        ),
    ):
        SudokuGrid(sudoku_to_long)


def test_parsed_sudoku_special_character():
    sudoku_to_long = "-2345678912+456789123456789123456789123456789123456789123456789123456789123456722"
    assert len(sudoku_to_long) == 81, "Sudoku string should have 81 cells"

    with pytest.raises(
        InvalidSudokuInput, match="Parsed sudoku contains character that is not a digit"
    ):
        SudokuGrid(sudoku_to_long)
