# -*- coding: utf-8 -*-
"""doc string"""

import numpy as np
from binary import utils
from binary.board import Board

_index_helper = np.arange(9)


def _dummy_fill(board: Board):
    """copy board and fill a dummy value into one cell"""
    # loop all unsolved cells
    for row, col in np.argwhere(~board.solved):
        for i in _index_helper:
            # find next value to be tried
            next_num = utils.get_available_number(board[row, col], i)
            if next_num == -1:
                break  # skip to next cell if no valid value left
            dummy_board = board.copy()  # avoid side effects
            dummy_board[row, col] = next_num  # fill dummy value
            yield dummy_board  # act like generator


def _simple_fill(board: Board):
    """fill all solved but not confirmed cells"""
    # find all solved but not confirmed cells
    to_fill = np.logical_and(board.solved, ~board.confirmed)
    while to_fill.any():  # confirm them if found
        for row, col in np.argwhere(to_fill):
            # this can delete other cells' possible values
            board.confirm(row, col)
        # keep looping until all solved cells are confirmed
        to_fill = np.logical_and(board.solved, ~board.confirmed)


def _solve(board: Board):
    """recursion function to solve sudoku board"""
    _simple_fill(board)  # confirm solved cells
    if board.status == 1:
        return board  # return current board if solved
    elif board.status == 0:
        # complex sudoku problem which needs guessing
        # fill dummy cell one by one to find solution
        for dummy_board in _dummy_fill(board):
            result = _solve(dummy_board)
            if result is not None:
                return result
    return None  # if no solution found, return None


def solve(sudoku_matrix: np.array):
    """
    solve sudoku matrix

    parameters
    ----------
    sudoku_matrix: sudoku matrix to be solved
        should be a numpy 2D array with shape (9, 9)
        its elements should be integer within [1, 9]

    returns
    -------
    numpy array (int16)
    solved sudoku matrix with same dimension of input
    """
    board = Board()  # initialize empty sudoku board
    board.setup(sudoku_matrix)  # setup initial values
    result = _solve(board)  # solve sudoku board
    if result is None:
        return None  # return None when no solution found
    return result.decimal  # return result in decimal


if __name__ == '__main__':
    import time
    test_matrix = np.array(
        [[8, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 3, 6, 0, 0, 0, 0, 0],
         [0, 7, 0, 0, 9, 0, 2, 0, 0],
         [0, 5, 0, 0, 0, 7, 0, 0, 0],
         [0, 0, 0, 8, 4, 5, 7, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 3, 0],
         [0, 0, 1, 0, 0, 0, 0, 6, 8],
         [0, 0, 8, 5, 0, 0, 0, 1, 0],
         [0, 9, 0, 0, 0, 0, 4, 0, 0]]
    )
    res = None
    s = time.time()
    for _ in range(100):
        res = solve(test_matrix)
    e = time.time()
    print(res)
    print(f'Time elapsed: {round(e - s, 4)} sec')
