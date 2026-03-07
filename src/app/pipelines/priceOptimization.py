import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def run_price_optimization():
    # Historical data
    df = pd.DataFrame({
        "price": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "competitor_price": [11, 11, 12, 12, 13, 14, 14, 15, 15, 16],
        "promotion": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        "seasonality_index": [0.9, 1.0, 1.1, 1.0, 1.2, 1.1, 1.0, 0.95, 0.9, 0.85],
        "marketing_spend": [1000, 1200, 1100, 1300, 1250, 1400, 1350, 1450, 1500, 1550],
        "units_sold": [1200, 1250, 1100, 1150, 980, 1020, 900, 930, 820, 850]
    })

    # Features and target
    X = df[["price", "competitor_price", "promotion", "seasonality_index", "marketing_spend"]]
    y = df["units_sold"]

    # Train demand model
    model = LinearRegression()
    model.fit(X, y)

    # Business assumptions for future scenario
    competitor_price = 15
    promotion = 1
    seasonality_index = 1.1
    marketing_spend = 1400
    unit_cost = 6

    # Try different candidate prices
    candidate_prices = np.arange(8, 22, 0.5)

    results = []

    for price in candidate_prices:
        features = pd.DataFrame({
            "price": [price],
            "competitor_price": [competitor_price],
            "promotion": [promotion],
            "seasonality_index": [seasonality_index],
            "marketing_spend": [marketing_spend]
        })

        predicted_units = model.predict(features)[0]
        predicted_units = max(predicted_units, 0)  # prevent negative demand

        revenue = price * predicted_units
        profit = (price - unit_cost) * predicted_units

        results.append({
            "price": price,
            "predicted_units": predicted_units,
            "revenue": revenue,
            "profit": profit
        })

    results_df = pd.DataFrame(results)

    # Best price for profit
    best_row = results_df.loc[results_df["profit"].idxmax()]

    print("Optimal price:")
    print(best_row)