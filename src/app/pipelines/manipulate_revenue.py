import pandas as pd
from sqlalchemy import text
from app.db.engine import engine
from app.transformations.revenue_transform import (
    standardize_columns,
    remove_bad_rows,
    add_features,
    monthly_rollups,
)


def run():
    # engine = create_engine()

    # Read data (adjust table/schema as needed)
    df = pd.read_sql(
        text("SELECT * FROM dbo.revenue where year(RevenueMonth) > 2023"),
        engine,
    )

    print("Rows read:", len(df))
    print(df.head())

    # Manipulate
    df2 = standardize_columns(df)
    df2 = remove_bad_rows(df2)
    df2 = add_features(df2)

    # Example analytics output
    monthly = monthly_rollups(df2)

    print("\nCleaned + featured:")
    print(df2.head())

    print("\nMonthly rollups:")
    print(monthly.head(12))

    # Write results back
    df2.to_sql("stg_revenue_clean", engine, schema="dbo", if_exists="replace", index=False)
    monthly.to_sql("revenue_monthly_metrics", engine, schema="dbo", if_exists="replace", index=False)

    print("\nWrote tables: dbo.stg_revenue_clean, dbo.revenue_monthly_metrics")


if __name__ == "__main__":
    run()