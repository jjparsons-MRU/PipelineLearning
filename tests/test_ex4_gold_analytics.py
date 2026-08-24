"""
Unit tests for Exercise 4: Gold Analytics
"""

import unittest
from pathlib import Path
from exercises.ex1_bronze_ingest import BronzeIngestor
from exercises.ex4_gold_analytics import GoldAnalyticsEngine


class TestGoldAnalytics(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        BronzeIngestor(base_dir=self.base_dir).run_ingestion(use_mock=True)
        self.engine = GoldAnalyticsEngine(base_dir=self.base_dir, current_year=2024)

    def test_recency_calculation(self):
        months = self.engine.calculate_recency_months("2024-06-30", ref_date="2024-12-31")
        self.assertIsNotNone(months)
        self.assertGreater(months, 0)

    def test_run_analytics(self):
        gold_df = self.engine.run_analytics()

        gold_dir = self.base_dir / "data" / "gold"
        self.assertTrue((gold_dir / "gold_donor_analytics.csv").exists())

        self.assertIn("lybunt", gold_df.columns)
        self.assertIn("sybunt", gold_df.columns)
        self.assertIn("recency_months", gold_df.columns)
        self.assertIn("total_transactions", gold_df.columns)


if __name__ == "__main__":
    unittest.main()
