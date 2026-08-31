"""
Exercise 5: Gold Publishing
----------------------------
Goal: Export curated data products to Power BI / SharePoint publishing targets (data/publish/).
"""

import os
import sys
from pathlib import Path

file_root = Path(__file__).resolve().parent.parent
if str(file_root) not in sys.path:
    sys.path.insert(0, str(file_root))

import pandas as pd
from ex4_gold_analytics_completed import GoldAnalyticsEngine


class GoldPublisher:
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        self.publish_dir = self.base_dir / "data" / "publish"
        self.publish_dir.mkdir(parents=True, exist_ok=True)
        self.analytics_engine = GoldAnalyticsEngine(base_dir=self.base_dir)

    def publish_data_products(self):
        """Export analytics tables to publishing target."""
        print("Starting Gold Data Publishing...")

        gold_df = self.analytics_engine.run_analytics()

        # Publish Donor Analytics Table
        target_path = self.publish_dir / "powerbi_donor_analytics.csv"
        gold_df.to_csv(target_path, index=False)
        print(f"Published Power BI Donor Analytics file: .{os.sep}{target_path.relative_to(self.base_dir)}")

        # Also publish Excel report version for business stakeholders
        excel_path = self.publish_dir / "powerbi_donor_analytics.xlsx"
        try:
            gold_df.to_excel(excel_path, index=False, sheet_name="Donor Analytics")
            print(f"Published Excel report file: .{os.sep}{excel_path.relative_to(self.base_dir)}")
        except Exception as e:
            print(f"Excel export skipped ({e})")

        print("Gold Publishing Completed Successfully!\n")
        return target_path


if __name__ == "__main__":
    publisher = GoldPublisher()
    publisher.publish_data_products()
