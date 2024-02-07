import pytest
import numpy as np
from sudoku.backtracking import Backtracking
from sudoku.sudokuGrid import SudokuGrid, ROWS, COLUMNS
from sudoku.backtracking import State, Variable, Constraint, CONSTRAINT


@pytest.fixture
def example_variables():
    return [
        Variable("A", value=None, domain=[1, 2, 3]),
        Variable("B", value=None, domain=[1, 2, 3]),
        Variable("C", value=None, domain=[1, 2, 3]),
    ]


@pytest.fixture
def example_constraints(example_variables):
    return [
        Constraint(example_variables[0], example_variables[1], CONSTRAINT.EQUALS),
        Constraint(example_variables[1], example_variables[2], CONSTRAINT.NOT_EQUALS),
    ]


def test_valid_solution_with_all_assigned_and_satisfied_constraints(
    example_variables, example_constraints
):
    state = State(example_variables, [example_constraints[0]])
    for variable in example_variables:
        variable.set_value(1)
    assert state.valid_solution()


def test_invalid_solution_with_all_assigned_but_unsatisfied_constraints(
    example_variables, example_constraints
):
    state = State(example_variables, example_constraints)
    for variable in example_variables:
        variable.set_value(1)
    assert not state.valid_solution()


def test_invalid_solution_with_unassigned_variable(
    example_variables, example_constraints
):
    state = State(example_variables, [example_constraints[0]])
    for variable in example_variables[:-1]:
        variable.set_value(1)
    assert not state.valid_solution()


def test_invalid_solution_with_unassigned_variable_and_unsatisfied_constraints(
    example_variables, example_constraints
):
    state = State(example_variables, example_constraints)
    for variable in example_variables[:-1]:
        variable.set_value(1)
    assert not state.valid_solution()


def test_all_variables_assigned(example_variables, example_constraints):
    state = State(example_variables, example_constraints)
    for variable in example_variables:
        variable.set_value(1)
    assert state._all_variables_assigned()


def test_all_variables_not_assigned(example_variables, example_constraints):
    state = State(example_variables, example_constraints)
    assert not state._all_variables_assigned()


def test_all_variables_one_assigned(example_variables, example_constraints):
    state = State(example_variables, example_constraints)
    example_variables[0].set_value(1)

    assert not state._all_variables_assigned()


def test_valid_state_with_satisfied_constraints_all_variables_assigned(
    example_variables, example_constraints
):
    state = State(example_variables, [example_constraints[0]])
    for variable in example_variables:
        variable.set_value(1)
    assert state.valid_state()


def test_invalid_state_with_unsatisfied_constraints_all_variables_assigned(
    example_variables, example_constraints
):
    state = State(example_variables, example_constraints)
    for variable in example_variables:
        variable.set_value(1)
    assert not state.valid_state()


def test_valid_state_with_satisfied_constraints_no_variables_assigned(
    example_variables, example_constraints
):
    state = State(example_variables, example_constraints)
    assert state.valid_state()


def test_invalid_state_with_satisfied_constraints_all_variables_assigned(
    example_variables, example_constraints
):
    state = State(example_variables, [example_constraints[0]])

    example_variables[1].set_value(1)
    example_variables[2].set_value(1)
    assert state.valid_state()


def test_valid_state_with_satisfied_constraints_all_variables_assigned(
    example_variables, example_constraints
):
    state = State(example_variables, example_constraints)
    example_variables[0].set_value(1)
    example_variables[1].set_value(1)
    example_variables[2].set_value(2)
    assert state.valid_state()


def test_valid_state_with_unsatisfied_constraints_not_all_variables_assigned(
    example_variables, example_constraints
):
    state = State(example_variables, example_constraints)

    example_variables[1].set_value(1)
    example_variables[2].set_value(2)
    assert state.valid_state()


def test__next_state(example_variables, example_constraints):
    state = State(example_variables, example_constraints)
    new_state = state._next_state(example_variables[0], 1)
    assert new_state.get_variable_by_name("A").get_value() == 1
    assert state.get_variable_by_name("A").get_value() is None


def test_get_domain_with_valid_variable(example_variables, example_constraints):
    state = State(example_variables, example_constraints)
    assert state.get_domain_of_variable("A") == [1, 2, 3]


def test_get_domain_with_invalid_variable(example_variables, example_constraints):
    state = State(example_variables, example_constraints)
    with pytest.raises(ValueError, match="variable name: D doesnt exist"):
        state.get_domain_of_variable("D")


def test_state_get_variable_by_name():
    v1 = Variable[int]("v1", None, [1, 2, 3])
    v1.set_value(2)
    state = State[int]([v1])
    assert (
        state.get_variable_by_name("v1") == v1
    ) == True, "should be True, because it should be the same variable"


def test_state_get_variable_by_name():
    v1 = Variable[int]("v1", None, [1, 2, 3])
    v2 = Variable[int]("v2", None, [1, 2, 3])
    v1.set_value(2)
    state = State[int]([v1])
    assert (
        state.get_variable_by_name("v1") == v2
    ) == False, "should be False, because they are different variable"
