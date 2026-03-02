# src/app/core/validate.py
from typing import Type
import pandas as pd
from pydantic import BaseModel, ValidationError

def validate_df(df: pd.DataFrame, model: Type[BaseModel], sample: int = 200) -> None:
    # validate a sample for speed; increase for high-stakes loads
    s = df.head(sample).to_dict(orient="records")
    errors = []
    for i, row in enumerate(s):
        try:
            model.model_validate(row)
        except ValidationError as e:
            errors.append((i, e))
    if errors:
        # raise with useful context
        i, e = errors[0]
        raise ValueError(f"Schema validation failed at row {i}: {e}") from e