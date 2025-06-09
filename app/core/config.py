from pydantic_settings import BaseSettings
from pydantic.networks import AnyUrl
import os
from dotenv import load_dotenv, find_dotenv


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FEATURE_X_ENABLED: bool = False
    LOG_LEVEL: str = "info"

    def __init__(self, **kwargs):
        load_dotenv(find_dotenv(), override=True)
        super().__init__(**kwargs)


settings = Settings()  # <== L’instance !
