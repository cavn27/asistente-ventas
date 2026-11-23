from fastapi.testclient import TestClient
from asistente.api import app

client = TestClient(app)

def test_health():
    assert client.get("/health").status_code == 200

def test_pregunta_valida_devuelve_sql():
    r = client.post("/preguntas", json={"metrica": "sacos", "pais": "Alemania", "mes": 10, "anio": 2026})
    assert r.status_code == 200
    assert r.json()["params"]["pais"] == "Alemania"

def test_pregunta_invalida_devuelve_422():
    r = client.post("/preguntas", json={"metrica": "sacos", "mes": 13, "anio": 2026})
    assert r.status_code == 422
