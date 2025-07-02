from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl
from dotenv import load_dotenv, find_dotenv


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl                # ← nom unique (on n’en maintient qu’un)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FEATURE_X_ENABLED: bool = False
    LOG_LEVEL: str = "info"

    def __init__(self, **kwargs):
        load_dotenv(find_dotenv(), override=True)
        super().__init__(**kwargs)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # ───────────────
    #  Compatibilité
    # ───────────────
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:     # ← NEW
        """Retourne l’URL DB sous forme de chaîne pour SQLAlchemy."""
        return str(self.DATABASE_URL)

settings = Settings()
