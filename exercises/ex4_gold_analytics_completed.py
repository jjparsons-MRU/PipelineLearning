"""
Exercise 4: Gold Analytics
---------------------------
Goal: Compute business analytics and segmentation metrics (LYBUNT, SYBUNT, Recency, Predictive stats).
Outputs gold_donor_analytics.csv to data/gold/.
"""

import sys
from datetime import datetime
from pathlib import Path

file_root = Path(__file__).resolve().parent.parent
if str(file_root) not in sys.path:
    sys.path.insert(0, str(file_root))

import pandas as pd
from ex3_silver_model_completed import SilverModeler


class GoldAnalyticsEngine:
    def __init__(self, base_dir: Path = None, current_year: int = 2024):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = base_dir
        self.gold_dir = self.base_dir / "data" / "gold"
        self.gold_dir.mkdir(parents=True, exist_ok=True)
        self.modeler = SilverModeler(base_dir=self.base_dir)
        self.current_year = current_year

    def calculate_recency_months(self, latest_gift_date_str: str, ref_date: str = "2024-12-31") -> float:
        """Calculate number of months between latest gift date and reference date."""
        if pd.isna(latest_gift_date_str) or not latest_gift_date_str:
            return None
        dt_gift = pd.to_datetime(latest_gift_date_str, errors='coerce')
        if pd.isna(dt_gift):
            return None
        dt_ref = pd.to_datetime(ref_date)
        return round((dt_ref - dt_gift).days / 30.4375, 1)

    def calculate_donor_metrics(self, summary_df: pd.DataFrame, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Compute donor analytics including LYBUNT, SYBUNT, recency, and monetary stats."""
        analytics_df = summary_df.copy()

        current_fy = self.current_year
        last_fy = current_fy - 1

        # Calculate fiscal year giving totals per constituent
        if not transactions_df.empty and 'fiscal_year' in transactions_df.columns:
            fy_giving = transactions_df.groupby(['constituent_id', 'fiscal_year'])['amount'].sum().unstack(fill_value=0)
        else:
            fy_giving = pd.DataFrame()

        # Helper flags for LYBUNT & SYBUNT
        lybunt_list = []
        sybunt_list = []
        total_tx_list = []
        avg_gift_list = []

        for _, row in analytics_df.iterrows():
            cid = row['constituent_id']

            has_current_fy_giving = False
            has_last_fy_giving = False
            has_prior_fy_giving = False

            if cid in fy_giving.index:
                cid_fy = fy_giving.loc[cid]
                if current_fy in cid_fy and cid_fy[current_fy] > 0:
                    has_current_fy_giving = True
                if last_fy in cid_fy and cid_fy[last_fy] > 0:
                    has_last_fy_giving = True
                prior_years = [y for y in cid_fy.index if y < last_fy]
                if any(cid_fy[y] > 0 for y in prior_years):
                    has_prior_fy_giving = True

            # LYBUNT: Last Year But Not This Year
            is_lybunt = has_last_fy_giving and not has_current_fy_giving

            # SYBUNT: Some Year (prior to last year or previous) But Not This Year
            is_sybunt = (has_last_fy_giving or has_prior_fy_giving) and not has_current_fy_giving

            lybunt_list.append(is_lybunt)
            sybunt_list.append(is_sybunt)

            # Transaction stats
            cid_txs = transactions_df[transactions_df['constituent_id'] == cid] if 'constituent_id' in transactions_df.columns else pd.DataFrame()
            total_tx_list.append(len(cid_txs))
            avg_gift_list.append(round(cid_txs['amount'].mean(), 2) if len(cid_txs) > 0 else 0.0)

        analytics_df['lybunt'] = lybunt_list
        analytics_df['sybunt'] = sybunt_list
        analytics_df['total_transactions'] = total_tx_list
        analytics_df['average_gift_amount'] = avg_gift_list

        # Recency calculation
        analytics_df['recency_months'] = analytics_df['latest_gift_date'].apply(
            lambda d: self.calculate_recency_months(d, ref_date=f"{self.current_year}-12-31")
        )

        return analytics_df

    def run_analytics(self):
        """Execute analytics and write gold_donor_analytics.csv."""
        print("Starting Gold Layer Analytics...")
        const_summary, gift_transactions = self.modeler.run_modeling()

        gold_df = self.calculate_donor_metrics(const_summary, gift_transactions)
        gold_path = self.gold_dir / "gold_donor_analytics.csv"
        gold_df.to_csv(gold_path, index=False)

        print(f"Saved Gold Donor Analytics: {gold_path}")
        print("Gold Analytics Completed Successfully!\n")
        return gold_df


if __name__ == "__main__":
    engine = GoldAnalyticsEngine()
    engine.run_analytics()
