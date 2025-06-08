# backend/app/core/config.py

from pydantic_settings import BaseSettings
from pydantic.networks import AnyUrl
import os
from app.core.config import Settings



class Settings(BaseSettings):
    """
    Charge un fichier .env à l'instanciation (override des env vars existantes),
    puis laisse Pydantic lire les env vars (qui viennent du .env si présent).
    """

    DATABASE_URL: AnyUrl
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FEATURE_X_ENABLED: bool = False
    LOG_LEVEL: str = "info"

    def __init__(self, **kwargs):
        # Recharge le .env **après** le cwd ait été modifié (monkeypatch.chdir)
        from dotenv import load_dotenv, find_dotenv

        # find_dotenv() cherche un .env à partir du cwd courant
        load_dotenv(find_dotenv(), override=True)
        super().__init__(**kwargs)


# Remarquez qu'on n'instancie plus globalement ici :
# settings = Settings()
