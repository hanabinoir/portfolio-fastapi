from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_DB_URL: str
    MONGO_DB_NAME: str = "stg"
    MONGO_COLL_PROFILES: str = "profiles"
    MONGO_COLL_PROJECTS: str = "projects"
    PG_DATABASE_URL: str
    ADMIN_EMAILS: list[str]
    ADMIN_ID: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()