from sqlalchemy import create_engine
from urllib.parse import quote_plus
from app.config import settings

def build_connection_url() -> str:
    driver = settings.sqlserver_driver
    host = settings.sqlserver_host
    db = settings.sqlserver_db

    trust = "yes" if settings.sqlserver_trust_cert else "no"

    if settings.sqlserver_auth.lower() == "windows":
        odbc = (
            f"DRIVER={{{driver}}};"
            f"SERVER={host};"
            f"DATABASE={db};"
            "Trusted_Connection=yes;"
            f"TrustServerCertificate={trust};"
        )
    else:
        if not settings.sqlserver_user or not settings.sqlserver_password:
            raise ValueError("SQL auth selected but SQLSERVER_USER/PASSWORD not set.")
        odbc = (
            f"DRIVER={{{driver}}};"
            f"SERVER={host};"
            f"DATABASE={db};"
            f"UID={settings.sqlserver_user};"
            f"PWD={settings.sqlserver_password};"
            f"TrustServerCertificate={trust};"
        )

    return "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc)

engine = create_engine(
    build_connection_url(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True,
)