from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_DB_URL: str
    MONGO_DB_NAME: str
    MONGO_COLLECTION_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()