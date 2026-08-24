"""
Unit tests for Exercise 2: Silver Cleansing
"""

import unittest
from pathlib import Path
from exercises.ex1_bronze_ingest import BronzeIngestor
from exercises.ex2_silver_cleanse import SilverCleanser, to_snake_case, format_date


class TestSilverCleanse(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        # Ensure bronze data exists
        BronzeIngestor(base_dir=self.base_dir).run_ingestion(use_mock=True)
        self.cleanser = SilverCleanser(base_dir=self.base_dir)

    def test_snake_case_conversion(self):
        self.assertEqual(to_snake_case("Fiscal_Year"), "fiscal_year")
        self.assertEqual(to_snake_case("Revenue Type ID"), "revenue_type_id")
        self.assertEqual(to_snake_case("first_gift_date"), "first_gift_date")

    def test_format_date(self):
        self.assertEqual(format_date("2024-11-20"), "11/20/2024")
        self.assertIsNone(format_date(None))
        self.assertIsNone(format_date("InvalidDate"))

    def test_run_cleansing(self):
        const_df, gifts_df, dates_df, rev_df = self.cleanser.run_cleansing()

        self.assertTrue("id" in const_df.columns or "constituent_id" in const_df.columns)
        self.assertIn("lifetime_giving", const_df.columns)
        self.assertIn("gift_date", gifts_df.columns)
        self.assertIn("fiscal_year", dates_df.columns)
        self.assertIn("revenue_type_id", rev_df.columns)


if __name__ == "__main__":
    unittest.main()
