import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

def seasonaldecomposite():
    # Sample monthly sales data
    data = {
        "date": pd.date_range(start="2024-01-01", periods=24, freq="ME"),
        "sales": [
            120, 135, 150, 170, 180, 200,
            210, 220, 210, 190, 170, 160,
            130, 145, 160, 180, 190, 210,
            220, 230, 220, 200, 180, 170
        ]
    }

    df = pd.DataFrame(data)
    df.set_index("date", inplace=True)

    # Perform seasonal decomposition
    result = seasonal_decompose(df["sales"], model="additive", period=12)

    # Plot components
    result.plot()
    plt.show()