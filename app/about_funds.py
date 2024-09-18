"""
@Time : 2024-09-18 23:37
@Author : rainmon
@File : about_funds.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import asyncio
import time
from ast import literal_eval
import httpx
import requests
import pandas as pd


def get_fund_names() -> pd.DataFrame:
    # 基金名称
    name_url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    with httpx.Client(timeout=None) as client:
        res = client.get(name_url)
    df_fund = pd.DataFrame(literal_eval(res.content.decode('utf-8-sig').lstrip('var r =').rstrip(';')),
                           columns=['fundcode', 'short_name', 'name', 'type', 'long_name'])
    return df_fund


def get_all_corps() -> pd.DataFrame:
    # 基金公司名
    name_url = 'http://fund.eastmoney.com/js/jjjz_gs.js'
    res = requests.get(name_url)
    df_corp = pd.DataFrame(literal_eval(res.content.decode('utf-8-sig').lstrip('var gs={op:').rstrip('}')),
                           columns=['code', 'name'])
    return df_corp


async def get_one_fund(code) -> pd.DataFrame:
    # 基金当前信息
    name_url = f'http://fundgz.1234567.com.cn/js/{code}.js'
    async with httpx.AsyncClient(timeout=None) as client:
        res = await client.get(name_url)
        if res.status_code != 200:
            return pd.DataFrame()
    name_mapping = {
        'jzrq': 'start_date',  # 基金开始日期
        'dwjz': 'net_worth',  # 净值
        'gsz': 'estimate_worth',  # 估算净值
        'gszzl': 'estimate_inc',  # 估算涨幅，负值为跌
        'gztime': 'latest_time',  # 最近统计时间
    }
    info = res.text.strip().lstrip('jsonpgz(').rstrip(');').strip()
    if not info:
        return pd.DataFrame()
    try:
        info = literal_eval(info)
    except Exception:
        print(name_url, 'bug')
        return pd.DataFrame()
    df_info = pd.Series(info).to_frame().T.rename(name_mapping)
    print(code, info)
    return df_info


async def get_funds_info(num: int):
    start = time.time()
    df_funds = get_fund_names()
    df_info = pd.DataFrame()
    for _, df_fund in df_funds.groupby(df_funds.index // num):
        task_list = [asyncio.create_task(get_one_fund(code)) for code in df_fund['fundcode']]
        info = await asyncio.gather(*task_list)
        df_info = pd.concat([df_info, *info])
    df_funds = pd.merge(df_funds, df_info, on=['fundcode', 'name'], how='left')
    end = time.time()
    print(f'一共耗时：{end - start}')
    return df_funds

if __name__ == '__main__':
    df = asyncio.run(get_funds_info(8))
    print('done')