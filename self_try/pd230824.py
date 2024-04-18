#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   pd230824.py
@Time    :   2023/08/24 22:45:06
@Author  :   rainmonG
@Version :   1.0
@Desc    :   None
"""

import pandas as pd


class PandasTest:
    """
    to practice more about Pandas
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def test1():
        grid = [[1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        df = pd.DataFrame(grid)
        df1 = df.sum(axis=0)
        df2 = df.sum(axis=1)
        print(grid + grid)

    @staticmethod
    def test2():
        grid = [[1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        m = len(grid)
        n = len(grid[0])
        rsum = [sum(x) for x in grid]
        csum = [sum([grid[i][j] for i in range(m)]) for j in range(n)]
        for i in range(m):
            for j in range(n):
                if rsum[i] == 1 and csum[j] == 1 and grid[i][j] == 1:
                    grid[i][j] = 0
        print(sum(list(map(sum, grid))))

    @staticmethod
    def test3():
        grid = [[1, 1, 0, 0], [0, 3, 1, 0], [0, 4, 1, 0], [0, 0, 0, 1]]
        df = pd.DataFrame(grid, columns=['a', 'b', 'c', 'd'])
        print(df['b'].sort_values(ascending=False).iloc[1])

    @staticmethod
    def test4():
        grid = [[1, 1, 0, 0], [0, 3, 1, 0], [0, 4, 1, 0], [0, 0, 0, 1]]
        df = pd.DataFrame(grid, columns=['a', 'b', 'c', 'd'])
        # df = pd.concat([df, pd.DataFrame([[0]]*5)], axis=1)
        # print(df.loc[4:4, ['b']])
        print(df.head(5).tail(1))


if __name__ == '__main__':
    test = PandasTest()
    test.test4()
