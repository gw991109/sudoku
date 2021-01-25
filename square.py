from __future__ import annotations
from typing import List, Tuple


class Square:
    """
    A 3x3 square. Each board should have 9 of such squares

    ---Attributes---
    _square: three rows of 3 integers to represent a square
    _original: the original square
    """

    _square: List[List[int]]
    _original: List[List[int]]

    def __init__(self, square):
        """
        Initialize a square instance
        :param square: numbers in this square
        """
        # precondition: square is 3x3
        self._square = square
        self._original = []
        for item in self._square:
            self._original.append(item.copy())

    def validate(self) -> bool:
        """
        Check if this square breaks the rule of sudoku
        :return: true or false
        """
        lst = []
        for row in self._square:
            for col in row:
                if col != 0 and col in lst:
                    return False
                else:
                    lst.append(col)
        return True

    def fill(self, row, col, number) -> bool:
        """
        Fill a number into a position
        :param row: row of the cell
        :param col: column of the cell
        :param number: number to fill
        :return: true on success false otherwise
        """
        if self._square[row][col] != 0:
            return False
        for item in self._square:
            if number in item:
                return False
        self._square[row][col] = number
        return True

    def clear(self, row, col) -> None:
        """
        set the given cell to 0
        :param row: row of cell
        :param col: col of cell
        :return: None
        """
        self._square[row][col] = 0

    def reset(self) -> None:
        """
        reset this square to the original square after initially finding the
        solutions
        :return: None
        """
        self._square = []
        for item in self._original:
            self._square.append(item.copy())
