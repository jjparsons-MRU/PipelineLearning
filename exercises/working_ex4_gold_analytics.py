"""
Exercise 4: Gold Analytics (Working File)
-----------------------------------------
Goal: Generate advanced metrics on Silver tables (LYBUNT, SYBUNT, Recency).
"""
import sys
from pathlib import Path
import pandas as pd

class GoldAnalyticsEngine:
    def __init__(self, base_dir: Path = None, current_year: int = 2024):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        self.silver_dir = self.base_dir / "data" / "silver"
        self.gold_dir = self.base_dir / "data" / "gold"
        self.gold_dir.mkdir(parents=True, exist_ok=True)
        self.current_year = current_year

    def calculate_recency_months(self, latest_gift_date_str: str, ref_date: str = "2024-12-31") -> float:
        """TODO: Calculate months since last gift."""
        pass

    def calculate_donor_metrics(self, summary_df: pd.DataFrame, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """TODO: Calculate LYBUNT, SYBUNT flags, and other metrics."""
        pass

    def run_analytics(self):
        print("Starting Gold Layer Analytics...")
        # TODO: Load silver tables, calculate metrics, save to gold dir
        print("Gold Analytics Completed Successfully!\n")

if __name__ == "__main__":
    engine = GoldAnalyticsEngine()
    engine.run_analytics()
