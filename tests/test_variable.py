import pytest
import re
import numpy as np
from sudoku.backtracking import Backtracking
from sudoku.sudokuGrid import SudokuGrid, ROWS, COLUMNS
from sudoku.backtracking import State, Variable, Constraint, CONSTRAINT


def test_initialization_assigned_value():
    variable = Variable[int]("v1", value=1, domain=[1, 2, 3])
    assert variable.get_variable_name() == "v1"
    assert variable.get_value() == 1
    assert variable.get_domain() == [1, 2, 3]


def test_initialization_no_assigned_value():
    variable = Variable[int]("v1", value=None, domain=[1, 2, 3])
    assert variable.get_variable_name() == "v1"
    assert variable.get_value() == None
    assert variable.get_domain() == [1, 2, 3]


def test_set_variable_from_domain():
    v1 = Variable[int]("v1", value=None, domain=[1, 2, 3])
    v1.set_value(2)
    assert v1.get_value() == 2, "should be 2"


def test_set_variable_not_in_domain():
    v1 = Variable[int]("v1", None, [1, 2, 3])
    with pytest.raises(
        ValueError, match=re.escape("Given value: 4 is not in domain: [1, 2, 3]")
    ):
        v1.set_value(4)
    assert v1.get_value() == None, "should be None"


def test_set_domain_without_assigned_variable():
    v1 = Variable[int]("v1", 1, [1, 2, 3])
    with pytest.raises(
        ValueError, match=re.escape("New domain: [2, 3] doesnt contain value: 1")
    ):
        v1.set_domain([2, 3])
    assert v1.get_value() == 1, "should still be 1"


def test_value_is_assigned():
    variable = Variable("v1", value=None, domain=[1, 2, 3])
    assert not variable.value_is_assigned()

    variable.set_value(1)
    assert variable.value_is_assigned()


def test_str_representation():
    variable = Variable("v1", value=1, domain=[1, 2, 3])
    expected_str = "name: v1, value: 1, domain: 1 ,2 ,3 ,"
    assert str(variable) == expected_str


def test_state_variables_equal():
    v1 = Variable[int]("v1", None, [1, 2, 3])
    v2 = Variable[int]("v1", None, [1, 2, 3])

    assert (
        v1 == v2
    ) == True, "should be True, because both variables have the same values domains and value assigned"


def test_state_variables_not_equal():
    v1 = Variable[int]("v1", None, [1, 3])
    v2 = Variable[int]("v1", None, [1, 2, 3])

    assert (v1 == v2) == False, "should be False, the variables have different domains"
