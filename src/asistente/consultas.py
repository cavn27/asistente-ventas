import logging
from asistente.modelos import PreguntaAnalisis

logger = logging.getLogger(__name__)

COLUMNAS = {"sacos": "sacos", "ingresos": "ingresos_usd"}

def a_sql(p: PreguntaAnalisis) -> tuple[str, dict]:
    sql = f"SELECT SUM({COLUMNAS[p.metrica]}) FROM ventas WHERE anio = %(anio)s AND mes = %(mes)s"
    params: dict = {"anio": p.anio, "mes": p.mes}
    if p.calidad:
        sql += " AND calidad = %(calidad)s"
        params["calidad"] = p.calidad
    if p.pais:
        sql += " AND pais = %(pais)s"
        params["pais"] = p.pais
    logger.info("consulta_generada metrica=%s filtros=%s", p.metrica, sorted(params))
    return sql, params
