import numpy as np
from typing import Union, Tuple, List, Set
from sudoku.sudokuGrid import SudokuGrid, ROWS, COLUMNS, DIGITS
from sudoku.backtracking import Variable, Constraint, CONSTRAINT, State, Backtracking
import time

DEBUG = True

# same for rows
all_rows = [[(row, column) for column in range(COLUMNS)] for row in range(ROWS)]

# return columns' lists of cells
all_columns = [[(row, column) for row in range(ROWS)] for column in range(COLUMNS)]

# same for blocks
# this list comprehension is unreadable, but quite cool!
all_blocks = [
    [
        ((row // 3) * 3 + column // 3, (row % 3) * 3 + column % 3)
        for column in range(COLUMNS)
    ]
    for row in range(ROWS)
]

# combine three
all_houses = all_columns + all_rows + all_blocks


def print_debug(msg):
    if DEBUG:
        print("***** {} *****".format(msg))


class SudokuSolver:
    """
    SudokuSolver class represents a Sudoku puzzle solver.

    Attributes:
    - __grid (SudokuGrid): An instance of SudokuGrid representing the Sudoku puzzle.

    Methods:
    - __init__(self, grid_str: Union[None, str] = None) -> None:
        Constructor for the SudokuSolver class. Initializes the Sudoku grid.

    - simple_elimination(self) -> None:
        Applies simple elimination technique to fill in candidates for empty cells.

    - remove_element(self, arr: np.ndarray, value_to_remove: int) -> np.ndarray:
        Removes a specified value from the given NumPy array.

    - get_sudoku_grid(self) -> SudokuGrid:
        Returns the SudokuGrid instance representing the Sudoku puzzle.

    - __str__(self) -> str:
        Returns a string representation of the Sudoku puzzle.

    Example Usage:
    >>> sudoku_solver = SudokuSolver("530070000600195000098000060800060003400803001700020006060000280000419005000080079")
    >>> sudoku_solver.simple_elimination()
    >>> print(sudoku_solver)
    5 3 0 | 0 7 0 | 0 0 0
    6 0 0 | 1 9 5 | 0 0 0
    0 9 8 | 0 0 0 | 0 6 0
    ---------------------
    8 0 0 | 0 6 0 | 0 0 3
    4 0 0 | 8 0 3 | 0 0 1
    7 0 0 | 0 2 0 | 0 0 6
    ---------------------
    0 6 0 | 0 0 0 | 2 8 0
    0 0 0 | 4 1 9 | 0 0 5
    0 0 0 | 0 8 0 | 0 7 9
    """

    def __init__(self, grid_str: Union[None, str] = None) -> None:
        """
        Constructor for the SudokuSolver class.

        Parameters:
        - grid_str (Union[None, str]): A string containing digits representing the initial Sudoku grid.
          If None, an empty Sudoku grid is created. The string has to be of length 9x9=81

        Returns:
        - None
        """
        self.__grid = SudokuGrid(grid_str)

    def fill_in_candidates(self) -> None:
        """
        Fills in candidate values for empty cells in the Sudoku grid.

        Returns:
        - None
        """
        grid = self.get_sudoku_grid()
        rows, columns = grid.get_shape()
        for row in range(rows):
            for column in range(columns):
                cell = grid.get_cell((row, column))
                if len(cell) == 1 and cell == [0]:
                    candidates = list(range(1, DIGITS))
                    grid.set_cell((row, column), candidates)

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
                and value_to_remove
                in self.get_sudoku_grid().get_cell(other_cell_position)
            ):
                updated_candidates, removed = self.__remove_element(
                    self.get_sudoku_grid().get_cell(other_cell_position),
                    value_to_remove,
                )
                report += removed
                self.get_sudoku_grid().set_cell(other_cell_position, updated_candidates)
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

    def get_sudoku_grid(self) -> SudokuGrid:
        """
        Returns the SudokuGrid instance representing the Sudoku puzzle.

        Returns:
        - SudokuGrid: The SudokuGrid instance.
        """
        return self.__grid

    def set_sudoku_grid(self, grid: SudokuGrid):
        self.__grid = grid

    def logical_deduction(self, grid: SudokuGrid):
        # if simple elimination cant do further deduction set hidden singles try.
        # if hidden single found a deduction set simple elimination look and so on
        while True:
            removed = self.simple_elimination(grid)
            print_debug("simple elimination removed: {} candidates".format(removed))
            if removed == 0:
                removed += self.hidden_single(grid)
                print_debug("hidden single removed: {} candidates".format(removed))
            if removed == 0:
                break

    def solve_soduku(self, options=None) -> float:
        start_time = time.time()

        print_debug("Started Sudoku Solver")
        print_debug("Sudoku given: ")
        print_debug(self)

        self.fill_in_candidates()

        self.logical_deduction(self.get_sudoku_grid())

        print_debug("")
        print_debug("After logical deduction:")
        print_debug(self)

        state = SudokuCSPAdapter.soduku_to_init_state(self.get_sudoku_grid())
        backtracking = Backtracking(state)
        print_debug("")
        print_debug("Started backtracking, searching for solution:")
        solve = backtracking.solve()

        if solve == None:
            print_debug("NO SOLUTION")
            return

        print_debug("SOLUTION FOUND:")
        self.set_sudoku_grid(SudokuCSPAdapter.state_to_grid(solve))
        print_debug("Sudoku string: {}".format(solve))

        print_debug(self)

        end_time = time.time()
        return end_time - start_time

    def __str__(self) -> str:
        """
        Returns a string representation of the Sudoku puzzle.

        Returns:
        - str: The string representation of the Sudoku puzzle.
        """
        return self.get_sudoku_grid().__str__()


class SudokuCSPAdapter:
    @staticmethod
    def state_to_grid(state: State) -> SudokuGrid:
        return SudokuGrid(state.__str__())

    @staticmethod
    def soduku_to_init_state(sudoku_grid: SudokuGrid) -> State[int]:
        ## need a method generate next state
        variables: List[Variable[int]] = SudokuCSPAdapter.__cells_to_variables(
            sudoku_grid
        )
        constraints: List[Constraint] = SudokuCSPAdapter.__generate_sudoku_constraints(
            variables
        )

        return State(variables, constraints)

    @staticmethod
    def __generate_sudoku_constraints(
        variables: List[Variable[int]],
    ) -> List[Constraint]:
        constraints: List[Constraint] = []
        # Generate constraints for each row
        variable_positions = [variable.get_variable_name() for variable in variables]

        for row in range(9):
            for col1 in range(8):
                for col2 in range(col1 + 1, 9):
                    v1 = variables[
                        variable_positions.index("({}, {})".format(row, col1))
                    ]
                    v2 = variables[
                        variable_positions.index("({}, {})".format(row, col2))
                    ]
                    constraints.append(Constraint(v1, v2, CONSTRAINT.NOT_EQUALS))

        # Generate constraints for each column
        for col in range(9):
            for row1 in range(8):
                for row2 in range(row1 + 1, 9):
                    v1 = variables[
                        variable_positions.index("({}, {})".format(row1, col))
                    ]
                    v2 = variables[
                        variable_positions.index("({}, {})".format(row2, col))
                    ]
                    constraints.append(Constraint(v1, v2, CONSTRAINT.NOT_EQUALS))

        # Generate constraints for each 3x3 subgrid
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                for i in range(8):
                    for j in range(i + 1, 9):
                        v1 = variables[
                            variable_positions.index(
                                "({}, {})".format(start_row + i // 3, start_col + i % 3)
                            )
                        ]
                        v2 = variables[
                            variable_positions.index(
                                "({}, {})".format(start_row + j // 3, start_col + j % 3)
                            )
                        ]
                        constraints.append(Constraint(v1, v2, CONSTRAINT.NOT_EQUALS))

        return constraints

    @staticmethod
    def __cells_to_variables(sudoku_grid: SudokuGrid) -> List[Variable[int]]:
        # TODO implement np.ndarray in backtracking
        variables: List[Variable[int]] = []
        for row in all_rows:
            for cell_position in row:
                cell = sudoku_grid.get_cell(cell_position)
                candidates: List[int] = []
                value = None

                for candidate in cell:
                    candidates.append(int(candidate))
                if len(cell) == 1:
                    value = cell[0]
                    candidates = [value]
                variables.append(
                    Variable[int]("{}".format(cell_position), value, candidates)
                )
        return variables


if __name__ == "__main__":
    weird_sudoku = "100000000000000000000000000000000000010000000000000000000000000000000000000000000"
    hard_sudoku = "805000002000901000300000000060700400200050000000000060000380000010000900040000070"
    other_hard_sudoku = "805000002000901000300000000060700400200050000000000060000380000040000700010000090"
    easy_sudoku = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    s = SudokuSolver(hard_sudoku)
    s.fill_in_candidates()
    # s.logical_deduction()

    # s2 = SudokuCSP(s.get_sudoku_grid())
    # start_time = time.time()
    # print(s.get_sudoku_grid())
    # print(s2.backtracking(s.get_sudoku_grid()))
    # end_time = time.time()
    # print(end_time - start_time)
