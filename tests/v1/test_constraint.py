import pytest
import numpy as np
from sudoku.backtracking import Backtracking
from sudoku.sudokuGrid import SudokuGrid, ROWS, COLUMNS
from sudoku.backtracking import State, Variable, Constraint, CONSTRAINT


@pytest.fixture
def variables():
    return [
        Variable("v1", value=None, domain=[1, 2, 3]),
        Variable("v2", value=None, domain=[1, 2, 3]),
        Variable("v3", value=3, domain=[1, 2, 3]),
    ]


def test_constraint_equals(variables):
    variables[0].set_value(1)
    variables[1].set_value(2)
    constraint = Constraint(variables[0], variables[1], CONSTRAINT.EQUALS)
    assert constraint.satisfied() is False, "False because 1 != 2"

    constraint = Constraint(variables[0], variables[0], CONSTRAINT.EQUALS)
    assert constraint.satisfied() is True, "True because 1 == 1"


def test_constraint_not_equals(variables):
    variables[0].set_value(1)
    variables[1].set_value(2)
    constraint = Constraint(variables[0], variables[1], CONSTRAINT.NOT_EQUALS)
    assert constraint.satisfied() is True, "False because 1 != 2"

    constraint = Constraint(variables[0], variables[0], CONSTRAINT.NOT_EQUALS)
    assert constraint.satisfied() is False, "True because 1 == 1"


def test_invalid_constraint_type(variables):
    variables[0].set_value(1)
    variables[1].set_value(2)
    with pytest.raises(ValueError, match="Invalid constraint type: INVALID_TYPE"):
        Constraint(variables[0], variables[1], "INVALID_TYPE")


###
def test_constraint_equals_one_constraint_variable_is_null_equals(variables):
    variables[1].set_value(2)
    constraint = Constraint(variables[0], variables[1], CONSTRAINT.EQUALS)
    assert constraint.satisfied() is True, "True None and 2 satisfied constraint"

    constraint = Constraint(variables[0], variables[0], CONSTRAINT.EQUALS)
    assert constraint.satisfied() is True, "True because None == None"


def test_constraint_equals_one_constraint_variable_is_null_not_equals(variables):
    variables[1].set_value(2)
    constraint = Constraint(variables[0], variables[1], CONSTRAINT.NOT_EQUALS)
    assert constraint.satisfied() is True, "True None and 2 satisfied constraint"

    constraint = Constraint(variables[0], variables[1], CONSTRAINT.NOT_EQUALS)
    assert constraint.satisfied() is True, "True because None == None"
