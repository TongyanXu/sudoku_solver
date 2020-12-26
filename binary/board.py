# -*- coding: utf-8 -*-
"""doc string"""

import numpy as np
from binary import utils

_vec_bin_remove = np.vectorize(utils.remove_number)
_vec_bin_count = np.vectorize(utils.count_number)
_vec_bin_parse = np.vectorize(utils.from_binary)


def _sub_slice(row, col):
    """get slicing of sub matrix"""
    i, j = row // 3, col // 3
    return slice(3 * i, 3 * i + 3), slice(3 * j, 3 * j + 3)


class Board:
    """Sudoku Board"""

    def __init__(self, data_set: tuple = None):
        """
        initialize sudoku board with data set (optional)
        if data set is not given, create an empty board

        parameters
        ----------
        data_set: key data for sudoku board
            including cell matrix and confirming matrix
        """
        if data_set:
            self.cells, self.confirmed = data_set
        else:
            self.cells = np.ones((9, 9), dtype='int16') * utils.base_number
            self.confirmed = np.zeros((9, 9), dtype='bool')

    def setup(self, init_matrix: np.array):
        """
        set initial status of sudoku board

        parameters
        ----------
        init_matrix: initial status of sudoku board
            should be a numpy 2D array with shape (9, 9)
            its elements should be integer within [1, 9]
        """
        assert init_matrix.shape == (9, 9)
        for row, col in np.argwhere(init_matrix > 0):
            val = init_matrix[row, col]
            self[row, col] = utils.to_binary(val)

    def confirm(self, row: int, col: int):
        """
        confirm value of given row and column

        parameters
        ----------
        row: row index of value to be confirmed
        col: column index of value to be confirmed
        """
        self[row, col] = self[row, col]

    def copy(self):
        """
        copy current instance to a new one

        returns
        -------
        another Board instance with same data
        but new one is independent to current one
        """
        data_set = self.cells.copy(), self.confirmed.copy()
        return Board(data_set)

    @property
    def status(self):
        """
        status of current sudoku board

        returns
        -------
        integer indicating status
        1: sudoku is solved
        0: sudoku is not solved
        -1: sudoku has no solution
        """
        if (self.cells == 0).any():
            return -1  # if any cell equals to 0, sudoku has no solution
        if (_vec_bin_count(self.cells) == 1).all():
            return 1  # if all cells have only one number, sudoku is solved
        return 0  # for other situations, sudoku is not solved yet

    @property
    def decimal(self):
        """
        decimal based sudoku matrix

        returns
        -------
        numpy array (int16)
        """
        return utils.from_binary_matrix(self.cells)

    @property
    def solved(self):
        """
        cells are solved or not

        returns
        -------
        numpy array (bool)
        same dimension as sudoku matrix
        for solved cells, return True
        for unsolved cells, return False
        """
        return _vec_bin_count(self.cells) == 1

    def __setitem__(self, key, number):
        """set binary number to cell"""
        row, col = key
        for r_slice, c_slice in [
            (row, slice(None)),  # remove occurrence within same row
            (slice(None), col),  # remove occurrence within same column
            _sub_slice(row, col),  # remove occurrence within same sub matrix
        ]:
            self.cells[r_slice, c_slice] = \
                _vec_bin_remove(self.cells[r_slice, c_slice], number)
        self.cells[row, col] = number  # set the cell value
        self.confirmed[row, col] = 1  # mark the cell as confirmed

    def __getitem__(self, item):
        """get binary number of cell"""
        return self.cells[item]

    def __repr__(self):
        """description string"""
        return repr(self.cells)
