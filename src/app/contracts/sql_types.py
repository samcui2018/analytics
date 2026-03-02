# src/app/contracts/sql_types.py
from sqlalchemy import Date, Float

SQLALCHEMY_TYPES = {
    "RevenueMonth": Date(),
    "Revenue": Float(precision=53),
}