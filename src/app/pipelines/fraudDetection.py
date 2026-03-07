import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def run_fraud_detection_RandomForest():
    df = pd.DataFrame({
        "amount": [20, 150, 2000, 15, 5000, 35, 70, 3000, 45, 10000],
        "hour": [10, 14, 2, 11, 1, 15, 9, 3, 13, 0],
        "is_international": [0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        "is_new_merchant": [0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        "fraud": [0, 0, 1, 0, 1, 0, 0, 1, 0, 1]
    })

    X = df[["amount", "hour", "is_international", "is_new_merchant"]]
    y = df["fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

def run_fraud_detection_RuleBased():
    df = pd.DataFrame({
    "amount": [20, 150, 2000, 15, 5000],
    "hour": [10, 14, 2, 11, 1],
    "is_international": [0, 0, 1, 0, 1]
    })

    df["fraud_flag"] = (
        (df["amount"] > 3000) &
        (df["hour"] < 4) &
        (df["is_international"] == 1)
    )

    print(df)