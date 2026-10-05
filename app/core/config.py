from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    UPLOAD_DIR: str = "uploads"

    model_config = ConfigDict(env_file=".env")


settings = Settings()