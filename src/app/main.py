from app.logging_config import configure_logging
from app.pipelines.ingest import ingest_merchants
from app.pipelines.transform import transform_merchants

def run():
    configure_logging()
    rows = ingest_merchants()
    transform_merchants()
    print(f"Done. Ingested rows: {rows}")

if __name__ == "__main__":
    run()