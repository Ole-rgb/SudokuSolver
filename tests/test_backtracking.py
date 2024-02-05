import pytest
import numpy as np
from sudoku.backtracking import Backtracking
from sudoku.sudokuGrid import SudokuGrid, ROWS, COLUMNS
from sudoku.backtracking import State, Variable, Constraint, CONSTRAINT


@pytest.fixture
def example_variables():
    return [
        Variable[int]("v1", None, [1, 2, 3]),
        Variable[int]("v2", None, [1, 2, 3]),
        Variable[int]("v3", None, [1, 2]),
    ]


@pytest.fixture
def example_constraints(example_variables):
    return [
        Constraint(example_variables[0], example_variables[1], CONSTRAINT.EQUALS),
        Constraint(example_variables[0], example_variables[1], CONSTRAINT.NOT_EQUALS),
        Constraint(example_variables[1], example_variables[2], CONSTRAINT.NOT_EQUALS),
    ]


def test_backtracking_least_values_heuristics():
    pass


def test_backtracking_first_field_heuristics():
    pass


def test_backtracking_simple_csp_no_heuristic_no_constraints(example_variables):
    root_state = State[int](example_variables)
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


def test_backtracking_with_constraints_no_heuristic_one_backtracking(
    example_variables, example_constraints
):
    root_state = State[int](example_variables, [example_constraints[1]])
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


def test_backtracking_with_conflicing_constraints_no_heuristic_pinched_domain(
    example_variables, example_constraints
):
    example_variables[0].set_domain([2, 3])
    example_variables[1].set_domain([2, 3])
    root_state = State[int](example_variables, [example_constraints[1]])
    backtracking = Backtracking(root_state)
    res = backtracking.solve()
    assert res != None, "with simple constraint there should be a solution"
    assert (
        res.get_variable_by_name("v1").get_value() == 2
    ), "Should be 1 because one is the first value"
    assert (
        res.get_variable_by_name("v2").get_value() == 3
    ), "Should be 2 because of constraint v2!=v1 -> 1 already taken, backtrack to next value 2"
    assert (
        res.get_variable_by_name("v3").get_value() == 1
    ), "Should choose the first value"


def test_backtracking_with_conflicing_constraints_no_heuristic_no_solution(
    example_variables, example_constraints
):
    root_state = State[int](
        example_variables, [example_constraints[0], example_constraints[1]]
    )
    backtracking = Backtracking(root_state)
    res = backtracking.solve()
    assert res == None


def test_backtracking_with_two_constraints_conflicting_down_the_road_no_heuristic_no_solution(
    example_variables, example_constraints
):
    for variable in example_variables:
        variable.set_domain([1])
    root_state = State[int](
        example_variables, [example_constraints[0], example_constraints[2]]
    )
    backtracking = Backtracking(root_state)
    res = backtracking.solve()
    assert res == None


def test_backtracking_with_two_constraints_no_heuristic_lots_of_backtracking(
    example_variables, example_constraints
):
    example_variables[1].set_domain([2, 3])
    example_variables[2].set_domain([2])

    root_state = State[int](
        example_variables, [example_constraints[0], example_constraints[2]]
    )
    backtracking = Backtracking(root_state)
    res = backtracking.solve()
    assert res != None

    assert res.get_variable_by_name("v1").get_value() == 3
    assert res.get_variable_by_name("v2").get_value() == 3
    assert res.get_variable_by_name("v3").get_value() == 2
