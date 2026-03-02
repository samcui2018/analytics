from sqlalchemy import text
from app.db.engine import engine

def db_healthcheck() -> None:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        if conn.scalar(text("SELECT 1")) != 1:
            raise Exception("DB healthcheck failed: unexpected result")
        else:
            print("DB healthcheck passed")

# if __name__ == "__main__":
#     db_healthcheck()