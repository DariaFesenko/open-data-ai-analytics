import os
import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DB_PATH = Path(os.getenv("DB_PATH", "/storage/data.db"))
TABLE_NAME = os.getenv("TABLE_NAME", "contracts")
PLOTS_DIR = Path(os.getenv("PLOTS_DIR", "/plots"))


import time

def load_data(retries=20, delay=1):
    last_error = None
    for _ in range(retries):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                tables = pd.read_sql_query(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    conn,
                    params=(TABLE_NAME,)
                )
                if not tables.empty:
                    return pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
        except Exception as e:
            last_error = e
        time.sleep(delay)
    raise last_error if last_error else RuntimeError("Table not found")


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()

    if "all_contract_price" in df.columns:
        prices = pd.to_numeric(df["all_contract_price"], errors="coerce").dropna()
        plt.figure(figsize=(10, 6))
        sns.histplot(prices, bins=20, kde=True)
        plt.title("Distribution of all_contract_price")
        plt.xlabel("Price")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "all_contract_price_distribution.png", dpi=150)
        plt.close()

    if "legal_entity_name" in df.columns:
        top_entities = df["legal_entity_name"].fillna("NULL").astype(str).value_counts().head(10)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_entities.values, y=top_entities.index, orient="h")
        plt.title("Top 10 legal_entity_name by count")
        plt.xlabel("Count")
        plt.ylabel("Legal entity")
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "top_legal_entities.png", dpi=150)
        plt.close()

    print(f"Plots saved to {PLOTS_DIR}")


if __name__ == "__main__":
    main()