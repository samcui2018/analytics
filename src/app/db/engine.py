from sqlalchemy import create_engine, event, text
from urllib.parse import quote_plus
from src.app.config import settings
import pandas as pd

def build_connection_url() -> str:
    driver = settings.sqlserver_driver
    host = settings.sqlserver_host
    db = settings.sqlserver_db

    trust = "yes" if settings.sqlserver_trust_cert else "no"

    if settings.sqlserver_auth.lower() == "windows":
        odbc = (
            f"DRIVER={{{driver}}};"
            f"SERVER={host};"
            f"DATABASE={db};"
            "Trusted_Connection=yes;"
            f"TrustServerCertificate={trust};"
        )
    else:
        if not settings.sqlserver_user or not settings.sqlserver_password:
            raise ValueError("SQL auth selected but SQLSERVER_USER/PASSWORD not set.")
        odbc = (
            f"DRIVER={{{driver}}};"
            f"SERVER={host};"
            f"DATABASE={db};"
            f"UID={settings.sqlserver_user};"
            f"PWD={settings.sqlserver_password};"
            f"TrustServerCertificate={trust};"
        )

    return "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc)

engine = create_engine(
    build_connection_url(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True,
)

@event.listens_for(engine, "before_cursor_execute")
def _configure_fast_executemany(conn, cursor, statement, parameters, context, executemany):
    if executemany:
        cursor.fast_executemany = True

CSV_PATH = r"C:\PythonIntel\TestData\jobs2026.csv"
TARGET_SCHEMA = "dbo"
TARGET_TABLE = "Jobs2026"


# ✅ Do NOT use index_col=0. Force pandas to keep all columns as columns.
df = pd.read_csv(CSV_PATH, dtype=str, index_col=False)

# Remove completely empty rows
df = df.dropna(how="all")

# Normalize headers
df.columns = df.columns.str.replace("\ufeff", "", regex=False).str.strip()

# ✅ Safety: if something still made the index non-default, reset it
if not isinstance(df.index, pd.RangeIndex):
    df = df.reset_index(drop=True)

# Only keep the columns you want to insert (DB fills Id + datetimestamp)
insert_cols = ["Position", "ApplicationDate", "Notes", "Source", "JobUrl"]

missing = [c for c in insert_cols if c not in df.columns]
if missing:
    raise ValueError(f"CSV is missing columns: {missing}. Found: {df.columns.tolist()}")

df_insert = df[insert_cols].replace({"": None})

# Optional: parse date
df_insert["ApplicationDate"] = pd.to_datetime(df_insert["ApplicationDate"], errors="coerce")

with engine.begin() as conn:
    conn.execute(text(f"TRUNCATE TABLE {TARGET_SCHEMA}.{TARGET_TABLE}"))
    df_insert.to_sql(
        name=TARGET_TABLE,
        schema=TARGET_SCHEMA,
        con=conn,
        if_exists="append",
        index=False,
        chunksize=10000,
        method="multi",
    )

print(f"Inserted {len(df_insert):,} rows into {TARGET_SCHEMA}.{TARGET_TABLE}")