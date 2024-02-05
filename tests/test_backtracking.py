import pytest
import numpy as np
from sudoku.backtracking import Backtracking
from sudoku.sudokuGrid import SudokuGrid, ROWS, COLUMNS
from sudoku.backtracking import State, Variable, Constraint, CONSTRAINT


def test_backtracking_least_values_heuristics():
    pass


def test_backtracking_first_field_heuristics():
    pass


def test_backtracking_simple_csp_no_heuristic_no_backtracking():
    v1 = Variable[int]("v1", None, [1, 2, 3])
    v2 = Variable[int]("v2", None, [1, 2, 3])
    v3 = Variable[int]("v3", None, [1, 2])
    variables = [v1, v2, v3]
    root_state = State[int](variables)  # TODO implement constraints that work properly
    backtracking = Backtracking(root_state)
    res = backtracking.solve()
    assert res != None, "without constraints there should be a solution"
    assert (
        res.get_variable_by_name("v1").get_value() == 1
    ), "Should choose the first value"
    assert (
        res.get_variable_by_name("v2").get_value() == 1
    ), "Should choose the first value"
    assert (
        res.get_variable_by_name("v3").get_value() == 1
    ), "Should choose the first value"


def test_backtracking_with_conflicing_constraints_no_heuristic_one_backtracking():
    v1 = Variable[int]("v1", None, [1, 2, 3])
    v2 = Variable[int]("v2", None, [1, 2, 3])
    v3 = Variable[int]("v3", None, [1, 2])
    c1 = Constraint(v1, v2, CONSTRAINT.NOT_EQUALS)
    variables = [v1, v2, v3]
    constraints = [c1]
    root_state = State[int](
        variables, constraints
    )  # TODO implement constraints that work properly
    backtracking = Backtracking(root_state)
    res = backtracking.solve()
    assert res != None, "with simple constraint there should be a solution"
    assert (
        res.get_variable_by_name("v1").get_value() == 1
    ), "Should be 1 because one is the first value"
    assert (
        res.get_variable_by_name("v2").get_value() == 2
    ), "Should be 2 because of constraint v2!=v1 -> 1 already taken, backtrack to next value 2"
    assert (
        res.get_variable_by_name("v3").get_value() == 1
    ), "Should choose the first value"
