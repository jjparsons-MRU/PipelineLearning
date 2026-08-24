"""
Unit tests for Exercise 3: Silver Modeling
"""

import unittest
from pathlib import Path
from exercises.ex1_bronze_ingest import BronzeIngestor
from exercises.ex3_silver_model import SilverModeler


class TestSilverModel(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        BronzeIngestor(base_dir=self.base_dir).run_ingestion(use_mock=True)
        self.modeler = SilverModeler(base_dir=self.base_dir)

    def test_run_modeling(self):
        const_summary, gift_transactions = self.modeler.run_modeling()

        silver_dir = self.base_dir / "data" / "silver"
        self.assertTrue((silver_dir / "silver_constituent_summary.csv").exists())
        self.assertTrue((silver_dir / "silver_gift_transactions.csv").exists())

        self.assertIn("constituent_id", const_summary.columns)
        self.assertIn("fiscal_year", gift_transactions.columns)
        self.assertIn("revenue_type_name", gift_transactions.columns)


if __name__ == "__main__":
    unittest.main()
