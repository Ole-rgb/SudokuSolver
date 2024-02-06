import pytest
from sudoku.sudokuSolver import (
    SudokuSolver,
    all_blocks,
    all_columns,
    all_rows,
)
import numpy as np

from sudoku.sudokuGrid import ROWS, COLUMNS


def test_fill_in_candidates_normal_sudoku():
    """
    Every 0 gets replaces with the numbers from 1 to 9
    Every numbers that is not 0 is a filled in number and therefore immutable
    """
    grid_string = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

    solver = SudokuSolver(grid_string)
    grid = solver.get_sudoku_grid()
    solver.fill_in_candidates()

    assert np.array_equal(
        grid.get_cell((0, 0)), np.array([5])
    ), "first element in the first row is 5"
    assert np.array_equal(
        grid.get_cell((0, 1)), np.array([3])
    ), "second entry in the first row is 3"
    assert np.array_equal(
        grid.get_cell((0, 2)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "third element in the first row is 0 -> [0,...,9]"
    assert np.array_equal(
        grid.get_cell((0, 3)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "forth element in the first row is 0 -> [0,...,9]"
    assert np.array_equal(
        grid.get_cell((0, 4)), np.array([7])
    ), "fifth element in the first row should be 7"
    assert np.array_equal(
        grid.get_cell((0, 5)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "sixth element in the first row is 0 -> [0,...,9]"
    assert np.array_equal(
        grid.get_cell((1, 0)), np.array([6])
    ), "first element in the second row should be 6"
    assert np.array_equal(
        grid.get_cell((1, 1)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "second element in the second row is 0 -> [0,...,9]"
    assert np.array_equal(
        grid.get_cell((1, 2)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ), "third element in the second row is 0 -> [0,...,9]"
    assert np.array_equal(
        grid.get_cell((1, 3)), np.array([1])
    ), "third element in the second row should be 1"


def test_fill_in_candidates_two_iterations_shouldnt_fail():
    """
    Every 0 gets replaces with the numbers from 1 to 9
    Every numbers that is not 0 is a filled in number and therefore immutable
    """
    grid_string = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

    solver = SudokuSolver(grid_string)
    grid = solver.get_sudoku_grid()
    solver.fill_in_candidates()
    solver.fill_in_candidates()


def test_fill_in_candidates_easy_sudoku():
    sudoku_solver = SudokuSolver(
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000"
    )
    grid = sudoku_solver.get_sudoku_grid()
    sudoku_solver.fill_in_candidates()

    # all candidates
    for row in range(0, ROWS):
        for column in range(0, COLUMNS):
            if (row, column) == (0, 0):
                assert grid.get_cell((row, column)) == [1]
                continue

            assert np.array_equal(
                grid.get_cell((row, column)), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
            )


def test_simple_elemination_one_number():
    # with empty sudoku
    solver = SudokuSolver(
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000"
    )
    solver.fill_in_candidates()
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
    solver.fill_in_candidates()
    solver.simple_elimination()

    # fixed values
    assert (
        solver.get_sudoku_grid().get_cell((0, 0)) == 1
    ), "fixed value 1 shouldnt be changed"

    assert (
        solver.get_sudoku_grid().get_cell((1, 1)) == 2
    ), "fixed value 2 shouldnt be changed"

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
    solver.fill_in_candidates()
    solver.simple_elimination()

    # fixed values
    assert (
        solver.get_sudoku_grid().get_cell((0, 0)) == 1
    ), "fixed value 1 at location (3, 8) shouldnt be changed"

    assert (
        solver.get_sudoku_grid().get_cell((3, 8)) == 1
    ), "fixed value 1 at location (3, 8) shouldnt be changed"

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


def test_simple_elemination_numbers_no_candidates():
    solver = SudokuSolver(
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000"
    )
    assert (
        solver.simple_elimination() == 0
    ), "there are no filled in candidates to remove"


def test_simple_elemination_numbers_removed_candidates():
    solver = SudokuSolver(
        "100000000000000000000000000000000000000000000000000000000000000000000000000000000"
    )
    solver.fill_in_candidates()  # 9 candidates in 80 cells 9*80
    assert (
        solver.simple_elimination() == 20
    ), "should removed 1 from every cell in constraint houses"


def test_simple_elemination_numbers_same_value_different_row_different_block_different_column():
    solver = SudokuSolver(
        "100000000000000000000000000000000000010000000000000000000000000000000000000000000"
    )
    solver.fill_in_candidates()
    assert solver.simple_elimination() == 34


def test_simple_elemination_numbers_different_value_different_row_different_block_different_column():
    solver = SudokuSolver(
        "100000000000000000000000000000000000020000000000000000000000000000000000000000000"
    )
    solver.fill_in_candidates()
    assert solver.simple_elimination() == 40


def test_simple_elemination_two_iterations_second_empty():
    solver = SudokuSolver(
        "100000000000000000000000000000000000020000000000000000000000000000000000000000000"
    )
    solver.fill_in_candidates()
    assert solver.simple_elimination() == 40
    assert solver.simple_elimination() == 0


def test_simple_elemination_two_iterations_second_removes_values():
    solver = SudokuSolver(
        "123456700000000000000000000000008000000000000000000000391547620000000000000000000"
    )
    solver.fill_in_candidates()
    assert (
        solver.simple_elimination() != 0
    ), "remove alot of candidates because everywhere [1,2,..,9]"
    assert (
        solver.simple_elimination() != 0
    ), "can remove further, because 7th row has only one candidate for last cell"
    assert (
        solver.simple_elimination() != 0
    ), "can remove further, because 1th row has only one candidate in last cell"
    assert (
        solver.simple_elimination() == 0
    ), "cant remove further, no additional call has only one candidate."


def test_remove_element_remove_element():
    solver = SudokuSolver()
    new_array, removed = solver._SudokuSolver__remove_element([0, 1, 2], 2)

    assert np.array_equal(new_array, [0, 1])
    assert removed == 1


def test_remove_element_not_in_list():
    solver = SudokuSolver()
    new_array, removed = solver._SudokuSolver__remove_element([0, 1, 2], 3)

    assert np.array_equal(new_array, [0, 1, 2])
    assert removed == 0


def test_remove_element_one_element_left():
    solver = SudokuSolver()
    new_array, removed = solver._SudokuSolver__remove_element([0, 1], 1)

    assert np.array_equal(new_array, [0])
    assert removed == 1


def test_remove_element_array_empty_after_remove():
    solver = SudokuSolver()

    new_array, removed = solver._SudokuSolver__remove_element([1], 1)


def test_remove_element_one_element_array_remove_other_candidate():
    solver = SudokuSolver()

    new_array, removed = solver._SudokuSolver__remove_element([1], 2)
    assert new_array == [1]
    assert removed == 0


def test_remove_candidates_from_house():
    # solver = SudokuSolver()
    # solver._SudokuSolver__remove_candidate_from_house()
    pass
