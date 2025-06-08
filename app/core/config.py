# backend/app/core/config.py

from pydantic_settings import BaseSettings
from pydantic.networks import AnyUrl
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    # indique à Pydantic de lire le fichier .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # --- Base de données ---
    DATABASE_URL: AnyUrl

    # --- Sécurité / JWT ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- Feature flags (exemple) ---
    FEATURE_X_ENABLED: bool = False

    # --- Log Niveau ou autre config éventuelle ---
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
