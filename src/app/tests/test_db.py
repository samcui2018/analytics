from app.db.healthcheck import db_healthcheck

def test_db_healthcheck():
    db_healthcheck()