import pandas as pd

def load_jobs_from_csv(db_engine, csv_path: str, schema="dbo", table="Jobs2026"):
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False, index_col=False)

    # Clean headers
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    # If Position somehow became the index, bring it back as a column
    if df.index.name == "Position":
        df = df.reset_index()

    # If the first visible values are in the index, also force-reset
    if "Position" not in df.columns:
        df = df.reset_index()

    # After reset_index(), pandas may create a column named "index"
    # If that index column is actually your Position data, rename it.
    if "Position" not in df.columns and "index" in df.columns:
        df = df.rename(columns={"index": "Position"})

    # Keep only the columns you want
    insert_cols = ["Position", "ApplicationDate", "Notes", "Source", "JobUrl"]

    missing = [c for c in insert_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}. Found: {df.columns.tolist()}")

    df = df[insert_cols].copy()

    # Replace empty strings with NULL
    df = df.replace({"": None})

    # Convert date safely
    df["ApplicationDate"] = pd.to_datetime(
        df["ApplicationDate"],
        format="%m/%d/%Y",
        errors="coerce"
    )

    # Drop fully empty rows
    df = df.dropna(how="all")

    # Drop rows with no Position
    df = df.dropna(subset=["Position"])

    print("Final columns:", df.columns.tolist())
    print(df.head())

    with db_engine.begin() as conn:
        existing = pd.read_sql(
            text(f"SELECT Position FROM {schema}.{table}"),
            conn
        )

        if not existing.empty:
            existing_positions = set(existing["Position"].astype(str).str.strip())

            # Remove rows already in DB
            df = df[~df["Position"].astype(str).str.strip().isin(existing_positions)]

        if len(df) == 0:
            print("No new rows to insert.")
            return
        df.to_sql(
            name=table,
            schema=schema,
            con=conn,
            if_exists="append",
            index=False,
            chunksize=10000,
            method="multi",
        )

    print(f"Loaded {len(df):,} rows into {schema}.{table}")