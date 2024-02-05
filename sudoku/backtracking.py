from enum import Enum
from typing import Union
from sudoku.sudokuGrid import SudokuGrid


class Heuristics(Enum):
    LEAST_VALUES = 1
    LEAST_CONSTRAINT_VARIABLE = 2


class Backtracking:
    def __init__(
        self, problem: SudokuGrid, heuristics: Union(None, Heuristics) = None
    ) -> None:
        self.heuristics = heuristics
        self.problem = problem

    def solve(self):
        raise NotImplementedError("Todo implement")

    def backtracking(self):
        raise NotImplementedError("Todo implement")

    def next(self):
        # TODO implement algorithm that generates the next state to explore. Take heuristics into account
        raise NotImplementedError("Todo implement")

    def valid(self, state: SudokuGrid) -> bool:
        # TODO checks if the given state is a valid state
        pass
