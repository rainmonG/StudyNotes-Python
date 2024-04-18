"""
@Time : 2024/1/20 18:35
@Author : rainmon
@File : test_pandas2.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def test(chap):
    """
    notes
    :param int chap: methods category
    :return:
    """
    df1 = pd.DataFrame({
        "A": 1.,
        "B": pd.Timestamp(r'2024/01/20'),  # 虽然有警告，但其实格式是支持的，而且支持多种，可以连着也可以连字符也可以斜杠
        "C": pd.Series(1, index=list(range(4)), dtype="float32"),
        "D": np.array([3] * 4, dtype="int32"),
        "E": pd.Categorical(['test', 'train'] * 2),
        "F": 'foo'
    })
    s = pd.Series([14.34, 21.34, 5.08], name='gdp')
    if chap == 1:
        print(df1)
    elif chap == 2:
        print(s)
    elif chap == 3:
        print(pd.json_normalize(df1.A))


def data_a(n):
    """

    :param int n:
    :return:
    """
    df = pd.DataFrame({'a': np.arange(10), 'b': [chr(i + 50) for i in range(10)]})
    if n == 1:
        df1 = df.append(pd.DataFrame([[np.nan, pd.NA]]))
        print(df1['a'].nunique(dropna=False))
        print(df1['a'].nunique())
        df2 = df1.round({'a': 2})
        print(df2)
        print(df1.round(0))
    elif n == 2:
        df1 = df[:]
        df1.loc[:, 'c'] = [chr(i % 4 + 50) for i in range(10)]
        ax = df1.groupby(by=['c'])['a'].sum().to_frame().plot(kind='barh', colormap='rainbow')
        ax.bar_label(ax.containers[0])
        plt.show()


if __name__ == '__main__':
    data_a(2)
