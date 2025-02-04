from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    CHROMA_PATH: str = "chroma"
    TEMP_UPLOAD_DIR: str = "temp_uploads"
    MAX_FILE_SIZE: int = 25_000_000
    ALLOWED_FILE_TYPES: list = ['.pdf']
    DEFAULT_MODEL: str = "llama3.2"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = AppSettings()
