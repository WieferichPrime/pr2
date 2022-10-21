import networkx as nx
import matplotlib.pyplot as plt
from GraphData import MyApi
import json
import getpass


def main():
    login = input("Login:")
    print()
    password = getpass.getpass("Password:")
    api = MyApi()
    api.init_session(login, password)
    # api.get_friends()
    with open("data.json", "r") as read_file:
        data = json.load(read_file)
    G = nx.Graph()
    for edge in data:
        G.add_edge(edge[0], edge[1])

    group_list = []
    with open("group.json", "r") as group:
        group_list = list(json.load(group))
    by_lambda = dict(sorted(nx.eigenvector_centrality_numpy(G).items(), key=lambda x: x[1], reverse=True))
    by_between = dict(sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True))
    by_closeness = dict(sorted(nx.closeness_centrality(G).items(), key=lambda x: x[1], reverse=True))
    centered = {}

    for node in by_lambda.keys():
        if node in group_list:
            if node in centered.keys():
                centered[node] += "L"
            else:
                centered[node] = "L"
            break

    for node in by_between.keys():
        if node in centered.keys():
            centered[node] += "B"
        else:
            centered[node] = "B"
        break

    for node in by_closeness.keys():
        if node in centered.keys():
            centered[node] += "C"
        else:
            centered[node] = "C"
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