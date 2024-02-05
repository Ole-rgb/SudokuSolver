from enum import Enum
import copy
from typing import Union, List, TypeVar, Generic
from sudoku.sudokuGrid import SudokuGrid
import numpy as np

T = TypeVar("T")


class Heuristics(Enum):
    LEAST_VALUES = 1
    LEAST_CONSTRAINT_VARIABLE = 2


class CONSTRAINT(Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"


class Variable(Generic[T]):
    def __init__(
        self,
        unique_name: str,
        value: Union[None, T] = None,
        domain: Union[None, List[T]] = None,
    ) -> None:
        self.__unique_name = unique_name  # location of the cell e.g. (1,1)

        self.__value = value  # None if candidates of cell > 1
        self.__domain = domain  # candidates in a sudoku

    def set_value(self, value: [T]):
        if value not in self.get_domain() and value != None:
            raise ValueError(
                "Given value: {} is not in domain: {}".format(value, self.get_domain())
            )
        self.__value = value

    def set_domain(self, domain):
        current_value = self.get_value()

        if current_value is None:
            self.__domain = domain
            return
        if current_value in domain:
            self.__domain = domain
            return

        raise ValueError(
            "New domain: {} doesn't contain value: {}".format(domain, current_value)
        )

    def get_variable_name(self) -> str:
        return self.__unique_name

    def value_is_assigned(self) -> bool:
        return self.__value != None

    def get_value(self):
        if not self.value_is_assigned():
            return None
        return self.__value

    def get_domain(self):
        return self.__domain

    def __str__(self) -> str:
        res = "name: {}, ".format(self.get_variable_name())

        res += "value: {}, ".format(self.get_value())

        res += "domain: "
        if self.get_domain() != None:
            for value in self.get_domain():
                res += "{} ,".format(value)

        return res

    def __eq__(self, other):
        if isinstance(other, Variable):
            return (
                self.get_variable_name() == other.get_variable_name()
                and self.get_value() == other.get_value()
                and self.get_domain() == other.get_domain()
            )
        return False


class Constraint:
    # only binary constraints aka v1 != v2
    def __init__(self, v1: Variable, v2: Variable, constraint: CONSTRAINT) -> None:
        self.__v1 = v1
        self.__v2 = v2

        if isinstance(constraint, str) and constraint not in {
            type.name for type in CONSTRAINT
        }:
            raise ValueError("Invalid constraint type: {}".format(constraint))
        elif constraint.name not in {type.name for type in CONSTRAINT}:
            raise ValueError("Invalid constraint type: {}".format(constraint))
        self.__constraint = constraint

    def satisfied(self) -> bool:
        # if one field is null, all binary constraints are fulfilled, because there is nothing to compare to
        if self.__v1.get_value() == None or self.__v2.get_value() == None:
            return True
        if self.__v1.get_value() == None and self.__v2.get_value() == None:
            return True
        if self.__constraint == CONSTRAINT.EQUALS:
            return self.__v1.get_value() == self.__v2.get_value()
        if self.__constraint == CONSTRAINT.NOT_EQUALS:
            return self.__v1.get_value() != self.__v2.get_value()


class CSP(Generic[T]):
    def __init__(
        self,
        variables: List[Variable[T]],
        constraints: Union[None, List[Constraint]] = None,
    ) -> None:
        self.__variables = variables
        self.__constraints = constraints

    def _valid_state(self) -> bool:
        if self.__constraints == None:
            return True
        for constraint in self.__constraints:
            if not constraint.satisfied():
                return False
        return True

    def _valid_solution(self) -> bool:
        raise NotImplementedError("TODO overwrite to formulate goalcheck")

    def _get_variables(self) -> List[Variable[T]]:
        return self.__variables

    def _get_constraints(self) -> Union[None, List[Constraint]]:
        return self.__constraints

    def get_variable_by_name(self, variable_name: str) -> Variable[T]:
        for variable in self._get_variables():
            if variable.get_variable_name() == variable_name:
                return variable
        raise ValueError("variable name: {} doesnt exist".format(variable_name))

    def __str__(self) -> str:
        res = "STATE:\n    Variables: \n"
        for variable in self.__variables:
            res += "        " + variable.__str__() + "\n"
        res += "    Constraints: \n"
        if self.__constraints != None:
            for constraint in self.__constraints:
                res += "        " + constraint.__str__() + "\n"

        return res


class State(CSP, Generic[T]):
    def __init__(
        self,
        variables: List[Variable[T]],
        constraints: Union[None, List[Constraint]] = None,
    ) -> None:
        super().__init__(variables, constraints)

    def _valid_solution(self) -> bool:
        return self._all_variables_assigned() and self.valid_state()

    def _all_variables_assigned(self) -> bool:
        for variable in self._get_variables():
            if variable.value_is_assigned():
                continue
            return False

        return True

    def valid_state(self) -> bool:
        return self._valid_state()

    def _next_state(self):
        raise NotImplementedError("TODO implement")

    def assign_variable(self, variable: Variable[T], value: [T]):
        new_state = copy.deepcopy(self)
        new_state.get_variable_by_name(variable.get_variable_name()).set_value(value)
        return new_state

    def get_domain_of_variable(self, variable_name):
        return self.get_variable_by_name(variable_name).get_domain()

    def __str__(self) -> str:
        return super().__str__()


class Backtracking(Generic[T]):
    def __init__(
        self, init_state: State[T], heuristics: Union[None, Heuristics] = None
    ) -> None:
        self.__heuristics = heuristics
        self.__problem = init_state

    def solve(self) -> Union[State, None]:
        return self.__backtracking(self.__problem)

    def __backtracking(
        self, root_state: State, seen: List[State] = []
    ) -> Union[State, None]:

        if root_state in seen:
            return None

        if root_state._valid_solution():
            return root_state

        variable_to_assign = self.__variable_to_assign(root_state)

        for candidate in variable_to_assign.get_domain():
            new_state = root_state.assign_variable(variable_to_assign, candidate)
            if new_state.valid_state():

                solution = self.__backtracking(new_state)

                if solution != None:
                    return solution

        return None

    def __variable_to_assign(self, state: State) -> Union[Variable, None]:
        if self.__heuristics == None:
            return self.__first_unassigned_variable(state._get_variables())
        raise NotImplementedError("Implement other heuristics")

    def __first_unassigned_variable(self, variables: List[Variable]) -> Variable:
        for variable in variables:
            if not variable.value_is_assigned():
                return variable


if __name__ == "__main__":
    v1 = Variable[int]("v1", None, [1, 2, 3])
    v2 = Variable[int]("v2", None, [1, 2, 3])
    v3 = Variable[int]("v3", None, [1, 2])
    variables = [v1, v2, v3]
    root_state = State[int](variables)  # TODO implement constraints that work properly
    backtracking = Backtracking(root_state)
    res = backtracking.solve()

    print(res)
