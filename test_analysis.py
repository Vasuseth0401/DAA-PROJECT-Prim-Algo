
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.graph import Graph
from core.prims import PrimsAlgorithm
from analysis.cost_analysis import CostAnalysis


class TestCostAnalysis(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

        self.graph.add_connection("Hospital", "University", 20000)
        self.graph.add_connection("Hospital", "School", 15000)
        self.graph.add_connection("University", "Data Center", 25000)
        self.graph.add_connection("School", "Data Center", 10000)

        self.edges, self.cost = PrimsAlgorithm(
            self.graph
        ).find_mst("Hospital")

        self.analysis = CostAnalysis(
            self.graph,
            self.edges,
            self.cost
        )

    def test_total_network_cost(self):
        self.assertEqual(
            self.analysis.calculate_total_network_cost(),
            70000
        )

    def test_minimum_network_cost(self):
        self.assertEqual(self.cost, 45000)

    def test_cost_reduction(self):
        self.assertEqual(
            self.analysis.calculate_cost_reduction(),
            25000
        )

    def test_savings_percentage(self):
        self.assertEqual(
            self.analysis.calculate_savings_percentage(),
            (25000 / 70000) * 100
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
