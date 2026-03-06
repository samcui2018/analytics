import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def run_clustering() -> pd.DataFrame:
    # Sample dataset
    data = {
        "income": [30, 35, 40, 80, 85, 90, 25, 27, 100, 105],
        "spending_score": [40, 42, 45, 80, 82, 85, 38, 36, 90, 95]
    }

    df = pd.DataFrame(data)

    # Select features
    X = df[["income", "spending_score"]]

    # Create clustering model
    kmeans = KMeans(n_clusters=3, random_state=42)

    # Fit model
    df["cluster"] = kmeans.fit_predict(X)

    print(df)
    return df, kmeans

def plot_clusters(df):
    plt.scatter(df["income"], df["spending_score"], c=df["cluster"])

    plt.xlabel("Income")
    plt.ylabel("Spending Score")
    plt.title("Customer Segmentation")

    plt.show()

def plot_cluster_centers(df, kmeans):
    plt.scatter(df["income"], df["spending_score"], c=df["cluster"])
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c="red", marker="x", s=200, label="Cluster Centers")
    plt.xlabel("Income")
    plt.ylabel("Spending Score")
    plt.title("Customer Segmentation with Cluster Centers")
    plt.legend()
    plt.grid(True)
    plt.show()