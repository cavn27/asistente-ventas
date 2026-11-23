import logging
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from asistente.consultas import a_sql
from asistente.modelos import PreguntaAnalisis
from asistente.repositorio import ejecutar

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)

app = FastAPI(title="Asistente de ventas", version="0.3.0")

class ConsultaGenerada(BaseModel):
    sql: str
    params: dict
    resultado: float | None

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/preguntas", response_model=ConsultaGenerada)
def crear_consulta(pregunta: PreguntaAnalisis) -> ConsultaGenerada:
    sql, params = a_sql(pregunta)
    try:
        resultado = ejecutar(sql, params)
    except psycopg.OperationalError:
        logger.exception("db_no_disponible")
        raise HTTPException(status_code=503, detail="Base de datos no disponible, reintenta en unos segundos")
    return ConsultaGenerada(sql=sql, params=params, resultado=resultado)
