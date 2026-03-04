import logging
from sqlalchemy import text
from src.app.db.engine import engine

log = logging.getLogger(__name__)

def call_sp() -> None:
    with engine.begin() as conn:
        # conn.execute(text(sql))
        result = conn.execute(text("EXEC spJobGet"))
        rows = result.fetchall()
        print(rows)
    log.info("running spJobGet")
# IF OBJECT_ID('cur.dim_merchant', 'U') IS NULL
#     BEGIN
        #     SELECT DISTINCT
    #         MerchantId,
    #         MerchantName,
    #         CreatedDate
    #     INTO cur.dim_merchant
    #     FROM stg.stg_merchants;
    # END
    # ELSE
    # BEGIN
    #     -- basic upsert example (replace with MERGE pattern you prefer)
    #     TRUNCATE TABLE cur.dim_merchant;
    #     INSERT INTO cur.dim_merchant (MerchantId, MerchantName, CreatedDate)
    #     SELECT DISTINCT MerchantId, MerchantName, CreatedDate
    #     FROM stg.stg_merchants;
    # END