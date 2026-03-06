import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def run_stat_modelling():
    # Sample data - replace with actual data loading
    data = {
        'Revenue': [100, 150, 200, 250, 300],
        'AdSpend': [10, 15, 20, 25, 30],
        'Seasonality': [1, 0, 1, 0, 1]
    }
    df = pd.DataFrame(data)

    # Define dependent and independent variables
    X = df[['AdSpend', 'Seasonality']]
    y = df['Revenue']

    # Add constant to the model (intercept)
    X = sm.add_constant(X)

    # Fit the OLS regression model
    model = sm.OLS(y, X).fit()

    # Print the summary of the regression results
    print(model.summary())

    # Plotting the results
    plt.scatter(df['AdSpend'], df['Revenue'], label='Data Points')
    plt.plot(df['AdSpend'], model.predict(X), color='red', label='Fitted Line')
    plt.xlabel('Ad Spend')
    plt.ylabel('Revenue')
    plt.title('Revenue vs Ad Spend')
    plt.legend()
    plt.show()