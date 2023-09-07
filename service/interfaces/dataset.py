from pydantic import BaseModel
from typing import Literal

class InputDataRow(BaseModel):
    # Information about the flight at the time of programming
    flight_date_i: str
    flight_number_i: str
    city_code_from_i: str
    city_code_to_i: str
    airline_code_i: str
    
    # Information about the flight at the time of operation
    flight_date_o: str
    flight_number_o: str
    city_code_from_o: str
    city_code_to_o: str
    airline_code_o: str

    # More information about the flight at the time of operation
    day: int
    month: int
    year: int
    dayname: str
    flight_type: Literal['I', 'N']
    operator: str
    city_name_from: str
    city_name_to: str