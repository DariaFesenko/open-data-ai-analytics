import os
import sqlite3
from pathlib import Path

import pandas as pd

DATA_PATH = Path(os.getenv("CSV_PATH", "/data/dataset.csv"))
DB_PATH = Path(os.getenv("DB_PATH", "/storage/data.db"))
TABLE_NAME = os.getenv("TABLE_NAME", "contracts")

DATE_COLUMNS = [
    "contract_date",
    "contract_start_date",
    "contract_end_date",
    "last_update_contract",
]


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {DATA_PATH}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        rows = cur.fetchone()[0]

    print(f"Loaded {rows} rows into {DB_PATH} table '{TABLE_NAME}'")


if __name__ == "__main__":
    main()