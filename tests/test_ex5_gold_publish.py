"""
Unit tests for Exercise 5: Gold Publishing
"""

import unittest
from pathlib import Path
from exercises.ex1_bronze_ingest import BronzeIngestor
from exercises.ex5_gold_publish import GoldPublisher


class TestGoldPublish(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        BronzeIngestor(base_dir=self.base_dir).run_ingestion(use_mock=True)
        self.publisher = GoldPublisher(base_dir=self.base_dir)

    def test_publish_data_products(self):
        target_path = self.publisher.publish_data_products()

        publish_dir = self.base_dir / "data" / "publish"
        self.assertTrue((publish_dir / "powerbi_donor_analytics.csv").exists())


if __name__ == "__main__":
    unittest.main()
