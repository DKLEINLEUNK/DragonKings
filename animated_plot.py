import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
import numpy as np
from network import Network
from network_modifier import (
    create_shock,
    get_weak_nodes,
    threshold_test,
    propagate_shock,
    degrade,
    fail,
    save_state,
    load_state,
)

## Animation properties

ANIMATION = True 
EDGE_LABELS = False  
NODE_SIZE = 20  

## Network properties

THRESHOLDS = 0.3  #
LOSS_IF_INFECTED = 0.85
USE_REAL_DATA = False
POWER_LAW_OWNS = (
    0.55  
)
NETWORK_SIZE = 100

def update_node_status(iteration):
    """
    For each iterations, it propagates a shock and plots the results
    """

    global graph
    global nodes
    global color_mapping
    nodes.remove()

    propagate_shock(network,LOSS_IF_INFECTED , THRESHOLDS, recovery_rate = 0.6)

    node_statuses = nx.get_node_attributes(graph, "status")

    node_colors = [color_mapping[node_statuses[node]] for node in graph.nodes]

    nodes = nx.draw_networkx_nodes(
        graph, pos=pos, node_color=node_colors, node_size=NODE_SIZE
    )



if __name__ == "__main__":
    ## Network creation
    network = Network(n = NETWORK_SIZE, p = 0.1)
    graph = network.graph
    network.set_all_statuses(2)
    network.set_all_edges()
    create_shock(network, int(0.1*NETWORK_SIZE))

    ## Network plot
    pos = nx.spring_layout(graph)
    fig, ax = plt.subplots()

    ## Color setter
    color_mapping = {0: "red", 1: "yellow", 2: "green"}

    ## PLots
    ax.set_title(f"Erdos Renyi network with p = 0.1, Threshold = 20%, EPS = 85% and Recovery = 10% ")
    node_statuses = nx.get_node_attributes(graph, "status")
    node_colors = [color_mapping[node_statuses[node]] for node in graph.nodes]
    nodes = nx.draw_networkx_nodes(
        graph, pos=pos, node_color=node_colors, node_size=NODE_SIZE
    )

    edges = nx.draw_networkx_edges(
        graph, pos=pos, width=0.1, edge_color="black", arrowsize=3
    )

    if EDGE_LABELS == True:
        edge_labels = {
            (u, v): f'{d["ownership"]:.2f}' for u, v, d in graph.edges(data=True)
        }
        print(edge_labels)
        edge_label = nx.draw_networkx_edge_labels(
            graph, pos=pos, edge_labels=edge_labels, font_size=8
        )

    if ANIMATION == True:
        animation = FuncAnimation(
            fig, update_node_status, frames=8, interval=2000, blit=False
        )

    plt.show()
