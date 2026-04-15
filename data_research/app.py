import json
import os
import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd

DB_PATH = Path(os.getenv("DB_PATH", "/storage/data.db"))
TABLE_NAME = os.getenv("TABLE_NAME", "contracts")
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/reports"))

NUMERIC_COLUMNS = [
    "package_contract_price",
    "all_contract_price",
    "contract_count_division_id",
]

TEXT_COLUMNS = [
    "legal_entity_name",
    "package_id",
    "contract_divisions",
]



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

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "rows": int(len(df)),
        "columns": list(df.columns),
        "numeric_summary": {},
        "top_values": {},
    }

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            series = pd.to_numeric(df[col], errors="coerce")
            desc = series.describe()
            report["numeric_summary"][col] = {
                "count": int(desc.get("count", 0)),
                "mean": None if pd.isna(desc.get("mean")) else float(desc.get("mean")),
                "std": None if pd.isna(desc.get("std")) else float(desc.get("std")),
                "min": None if pd.isna(desc.get("min")) else float(desc.get("min")),
                "25%": None if pd.isna(desc.get("25%")) else float(desc.get("25%")),
                "50%": None if pd.isna(desc.get("50%")) else float(desc.get("50%")),
                "75%": None if pd.isna(desc.get("75%")) else float(desc.get("75%")),
                "max": None if pd.isna(desc.get("max")) else float(desc.get("max")),
            }

    for col in TEXT_COLUMNS:
        if col in df.columns:
            top = (
                df[col]
                .fillna("NULL")
                .astype(str)
                .value_counts()
                .head(10)
                .to_dict()
            )
            report["top_values"][col] = {str(k): int(v) for k, v in top.items()}

    json_path = REPORTS_DIR / "research_report.json"
    txt_path = REPORTS_DIR / "research_report.txt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("DATA RESEARCH REPORT\n")
        f.write(f"Generated at: {report['generated_at']}\n")
        f.write(f"Rows: {report['rows']}\n\n")
        f.write("Numeric summary:\n")
        for col, stats in report["numeric_summary"].items():
            f.write(f"- {col}:\n")
            for k, v in stats.items():
                f.write(f"  {k}: {v}\n")
        f.write("\nTop values:\n")
        for col, vals in report["top_values"].items():
            f.write(f"- {col}:\n")
            for k, v in vals.items():
                f.write(f"  {k}: {v}\n")

    print(f"Research report saved to {json_path} and {txt_path}")


if __name__ == "__main__":
    main()