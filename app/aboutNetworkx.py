"""
@Time : 2024/5/10 0:03
@Author : rainmon
@File : aboutNetworkx.py
@Project : StudyNotes-Python
@feature : 
@description：
"""
import pandas as pd
import networkx as nx


def test():
    datas = pd.read_excel('../self_try/treetest.xlsx', sheet_name=0, dtype=str)
    datas['srcport'] = pd.to_numeric(datas['srcport'], downcast="integer", errors="coerce")
    datas['dstport'] = pd.to_numeric(datas['dstport'], downcast="integer", errors="coerce")
    if len(datas) > 1:
        compensate1 = datas.iloc[:-1][['dstslot', 'dstport']].reset_index(drop=True)
        compensate2 = datas.iloc[1:][['srcslot', 'srcport']].reset_index(drop=True)
        compensate = pd.concat([compensate1, compensate2], axis=1)
        compensate = compensate.rename(columns={
            'dstslot': 'srcslot', 'dstport': 'srcport', 'srcslot': 'dstslot', 'srcport': 'dstport'
        })
        datas = pd.concat([datas, compensate])
    datas = datas.dropna(subset=['srcslot', 'dstslot', 'srcport', 'dstport'])
    graph = nx.DiGraph()
    nodes = {}
    links = []
    for _, row in datas.iterrows():
        srcid = '-'.join([row['srcslot'], str(row['srcport'])])
        dstid = '-'.join([row['dstslot'], str(row['dstport'])])
        nodes.update({
            srcid: {'slot': row['srcslot'], 'port': row['srcport']},
            dstid: {'slot': row['dstslot'], 'port': row['dstport']}
        })
        links.append((srcid, dstid))
    graph.add_nodes_from(nodes)
    graph.add_edges_from(links)
    # 广度优先
    print(list(nx.bfs_tree(graph, '2-2')))
    print(list(nx.bfs_tree(graph, '2-2', reverse=True)))
    # 深度优先
    # print(list(nx.dfs_preorder_nodes(graph, '2-2')))
    # print(list(nx.dfs_postorder_nodes(graph, '2-2')))