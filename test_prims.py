
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.graph import Graph
from core.prims import PrimsAlgorithm


class TestPrimsAlgorithm(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

        self.graph.add_connection("Hospital", "University", 20000)
        self.graph.add_connection("Hospital", "School", 15000)
        self.graph.add_connection("University", "Data Center", 25000)
        self.graph.add_connection("School", "Data Center", 10000)

    def test_mst_cost(self):
        algorithm = PrimsAlgorithm(self.graph)
        edges, cost = algorithm.find_mst("Hospital")

        self.assertEqual(cost, 45000)
        self.assertEqual(len(edges), 3)

    def test_disconnected_graph(self):
        self.graph.add_location("Airport")

        algorithm = PrimsAlgorithm(self.graph)

        with self.assertRaises(ValueError):
            algorithm.find_mst("Hospital")

    def test_mst_edge_count(self):
        algorithm = PrimsAlgorithm(self.graph)
        edges, cost = algorithm.find_mst("Hospital")

        self.assertEqual(len(edges), self.graph.get_location_count() - 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
