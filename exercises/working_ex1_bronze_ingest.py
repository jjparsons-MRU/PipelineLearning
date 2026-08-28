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

    """
    Future proofing this to allow for easier scalability when adding APIs.

    API_ENDPOINTS = {
        "constituents": "https://api.sky.blackbaud.com/constituent/",
        "gifts": "https://api.sky.blackbaud.com/gift/",
        "prospect":"https://api.sky.blackbaud.com/prospect"          
    }
    """
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
        with open(out_path, "w") as f:
            json.dump(constituent_data, f, indent=4)
        
        gift_data = self.generate_mock_gifts()
        out_path = self.bronze_dir/"gifts.json"
        with open(out_path, "w") as f:
            json.dump(gift_data, f, indent=4)
    """Future proofing: calling from the API dictionary.
    def ingest_all_apis(self, api_endpoints: dict = API_ENDPOINTS):
        #this will iterate over all endpoints in the disctionary.
        for name, url in api_endpoints.items():
            print(f"Fetching {name} from {url} ...")
            try:
                # Send HTTP request
                headers = {"Authorization": f"Bearer {my_access_token}"}
                response = requests.get(url, headers=headers, timeout=10)
                
                # Raise an exception for HTTP error statuses (4xx, 5xx)
                response.raise_for_status()
                
                # Parse response body as JSON
                data = response.json()
                
                # Define output destination
                out_path = self.bronze_dir / f"{name}.json"
                
                # Write raw JSON output
                with open(out_path, "w") as f:
                    json.dump(data, f, indent=4)
                
                print(f"Successfully saved {name} to {out_path}")

            except requests.exceptions.RequestException as e:
                # Catch network errors, timeouts, or bad HTTP status codes without stopping the pipeline
                print(f"Failed to ingest {name} from {url}: {e}")
    """


    def ingest_from_csv(self):

        dates = self.generate_mock_dates_csv()
        revenue_data = self.generate_mock_revenue_csv()

        dates.to_csv(self.bronze_dir/"dates.csv", index=False)
        revenue_data.to_csv(self.bronze_dir/"revenue.csv", index=False)
           

        """
        TODO: Fetch dates and revenue types (using the mock dataframe methods above),
        and write them to data/bronze as CSV files.
        """
 

    def ingest_from_sql(self):
        """
        TODO: Future-proofing! Create a stub for SQL ingestion.
        It doesn't need to do anything yet, just pass or raise NotImplementedError.
        """
        #This is a future implementation to allow for SQL ingestion. Right now we're just mockin in the free world.
        # 1. We wrap it in a try/except because we know the database doesn't exist yet!
        try:
            # 2. Write your mock connection string and query
            conn_str = "sqlite:///mock_database.db"
            query = "SELECT * FROM campaigns"
            
            # 3. Use pandas to read the SQL query into a DataFrame
            df = pd.read_sql(query, conn_str)
            
            # 4. Save the DataFrame to the Bronze directory as a CSV
            df.to_csv(self.bronze_dir / "sql_campaigns.csv", index=False)
            
        except Exception as e:
            print(f"SQL Ingestion skipped (Future implementation): {e}")

    def run_ingestion(self):
        """
        TODO: Orchestrate the ingestion process by calling the methods above.
        """
        print("Starting Bronze Layer Ingestion...")
        self.ingest_from_api()
        print("Processing API ...")
        self.ingest_from_csv()
        print("Processing CSV ...")
   
        # Call your ingestion methods here!
        print("Bronze Ingestion Completed Successfully!\n")


if __name__ == "__main__":
    ingestor = BronzeIngestor()
    ingestor.run_ingestion()

