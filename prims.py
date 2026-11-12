
import heapq


class PrimsAlgorithm:

    def __init__(self, graph):
        self.graph = graph

    def find_mst(self, start):

        adjacency_list = self.graph.adjacency_list

        if not adjacency_list:
            return [], 0

        if start not in adjacency_list:
            raise ValueError("Starting location does not exist")

        visited = set()
        min_heap = []

        mst_edges = []
        total_cost = 0

        visited.add(start)

        for neighbor, cost in adjacency_list[start]:
            heapq.heappush(
                min_heap,
                (cost, start, neighbor)
            )

        while min_heap and len(visited) < len(adjacency_list):

            cost, source, destination = heapq.heappop(min_heap)

            if destination in visited:
                continue

            visited.add(destination)

            mst_edges.append(
                (source, destination, cost)
            )

            total_cost += cost

            for neighbor, edge_cost in adjacency_list[destination]:

                if neighbor not in visited:
                    heapq.heappush(
                        min_heap,
                        (edge_cost, destination, neighbor)
                    )

        if len(visited) != len(adjacency_list):
            raise ValueError(
                "Network is disconnected! MST cannot connect all locations."
            )

        return mst_edges, total_cost
