import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def Customer_Churn_Prediction():
    # -----------------------------
    # 1. Create sample dataset
    # -----------------------------
    data = {
        "tenure": [1, 5, 12, 24, 36, 48, 60, 3, 8, 15, 2, 20, 40, 7, 18, 30, 50, 4, 10, 22],
        "monthly_charges": [70, 65, 80, 90, 85, 75, 60, 95, 88, 72, 99, 78, 68, 92, 76, 82, 64, 97, 89, 74],
        "support_calls": [5, 3, 2, 1, 1, 0, 0, 6, 4, 2, 7, 2, 1, 5, 3, 1, 0, 6, 4, 2],
        "contract": [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],  # 0 = month-to-month, 1 = contract
        "usage_frequency": [2, 3, 6, 8, 9, 10, 11, 1, 3, 6, 1, 7, 9, 2, 6, 8, 10, 1, 3, 7],
        "payment_failures": [2, 1, 0, 0, 0, 0, 0, 3, 1, 0, 4, 0, 0, 2, 1, 0, 0, 3, 1, 0],
        "churn": [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0]
    }

    df = pd.DataFrame(data)

    # -----------------------------
    # 2. Define features and target
    # -----------------------------
    X = df[[
        "tenure",
        "monthly_charges",
        "support_calls",
        "contract",
        "usage_frequency",
        "payment_failures"
    ]]
    y = df["churn"]

    # -----------------------------
    # 3. Split into training/testing
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    # -----------------------------
    # 4. Train Random Forest model
    # -----------------------------
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=42
    )

    model.fit(X_train, y_train)

    # -----------------------------
    # 5. Make predictions
    # -----------------------------
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # -----------------------------
    # 6. Evaluate model
    # -----------------------------
    print("Accuracy:")
    print(accuracy_score(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # -----------------------------
    # 7. Show prediction probabilities
    # -----------------------------
    results = X_test.copy()
    results["actual_churn"] = y_test.values
    results["predicted_churn"] = y_pred
    results["churn_probability"] = y_prob

    print("\nTest Predictions:")
    print(results)

    # -----------------------------
    # 8. Predict for a new customer
    # -----------------------------
    new_customer = pd.DataFrame({
        "tenure": [2],
        "monthly_charges": [95],
        "support_calls": [5],
        "contract": [0],
        "usage_frequency": [2],
        "payment_failures": [2]
    })

    new_prediction = model.predict(new_customer)[0]
    new_probability = model.predict_proba(new_customer)[0][1]

    print("\nNew Customer Prediction:")
    print("Predicted Churn:", new_prediction)  # 1 = churn, 0 = stay
    print("Churn Probability:", round(new_probability, 4))

    # -----------------------------
    # 9. Feature importance
    # -----------------------------
    feature_importance = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    print("\nFeature Importance:")
    print(feature_importance)