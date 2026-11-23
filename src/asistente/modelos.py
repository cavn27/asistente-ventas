from typing import Literal
from pydantic import BaseModel, Field

class PreguntaAnalisis(BaseModel):
    metrica: Literal["sacos", "ingresos"]
    calidad: Literal["especial", "convencional", "organico"] | None = None
    pais: str | None = None
    mes: int = Field(ge=1, le=12)
    anio: int = Field(ge=2020)
