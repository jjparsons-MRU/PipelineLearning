"""
Exercise 2: Silver Cleansing (Working File)
-------------------------------------------
Goal: Cleanse and normalize raw Bronze datasets.
- Convert headers to snake_case.
- Standardize dates to MM/DD/YYYY.
- Handle missing values and column data types.
"""
import json
import re
from pathlib import Path
import pandas as pd
import datetime

def to_snake_case(name: str) -> str:
    """Helper to convert string to snake_case."""
    # TODO: write regex or string replacements to convert CamelCase to snake_case
    s = name.strip() #removes whitespace
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s) #looks for a capital letter followed by any number of lowercase, then inserts _ after the character immediately preceeding the capital
    s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)#similarly, looks for a capital letter preceeded by lowercase or a number and inserts _
    s = s.lower() #converts all uppercase letters to lowercase
    return re.sub(r'[\s\-_]+', '_', s) #replaces any whitespace, hyphens, or underscores with a single underscore
 

def format_date(val) -> str:
    """Helper to format date string to MM/DD/YYYY format."""
    if pd.isna(val):
        return None
    try:
        dt = pd.to_datetime(val)
        return dt.strftime('%m/%d/%Y')
    except Exception:
        return None

class SilverCleanser:
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        self.bronze_dir = self.base_dir / "data" / "bronze"
        self.silver_dir = self.base_dir / "data" / "silver"
        self.silver_dir.mkdir(parents=True, exist_ok=True)

    def cleanse_constituents(self) -> pd.DataFrame:
        """
        TODO: 
        1. Read 'bronze_constituents.json'
        2. Normalize column headers
        3. Format date columns
        4. Return DataFrame
        """
        pass

    def cleanse_gifts(self) -> pd.DataFrame:
        """TODO: Cleanse raw bronze gifts JSON."""
        pass

    def cleanse_dates(self) -> pd.DataFrame:
        """TODO: Cleanse raw dates CSV."""
        pass

    def cleanse_revenue(self) -> pd.DataFrame:
        """TODO: Cleanse raw revenue CSV."""
        pass

    def run_cleansing(self):
        print("Starting Silver Layer Cleansing...")
        # TODO: Call your cleanse methods and save them to self.silver_dir
        print("Silver Cleansing Completed Successfully!\n")

if __name__ == "__main__":
    cleanser = SilverCleanser()
    cleanser.run_cleansing()
