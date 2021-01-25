from __future__ import annotations
from board import *
"""
This is the standalone solving algorithm.
"""


def solve(board: Board) -> bool:
    board.reset()
    if helper_solve(board):
        board.print_board(board.get_board())
        return True
    return False


def helper_solve(board: Board) -> bool:
    # backtrack from the empty slot and try every number
    candidates = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # we have an empty slot
    pos = board.find_empty()
    if pos[0] == -1:
        if board.check_win():
            return True
        else:
            return False
    else:
        for item in candidates:
            if board.fill(pos[0], pos[1], item):
                if helper_solve(board):
                    return True
                board.clear(pos[0], pos[1])
        return False


def main():
    board = [[6,0,2,3,8,0,0,0,4],
             [4,0,5,0,7,0,0,9,0],
             [0,0,3,0,5,0,0,0,0],
             [5,0,0,8,9,0,0,2,0],
             [2,4,9,0,0,0,5,8,7],
             [0,3,0,0,2,4,0,0,1],
             [0,0,0,0,4,0,6,0,0],
             [0,9,0,0,1,0,7,0,8],
             [8,0,0,0,3,6,2,0,9]]
    bo = Board(board)
    bo.print_board(bo.get_board())
    solve(bo)


if __name__ == '__main__':
    main()
