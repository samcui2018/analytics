#from sklearn.cluster import KMeans

from src.app.db.engine import engine
from src.app.logging_config import configure_logging
from src.app.pipelines.ingest import ingest_merchants
from src.app.pipelines.transform import call_sp
from src.app.pipelines.manipulate_revenue import run as manipulate_revenue
from src.app.pipelines.CSVProcessing import load_jobs_from_csv
from src.app.pipelines.pivottable import run_pivot
from src.app.graphs.graph import create_pdf_with_image
from src.app.pipelines.statModelling import run_stat_modelling
from src.app.pipelines.detectAnomaly import detect_anomalies
from src.app.pipelines.clustering import run_clustering, plot_cluster_centers, plot_clusters
from src.app.pipelines.seasonalDecomposition import seasonaldecomposite
from src.app.pipelines.priceOptimization import run_price_optimization
from src.app.pipelines.fraudDetection import run_fraud_detection_RandomForest, run_fraud_detection_RuleBased
from src.app.pipelines.CustomerChurnPrediction import Customer_Churn_Prediction
def run():
    configure_logging()
    
    # rows = ingest_merchants()
    # print(f"Done. Ingested rows: {rows}")
    # call_sp()
    # csv_path = r"C:\PythonIntel\TestData\jobs2026.csv"
    # print(f"Loading jobs from CSV: {csv_path}")
    # print(type(engine))
    # load_jobs_from_csv(engine, csv_path)
    # manipulate_revenue()
  
    # run_pivot()
    # create_pdf_with_image("sales_pivot.png", "sales_report.pdf")
    #run_stat_modelling()
    #detect_anomalies()
    #df, kmeans = run_clustering()
    # plot_clusters(df)
    #plot_cluster_centers(df, kmeans)
    #seasonaldecomposite()
    #run_price_optimization()
    #run_fraud_detection_RuleBased()
    Customer_Churn_Prediction()

if __name__ == "__main__":
    run()