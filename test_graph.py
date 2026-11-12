
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.graph import Graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

    def test_add_location(self):
        self.graph.add_location("Hospital")
        self.assertIn("Hospital", self.graph.adjacency_list)

    def test_add_connection(self):
        self.graph.add_connection("Hospital", "School", 15000)
        self.assertEqual(self.graph.get_connection_count(), 1)

    def test_remove_connection(self):
        self.graph.add_connection("Hospital", "School", 15000)
        self.graph.remove_connection("Hospital", "School")
        self.assertEqual(self.graph.get_connection_count(), 0)

    def test_remove_location(self):
        self.graph.add_connection("Hospital", "School", 15000)
        self.graph.remove_location("Hospital")
        self.assertNotIn("Hospital", self.graph.adjacency_list)


if __name__ == "__main__":
    unittest.main(verbosity=2)
