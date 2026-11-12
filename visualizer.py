
import networkx as nx
import matplotlib.pyplot as plt


class NetworkVisualizer:

    def __init__(self, graph):
        self.graph = graph

    def visualize(self, mst_edges, total_cost):

        adjacency_list = self.graph.adjacency_list

        if not adjacency_list:
            raise ValueError("Cannot visualize an empty network")

        # Create a NetworkX graph
        network = nx.Graph()

        # Add all locations as nodes
        for location in adjacency_list:
            network.add_node(location)

        # Add all available connections
        for location, connections in adjacency_list.items():

            for neighbor, cost in connections:

                # Avoid adding duplicate undirected edges
                if location < neighbor:
                    network.add_edge(
                        location,
                        neighbor,
                        weight=cost
                    )

        # Identify the edges selected by Prim's algorithm
        mst_edge_set = {
            frozenset((source, destination))
            for source, destination, cost in mst_edges
        }

        # Separate selected and unselected connections
        selected_edges = []
        unused_edges = []

        for source, destination in network.edges():

            edge = frozenset((source, destination))

            if edge in mst_edge_set:
                selected_edges.append((source, destination))
            else:
                unused_edges.append((source, destination))

        # Generate graph layout
        positions = nx.spring_layout(
            network,
            seed=42,
            k=1.5
        )

        plt.figure(figsize=(12, 8))

        # Draw locations
        nx.draw_networkx_nodes(
            network,
            positions,
            node_size=2200,
            node_color="skyblue",
            edgecolors="black"
        )

        # Draw all available connections
        nx.draw_networkx_edges(
            network,
            positions,
            edgelist=unused_edges,
            edge_color="gray",
            width=1.8,
            style="dashed"
        )

        # Highlight MST connections
        nx.draw_networkx_edges(
            network,
            positions,
            edgelist=selected_edges,
            edge_color="green",
            width=3.5
        )

        # Draw location names
        nx.draw_networkx_labels(
            network,
            positions,
            font_size=9,
            font_weight="bold"
        )

        # Display installation costs on connections
        edge_labels = nx.get_edge_attributes(
            network,
            "weight"
        )

        nx.draw_networkx_edge_labels(
            network,
            positions,
            edge_labels=edge_labels,
            font_size=8
        )

        plt.title(
            "NetOptima - Optimized Network Infrastructure\n"
            f"Minimum Installation Cost: Rs. {total_cost:,.2f}",
            fontsize=14,
            fontweight="bold"
        )

        # Add legend
        plt.plot([], [], color="green", linewidth=3,
                 label="Selected MST Connection")

        plt.plot([], [], color="gray", linestyle="dashed",
                 label="Unused Connection")

        plt.legend(loc="upper right")

        plt.axis("off")
        plt.tight_layout()
        plt.show()
