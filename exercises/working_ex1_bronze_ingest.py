"""
Exercise 1: Bronze Ingestion (Working File)
-------------------------------------------
Goal: Ingest raw data from APIs (Mocked), CSVs, and a stub for SQL 
into the Bronze layer (data/bronze/).
"""

import json
import os
from pathlib import Path
import pandas as pd
import requests

class BronzeIngestor:
    def __init__(self, base_dir: Path = None):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        self.bronze_dir = self.base_dir / "data" / "bronze"
        self.bronze_dir.mkdir(parents=True, exist_ok=True)
        
        # TODO: Make sure the bronze directory exists! (Hint: use mkdir)
        
    def generate_mock_constituents(self) -> list:
        """Returns mock constituent data to simulate an API response."""
        return [
            {"id": "CON-1001", "name": "Jane Doe", "prospect_status": "Major Donor"},
            {"id": "CON-1002", "name": "John Smith", "prospect_status": "Lapsed"},
        ]

    def generate_mock_gifts(self) -> list:
        """Returns mock gift transaction data to simulate an API response."""
        return [
            {"gift_id": "GFT-5001", "constituent_id": "CON-1001", "amount": 100.00, "gift_date": "2018-05-15"},
            {"gift_id": "GFT-5004", "constituent_id": "CON-1002", "amount": 50.00, "gift_date": "2019-02-10"},
        ]

    def generate_mock_dates_csv(self) -> pd.DataFrame:
        """Generate mock date dimension reference dataframe."""
        dates_data = [{"Date": "2018-05-15", "Fiscal_Year": 2018, "Quarter": "Q2", "Month_Name": "May"}]
        return pd.DataFrame(dates_data)

    def generate_mock_revenue_csv(self) -> pd.DataFrame:
        """Generate mock revenue type reference dataframe."""
        revenue_data = [{"Revenue_Type_ID": "REV-01", "Name": "Unrestricted Annual Fund", "Category": "Annual"}]
        return pd.DataFrame(revenue_data)

    # -------------------------------------------------------------------------
    # TODO: Implement Strategy Pattern / Ingestion Methods Below
    # -------------------------------------------------------------------------

    def ingest_from_api(self):
        """
        TODO: Fetch constituents and gifts (using the mock methods above for now),
        and write them to data/bronze as JSON files.
        """
        constituent_data = self.generate_mock_constituents()
        out_path = self.bronze_dir/"constituents.json"
        with open(outpath, "w") as f:
                json.dump(constituent_data, f, indent=4)
        
        gift_data = self.generate_mock_gifts()
        out_path = self.bronze_dir/"gifts_json"
        with open(out_path, "w") as f:
            json.dump(gift_data, f, indent=4)

    def ingest_from_csv(self):
        """
        TODO: Fetch dates and revenue types (using the mock dataframe methods above),
        and write them to data/bronze as CSV files.
        """
        outliers_df.to_csv(output_path, index=False)
        pass

    def ingest_from_sql(self):
        """
        TODO: Future-proofing! Create a stub for SQL ingestion.
        It doesn't need to do anything yet, just pass or raise NotImplementedError.
        """
        pass

    def run_ingestion(self):
        """
        TODO: Orchestrate the ingestion process by calling the methods above.
        """
        print("Starting Bronze Layer Ingestion...")
        # Call your ingestion methods here!
        print("Bronze Ingestion Completed Successfully!\n")


if __name__ == "__main__":
    ingestor = BronzeIngestor()
    ingestor.run_ingestion()

