from asistente.consultas import a_sql
from asistente.modelos import PreguntaAnalisis

def test_filtra_por_pais_con_parametro():
    sql, params = a_sql(PreguntaAnalisis(metrica="sacos", pais="Alemania", mes=10, anio=2026))
    assert "pais = %(pais)s" in sql
    assert params["pais"] == "Alemania"
    assert "Alemania" not in sql

def test_ingresos_usa_columna_correcta():
    sql, _ = a_sql(PreguntaAnalisis(metrica="ingresos", mes=10, anio=2026))
    assert "SUM(ingresos_usd)" in sql
    assert "pais" not in sql
