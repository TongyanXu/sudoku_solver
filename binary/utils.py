# -*- coding: utf-8 -*-
"""doc string"""

import numpy as np

base_number = 0b111111111
_bin_num = np.power(2, np.arange(9))


def to_binary(number):
    """convert a 0-9 integer number to binary"""
    return _bin_num[number - 1]


def from_binary(number):
    """convert a 0-9 binary number to integer"""
    return np.argwhere(_bin_num == number)[0, 0] + 1


def from_binary_matrix(matrix):
    """convert a binary matrix to integer"""
    return np.log2(matrix).astype('int16') + 1


def remove_number(value, number):
    """remove a number from possible list"""
    return value & (number ^ base_number)


def count_number(value):
    """count possible numbers"""
    count = 0
    while value:
        value = value & (value - 1)
        count += 1
    return count


def get_available_number(value, index):
    """get an available number from possible list"""
    index_count = -1
    for num in _bin_num:
        if value & num:
            index_count += 1
        if index == index_count:
            return num
    return -1


if __name__ == '__main__':
    num1 = 0b101100100
    unit1 = 0b001000000
    print(count_number(num1))
    res1 = remove_number(num1, unit1)
    print(bin(res1))
    print(from_binary(unit1))
    print(from_binary(get_available_number(res1, 0)))
    print(from_binary(get_available_number(res1, 1)))
    print(from_binary(get_available_number(res1, 2)))
    print(get_available_number(res1, 3))
