"""
@Time : 2024-06-25 22:55
@Author : rainmon
@File : handlers.py
@Project : StudyNotes-Python
@feature : 
@description：design notes
"""
import pandas as pd

df1 = pd.DataFrame({
    'board_code': ['a', 'a', 'a', 'd', 'e'],
    'num_new': [1, 1, 1, 0, 1],
    'old_board_code': ['a', 'b', 'c', 'd', pd.NA],
    'num_old': [1, 1, pd.NA, 1, pd.NA],
    'exist_date': ['2024-02-01', '2024-02-01', pd.NA, '2024-01-01', pd.NA]
})

df1['exist_date'] = pd.to_datetime(df1['exist_date'])
df1['old_board_code'] = df1['old_board_code'].fillna('')
print(df1)

df1['old_board_code'] = df1.apply(lambda r: '' if r['old_board_code'] == r['board_code'] else r['old_board_code'],
                                  axis=1)
df1 = df1.sort_values(by=['exist_date', 'old_board_code'], ascending=False, na_position='last')
print(df1)
