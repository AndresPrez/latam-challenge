from functools import wraps
from interfaces.dataset import InputDataRow

PARSER_MAP = {
    "Fecha-I": "flight_date_i",
    "Vlo-I": "flight_number_i",
    "Ori-I": "city_code_from_i",
    "Des-I": "city_code_to_i",
    "Emp-I": "airline_code_i",
    "Fecha-O": "flight_date_o",
    "Vlo-O": "flight_number_o",
    "Ori-O": "city_code_from_o",
    "Des-O": "city_code_to_o",
    "Emp-O": "airline_code_o",
    "DIA": "day",
    "MES": "month",
    "AÑO": "year",
    "DIANOM": "dayname",
    "TIPOVUELO": "flight_type",
    "OPERA": "operator",
    "SIGLAORI": "city_name_from",
    "SIGLADES": "city_name_to"
}

def parser(input: dict):
    parsed_input = { PARSER_MAP[key]: value for key, value in input.items() }
    return parsed_input
    