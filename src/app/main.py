from src.app.logging_config import configure_logging
from src.app.pipelines.ingest import ingest_merchants
from src.app.pipelines.transform import call_sp
from src.app.pipelines.manipulate_revenue import run as manipulate_revenue


def run():
    configure_logging()
    rows = ingest_merchants()
    print(f"Done. Ingested rows: {rows}")
    call_sp()
    manipulate_revenue()
    
if __name__ == "__main__":
    run()