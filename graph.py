
class Graph:

    def __init__(self):
        self.adjacency_list = {}
        print("[SUCCESS] Graph initialized!")

    # ADD LOCATION
    def add_location(self, location):

        if not isinstance(location, str):
            raise ValueError("Location name must be a string")

        location = location.strip()

        if not location:
            raise ValueError("Location cannot be empty")

        if location not in self.adjacency_list:
            self.adjacency_list[location] = []
            print(f"[SUCCESS] Location created: {location}")
        else:
            print(f"[INFO] Location already exists: {location}")

    # ADD CONNECTION
    def add_connection(self, location1, location2, cost):

        if not isinstance(location1, str) or not isinstance(location2, str):
            raise ValueError("Location names must be strings")

        location1 = location1.strip()
        location2 = location2.strip()

        if not location1 or not location2:
            raise ValueError("Location names cannot be empty")

        if isinstance(cost, bool) or not isinstance(cost, (int, float)) or cost <= 0:
            raise ValueError("Cost must be positive")

        if location1 == location2:
            raise ValueError("Self connection not allowed")

        self.add_location(location1)
        self.add_location(location2)

        if any(n == location2 for n, _ in self.adjacency_list[location1]):
            raise ValueError("Connection already exists")

        self.adjacency_list[location1].append((location2, cost))
        self.adjacency_list[location2].append((location1, cost))

        print(
            f"[SUCCESS] Connection created: "
            f"{location1} <-> {location2} | Rs. {cost:,.2f}"
        )

    # REMOVE CONNECTION
    def remove_connection(self, location1, location2):

        if location1 not in self.adjacency_list:
            raise ValueError("First location does not exist")

        if location2 not in self.adjacency_list:
            raise ValueError("Second location does not exist")

        if not any(n == location2 for n, _ in self.adjacency_list[location1]):
            raise ValueError("Connection does not exist")

        self.adjacency_list[location1] = [
            (n, c) for n, c in self.adjacency_list[location1]
            if n != location2
        ]

        self.adjacency_list[location2] = [
            (n, c) for n, c in self.adjacency_list[location2]
            if n != location1
        ]

        print(f"[SUCCESS] Connection removed: {location1} <-> {location2}")

    # REMOVE LOCATION
    def remove_location(self, location):

        if location not in self.adjacency_list:
            raise ValueError("Location does not exist")

        for neighbor, _ in self.adjacency_list[location]:
            self.adjacency_list[neighbor] = [
                (n, c) for n, c in self.adjacency_list[neighbor]
                if n != location
            ]

        del self.adjacency_list[location]

        print(f"[SUCCESS] Location removed: {location}")

    # LOCATION COUNT
    def get_location_count(self):
        return len(self.adjacency_list)

    # CONNECTION COUNT
    def get_connection_count(self):
        return sum(
            len(edges) for edges in self.adjacency_list.values()
        ) // 2

    # GET ALL CONNECTIONS
    def get_all_connections(self):

        connections = []

        for location, edges in self.adjacency_list.items():
            for neighbor, cost in edges:
                if location < neighbor:
                    connections.append((location, neighbor, cost))

        return connections

    # DISPLAY GRAPH
    def display_graph(self):

        print("\n========== NETWORK INFRASTRUCTURE ==========")

        if not self.adjacency_list:
            print("[INFO] No locations available.")
            return

        for location, connections in self.adjacency_list.items():

            print(f"\nLocation: {location}")

            if not connections:
                print("  No connections")

            for neighbor, cost in connections:
                print(f"  -> {neighbor} | Cost: Rs. {cost:,.2f}")

        print("\n============================================")
        print("[INFO] Total Locations:", self.get_location_count())
        print("[INFO] Total Connections:", self.get_connection_count())
        print("[SUCCESS] Graph displayed successfully!")
        print("============================================")

if __name__ == "__main__":
    print("\n========== GRAPH TEST ==========")

    graph = Graph()

    graph.add_connection("Hospital", "School", 15000)
    graph.add_connection("School", "University", 20000)

    graph.display_graph()

    print("\n[SUCCESS] Graph test completed!")