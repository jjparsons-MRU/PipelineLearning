# Project Summary: Python Data Staging Area & Analytics Pipeline

This document provides a summary of our conversation, project goals, and the path forward for your Python learning and development project.

---

## 1. Project Goal
The objective is to build a **Data Staging Area in Python** that:
* **Ingests** data from two sources: local CSV files and the Blackbaud SKY API.
* **Transforms/Cleanses** the data (standardizing formats, handling missing values, etc.).
* **Models & Analyzes** the combined dataset to produce insights.
* **Loads/Exports** a final, cleansed CSV file for reporting.

---

## 2. Learning & Collaboration Method
* **User-Led Coding:** You will write the code yourself to learn Python hands-on.
* **Agent Guidance:** Antigravity (your AI assistant) will explain the concepts, provide template examples, and review/debug the code you write.
* **Workspace:** All project files, scripts, and output files will be created in your dedicated project directory:
  `C:\Users\jjparsons\Desktop\Hackathon Project\Pipeline Learning`

---

## 3. Proposed Technology Stack
* **Language:** Python
* **Data Manipulation & Analysis:** `pandas` (industry standard for tabular data).
* **API Requests:** `requests` (user-friendly library for HTTP calls to Blackbaud SKY API).
* **Configuration & Security:** `python-dotenv` (for storing sensitive API keys in a `.env` file).

---

## 4. Key Project Milestones (The Roadmap)
1. **Phase 1: Environment & Version Control Setup** (Virtual environment, libraries, `.env`/`.gitignore`, Git local repository, and remote GitHub synchronization).
2. **Phase 2: Ingesting CSV Files** (Reading CSVs using Pandas).
3. **Phase 3: Fetching Blackbaud API Data** (Authentication, making endpoint requests, converting JSON to DataFrame).
4. **Phase 4: Staging & Transformations** (Standardizing schemas, formatting columns/dates, cleansing strings).
5. **Phase 5: Data Modeling & Analytics** (Merging tables/DataFrames, calculating custom metrics).
6. **Phase 6: Loading & Exporting** (Generating clean CSV output reports).
7. **Phase 7: SQL Database Integration (Future Scaling)** (Connecting to database, querying via SQL, and direct ingestion into Pandas using `sqlalchemy` and `pandas.read_sql`).

---

## 5. File Locations
* **Implementation Plan:** Located in your project directory at `C:\Users\jjparsons\Desktop\Hackathon Project\Pipeline Learning\implementation_plan.md`
* **Conversation Summary:** This file, saved at `C:\Users\jjparsons\Desktop\Hackathon Project\Pipeline Learning\conversation_summary.md`

---

## 6. Next Steps & Open Questions
To kick off Phase 1, we will want to align on the following details:
1. **CSV Ingestion:** What kind of CSV files are you planning to ingest?
2. **Blackbaud API:** Which specific endpoints do you want to query? (e.g., Constituents, Gifts, etc.)
3. **Analytics:** What metrics/transformations are we aiming to produce?
4. **API Credentials:** Do you already have a Blackbaud Developer account and API subscription key?
