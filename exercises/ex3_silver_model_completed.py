"""
Exercise 3: Silver Modeling
----------------------------
Goal: Build Silver tables ready for analytics.
- silver_constituent_summary.csv: Master donor summary table.
- silver_gift_transactions.csv: Enriched gift transactions joined with Date & Revenue dimensions.
"""

import os
import sys
from pathlib import Path

file_root = Path(__file__).resolve().parent.parent
if str(file_root) not in sys.path:
    sys.path.insert(0, str(file_root))

import pandas as pd
from ex2_silver_cleanse_completed import SilverCleanser


class SilverModeler:
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        self.silver_dir = self.base_dir / "data" / "silver"
        self.silver_dir.mkdir(parents=True, exist_ok=True)
        self.cleanser = SilverCleanser(base_dir=self.base_dir)

    def build_constituent_summary(self, const_df: pd.DataFrame) -> pd.DataFrame:
        """Create constituent summary table."""
        df = const_df.copy()
        # Ensure key columns exist
        expected_cols = [
            'id', 'name', 'prospect_status', 'lifetime_giving',
            'first_gift_date', 'first_gift_amount',
            'latest_gift_date', 'latest_gift_amount',
            'largest_gift_date', 'largest_gift_amount'
        ]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None

        if 'id' in df.columns and 'constituent_id' not in df.columns:
            df.rename(columns={'id': 'constituent_id'}, inplace=True)

        return df

    def build_gift_transactions(self, gifts_df: pd.DataFrame, dates_df: pd.DataFrame, rev_df: pd.DataFrame) -> pd.DataFrame:
        """Create enriched gift transaction table joined with dimension lookup tables."""
        tx_df = gifts_df.copy()

        # Join Date dimension
        if 'gift_date' in tx_df.columns and 'date' in dates_df.columns:
            tx_df = pd.merge(
                tx_df,
                dates_df[['date', 'fiscal_year', 'quarter', 'month_name']],
                left_on='gift_date',
                right_on='date',
                how='left'
            ).drop(columns=['date'])

        # Join Revenue dimension
        if 'revenue_type_id' in tx_df.columns and 'revenue_type_id' in rev_df.columns:
            tx_df = pd.merge(
                tx_df,
                rev_df[['revenue_type_id', 'name', 'category']],
                on='revenue_type_id',
                how='left'
            ).rename(columns={'name': 'revenue_type_name', 'category': 'revenue_category'})

        return tx_df

    def run_modeling(self):
        """Execute modeling and write CSVs to data/silver/."""
        print("Starting Silver Layer Modeling...")

        const_raw, gifts_raw, dates_raw, rev_raw = self.cleanser.run_cleansing()

        # 1. Build constituent summary
        const_summary = self.build_constituent_summary(const_raw)
        summary_path = self.silver_dir / "silver_constituent_summary.csv"
        const_summary.to_csv(summary_path, index=False)
        print(f"Saved Silver Constituent Summary: .{os.sep}{summary_path.relative_to(self.base_dir)}")

        # 2. Build gift transactions
        gift_transactions = self.build_gift_transactions(gifts_raw, dates_raw, rev_raw)
        transactions_path = self.silver_dir / "silver_gift_transactions.csv"
        gift_transactions.to_csv(transactions_path, index=False)
        print(f"Saved Silver Gift Transactions: .{os.sep}{transactions_path.relative_to(self.base_dir)}")

        print("Silver Modeling Completed Successfully!\n")
        return const_summary, gift_transactions


if __name__ == "__main__":
    modeler = SilverModeler()
    modeler.run_modeling()
