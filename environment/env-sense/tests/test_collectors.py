import unittest
from src.data.collectors import DataCollector

class TestDataCollector(unittest.TestCase):

    def setUp(self):
        self.collector = DataCollector()

    def test_collect_data(self):
        data = self.collector.collect_data()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)

    def test_collect_data_structure(self):
        data = self.collector.collect_data()
        self.assertIn('time', data)
        self.assertIn('environment', data)
        self.assertIn('preferences', data)

    def test_collect_data_empty(self):
        self.collector.clear_data()
        data = self.collector.collect_data()
        self.assertEqual(data, {})

if __name__ == '__main__':
    unittest.main()