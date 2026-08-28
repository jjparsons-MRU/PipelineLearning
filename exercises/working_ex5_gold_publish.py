"""
Exercise 5: Gold Publishing (Working File)
------------------------------------------
Goal: Export final data products to target directories (e.g. for PowerBI).
"""
import sys
from pathlib import Path
import pandas as pd

class GoldPublisher:
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        self.gold_dir = self.base_dir / "data" / "gold"
        self.publish_dir = self.base_dir / "data" / "publish"
        self.publish_dir.mkdir(parents=True, exist_ok=True)

    def publish_data_products(self):
        print("Starting Gold Data Publishing...")
        # TODO: Read from gold dir, export as CSV and Excel to publish dir
        print("Gold Publishing Completed Successfully!\n")

if __name__ == "__main__":
    publisher = GoldPublisher()
    publisher.publish_data_products()
