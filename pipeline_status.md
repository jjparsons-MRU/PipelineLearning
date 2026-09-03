# Pipeline Learning — Status Handoff

**Current Workspace:** `PipelineLearning` (Medallion Architecture & Analytics)  
**Current Exercise:** Exercise 2 — Silver Cleansing (`exercises/working_ex2_silver_cleanse.py`)  
**Date:** September 3, 2026

---

## 1. What We Completed Today
In [`exercises/working_ex2_silver_cleanse.py`](exercises/working_ex2_silver_cleanse.py):
- **`to_snake_case(name: str)`**: Completed and verified. Uses regex to cleanly convert PascalCase/CamelCase, spaces, and hyphens into standardized `snake_case` headers.
- **`format_date(val) -> str`**: Completed and verified. Uses `pd.to_datetime()` to convert dates to `MM/DD/YYYY` format while safely catching null/empty values and parsing exceptions.

---

## 2. Immediate Next Steps (To Start Tomorrow)
Open [`exercises/working_ex2_silver_cleanse.py`](exercises/working_ex2_silver_cleanse.py) and implement the cleansing methods inside the `SilverCleanser` class:

### Step 1: Implement `cleanse_constituents(self) -> pd.DataFrame`
1. Load Bronze JSON:
   ```python
   json_path = self.bronze_dir / "bronze_constituents.json"
   with open(json_path, "r", encoding="utf-8") as f:
       data = json.load(f)
   df = pd.DataFrame(data)
   ```
2. Normalize column headers:
   ```python
   df.columns = [to_snake_case(col) for col in df.columns]
   ```
3. Format date columns:
   ```python
   date_cols = [c for c in df.columns if 'date' in c]
   for col in date_cols:
       df[col] = df[col].apply(format_date)
   ```
4. Cast numeric giving fields:
   ```python
   df['lifetime_giving'] = pd.to_numeric(df['lifetime_giving'], errors='coerce').fillna(0.0)
   ```
5. Return the DataFrame: `return df`

### Step 2: Implement `cleanse_gifts(self) -> pd.DataFrame`
- Follow a similar pattern for `bronze_gifts.json`: normalize column headers, apply `format_date` to `gift_date`, and ensure `amount` is numeric.

### Step 3: Implement `cleanse_dates(self)` and `cleanse_revenue(self)`
- Read CSV lookup tables from `self.bronze_dir` (`bronze_dates.csv` and `bronze_revenue.csv`), normalize headers with `to_snake_case`, and format dates where applicable.

### Step 4: Implement `run_cleansing(self)` & Test
- Call each cleansing method and write the cleaned DataFrames to `self.silver_dir` as CSV files (`silver_constituents.csv`, `silver_gifts.csv`, etc.).
- Run the script:
  ```powershell
  py exercises/working_ex2_silver_cleanse.py
  ```

---
*Note for Office Antigravity Agent: Read this file along with `exercises/working_ex2_silver_cleanse.py` to pick up immediately on Step 1 (`cleanse_constituents`).*
