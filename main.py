"""sudoku solver"""

import numpy as np
from binary import binary_solver


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
    retry = 100
    s = time.time()
    for i in range(retry):
        res = binary_solver(test_matrix)
    e = time.time()
    print(res)
    print(f'Time elapsed: {round((e - s) / retry, 4)} sec')
