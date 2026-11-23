import logging
from fastapi import FastAPI
from pydantic import BaseModel
from asistente.consultas import a_sql
from asistente.modelos import PreguntaAnalisis

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Asistente de ventas", version="0.2.0")

class ConsultaGenerada(BaseModel):
    sql: str
    params: dict

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/preguntas", response_model=ConsultaGenerada)
def crear_consulta(pregunta: PreguntaAnalisis) -> ConsultaGenerada:
    sql, params = a_sql(pregunta)
    return ConsultaGenerada(sql=sql, params=params)
