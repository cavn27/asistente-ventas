import psycopg
from fastapi.testclient import TestClient
from asistente import api

client = TestClient(api.app)
VALIDA = {"metrica": "sacos", "pais": "Alemania", "mes": 10, "anio": 2026}

def test_health():
    assert client.get("/health").status_code == 200

def test_pregunta_valida_devuelve_resultado(monkeypatch):
    monkeypatch.setattr(api, "ejecutar", lambda sql, params: 1234.0)
    r = client.post("/preguntas", json=VALIDA)
    assert r.status_code == 200
    assert r.json()["resultado"] == 1234.0

def test_pregunta_invalida_devuelve_422():
    r = client.post("/preguntas", json={**VALIDA, "mes": 13})
    assert r.status_code == 422

def test_db_caida_devuelve_503(monkeypatch):
    def falla(sql, params):
        raise psycopg.OperationalError("sin conexión")
    monkeypatch.setattr(api, "ejecutar", falla)
    assert client.post("/preguntas", json=VALIDA).status_code == 503
