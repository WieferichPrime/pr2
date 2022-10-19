import networkx as nx
import matplotlib.pyplot as plt
from GraphData import MyApi
import json
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    login = input("Login:")
    password = input("Password:")
    api = MyApi(login=login, password=password)
    api.get_friends()
    with open("data.json", "r") as read_file:
        data = json.load(read_file)
    G = nx.Graph()
    for edge in data:
        G.add_edge(edge[0], edge[1])
    # G.add_edge(os.getenv("USER_ID"), 1)

    by_lambda = dict(sorted(nx.eigenvector_centrality_numpy(G).items(), key=lambda x: x[1])[-3:])
    by_betweenness = dict(sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1])[-3:])
    by_closeness = dict(sorted(nx.closeness_centrality(G).items(), key=lambda x: x[1])[-3:])
    color_map = []
    for node in G:
        if node in by_lambda.keys():
            color_map.append('red')
        elif node in by_betweenness.keys():
            color_map.append('orange')
        elif node in by_closeness.keys():
            color_map.append('pink')
        else:
            color_map.append('blue')
            # subax1 = plt.subplot(121)
    # nx.draw(G, node_size=8)
    labels = {}
    for node in G.nodes():
        if node == os.getenv("USER_ID"):
            # set the node name as the key and the label as its value
            labels[node] = "Я"
        if node in by_lambda.keys() or node in by_betweenness.keys() or node in by_closeness.keys():
            labels[node] = api.get_user_by_id(node)['first_name'] + " " + api.get_user_by_id(node)['last_name']


    nx.draw_networkx(G, pos=nx.spring_layout(G), node_color=color_map, labels=labels, font_color="r", font_size=12, node_size=12, width=0.5)
    # nx.draw_networkx_nodes(G, pos=nx.spring_layout(G), node_color=color_map)
    # nx.draw_networkx_labels(G, pos=nx.spring_layout(G), labels=labels, font_size=8, font_color='r')
    # subax2 = plt.subplot(122)
    # nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
    plt.savefig("graph.jpeg")
    plt.show()
if __name__ == "__main__":
    main()