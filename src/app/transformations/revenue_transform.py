import pandas as pd

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names + basic dtype coercion."""
    out = df.copy()
    # out.columns = [c.strip() for c in out.columns]
    out.columns = out.columns.str.strip()

    if "RevenueMonth" in out.columns:
        out["RevenueMonth"] = pd.to_datetime(out["RevenueMonth"], errors="coerce")

    if "Revenue" in out.columns:
        out["Revenue"] = pd.to_numeric(out["Revenue"], errors="coerce")

    return out

def remove_bad_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing key fields, keep data clean."""
    out = df.copy()

    required = [c for c in ["RevenueMonth", "Revenue"] if c in out.columns] 
    if required:
        out = out.dropna(subset=required)

    # Example: remove negative revenue if that doesn't make sense
    if "Revenue" in out.columns:
        out = out[out["Revenue"] >= 0] #“If the Revenue column exists, remove all rows where Revenue is negative.

    return out

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add helpful analytic columns."""
    out = df.copy()

    if "RevenueMonth" in out.columns:
        out["Year"] = out["RevenueMonth"].dt.year
        out["Month"] = out["RevenueMonth"].dt.month
        out["YearMonth"] = out["RevenueMonth"].dt.to_period("M").astype(str)

    if "Revenue" in out.columns:
        out["Revenue_k"] = out["Revenue"] / 1000.0

    return out
def monthly_rollups(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue by month, plus rolling metrics."""
    if not {"RevenueMonth", "Revenue"}.issubset(df.columns):
        raise ValueError("Expected columns: RevenueMonth, Revenue")

    out = df.copy()
    out = out.sort_values("RevenueMonth")

    # If multiple rows per month, aggregate first
    m = (
        out.groupby(pd.Grouper(key="RevenueMonth", freq="MS"), as_index=False)["Revenue"]
        .sum()
        .rename(columns={"RevenueMonth": "MonthStart"})
    )

    # Rolling 3-month sum/avg
    m["Revenue_3mo_sum"] = m["Revenue"].rolling(3, min_periods=1).sum()
    m["Revenue_3mo_avg"] = m["Revenue"].rolling(3, min_periods=1).mean()

    # Month-over-month growth (safe)
    m["Revenue_prev"] = m["Revenue"].shift(1)
    m["MoM_growth_pct"] = (m["Revenue"] - m["Revenue_prev"]) / m["Revenue_prev"]
    m.loc[m["Revenue_prev"].isna() | (m["Revenue_prev"] == 0), "MoM_growth_pct"] = pd.NA

    return m

