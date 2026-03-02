# src/app/contracts/revenue.py
from datetime import date
from pydantic import BaseModel, Field, ConfigDict

class StgRevenueRow(BaseModel):
    model_config = ConfigDict(extra="forbid")  # reject unknown columns

    RevenueMonth: date
    Revenue: float = Field(ge=0)  # example constraint