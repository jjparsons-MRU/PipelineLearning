"""
Unit tests for Exercise 1: Bronze Ingestion
"""

import json
import unittest
from pathlib import Path
import pandas as pd
from exercises.ex1_bronze_ingest import BronzeIngestor


class TestBronzeIngest(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.ingestor = BronzeIngestor(base_dir=self.base_dir)

    def test_run_ingestion(self):
        self.ingestor.run_ingestion(use_mock=True)

        bronze_dir = self.base_dir / "data" / "bronze"
        self.assertTrue((bronze_dir / "bronze_constituents.json").exists())
        self.assertTrue((bronze_dir / "bronze_gifts.json").exists())
        self.assertTrue((bronze_dir / "bronze_dates.csv").exists())
        self.assertTrue((bronze_dir / "bronze_revenue.csv").exists())

        # Validate constituents contents
        with open(bronze_dir / "bronze_constituents.json", "r") as f:
            constituents = json.load(f)
        self.assertGreater(len(constituents), 0)
        self.assertIn("id", constituents[0])

        # Validate dates dataframe
        dates_df = pd.read_csv(bronze_dir / "bronze_dates.csv")
        self.assertIn("Date", dates_df.columns)
        self.assertIn("Fiscal_Year", dates_df.columns)


if __name__ == "__main__":
    unittest.main()
