"""
Exercise 3: Silver Modeling (Working File)
------------------------------------------
Goal: Create final normalized relational tables.
"""
import sys
from pathlib import Path
import pandas as pd

class SilverModeler:
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        self.silver_dir = self.base_dir / "data" / "silver"

    def build_constituent_summary(self, const_df: pd.DataFrame) -> pd.DataFrame:
        """TODO: Return a modeled constituent summary DataFrame."""
        pass

    def build_gift_transactions(self, gifts_df: pd.DataFrame, dates_df: pd.DataFrame, rev_df: pd.DataFrame) -> pd.DataFrame:
        """TODO: Merge gifts with dates and revenue reference tables."""
        pass

    def run_modeling(self):
        print("Starting Silver Layer Modeling...")
        # TODO: Read from silver dir, call modeling methods, save back to silver dir
        print("Silver Modeling Completed Successfully!\n")

if __name__ == "__main__":
    modeler = SilverModeler()
    modeler.run_modeling()
