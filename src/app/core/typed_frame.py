# src/app/core/typed_frame.py
from dataclasses import dataclass
from typing import Generic, TypeVar, Type
import pandas as pd
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

@dataclass(frozen=True)
class TypedFrame(Generic[T]):
    model: Type[T]
    df: pd.DataFrame