from __future__ import annotations
from square import *
from numpy import transpose


class Board:
    """
    A class to represent the board we will be playing a sudoku game on.

    ---Attributes---
    _original_board: the original board passed in as an argument
    _solution: the solution to this board
    _board: the board we will operate on
    _notes: the notes board used to jot down notes
    _squares: the 9 squares of the board
    _transpose: transpose of the board so we can check columns easily
    """

    _original_board: List[List[int]]
    _solution: List[List[int]]
    _board: List[List[int]]
    _notes: List[List[int]]
    _squares = List[Square]
    _transpose = List[List[int]]

    def __init__(self, board: List[List[int]]):
        """
        the board we are playing with
        :param board: numbers for the board
        """
        self._original_board = board
        self._solution = []
        self._board = []
        self._notes = []
        self._squares = []
        self._transpose = transpose(board)

        sqr = self._dissect(board)
        for i in range(3):
            row = [Square(sqr[i * 3]),
                   Square(sqr[i * 3 + 1]),
                   Square(sqr[i * 3 + 2])]
            self._squares.append(row)

        for item in board:
            self._board.append(item.copy())
            self._notes.append(item.copy())

        self.set_solution()

    def get_board(self) -> List[List[int]]:
        """
        return the board
        :return: game board
        """
        return self._board

    def get_notes(self) -> List[List[int]]:
        """
        return the notes
        :return: notes
        """
        return self._notes

    def fill(self, row: int, col: int, number: int) -> bool:
        """
        fill a position on the game board with a number if the move is legal,
        used for finding a solution with backtracking
        :param row: row of the cell
        :param col: column of the cell
        :param number: number to fill with
        :return: true on success false otherwise
        """
        if self._board[row][col] != 0:
            return False
        if 0 <= row < 9 and 0 <= col < 9:
            if number and 0 < number < 10:
                for item in self._board[row]:
                    if item == number:
                        return False
                for item in self._board:
                    if item[col] == number:
                        return False
                sqr_row = row // 3
                sqr_col = col // 3
                x = row % 3
                y = col % 3
                if self._squares[sqr_row][sqr_col].fill(x, y, number):
                    self._board[row][col] = number
                    return True
        return False

    def fill_solution(self, row: int, col: int, number: int = None) -> bool:
        """
        This is fill but used for the player, it checks of the move is correct
        directly against the solution board which we found using backtracking
        when initializing.
        :param row: row of cell
        :param col: col of cell
        :param number: number to fill
        :return: True if the move is correct, false otherwise
        """
        if self._board[row][col] != 0:
            print("That's filled")
            return False
        if 0 <= row < 9 and 0 <= col < 9:
            if number and 0 < number < 10:
                if self._solution[row][col] == number:
                    self._board[row][col] = number
                    self._notes[row][col] = 0
                    print("That's correct")
                    return True
                print("That's incorrect")
            elif number is None:
                if self._notes[row][col] == 0:
                    print("No number entered")
                    return False
                if self._solution[row][col] == self._notes[row][col]:
                    self._board[row][col] = self._notes[row][col]
                    self._notes[row][col] = 0
                    print("That's correct")
                    return True
                print("That's incorrect")
        return False

    def get(self, row: int, col: int) -> int:
        """
        return the number in the playing board at the given cell
        :param row: row of cell
        :param col: col of cell
        :return: number at that cell
        """
        if 0 <= row < 9 and 0 <= col < 9:
            return self._board[row][col]

    def clear(self, row: int, col: int) -> None:
        """
        set the number at the given cell in the game board to be 0
        :param row: row of cell
        :param col: col of cell
        :return: None
        """
        if 0 <= row < 9 and 0 <= col < 9:
            self._board[row][col] = 0
            sqr_row = row // 3
            sqr_col = col // 3
            x = row % 3
            y = col % 3
            self._squares[sqr_row][sqr_col].clear(x, y)

    def clear_notes(self, row: int, col: int) -> None:
        """
        set the number at the given cell in the notes board to be 0
        :param row: row of cell
        :param col: col of cell
        :return: None
        """
        if 0 <= row < 9 and 0 <= col < 9:
            self._notes[row][col] = 0

    def fill_notes(self, row: int, col: int, number: int) -> bool:
        """
        fill the given cell with the given number in the notes board
        :param row: row of cell
        :param col: col of cell
        :param number: number to fill
        :return: true on success false otherwise
        """
        if 0 <= row < 9 and 0 <= col < 9 and 0 < number < 10:
            if self._board[row][col] == 0:
                self._notes[row][col] = number
                return True
        return False

    def find_empty(self) -> Tuple[int, int]:
        """
        Find the next empty position on the game board, used for solving
        :return: position of that cell
        """
        # only used for solve
        row_index = 0
        for row in self._board:
            col_index = 0
            for col in row:
                if col == 0:
                    return row_index, col_index
                col_index += 1
            row_index += 1
        return -1, -1

    def check_win(self) -> bool:
        """
        Check if we're in a winning state, i.e. all cells filled legally
        :return: True if won, false otherwise
        """
        empty = self.find_empty()
        if empty[0] != -1:
            return False
        for item in self._squares:
            for sqr in item:
                if not sqr.validate():
                    return False
        for row in self._board:
            if not self.validate_list(row):
                return False
        for col in self._transpose:
            if not self.validate_list(col):
                return False
        return True

    def set_solution(self) -> bool:
        """
        Given that a board is solved, move this board to be stored in
        self.solution for checking later. And then reset the playing board.
        This is necessary because the initial solve operates on the playing
        board, so the solved board needs to be moved elsewhere in order
        to allow this this board for further operations.
        :return: true on success false otherwise
        """
        if self.solve():
            for row in self._board:
                self._solution.append(row.copy())
            self.reset()
            return True
        return False

    def solve(self) -> bool:
        """
        Recursively solve the board by backtracking. This is only used for
        setting the solution upon initialization
        :return: true of solved, false otherwise
        """
        # backtrack from the empty slot and try every number
        candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # we have an empty slot
        pos = self.find_empty()
        if pos[0] == -1:
            if self.check_win():
                return True
            else:
                return False
        else:
            for item in candidates:
                if self.fill(pos[0], pos[1], item):
                    if self.solve():
                        return True
                    self.clear(pos[0], pos[1])
            return False

    def reset(self) -> None:
        """
        reset the playing board to be the original board, this is used for
        setting solution when initializing.
        :return: None
        """
        self._board = self._original_board.copy()
        for row in self._squares:
            for item in row:
                item.reset()
        return

    @staticmethod
    def _dissect(board: List[List[int]]) -> List[List[List[int]]]:
        """
        Dissect a board given in list of list of int format into the 9 large
        squares, and return them in list of list of int format.
        :param board: playing board
        :return: 9 squares
        """
        index = [(0, 3), (3, 6), (6, 9)]
        squares = []
        for rows in index:
            row = board[rows[0]:rows[1]]
            for cols in index:
                sqr = []
                for item in row:
                    sqr.append(item[cols[0]:cols[1]])
                squares.append(sqr)
        return squares

    @staticmethod
    def print_board(board: List[List[int]]) -> None:
        """
        Print the given board with some formatting.
        :param board: board to be printed
        :return: None
        """
        for i in range(9):
            if i % 3 == 0:
                print("---------------------------")
            for j in range(9):
                if j % 3 == 0:
                    print(" | ", end="")
                if j == 8:
                    print(board[i][j], end="\n")
                else:
                    print(str(board[i][j]) + " ", end="")

    @staticmethod
    def validate_list(lst: List[int]) -> bool:
        """
        Check if the list(row or column) is filled out legally.
        :param lst: a row or a column
        :return: true if legal false otherwise
        """
        num = []
        for item in lst:
            if item != 0 and item in num:
                return False
            else:
                num.append(item)
        return True
