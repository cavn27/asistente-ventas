from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:dev@localhost:5432/postgres"
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_s: int = 300
    db_timeout_s: int = 5

settings = Settings()
