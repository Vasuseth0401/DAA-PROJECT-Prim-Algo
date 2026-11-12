
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.graph import Graph


class NetworkManager:

    def __init__(self):
        self.graph = Graph()
        print("[SUCCESS] Network Manager initialized!")

    def add_location(self, location):
        self.graph.add_location(location)
        print(f"[SUCCESS] Location added: {location}")

    def add_connection(self, location1, location2, cost):
        self.graph.add_connection(location1, location2, cost)
        print(f"[SUCCESS] Connection added: {location1} <-> {location2}")

    def remove_location(self, location):
        self.graph.remove_location(location)
        print(f"[SUCCESS] Location removed: {location}")

    def remove_connection(self, location1, location2):
        self.graph.remove_connection(location1, location2)
        print(f"[SUCCESS] Connection removed: {location1} <-> {location2}")

    def display_network(self):
        self.graph.display_graph()

    def get_network_statistics(self):
        return {
            "locations": self.graph.get_location_count(),
            "connections": self.graph.get_connection_count()
        }

    def save_network(self, filename="data/network.json"):

        path = Path(filename)

        if not path.is_absolute():
            path = PROJECT_ROOT / path

        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "locations": list(self.graph.adjacency_list.keys()),
            "connections": [
                {
                    "from": source,
                    "to": destination,
                    "cost": cost
                }
                for source, destination, cost
                in self.graph.get_all_connections()
            ]
        }

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("[SUCCESS] Network saved successfully!")
        print(f"[INFO] File: {path}")

    def load_network(self, filename="data/network.json"):

        path = Path(filename)

        if not path.is_absolute():
            path = PROJECT_ROOT / path

        if not path.exists():
            print("[WARNING] No saved network found.")
            return

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        new_graph = Graph()

        for location in data["locations"]:
            new_graph.add_location(location)

        for connection in data["connections"]:
            new_graph.add_connection(
                connection["from"],
                connection["to"],
                connection["cost"]
            )

        self.graph = new_graph

        print("[SUCCESS] Network loaded successfully!")
        print(f"[INFO] Locations: {self.graph.get_location_count()}")
        print(f"[INFO] Connections: {self.graph.get_connection_count()}")


if __name__ == "__main__":

    print("\n========== NETOPTIMA NETWORK MANAGER ==========")

    manager = NetworkManager()

    manager.add_connection("Hospital", "School", 15000)
    manager.add_connection("School", "University", 20000)
    manager.add_connection("University", "Data Center", 25000)
    manager.add_connection("School", "Data Center", 10000)

    manager.display_network()

    manager.save_network()

    print("\n========== EXECUTION COMPLETED ==========")
