import pandas as pd
from sqlalchemy import event

@event.listens_for(engine, "before_cursor_execute")
def _configure_fast_executemany(conn, cursor, statement, parameters, context, executemany):
    if executemany:
        cursor.fast_executemany = True

CSV_PATH = r"C:\PythonIntel\jobs2026.csv"
TARGET_SCHEMA = "dbo"
TARGET_TABLE = "Jobs2026"

df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
df.columns = [c.strip().replace(" ", "_").replace("-", "_") for c in df.columns]
df = df.replace({"": None})

with engine.begin() as conn:
    df.to_sql(
        TARGET_TABLE,
        schema=TARGET_SCHEMA,
        con=conn,
        if_exists="append",
        index=False,
        chunksize=10000,
        method="multi",
    )

print(f"Loaded {len(df):,} rows into {TARGET_SCHEMA}.{TARGET_TABLE}")