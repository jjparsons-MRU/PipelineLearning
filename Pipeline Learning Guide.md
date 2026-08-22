# Pipeline Learning — Medallion Architecture & Analytics Guide

Welcome to the **Pipeline Learning** program! In this module, we will implement a real-world proof of concept for a **Medallion Architecture** data pipeline using Python. 

By the end of these exercises, you will have a pipeline that ingests data, cleanses and normalizes it, merges it into structured tables, calculates donor analytics (like LYBUNT/SYBUNT), and exports these tables ready for Power BI/SharePoint.

---

## Project Structure

Our workspace is structured as follows:

```text
PipelineLearning/
├── README.md
├── requirements.txt
├── .gitignore
├── .env
├── Pipeline Learning Guide.md    # This guide
├── data/
│   ├── bronze/                   # Raw JSON API payloads and raw CSVs
│   ├── silver/                   # Cleaned and structured summaries/transactions
│   └── gold/                     # Analytics outputs ready for Power BI/SharePoint
└── exercises/
    ├── ex1_bronze_ingest.py      # Ingesting APIs and CSVs into Bronze
    ├── ex2_silver_cleanse.py     # Cleaning & normalising Bronze data
    ├── ex3_silver_model.py       # Creating Silver Summary and Transaction tables
    ├── ex4_gold_analytics.py     # Gold layer: Recency, LYBUNT/SYBUNT, predictive stats
    └── ex5_gold_publish.py       # Exporting data products for Power BI / SharePoint
```

---

## Data Architecture (Medallion Layers)

| Layer | Goal | Description | Files Produced |
|---|---|---|---|
| **Bronze** | Raw Ingestion | Raw data exactly as received from APIs or files. No modifications. | `bronze_constituents.json`, `bronze_gifts.json`, `bronze_dates.csv`, `bronze_revenue.csv` |
| **Silver** | Clean & Model | Standardized schemas, cleaned dates, combined transaction/summary tables. | `silver_constituent_summary.csv`, `silver_gift_transactions.csv` |
| **Gold** | Analytics | Business-level aggregates, segmentations (LYBUNT/SYBUNT), prep for predictive models. | `gold_donor_analytics.csv` |

---

## Syllabus: Exercises to Build

### Exercise 1: Bronze Ingestion (`exercises/ex1_bronze_ingest.py`)
* **Goal**: Write scripts to fetch data and write them to `data/bronze/`.
* **API Endpoints**: 
  - *Constituents*: Request prospect status, lifetime giving, first/latest/largest gift.
  - *Gifts*: Retrieve individual gift transaction records.
* **CSVs**: Load dates and revenue type mappings.
* **Mock Mode**: Include a mock engine so you can run the exercise offline without API credentials.

### Exercise 2: Silver Cleansing (`exercises/ex2_silver_cleanse.py`)
* **Goal**: Normalise the raw Bronze files.
* **Cleansing Rules**:
  - Normalize dates to `MM/DD/YYYY` (per company business rules).
  - Convert column headers to `snake_case`.
  - Handle missing data (NaN) and data types.

### Exercise 3: Silver Modeling (`exercises/ex3_silver_model.py`)
* **Goal**: Create clean relational tables.
* **Summary Table**: Read constituent API fields directly (lifetime giving, first/largest/latest gift, prospect status) into a consolidated donor record.
* **Transaction Table**: Join raw gift records with Date dimension to extract fiscal years, and Revenue Types dimension to classify each gift.

### Exercise 4: Gold Analytics (`exercises/ex4_gold_analytics.py`)
* **Goal**: Generate advanced metrics on Silver tables.
* **Metrics**:
  - **LYBUNT**: Last Year But Not This Year (Donors who gave last fiscal year but not this fiscal year).
  - **SYBUNT**: Some Year But Not This Year (Donors who gave in previous years but not this fiscal year).
  - **Recency**: Months since the latest gift.
  - **Predictive Prep**: Feature engineering to prepare tables for future Gamma-Gamma modeling.

### Exercise 5: Gold Publishing (`exercises/ex5_gold_publish.py`)
* **Goal**: Export final data products to OneDrive/SharePoint or local targets ready for Power BI auto-refresh.

---

## Collaborative Learning Method

For each exercise:
1. **Explain**: I will outline the Python methods and libraries we will use.
2. **Draft**: We will write the starter code together.
3. **Execute & Test**: You or I will run the scripts, debug any errors, and review the files generated in the `data/` folders.
