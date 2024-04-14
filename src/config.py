from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn

    class Config:
        env_file = ".env/.dev.env"


settings = Config()
