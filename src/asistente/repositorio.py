import hashlib
import json
import logging
import psycopg
import redis
from asistente.config import settings

logger = logging.getLogger(__name__)
_cache = redis.Redis.from_url(settings.redis_url, socket_timeout=1)

def _clave(sql: str, params: dict) -> str:
    raw = json.dumps({"sql": sql, "params": params}, sort_keys=True)
    return "consulta:" + hashlib.sha256(raw.encode()).hexdigest()

def ejecutar(sql: str, params: dict) -> float | None:
    clave = _clave(sql, params)
    try:
        hit = _cache.get(clave)
        if hit is not None:
            logger.info("cache_hit")
            return json.loads(hit)
    except redis.RedisError:
        logger.warning("cache_no_disponible")

    opciones = f"-c statement_timeout={settings.db_timeout_s * 1000} -c default_transaction_read_only=on"
    with psycopg.connect(settings.database_url,
                         connect_timeout=settings.db_timeout_s,
                         options=opciones) as conn:
        valor = conn.execute(sql, params).fetchone()[0]
    resultado = float(valor) if valor is not None else None

    try:
        _cache.set(clave, json.dumps(resultado), ex=settings.cache_ttl_s)
    except redis.RedisError:
        pass
    logger.info("cache_miss")
    return resultado
