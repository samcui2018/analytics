import matplotlib.pyplot as plt
import reportlab.pdfgen.canvas as canvas
from reportlab.platypus import Image

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

def plot_sales(pivot):
    plt.figure(figsize=(10,6))

    # for product, group in df.groupby("ProductName"):
    #     plt.plot(
    #         group["Region"],
    #         group["Sales"],
    #         marker='o',
    #         label=product
    #     )
    pivot.plot(kind='bar', stacked=True, figsize=(10,6))

    plt.title("Sales by Region and Product")
    plt.xlabel("Region")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.legend(title="ProductName")

    plt.tight_layout()
    plt.savefig("sales_pivot.png")
    plt.show()

def create_pdf_with_image(image_path, pdf_path):
    c = canvas.Canvas(pdf_path)
    c.drawImage(image_path, 50, 500, width=500, height=300)  # Adjust position and size as needed
    c.save()    
   