from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_DB_URL: str
    MONGO_DB_NAME: str
    MONGO_COLLECTION_NAME: str
    PG_DATABASE_URL: str
    ADMIN_EMAILS: list[str]
    ADMIN_ID: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()