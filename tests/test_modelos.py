import pytest
from pydantic import ValidationError
from asistente.modelos import PreguntaAnalisis

def test_pregunta_valida():
    p = PreguntaAnalisis(metrica="sacos", mes=10, anio=2026)
    assert p.pais is None

@pytest.mark.parametrize("campos", [
    {"metrica": "sacos", "mes": 13, "anio": 2026},
    {"metrica": "toneladas", "mes": 10, "anio": 2026},
    {"metrica": "sacos", "mes": 10, "anio": 2019},
])
def test_pregunta_invalida(campos):
    with pytest.raises(ValidationError):
        PreguntaAnalisis(**campos)
