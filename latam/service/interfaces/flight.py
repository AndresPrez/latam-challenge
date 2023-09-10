from pydantic import BaseModel

class Flight(BaseModel):
    ["Fecha-I"]: str
    ["Vlo-I"]: str
    ["Ori-I"]: str
    ["Des-I"]: str
    ["Emp-I"]: str
    ["DIA"]: int
    ["MES"]: int
    ["AÑO"]: int
    ["TIPOVUELO"]: str
    ["OPERA"]: str
    ["SIGLAORI"]: str
    ["SIGLADES"]: str
    ["Temporada alta"]: bool
    ["Periodo día"]: str