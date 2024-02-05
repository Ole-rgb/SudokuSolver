import pytest
import re
from sudoku.sudokuSolver import all_rows, all_columns, all_blocks, SudokuSolver
import numpy as np
from sudoku.sudokuGrid import SudokuGrid, InvalidSudokuInput, ROWS, COLUMNS

"""
Testing the SudokuGrid() class
"""


def test_grid_size():
    grid = SudokuGrid()
    assert (
        grid.get_shape()[0] * grid.get_shape()[1] == ROWS * COLUMNS
    ), "Should have the size 81 aka 9*9"
    assert grid.get_shape() == (
        ROWS,
        COLUMNS,
    ), "Should be an array of form 9x9 with all zeros"


def test_grid_values():
    grid = SudokuGrid()
    assert (
        type(grid.get_cell((0, 0))) == np.ndarray
    ), "Should have the type of np.ndarray"


def test_default_grid_values():
    grid = SudokuGrid()
    for column in range(1, COLUMNS):
        for row in range(1, ROWS):
            assert grid.get_cell((row, column)) == [0], "every entry should be zero"


def test_parsed_sudoku_values_all_ones():
    sudoku = "111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    grid = SudokuGrid(sudoku)

    assert len(sudoku) == ROWS * COLUMNS, "Sudoku field has 81 cells"
    for column in range(1, COLUMNS):
        for row in range(1, ROWS):
            assert grid.get_cell((row, column)) == [1], "every entry should be one"


def test_parsed_sudoku_values_asc_in_row():
    sudoku = "123456789123456789123456789123456789123456789123456789123456789123456789123456789"
    grid = SudokuGrid(sudoku)

    assert len(sudoku) == ROWS * COLUMNS, "Sudoku field has 81 cells"
    assert (
        grid.get_cell((0, 0)) == [1]
        and grid.get_cell((0, 1)) == [2]
        and grid.get_cell((0, 2)) == [3]
        and grid.get_cell((0, 8)) == [9]
    ), "first row should have the values 1,2,...,9"
    assert (
        grid.get_cell((0, 0)) == [1]
        and grid.get_cell((1, 0)) == [1]
        and grid.get_cell((2, 0)) == [1]
        and grid.get_cell((8, 0)) == [1]
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


def test_iterate_grid():
    sudoku = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    grid = SudokuGrid(sudoku)
    counter = 0
    for _ in grid:
        counter += 1
    assert (
        counter == ROWS * COLUMNS
    ), "The counter should iterate over every element, aka 81 elements"

    for index, cell in enumerate(grid):
        if index == 0:
            assert np.array_equal(
                cell, [5]
            ), "The first element should be 5 (the first element of the array)"
        if index == 1:
            assert np.array_equal(
                cell, [3]
            ), "The gird should iterate each row (the second element of the array is 3)"
        if index == ROWS * COLUMNS - 1:
            assert np.array_equal(
                cell, [9]
            ), "The last element should be 9 (the last element of the array)"


def test_all_rows():
    assert all_rows[0] == [
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (0, 7),
        (0, 8),
    ], "the frist row should have row=0 and column=1-8"
    assert all_rows[8] == [
        (8, 0),
        (8, 1),
        (8, 2),
        (8, 3),
        (8, 4),
        (8, 5),
        (8, 6),
        (8, 7),
        (8, 8),
    ], "the last row should have row=8 and column=1-8"


def test_all_columns():
    assert all_columns[0] == [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (5, 0),
        (6, 0),
        (7, 0),
        (8, 0),
    ], "the frist column should have column=0 and row=1-8"
    assert all_columns[8] == [
        (0, 8),
        (1, 8),
        (2, 8),
        (3, 8),
        (4, 8),
        (5, 8),
        (6, 8),
        (7, 8),
        (8, 8),
    ], "the last column should have column=8 and row=1-8"


def test_all_blocks():
    assert all_blocks[0] == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    ], "the frist block should start with (0,0), goes to the left and after 3 elements to the next row"
    assert all_blocks[8] == [
        (6, 6),
        (6, 7),
        (6, 8),
        (7, 6),
        (7, 7),
        (7, 8),
        (8, 6),
        (8, 7),
        (8, 8),
    ], "the last block should be the block on the bottom right"


def test_set_cell():
    grid = SudokuGrid()
    new_value = np.array([1, 2, 3], dtype=np.ndarray)

    assert grid.get_cell((1, 0)) == [0]

    grid.set_cell((1, 0), new_value)

    assert grid.get_cell((0, 0)) == [0] and grid.get_cell((3, 3)) == [
        0 and grid.get_cell((8, 8)) == [0]
    ], "The other cells should still be [0]"

    assert np.array_equal(
        grid.get_cell((1, 0)), [1, 2, 3]
    ), "The cell should be filled with the new array [1,2,3]"


def test_set_cell_out_of_positive_bounds():
    MSG = "index 9 is out of bounds for axis 0 with size 9"
    grid = SudokuGrid()
    new_value = np.array([1, 2, 3], dtype=np.ndarray)
    with pytest.raises(IndexError, match=MSG):
        grid.set_cell((9, 0), new_value)
    with pytest.raises(IndexError, match=MSG):
        grid.set_cell((0, 9), new_value)
    with pytest.raises(IndexError, match=MSG):
        grid.set_cell((9, 9), new_value)

    for cell in grid:
        assert cell == [0], "All cells should still be filled with the initial [0]"


def test_set_cell_out_of_negative_bounds():
    grid = SudokuGrid()
    new_value = np.array([1, 2, 3], dtype=np.ndarray)

    with pytest.raises(
        IndexError, match=re.escape("out of bounds for position (-1,0)")
    ):
        grid.set_cell((-1, 0), new_value)
    with pytest.raises(
        IndexError, match=re.escape("out of bounds for position (0,-1)")
    ):
        grid.set_cell((0, -1), new_value)
    with pytest.raises(
        IndexError, match=re.escape("out of bounds for position (-1,-1)")
    ):
        grid.set_cell((-1, -1), new_value)

    for cell in grid:
        assert cell == [0], "All cells should still be filled with the initial [0]"


def test_get_cell():
    grid = SudokuGrid()
    new_value = np.array([1, 2, 3], dtype=np.ndarray)
    grid.set_cell((1, 0), new_value)

    assert grid.get_cell((0, 0)) == [0] and grid.get_cell((3, 3)) == [
        0 and grid.get_cell((8, 8)) == [0]
    ], "The other cells should still be [0]"

    assert np.array_equal(
        grid.get_cell((1, 0)), [1, 2, 3]
    ), "The cell should be filled with the new array [1,2,3]"


def test_get_cell_out_of_positive_bounds():
    grid = SudokuGrid()

    with pytest.raises(
        IndexError, match="index 9 is out of bounds for axis 0 with size 9"
    ):
        grid.get_cell((9, 0))
    with pytest.raises(
        IndexError, match="index 9 is out of bounds for axis 0 with size 9"
    ):
        grid.get_cell((0, 9))

    with pytest.raises(
        IndexError, match="index 9 is out of bounds for axis 0 with size 9"
    ):
        grid.get_cell((9, 9))


def test_get_cell_out_of_negative_bounds():
    grid = SudokuGrid()

    with pytest.raises(
        IndexError, match=re.escape("out of bounds for position (-1,0)")
    ):
        grid.get_cell((-1, 0))
    with pytest.raises(
        IndexError, match=re.escape("out of bounds for position (0,-1)")
    ):
        grid.get_cell((0, -1))
    with pytest.raises(
        IndexError, match=re.escape("out of bounds for position (-1,-1)")
    ):
        grid.get_cell((-1, -1))
