import json
import os
import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd

DB_PATH = Path(os.getenv("DB_PATH", "/storage/data.db"))
TABLE_NAME = os.getenv("TABLE_NAME", "contracts")
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/reports"))

DATE_COLUMNS = [
    "contract_date",
    "contract_start_date",
    "contract_end_date",
    "last_update_contract",
]

NUMERIC_COLUMNS = [
    "package_contract_price",
    "all_contract_price",
    "contract_count_division_id",
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
        "missing_values": {},
        "duplicates": {},
        "date_checks": {},
        "numeric_checks": {},
    }

    for col in df.columns:
        report["missing_values"][col] = int(df[col].isna().sum())

    report["duplicates"]["all_rows"] = int(df.duplicated().sum())
    if "legal_entity_id" in df.columns:
        report["duplicates"]["legal_entity_id"] = int(df.duplicated(subset=["legal_entity_id"]).sum())
    if "contract_number" in df.columns:
        report["duplicates"]["contract_number"] = int(df.duplicated(subset=["contract_number"]).sum())

    for col in DATE_COLUMNS:
        if col in df.columns:
            parsed = pd.to_datetime(df[col], errors="coerce")
            invalid = int(parsed.isna().sum() - df[col].isna().sum())
            report["date_checks"][col] = {
                "invalid_dates": invalid,
                "non_null_values": int(df[col].notna().sum()),
            }

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            numeric = pd.to_numeric(df[col], errors="coerce")
            invalid = int(numeric.isna().sum() - df[col].isna().sum())
            report["numeric_checks"][col] = {
                "invalid_numbers": invalid,
                "min": None if numeric.dropna().empty else float(numeric.min()),
                "max": None if numeric.dropna().empty else float(numeric.max()),
            }

    json_path = REPORTS_DIR / "quality_report.json"
    txt_path = REPORTS_DIR / "quality_report.txt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("DATA QUALITY REPORT\n")
        f.write(f"Generated at: {report['generated_at']}\n")
        f.write(f"Rows: {report['rows']}\n\n")
        f.write("Missing values:\n")
        for k, v in report["missing_values"].items():
            f.write(f"- {k}: {v}\n")
        f.write("\nDuplicates:\n")
        for k, v in report["duplicates"].items():
            f.write(f"- {k}: {v}\n")
        f.write("\nDate checks:\n")
        for k, v in report["date_checks"].items():
            f.write(f"- {k}: invalid={v['invalid_dates']}, non_null={v['non_null_values']}\n")
        f.write("\nNumeric checks:\n")
        for k, v in report["numeric_checks"].items():
            f.write(f"- {k}: invalid={v['invalid_numbers']}, min={v['min']}, max={v['max']}\n")

    print(f"Quality report saved to {json_path} and {txt_path}")


if __name__ == "__main__":
    main()