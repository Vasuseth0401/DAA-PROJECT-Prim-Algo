
import sys
from pathlib import Path
import unittest
import tempfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.network_manager import NetworkManager


class TestNetworkManager(unittest.TestCase):

    def setUp(self):
        self.manager = NetworkManager()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "network.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_location(self):
        self.manager.add_location("Hospital")
        self.assertEqual(
            self.manager.graph.get_location_count(), 1
        )

    def test_add_connection(self):
        self.manager.add_connection("Hospital", "School", 15000)
        self.assertEqual(
            self.manager.graph.get_connection_count(), 1
        )

    def test_save_network(self):
        self.manager.add_connection("Hospital", "School", 15000)
        self.manager.save_network(str(self.test_file))

        self.assertTrue(self.test_file.exists())

    def test_load_network(self):
        self.manager.add_connection("Hospital", "School", 15000)
        self.manager.save_network(str(self.test_file))

        new_manager = NetworkManager()
        new_manager.load_network(str(self.test_file))

        self.assertEqual(
            new_manager.graph.get_location_count(), 2
        )
        self.assertEqual(
            new_manager.graph.get_connection_count(), 1
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
