import argparse
from sudoku.sudokuSolver import SudokuSolver
from typing import Union, Tuple, List
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

BOARDS = ["debug", "n00b", "l33t", "error"]  # Available sudoku boards
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

parser = argparse.ArgumentParser(description="Solve a sudoku.")
parser.add_argument("--sudoku", type=str, help="Sudoku to be parsed")


class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """

    def __init__(self, parent: Tk, sudoku: SudokuSolver = None):
        Frame.__init__(self, parent)
        self.sudoku = sudoku
        self.parent = parent

        # saves the already filled cells
        self.filled_cells: List[Tuple[int, int]] = []
        # saves the previous solution, even if the sudoku gets reset
        self.solution = None

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        solve_button = Button(self, text="Solve sudoku", command=self.__solve_sudoku)
        solve_button.pack(fill=BOTH, side=BOTTOM)
        reset_button = Button(self, text="Reset sudoku", command=self.__reset)
        reset_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for row in range(9):
            for column in range(9):
                original = self.sudoku.get_sudoku_grid().get_cell((row, column))
                if len(original) == 1 and original != 0:
                    x = MARGIN + column * SIDE + SIDE / 2
                    y = MARGIN + row * SIDE + SIDE / 2
                    color = "black"
                    self.canvas.create_text(
                        x, y, text=original, tags="numbers", fill=color
                    )
                    self.filled_cells.append((row, column))

    def __draw_new_filled_cells(self):
        for row in range(9):
            for column in range(9):
                if (row, column) in self.filled_cells:
                    continue
                answer = (
                    self.solution.get_cell((row, column))
                    if self.solution
                    else self.sudoku.get_sudoku_grid().get_cell((row, column))
                )
                if len(answer) == 1 and answer != 0:
                    x = MARGIN + column * SIDE + SIDE / 2
                    y = MARGIN + row * SIDE + SIDE / 2
                    color = "grey"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )
                    self.filled_cells.append((row, column))

    def __solve_sudoku(self):
        if self.solution == None:
            self.sudoku.solve_soduku()
            self.solution = self.sudoku.get_sudoku_grid()
        self.__draw_new_filled_cells()

    def __reset(self):
        self.sudoku = SudokuSolver(args.sudoku)
        self.filled_cells = []
        self.__draw_puzzle()


if __name__ == "__main__":
    args = parser.parse_args()
    root = Tk()
    SudokuUI(
        root,
        SudokuSolver(args.sudoku),
    )
    root.mainloop()
