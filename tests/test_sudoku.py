import pytest
from sudoku.sudoku import (
    SudokuGrid,
    InvalidSudokuInput,
    SudokuSolver,
    all_blocks,
    all_columns,
    all_rows,
)
import numpy as np

ROWS, COLUMNS = 9, 9


def test_simple_elemination_one_number():
    # with empty sudoku
    solver = SudokuSolver(
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000"
    )
    solver.get_sudoku_grid().fill_in_candidates()
    solver.simple_elimination()

    # first block, first row and first column should have candidates 2-9, except (0,0) = [1]
    assert (
        solver.get_sudoku_grid().get_cell((0, 0)) == 1
    ), "fixed value 1 shouldnt be changed"

    for row, column in all_rows[0]:
        if (row, column) == (0, 0):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([2, 3, 4, 5, 6, 7, 8, 9]),
        ), "first row (starting at the second cell) should have the candidates 1-9 without the 1"

    for row, column in all_columns[0]:
        if (row, column) == (0, 0):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([2, 3, 4, 5, 6, 7, 8, 9]),
        ), "first column (starting at the second cell) should have the candidates 1-9 without the 1"

    for row, column in all_blocks[0]:
        if (row, column) == (0, 0):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([2, 3, 4, 5, 6, 7, 8, 9]),
        ), "first block (starting at the second cell) should have the candidates 1-9 without the 1"

    for column in range(3, 9):
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((1, column)),
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ), "the second row should still have all candidates"
    for column in range(3, 9):
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((2, column)),
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ), "the thrid should still have all candidates"
    for column in range(1, 9):
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((3, column)),
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ), "the fourth should still have all candidates"
    for column in range(1, 9):
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((4, column)),
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ), "the fifth should still have all candidates"
    for column in range(1, 9):
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((5, column)),
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ), "the sixth should still have all candidates"
    for column in range(1, 9):
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((6, column)),
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ), "the seventh should still have all candidates"
    for column in range(1, 9):
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((7, column)),
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ), "the eighth should still have all candidates"
    for column in range(1, 9):
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((8, column)),
            np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ), "the ninth should still have all candidates"


def test_simple_elemination_two_numbers_different_value_different_block_row_column_same_block():
    solver = SudokuSolver(
        "100000000020000000000000000000000000000000000000000000000000000000000000000000000"
    )
    solver.get_sudoku_grid().fill_in_candidates()
    solver.simple_elimination()

    # fixed values
    assert (
        solver.get_sudoku_grid().get_cell((0, 0)) == 1
    ), "fixed value 1 shouldnt be changed"

    assert (
        solver.get_sudoku_grid().get_cell((1, 1)) == 2
    ), "fixed value 1 shouldnt be changed"

    for row, column in all_blocks[0]:
        if (row, column) == (0, 0) or (row, column) == (1, 1):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([3, 4, 5, 6, 7, 8, 9]),
        ), "first block should have the candidates 1-9 without 1 and 2"

    for row, column in all_rows[0]:
        if (row, column) == (0, 0):
            continue
        elif column < 3:
            assert np.array_equal(
                solver.get_sudoku_grid().get_cell((row, column)),
                np.array([3, 4, 5, 6, 7, 8, 9]),
            ), "cells in the first block should have the candidates 1-9 without 1 and 2"
        else:
            assert np.array_equal(
                solver.get_sudoku_grid().get_cell((row, column)),
                np.array([2, 3, 4, 5, 6, 7, 8, 9]),
            ), "cells in the first row but not in the first block should have the candidates 1-9 without 1"

    for row, column in all_rows[1]:
        if (row, column) == (1, 1):
            continue
        elif column < 3:
            assert np.array_equal(
                solver.get_sudoku_grid().get_cell((row, column)),
                np.array([3, 4, 5, 6, 7, 8, 9]),
            ), "cells in the first block should have the candidates 1-9 without 1 and 2"
        else:
            assert np.array_equal(
                solver.get_sudoku_grid().get_cell((row, column)),
                np.array([1, 3, 4, 5, 6, 7, 8, 9]),
            ), "cells in the second row but not in the first block should have the candidates 1-9 without 2"

    for row, column in all_rows[2]:
        if column < 3:
            assert np.array_equal(
                solver.get_sudoku_grid().get_cell((row, column)),
                np.array([3, 4, 5, 6, 7, 8, 9]),
            ), "cells in the third block should have the candidates 1-9 without 1 and 2"
        else:
            assert np.array_equal(
                solver.get_sudoku_grid().get_cell((row, column)),
                np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
            ), "cells in the third row but not in the first block should have the candidates 1-9"

    # i dont want to test all cells so we just do sample cells
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((3, 3)), [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ), "cell(3,3) isnt effected and should have all candidates"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((8, 8)), [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ), "cell (0,1) should have all candidates (not constraint)"


