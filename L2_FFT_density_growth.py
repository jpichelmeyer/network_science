import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

def grow_graph(G=nx.Graph(), k=1, n_iter=100):

    # Initialize lists of nodes and edges of G
    G_nodes, G_edges = list(G.nodes), list(G.edges)

    # Initialize and populate dictionary for node renaming
    conversion_dict = {}
    for i in range(len(G_nodes)):
        conversion_dict[G_nodes[i]] = i

    # Initialize and populate graph with renamed nodes
    G_new = nx.Graph()
    G_new.add_nodes_from(range(len(G_nodes)))
    for e in G_edges:
        G_new.add_edges_from([(conversion_dict[e[0]], conversion_dict[e[1]])])

    # Extend number of nodes in new graph (if needed)
    if len(G_nodes) < k:
        G_new.add_nodes_from(range(len(G_nodes), len(G_nodes)+(k-len(G_nodes))))

    # Initialize density list
    densities = [nx.density(G_new)]

    # Iterate, adding one new node each iteration that connects to k existing nodes
    for _ in range(n_iter):
        node_id = len(list(G_new.nodes))
        nodes_to_connect_to = random.sample(range(len(list(G_new.nodes))), k)
        G_new.add_nodes_from([node_id])
        for node in nodes_to_connect_to:
            G_new.add_edges_from([(node_id, node)])
        densities.append(nx.density(G_new))

    return G_new, densities

def plot_densities(G=nx.Graph(), k_min=1, k_max=10, n_iter=400):
    for k in range(k_min, k_max+1):
        G, densities = grow_graph(G, k=k, n_iter=n_iter)
        densities = np.array(densities)
        density_max = np.max(densities)
        plt.plot(range(len(densities)), densities/density_max, label="k="+str(k))
    plt.title("Density graph for\nk=" + str(k_min) + " to k=" + str(k_max))
    plt.xlabel("Iteration")
    plt.ylabel("Normalized density\n(1.0 being the max density it every reaches)")
    plt.legend()
    plt.show()

plot_densities(G=nx.circular_ladder_graph(20))