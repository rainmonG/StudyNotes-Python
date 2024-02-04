"""
@Time : 2024/2/2 22:23
@Author : rainmon
@File : try_sqlalchemy.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

def at_home():
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


def in_office():
    engine = create_engine("mysql+mysqldb://root:xl11xh-hyrzh@localhost/gym")
    with engine.connect() as connection:
        with connection.begin():
            field = [r":'/\相干"]
            result = connection.execute(text("select * from test1 where field in :field"), {'field': field})
            df = pd.DataFrame(result, columns=result.keys())
            print(df)
    with engine.begin() as connection:
        result = connection.execute(text("select * from test101"))
        df = pd.DataFrame(result, columns=result.keys())
        print(df)
    # 都可以，但要注意pandas和sqlalchemy的版本对应
    with engine.connect() as conn, conn.begin():
        df = pd.read_sql_table('test102', conn)
        print(df)
    df = pd.read_sql_table('race_task', "mysql+mysqldb://root:xl11xh-hyrzh@localhost/gym")
    print(df)
    with engine.begin() as conn:
        df = pd.read_sql_table('race_task_bugs', conn)
        print(df)
        df_test = df.copy()
        df_test.drop(columns=['id'], inplace=True)
        df_test.loc[:, 'req_id'] = df_test['req_id']+8
        df_test.loc[:, 'find_phase'] = df_test['find_phase'] + ':tt'
        df_test.loc[:, 'create_time'] = datetime.now()
        df_test.to_sql('race_task_bugs', conn, index=False, if_exists='append')
        sql1 = "select * from race_task_bugs"
        df1 = pd.read_sql_query(sql1, conn)
        print(df1)


def conv():
    # from pymysql.converters import escape_item, escape_string, escape_str, escape_sequence
    # print(escape_item(None, 'utf8'))
    # print(escape_item('667', 'utf8'))
    # print(escape_string('667'))
    # print(escape_str(None))
    def temp(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(str(e))
        return wrapper

    @temp
    def temp2():
        try:
            print(4 / 0)
        except ZeroDivisionError as e:
            raise ValueError('错误') from e
    temp2()
    print('DONE')