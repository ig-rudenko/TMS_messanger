from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class _Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_hours: int = 24

    redis_url: str = 'redis://localhost:6379'
    redis_max_connections: int = 5

    broadcast_redis_url: str = 'redis://localhost:6379'
    broadcast_redis_max_connections: int = 5
    broadcast_type: str = 'local'  # 'redis', 'local', 'rabbitmq', 'kafka'


settings = _Settings()
