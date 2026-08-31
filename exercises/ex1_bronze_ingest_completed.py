"""
Exercise 1: Bronze Ingestion
-----------------------------
Goal: Ingest raw data from APIs (Blackbaud SKY API / Mock) and reference CSVs into the Bronze layer (data/bronze/).
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

    def generate_mock_constituents(self) -> list:
        """Generate mock constituent API payloads."""
        return [
            {
                "id": "CON-1001",
                "name": "Jane Doe",
                "prospect_status": "Major Donor",
                "lifetime_giving": 25000.00,
                "first_gift_date": "2018-05-15",
                "first_gift_amount": 100.00,
                "latest_gift_date": "2024-11-20",
                "latest_gift_amount": 5000.00,
                "largest_gift_date": "2023-12-10",
                "largest_gift_amount": 10000.00,
            },
            {
                "id": "CON-1002",
                "name": "John Smith",
                "prospect_status": "Lapsed",
                "lifetime_giving": 1200.00,
                "first_gift_date": "2019-02-10",
                "first_gift_amount": 50.00,
                "latest_gift_date": "2022-04-14",
                "latest_gift_amount": 250.00,
                "largest_gift_date": "2021-06-30",
                "largest_gift_amount": 500.00,
            },
            {
                "id": "CON-1003",
                "name": "Alice Johnson",
                "prospect_status": "Active Donor",
                "lifetime_giving": 4500.00,
                "first_gift_date": "2020-01-05",
                "first_gift_amount": 250.00,
                "latest_gift_date": "2024-10-01",
                "latest_gift_amount": 1000.00,
                "largest_gift_date": "2024-10-01",
                "largest_gift_amount": 1000.00,
            },
            {
                "id": "CON-1004",
                "name": "Robert Brown",
                "prospect_status": "Prospect",
                "lifetime_giving": 0.00,
                "first_gift_date": None,
                "first_gift_amount": None,
                "latest_gift_date": None,
                "latest_gift_amount": None,
                "largest_gift_date": None,
                "largest_gift_amount": None,
            },
            {
                "id": "CON-1005",
                "name": "Emily Davis",
                "prospect_status": "Active Donor",
                "lifetime_giving": 3200.00,
                "first_gift_date": "2021-07-19",
                "first_gift_amount": 200.00,
                "latest_gift_date": "2023-09-15",
                "latest_gift_amount": 500.00,
                "largest_gift_date": "2022-12-01",
                "largest_gift_amount": 1500.00,
            },
        ]

    def generate_mock_gifts(self) -> list:
        """Generate mock gift transaction API payloads."""
        return [
            {
                "gift_id": "GFT-5001",
                "constituent_id": "CON-1001",
                "amount": 100.00,
                "gift_date": "2018-05-15",
                "revenue_type_id": "REV-01",
                "payment_method": "Credit Card",
            },
            {
                "gift_id": "GFT-5002",
                "constituent_id": "CON-1001",
                "amount": 10000.00,
                "gift_date": "2023-12-10",
                "revenue_type_id": "REV-01",
                "payment_method": "Check",
            },
            {
                "gift_id": "GFT-5003",
                "constituent_id": "CON-1001",
                "amount": 5000.00,
                "gift_date": "2024-11-20",
                "revenue_type_id": "REV-02",
                "payment_method": "Wire Transfer",
            },
            {
                "gift_id": "GFT-5004",
                "constituent_id": "CON-1002",
                "amount": 50.00,
                "gift_date": "2019-02-10",
                "revenue_type_id": "REV-01",
                "payment_method": "Credit Card",
            },
            {
                "gift_id": "GFT-5005",
                "constituent_id": "CON-1002",
                "amount": 500.00,
                "gift_date": "2021-06-30",
                "revenue_type_id": "REV-01",
                "payment_method": "Credit Card",
            },
            {
                "gift_id": "GFT-5006",
                "constituent_id": "CON-1002",
                "amount": 250.00,
                "gift_date": "2022-04-14",
                "revenue_type_id": "REV-03",
                "payment_method": "Check",
            },
            {
                "gift_id": "GFT-5007",
                "constituent_id": "CON-1003",
                "amount": 250.00,
                "gift_date": "2020-01-05",
                "revenue_type_id": "REV-01",
                "payment_method": "Credit Card",
            },
            {
                "gift_id": "GFT-5008",
                "constituent_id": "CON-1003",
                "amount": 1000.00,
                "gift_date": "2024-10-01",
                "revenue_type_id": "REV-02",
                "payment_method": "Credit Card",
            },
            {
                "gift_id": "GFT-5009",
                "constituent_id": "CON-1005",
                "amount": 200.00,
                "gift_date": "2021-07-19",
                "revenue_type_id": "REV-01",
                "payment_method": "Credit Card",
            },
            {
                "gift_id": "GFT-5010",
                "constituent_id": "CON-1005",
                "amount": 1500.00,
                "gift_date": "2022-12-01",
                "revenue_type_id": "REV-01",
                "payment_method": "Check",
            },
            {
                "gift_id": "GFT-5011",
                "constituent_id": "CON-1005",
                "amount": 500.00,
                "gift_date": "2023-09-15",
                "revenue_type_id": "REV-03",
                "payment_method": "Credit Card",
            },
        ]

    def generate_mock_dates_csv(self) -> pd.DataFrame:
        """Generate mock date dimension reference dataframe."""
        dates_data = [
            {"Date": "2018-05-15", "Fiscal_Year": 2018, "Quarter": "Q2", "Month_Name": "May"},
            {"Date": "2019-02-10", "Fiscal_Year": 2019, "Quarter": "Q1", "Month_Name": "February"},
            {"Date": "2020-01-05", "Fiscal_Year": 2020, "Quarter": "Q1", "Month_Name": "January"},
            {"Date": "2021-06-30", "Fiscal_Year": 2021, "Quarter": "Q2", "Month_Name": "June"},
            {"Date": "2021-07-19", "Fiscal_Year": 2021, "Quarter": "Q3", "Month_Name": "July"},
            {"Date": "2022-04-14", "Fiscal_Year": 2022, "Quarter": "Q2", "Month_Name": "April"},
            {"Date": "2022-12-01", "Fiscal_Year": 2022, "Quarter": "Q4", "Month_Name": "December"},
            {"Date": "2023-09-15", "Fiscal_Year": 2023, "Quarter": "Q3", "Month_Name": "September"},
            {"Date": "2023-12-10", "Fiscal_Year": 2023, "Quarter": "Q4", "Month_Name": "December"},
            {"Date": "2024-10-01", "Fiscal_Year": 2024, "Quarter": "Q4", "Month_Name": "October"},
            {"Date": "2024-11-20", "Fiscal_Year": 2024, "Quarter": "Q4", "Month_Name": "November"},
        ]
        return pd.DataFrame(dates_data)

    def generate_mock_revenue_csv(self) -> pd.DataFrame:
        """Generate mock revenue type reference dataframe."""
        revenue_data = [
            {"Revenue_Type_ID": "REV-01", "Name": "Unrestricted Annual Fund", "Category": "Annual"},
            {"Revenue_Type_ID": "REV-02", "Name": "Endowment Fund", "Category": "Capital"},
            {"Revenue_Type_ID": "REV-03", "Name": "Special Event Ticket", "Category": "Events"},
        ]
        return pd.DataFrame(revenue_data)

    def run_ingestion(self, use_mock: bool = True):
        """Perform ingestion into data/bronze/ directory."""
        print("Starting Bronze Layer Ingestion...")

        # 1. Ingest Constituents
        constituents = self.generate_mock_constituents()
        const_path = self.bronze_dir / "bronze_constituents.json"
        with open(const_path, "w", encoding="utf-8") as f:
            json.dump(constituents, f, indent=2)
        print(f"Saved Bronze Constituents: .{os.sep}{const_path.relative_to(self.base_dir)}")

        # 2. Ingest Gifts
        gifts = self.generate_mock_gifts()
        gift_path = self.bronze_dir / "bronze_gifts.json"
        with open(gift_path, "w", encoding="utf-8") as f:
            json.dump(gifts, f, indent=2)
        print(f"Saved Bronze Gifts: .{os.sep}{gift_path.relative_to(self.base_dir)}")

        # 3. Ingest Dates CSV
        dates_df = self.generate_mock_dates_csv()
        dates_path = self.bronze_dir / "bronze_dates.csv"
        dates_df.to_csv(dates_path, index=False)
        print(f"Saved Bronze Dates: .{os.sep}{dates_path.relative_to(self.base_dir)}")

        # 4. Ingest Revenue CSV
        revenue_df = self.generate_mock_revenue_csv()
        revenue_path = self.bronze_dir / "bronze_revenue.csv"
        revenue_df.to_csv(revenue_path, index=False)
        print(f"Saved Bronze Revenue Types: .{os.sep}{revenue_path.relative_to(self.base_dir)}")

        print("Bronze Ingestion Completed Successfully!\n")


if __name__ == "__main__":
    ingestor = BronzeIngestor()
    ingestor.run_ingestion(use_mock=True)
