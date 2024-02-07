import numpy as np
from typing import Union, Tuple, List, Set
from sudoku.sudokuGrid import (
    SudokuGrid,
    ROWS,
    COLUMNS,
    DIGITS,
    all_blocks,
    all_columns,
    all_houses,
    all_rows,
)
from sudoku.backtracking import Heuristics

DEBUG = False


def print_debug(msg):
    if DEBUG:
        print("***** {} *****".format(msg))


import copy
import time


class SudokuCSP:
    def __init__(
        self, grid: SudokuGrid, heuristic: Union[Heuristics, None] = None
    ) -> None:
        self.grid = grid
        self.heuristic = heuristic

    def logical_deduction(self, grid: SudokuGrid):
        # if simple elimination cant do further deduction set hidden singles try.
        # if hidden single found a deduction set simple elimination look and so on
        while True:
            removed = self.simple_elimination(grid)
            # print_debug("simple elimination removed: {} candidates".format(removed))
            if removed == 0:
                removed += self.hidden_single(grid)
                # print_debug("hidden single removed: {} candidates".format(removed))
            if removed == 0:
                break

    def simple_elimination(self, grid: SudokuGrid) -> int:
        """
        Applies the simple elimination technique to remove candidates for unassigned cells.
        If there is one number in a cell - remove it from the candidates of the other cells in the house

        Returns:
        - int: number of removed candidates
        """
        report = 0
        for house in all_houses:
            for cell_position in house:
                cell = grid.get_cell(cell_position)
                if len(cell) == 1 and cell[0] != 0:
                    value_to_remove = cell[0]
                    report += self.__remove_candidate_from_house(
                        house, cell_position, value_to_remove
                    )
        return report

    def __remove_candidate_from_house(
        self,
        house: list(Tuple[int, int]),
        cell_position: Tuple[int, int],
        value_to_remove: int,
    ) -> int:
        """
        Removes the specified value from the candidates of other cells in the given house.

        Parameters:
        - house (list): The list of cell positions representing a house (row, column, or block).
        - cell_position (tuple): The position of the cell containing the value to be removed.
        - value_to_remove (int): The value to be removed from other cells in the house.

        Returns:
        - int: number of removed candidates
        """
        report = 0
        for other_cell_position in house:
            if (
                other_cell_position != cell_position
                and value_to_remove in self.grid.get_cell(other_cell_position)
            ):
                updated_candidates, removed = self.__remove_element(
                    self.grid.get_cell(other_cell_position),
                    value_to_remove,
                )
                report += removed
                self.grid.set_cell(other_cell_position, updated_candidates)
        return report

    def __remove_element(
        self, arr: np.ndarray, value_to_remove: Union[1, 2, 3, 4, 5, 6, 7, 8, 9]
    ) -> Tuple[np.ndarray, int]:
        """
        Removes a specified value from the given NumPy array.

        Parameters:
        - arr (np.ndarray): The NumPy array from which to remove the value.
        - value_to_remove (int): The value to be removed.

        Returns:
        - np.ndarray: The modified NumPy array.
        """
        removed = 1 if value_to_remove in arr else 0

        filtered_array = list(
            filter(lambda candidate: candidate != value_to_remove, arr)
        )
        return (filtered_array, removed)

    def hidden_single(self, grid) -> int:
        # if there is only one instance of a candidate in house - keep only it

        removed = 0
        for house in all_houses:
            for candidate in range(1, DIGITS):
                removed += self.find_only_canidate_in_house(grid, candidate, house)
        return removed

    def find_only_canidate_in_house(
        self, grid: SudokuGrid, candidate: int, house: Tuple[int, int]
    ):

        removed = 0
        count = 0
        cell_to_clean = (None, None)
        for cell_position in house:
            for cell_candidate in grid.get_cell(cell_position):
                if cell_candidate == candidate:
                    # found candidate amongst the cell_candidates
                    count += 1
                    cell_to_clean = cell_position
        if (
            count == 1
            and cell_to_clean != (None, None)
            and len(grid.get_cell(cell_to_clean)) > 1
        ):
            # only one instance of the candidate found
            removed = len(grid.get_cell(cell_to_clean)) - 1
            grid.set_cell(cell_to_clean, [candidate])
        return removed

    def __valid_state(self, grid: SudokuGrid) -> bool:
        return grid.valid_board()

    def valid_solution(self, grid: SudokuGrid) -> bool:
        return self.__all_variables_assigned(grid) and self.__valid_state(grid)

    def __all_variables_assigned(self, grid: SudokuGrid):
        for cell in grid:
            if len(cell) > 1:
                return False
        return True

    def solve(self):
        print("Starting Backtracking")
        return self.backtracking(self.grid)

    def backtracking(self, root_state: SudokuGrid, memo={}) -> Union[None, SudokuGrid]:
        if self.valid_solution(root_state):
            return root_state

        # choose variable to explore
        cell_to_explore = self.__choose_cell_to_explore(root_state)
        # assign values to variable
        for candidate in root_state.get_cell(cell_to_explore):
            new_state = copy.deepcopy(root_state)
            new_state.set_cell(cell_to_explore, [candidate])
            # test if assignment is valid before creating copy
            if not new_state.valid_board():
                continue

            self.logical_deduction(new_state)
            # did logical_deduction create invalid state?
            if not new_state.valid_board():
                continue

            solution = self.backtracking(new_state)

            if solution != None:
                return solution
        return None

    def __choose_cell_to_explore(self, grid: SudokuGrid):
        if self.heuristic == Heuristics.LEAST_VALUES:
            return self.__find_variable_with_least_values(grid)

        return self.__first_unassigned_cell(grid)

    def __find_variable_with_least_values(self, grid: SudokuGrid):
        min_candidates_cell: Tuple[Tuple[int, int], int] = ((None, None), 10)
        for row in all_rows:
            for cell in row:
                sum_candidates = len(grid.get_cell(cell))
                if sum_candidates == 1 or sum_candidates > min_candidates_cell[1]:
                    continue

                min_candidates_cell = (cell, sum_candidates)
        if min_candidates_cell[0] == (None, None):
            raise ValueError("Grid is already solved")
        return min_candidates_cell[0]

    def __first_unassigned_cell(self, grid: SudokuGrid) -> Tuple[int, int]:
        for row in all_rows:
            for cell in row:
                if len(grid.get_cell(cell)) == 1:
                    continue
                return cell

    def fill_in_candidates(self) -> None:
        """
        Fills in candidate values for empty cells in the Sudoku grid.

        Returns:
        - None
        """
        grid = self.grid
        rows, columns = grid.get_shape()
        for row in range(rows):
            for column in range(columns):
                cell = grid.get_cell((row, column))
                if len(cell) == 1 and cell == [0]:
                    candidates = list(range(1, DIGITS))
                    grid.set_cell((row, column), candidates)


if __name__ == "__main__":
    weird_sudoku = "100000000000000000000000000000000000010000000000000000000000000000000000000000000"
    hard_sudoku = "805000002000901000300000000060700400200050000000000060000380000010000900040000070"
    other_hard_sudoku = "805000002000901000300000000060700400200050000000000060000380000040000700010000090"
    easy_sudoku = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    medium = "100070009008096300050000020010000000940060072000000040030000080004720100200050003"

    s2 = SudokuCSP(SudokuGrid(hard_sudoku), Heuristics.LEAST_VALUES)
    s2.fill_in_candidates()
    s2.logical_deduction(s2.grid)
    print(s2.grid)
    print("{} variabels to assign.".format(s2.grid.sum_of_unassigned_variables()))

    start_time = time.time()
    print(s2.solve())
    end_time = time.time()
    print("Calculation took: {}seconds".format(end_time - start_time))
