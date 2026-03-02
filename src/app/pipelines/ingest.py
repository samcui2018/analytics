import logging
import pandas as pd
from sqlalchemy import text
from app.db.engine import engine

log = logging.getLogger(__name__)

def ingest_merchants() -> int:
    # Example: read source table, write to staging
    query = "SELECT TOP 1000 * FROM dbo.Revenue"
    df = pd.read_sql(query, engine)

    # write to staging schema/table
    # df.to_sql("stg_revenue", engine, schema="dbo", if_exists="append", index=False)
    # log.info("Ingested %s rows into stg.stg_revenue", len(df))
    print (df.head())
    return len(df)