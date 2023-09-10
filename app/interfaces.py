from datetime import datetime
from pydantic import BaseModel, Field

FIELD_MAP = {
    "Fecha_I": "Fecha-I",
    "Vlo_I": "Vlo-I",
    "Ori_I": "Ori-I",
    "Des_I": "Des-I",
    "Emp_I": "Emp-I",
    "ANO": "AÑO"
}

class Flight(BaseModel):
    Fecha_I: datetime = Field(alias="Fecha-I")
    Vlo_I: str = Field(alias="Vlo-I")
    Ori_I: str = Field(alias="Ori-I")
    Des_I: str = Field(alias="Des-I")
    Emp_I: str = Field(alias="Emp-I")
    DIA: int
    MES: int
    ANO: int = Field(alias="AÑO")
    TIPOVUELO: str
    OPERA: str
    SIGLAORI: str
    SIGLADES: str