# src/app/transforms/revenue.py
import pandas as pd
from src.app.contracts.revenue import StgRevenueRow
from src.app.core.typed_frame import TypedFrame
from src.app.core.validate import validate_df

def standardize_revenue(frame: TypedFrame[StgRevenueRow]) -> TypedFrame[StgRevenueRow]:
    df = frame.df.copy()
    df["RevenueMonth"] = pd.to_datetime(df["RevenueMonth"], errors="coerce").dt.date
    df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
    validate_df(df, StgRevenueRow)
    return TypedFrame(StgRevenueRow, df)