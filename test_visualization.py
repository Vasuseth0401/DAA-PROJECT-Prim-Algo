
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.graph import Graph
from core.prims import PrimsAlgorithm


class TestVisualizationData(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

        self.graph.add_connection("Hospital", "University", 20000)
        self.graph.add_connection("Hospital", "School", 15000)
        self.graph.add_connection("University", "Data Center", 25000)
        self.graph.add_connection("School", "Data Center", 10000)

    def test_graph_has_locations(self):
        self.assertEqual(self.graph.get_location_count(), 4)

    def test_graph_has_connections(self):
        self.assertEqual(self.graph.get_connection_count(), 4)

    def test_visualization_mst_edges(self):
        algorithm = PrimsAlgorithm(self.graph)
        mst_edges, mst_cost = algorithm.find_mst("Hospital")

        self.assertEqual(len(mst_edges), 3)
        self.assertEqual(mst_cost, 45000)

    def test_visualization_edge_data(self):
        connections = self.graph.get_all_connections()

        self.assertEqual(len(connections), 4)

        for source, destination, cost in connections:
            self.assertIsInstance(source, str)
            self.assertIsInstance(destination, str)
            self.assertGreater(cost, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
