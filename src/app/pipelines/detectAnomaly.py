import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg") # Use non-interactive backend for environments without display
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest
import io
import base64

def detect_anomalies():
    # Sample data
    df = pd.DataFrame({
        "day": range(1, 16),
        "sales": [102, 98, 105, 110, 97, 103, 101, 99, 104, 500, 96, 100, 102, 98, 95]
    })

    # Calculate mean and standard deviation
    mean_sales = df["sales"].mean()
    std_sales = df["sales"].std()

    # Calculate z-score
    df["z_score"] = (df["sales"] - mean_sales) / std_sales

    # Flag anomalies
    threshold = 2
    df["is_anomaly"] = df["z_score"].abs() > threshold

    print(df)

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df["day"], df["sales"], marker="o")
    plt.scatter(
        df[df["is_anomaly"]]["day"],
        df[df["is_anomaly"]]["sales"],
        s=100
    )
    plt.title("Daily Sales with Anomalies")
    plt.xlabel("Day")
    plt.ylabel("Sales")
    plt.grid(True)
    # plt.show()

    # Save graph to memory buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

     # Convert image to base64 string
    graph_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    # Using Isolation Forest
    df = pd.DataFrame({
    "sales": [102, 98, 105, 110, 97, 103, 101, 99, 104, 500, 96, 100, 102, 98, 95]
    })

    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomaly_flag"] = model.fit_predict(df[["sales"]])

    # -1 = anomaly, 1 = normal
    df["is_anomaly"] = df["anomaly_flag"] == -1

    print(df)
    return df, graph_base64
