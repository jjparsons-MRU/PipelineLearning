"""
Exercise 2: Silver Cleansing
-----------------------------
Goal: Cleanse and normalize raw Bronze datasets.
- Convert headers to snake_case.
- Standardize dates to MM/DD/YYYY.
- Handle missing values and column data types.
"""

import json
import re
from pathlib import Path
import pandas as pd


def to_snake_case(name: str) -> str:
    """Convert string to snake_case."""
    s = name.strip()
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)
    s = s.lower()
    return re.sub(r'[\s\-_]+', '_', s)


def format_date(val) -> str:
    """Format date string/timestamp to MM/DD/YYYY format."""
    if pd.isna(val) or val is None or str(val).strip() == "" or str(val).strip().lower() == "none":
        return None
    dt = pd.to_datetime(val, errors='coerce')
    if pd.isna(dt):
        return None
    return dt.strftime('%m/%d/%Y')


class SilverCleanser:
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        self.bronze_dir = self.base_dir / "data" / "bronze"
        self.silver_dir = self.base_dir / "data" / "silver"
        self.silver_dir.mkdir(parents=True, exist_ok=True)

    def cleanse_constituents(self) -> pd.DataFrame:
        """Cleanse raw bronze constituents JSON."""
        json_path = self.bronze_dir / "bronze_constituents.json"
        if not json_path.exists():
            raise FileNotFoundError(f"Missing bronze file: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        
        # 1. Normalize column headers
        df.columns = [to_snake_case(col) for col in df.columns]

        # 2. Format date columns
        date_cols = [c for c in df.columns if 'date' in c]
        for col in date_cols:
            df[col] = df[col].apply(format_date)

        # 3. Numeric fillna / typing
        df['lifetime_giving'] = pd.to_numeric(df['lifetime_giving'], errors='coerce').fillna(0.0)

        return df

    def cleanse_gifts(self) -> pd.DataFrame:
        """Cleanse raw bronze gifts JSON."""
        json_path = self.bronze_dir / "bronze_gifts.json"
        if not json_path.exists():
            raise FileNotFoundError(f"Missing bronze file: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        # 1. Normalize headers
        df.columns = [to_snake_case(col) for col in df.columns]

        # 2. Format date
        if 'gift_date' in df.columns:
            df['gift_date'] = df['gift_date'].apply(format_date)

        # 3. Numeric fillna
        if 'amount' in df.columns:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)

        return df

    def cleanse_dates(self) -> pd.DataFrame:
        """Cleanse raw dates CSV."""
        csv_path = self.bronze_dir / "bronze_dates.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing bronze file: {csv_path}")

        df = pd.read_csv(csv_path)

        # 1. Normalize headers
        df.columns = [to_snake_case(col) for col in df.columns]

        # 2. Clean dates
        if 'date' in df.columns:
            df['date'] = df['date'].apply(format_date)

        return df

    def cleanse_revenue(self) -> pd.DataFrame:
        """Cleanse raw revenue types CSV."""
        csv_path = self.bronze_dir / "bronze_revenue.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing bronze file: {csv_path}")

        df = pd.read_csv(csv_path)

        # 1. Normalize headers
        df.columns = [to_snake_case(col) for col in df.columns]

        return df

    def run_cleansing(self):
        """Execute cleansing and save cleansed tables to silver staging area."""
        print("Starting Silver Layer Cleansing...")
        const_df = self.cleanse_constituents()
        gifts_df = self.cleanse_gifts()
        dates_df = self.cleanse_dates()
        rev_df = self.cleanse_revenue()

        print(f"Cleansed Constituents: {len(const_df)} records")
        print(f"Cleansed Gifts: {len(gifts_df)} records")
        print(f"Cleansed Dates: {len(dates_df)} records")
        print(f"Cleansed Revenue Types: {len(rev_df)} records")
        print("Silver Cleansing Completed Successfully!\n")
        return const_df, gifts_df, dates_df, rev_df


if __name__ == "__main__":
    cleanser = SilverCleanser()
    cleanser.run_cleansing()
