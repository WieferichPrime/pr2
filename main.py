import networkx as nx
import matplotlib.pyplot as plt
from GraphData import MyApi
import json
import getpass
import numpy as np


def main():
    login = input("Login:")
    print()
    password = getpass.getpass("Password:")
    api = MyApi()
    api.init_session(login, password)
    api.get_friends()
    with open("data.json", "r") as read_file:
        data = json.load(read_file)
    G = nx.Graph()
    for edge in data:
        G.add_edge(edge[0], edge[1])

    remove = []

    for node in G:
        if len(list(G.neighbors(node))) == 1:
            remove.append(node)

    for node in remove:
        G.remove_node(node)

    group_list = []
    with open("group.json", "r") as group:
        group_list = list(json.load(group))

    by_lambda = nx.eigenvector_centrality_numpy(G)
    by_lambda_key = list(by_lambda)
    by_lambda_val = list(by_lambda.values())
    by_lambda_top = np.argpartition(by_lambda_val, 2)[:3]

    by_between = nx.betweenness_centrality(G)
    by_between_key = list(by_between)
    by_between_val = list(by_between.values())
    by_between_top = np.argpartition(by_between_val, 2)[:3]

    by_closeness = nx.closeness_centrality(G)
    by_closeness_key = list(by_closeness)
    by_closeness_val = list(by_closeness.values())
    by_closeness_top = np.argpartition(by_closeness_val, 2)[:3]

    centered = {}

    for i in by_lambda_top:
        if by_lambda_key[i] in group_list:
            if by_lambda_key[i] in centered.keys():
                centered[by_lambda_key[i]] += "L"
            else:
                centered[by_lambda_key[i]] = "L"
            break

    for i in by_between_top:
        if by_between_key[i] in centered.keys():
            centered[by_between_key[i]] += "B"
        else:
            centered[by_between_key[i]] = "B"
        break

    for i in by_closeness_top:
        if by_closeness_key[i] in centered.keys():
            centered[by_closeness_key[i]] += "C"
        else:
            centered[by_closeness_key[i]] = "C"
        break

    color_map = []
    for node in G:
        if node in centered.keys():
            color_map.append('red')
        else:
            color_map.append('blue')
    labels = {}

    for node in G.nodes():
        if node == api.get_self_id():
            labels[node] = "Я"
        if node in centered.keys():
            labels[node] = api.get_user_by_id(node)['first_name'] + " " + api.get_user_by_id(node)['last_name'] + " " + centered[node]

    print(labels)
    nx.draw_networkx(G, pos=nx.spring_layout(G), node_color=color_map, labels=labels, font_color="r", font_size=10, node_size=12, width=0.5)
    plt.savefig("graph.jpeg")
    plt.show()


if __name__ == "__main__":
    main()