def test_simple_elemination_two_numbers_some_value_different_block_row_column():
    solver = SudokuSolver(
        "100000000000000000000000000000000001000000000000000000000000000000000000000000000"
    )
    solver.get_sudoku_grid().fill_in_candidates()
    solver.simple_elimination()

    # fixed values
    assert (
        solver.get_sudoku_grid().get_cell((0, 0)) == 1
    ), "fixed value 1 shouldnt be changed"

    assert (
        solver.get_sudoku_grid().get_cell((3, 8)) == 1
    ), "fixed value 1 shouldnt be changed"

    for row, column in all_blocks[0]:
        if (row, column) == (0, 0):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([2, 3, 4, 5, 6, 7, 8, 9]),
        ), "first block should have the candidates 1-9 without 1"

    for row, column in all_blocks[5]:
        if (row, column) == (3, 8):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([2, 3, 4, 5, 6, 7, 8, 9]),
        ), "fifth block should have the candidates 1-9 without 1"

    for row, column in all_rows[0]:
        if (row, column) == (0, 0):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([2, 3, 4, 5, 6, 7, 8, 9]),
        ), "first row (starting at the second cell) should have the candidates 1-9 without the 1"

    for row, column in all_rows[3]:
        if (row, column) == (3, 8):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([2, 3, 4, 5, 6, 7, 8, 9]),
        ), "forth row (starting at the second cell) should have the candidates 1-9 without the 1"

    for row, column in all_columns[0]:
        if (row, column) == (0, 0):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([2, 3, 4, 5, 6, 7, 8, 9]),
        ), "first column (starting at the second cell) should have the candidates 1-9 without the 1"

    for row, column in all_columns[8]:
        if (row, column) == (3, 8):
            continue
        assert np.array_equal(
            solver.get_sudoku_grid().get_cell((row, column)),
            np.array([2, 3, 4, 5, 6, 7, 8, 9]),
        ), "the last column (starting at the second cell) should have the candidates 1-9 without the 1"

    # the rest should have all candidates
    # test via random sample survey

    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((1, 5)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(1, 5) should have all candidates"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((2, 5)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(2, 5) should have all candidates"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((3, 5)), np.array([2, 3, 4, 5, 6, 7, 8, 9])
    ), "(3, 5) shouldnt have 1 because row==3"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((4, 5)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(4, 5) should have all candidates"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((5, 5)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(5, 5) should have all candidates"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((6, 5)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(6, 5) should have all candidates"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((7, 5)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(7, 5) should have all candidates"

    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((1, 7)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(1, 7) should have all candidates"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((2, 7)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(2, 7) should have all candidates"
    assert not np.array_equal(
        solver.get_sudoku_grid().get_cell((3, 7)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(3, 7) shouldnt have all candidates [-1]"
    assert not np.array_equal(
        solver.get_sudoku_grid().get_cell((4, 7)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(4, 7) shouldnt have all candidates [-1]"
    assert not np.array_equal(
        solver.get_sudoku_grid().get_cell((5, 7)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(5, 7) shouldnt have all candidates [-1]"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((6, 7)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(6, 7) should have all candidates"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((7, 7)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(7, 7) should have all candidates"
    assert np.array_equal(
        solver.get_sudoku_grid().get_cell((8, 7)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "(8, 7) should have all candidates"
