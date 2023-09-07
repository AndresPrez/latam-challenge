from pydantic import BaseModel
from typing import Literal

class Flight(BaseModel):
    flight_code: str