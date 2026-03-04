import matplotlib.pyplot as plt

def plot_revenue_trends(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['RevenueMonth'], df['Revenue'], marker='o')
    plt.title('Monthly Revenue Trends')
    plt.xlabel('Month')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()