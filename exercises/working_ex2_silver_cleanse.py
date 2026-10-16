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

    

    def _infer_and_format_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Private helper method to detect and format date columns regardless of column name."""
        for col in df.columns:
            # Skip columns that are already numeric or boolean
            if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_bool_dtype(df[col]):
                continue
                
            sample =df[col].dropna()
            if not sample.empty:
                try:
                    # Test if sample values are valid dates
                    pd.to_datetime(sample.head(100), errors='raise')
                    # If valid, apply your date formatting function
                    df[col] = df[col].apply(format_date)
                except (ValueError, TypeError):
                    pass
        return df

    def cleanse_constituents(self) -> pd.DataFrame:
        """
        1. Read 'bronze_constituents.json'
        2. Normalize column headers
        3. Format date columns
        4. Return DataFrame
        """
        json_path = self.bronze_dir / "bronze_constituents.json"
        if not json_path.exists():
           raise FileNotFoundError(f"Missing bronze file: {json_path}")
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        
        df.columns = [to_snake_case(col) for col in df.columns]
        df = self._infer_and_format_dates(df)
        if 'lifetime_giving' in df.columns:
            df['lifetime_giving'] = pd.to_numeric(df['lifetime_giving'], errors='coerce').fillna(0.0)
        return df

    def cleanse_gifts(self) -> pd.DataFrame:
        """TODO: Cleanse raw bronze gifts JSON."""

        json_path = self.bronze_dir / "bronze_gifts.json"
        if not json_path.exists():
            raise FileNotFoundError(f"Missing bronze file: {json_path}")
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)

        df.columns = [to_snake_case(col) for col in df.columns]
        df = self._infer_and_format_dates(df)
        if 'amount' in df.columns:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
        return df
       
    def cleanse_dates(self) -> pd.DataFrame:
        """TODO: Cleanse raw dates CSV."""
        csv_path = self.bronze_dir / "bronze_dates.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing bronze file: {csv_path}")
        
        df = pd.read_csv(csv_path)

        df.columns = [to_snake_case(col) for col in df.columns]
        df = self._infer_and_format_dates(df)
        return df

    def cleanse_revenue(self) -> pd.DataFrame:
        """TODO: Cleanse raw revenue CSV."""
        csv_path = self.bronze_dir / "bronze_revenue.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing bronze file: {csv_path}")
        df = pd.read_csv(csv_path)

        df.columns = [to_snake_case(col) for col in df.columns]

        return df


    def run_cleansing(self):
        print("Starting Silver Layer Cleansing...")
        const = self.cleanse_constituents()
        gifts = self.cleanse_gifts()
        dates = self.cleanse_dates()
        rev = self.cleanse_revenue()

        print(f"Cleansed Constituents: {len(const)} records.")
        print(f"Cleansed Gifts: {len(gifts)} records.")
        print(f"Cleansed Dates: {len(dates)} records.")
        print(f"Cleansed Revenue: {len(rev)} records.")

        # Save cleansed tables to self.silver_dir
        const.to_csv(self.silver_dir / "clean_silver_constituents.csv", index=False)
        gifts.to_csv(self.silver_dir / "clean_silver_gifts.csv", index=False)
        dates.to_csv(self.silver_dir / "clean_silver_dates.csv", index=False)
        rev.to_csv(self.silver_dir / "clean_silver_revenue.csv", index=False)

        print("Silver Cleansing Completed Successfully!\n")
        return const, gifts, dates, rev
if __name__ == "__main__":
    cleanser = SilverCleanser()
    cleanser.run_cleansing()
    
