import pandas as pd
from sqlalchemy import text
from src.app.db.engine import engine
from src.app.graphs.graph import plot_sales

def run_pivot():
    df = pd.read_sql(text("SELECT * FROM dbo.sales"), engine)
    print(df.head())
    pivot = df.pivot_table(
        values="Sales",
        index="Region",
        columns="ProductName",
        # aggfunc=["sum", "mean"],
        aggfunc=["sum"],
        fill_value=0,
        margins=True,
        margins_name="Total"
        )
    print(pivot.head())
    plot_sales(pivot)