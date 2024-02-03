"""
@Time : 2024/2/2 22:23
@Author : rainmon
@File : try_sqlalchemy.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

# print(text(r"SELECT * FROM users WHERE name='\:username'"))
engine = create_engine("mysql+mysqldb://root:studytest@localhost/mysqlcrashcourse")
with engine.connect() as connection:
    with connection.begin():
        result = connection.execute(text("select * from customers"))
        df = pd.DataFrame(result, columns=result.keys())
        print(df)
with engine.begin() as connection:
    result = connection.execute(text("select * from orders"))
    df = pd.DataFrame(result, columns=result.keys())
    print(df)
# 都可以，但要注意pandas和sqlalchemy的版本对应
with engine.connect() as conn, conn.begin():
    df = pd.read_sql_table('orders', conn)
    print(df)
df = pd.read_sql_table('productnotes', "mysql+mysqldb://root:studytest@localhost/mysqlcrashcourse")
print(df)
with engine.begin() as conn:
    df = pd.read_sql_table('products', conn)
    print(df)
    df_test = df.copy()
    df_test.loc[:, 'prod_id'] = df_test['prod_id'].astype(str) + ':3'
    df_test.loc[:, 'prod_desc'] = df_test['prod_desc'].mask(df_test['prod_desc'].astype(str).str.len() > 28)
    df_test.to_sql('products', conn, index=False, if_exists='append')
    sql1 = "select prod_id from products where left(prod_id, 1) = 'A'"
    df1 = pd.read_sql_query(sql1, conn)
    print(df1)