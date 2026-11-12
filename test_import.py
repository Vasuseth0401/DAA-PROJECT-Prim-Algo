
import sys
from pathlib import Path

print("\n========== NETOPTIMA IMPORT TEST ==========")

# Automatically locate project root
search_paths = [
    Path(__file__).resolve().parent,
    Path.cwd()
]

PROJECT_ROOT = None

for start_path in search_paths:
    for folder in (start_path, *start_path.parents):
        if (
            (folder / "core" / "graph.py").is_file()
            and (folder / "analysis" / "cost_analysis.py").is_file()
        ):
            PROJECT_ROOT = folder
            break

    if PROJECT_ROOT:
        break

if PROJECT_ROOT is None:
    raise FileNotFoundError(
        "NetOptima project root not found. "
        "Check core/graph.py and analysis/cost_analysis.py"
    )

sys.path.insert(0, str(PROJECT_ROOT))

print("[SUCCESS] Project root:", PROJECT_ROOT)

# Import modules
from core.graph import Graph
from core.network_manager import NetworkManager
from core.prims import PrimsAlgorithm
from analysis.cost_analysis import CostAnalysis

print("[SUCCESS] Graph imported!")
print("[SUCCESS] Network Manager imported!")
print("[SUCCESS] Prim's Algorithm imported!")
print("[SUCCESS] Cost Analysis imported!")

# Create demo graph
graph = Graph()

graph.add_connection("Hospital", "University", 20000)
graph.add_connection("Hospital", "School", 15000)
graph.add_connection("University", "Data Center", 25000)
graph.add_connection("School", "Data Center", 10000)

# Run Prim's Algorithm
mst_edges, mst_cost = PrimsAlgorithm(graph).find_mst("Hospital")

print("\n[SUCCESS] Prim's Algorithm executed!")

# Run Cost Analysis
analysis = CostAnalysis(graph, mst_edges, mst_cost)

analysis.display_report()

print("\n[SUCCESS] ALL MODULE TESTS COMPLETED!")
