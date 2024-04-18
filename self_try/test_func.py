"""
@Time : 2024/1/16 21:46
@Author : rainmon
@File : test_func.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import pandas as pd


def test_df_in_func1(df):
    """
    试直接进函数的df会不会被直接改变
    :param pd.DataFrame df:
    :return:
    """
    if not df.empty:
        df.loc[:, 't'] = 'story'
    return df


def test_df_in_func2(df):
    """
    试直接进函数的df会不会被直接改变
    :param pd.DataFrame df:
    :return:
    """
    if not df.empty:
        df.loc[:, 'h'] = 'inplace'
        df = df['h'].str.split('p', expand=True)
    return df


if __name__ == '__main__':
    df1 = pd.DataFrame({'s': ['pp'] * 10})
    df2 = pd.DataFrame({'s': ['pp'] * 10})
    test_df_in_func1(df1)
    test_df_in_func2(df2)
    print('DONE')
