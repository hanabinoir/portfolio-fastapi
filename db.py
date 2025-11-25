from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from config import settings

# /mnt/d/Lab/portfolio-fastapi/db.py

MONGO_DB_URL = getattr(settings, "MONGO_DB_URL")
MONGO_DB_NAME = getattr(settings, "MONGO_DB_NAME")
MONGO_COLLECTION_NAME = getattr(settings, "MONGO_COLLECTION_NAME")
    

_client: Optional[MongoClient] = None
_db: Optional[Database] = None

def connect() -> MongoClient:
    """
    Create a MongoClient if not already created and verify the connection.
    """
    global _client, _db
    if _client is None:
        _client = MongoClient(MONGO_DB_URL, serverSelectionTimeoutMS=5000)
        # quick ping to raise early if connection fails
        _client.admin.command("ping")
        # prefer DB embedded in the URL, otherwise use MONGO_DB_NAME
        try:
            _db = _client.get_default_database()
        except Exception:
            _db = _client[MONGO_DB_NAME] if MONGO_DB_NAME else None
    return _client

def get_database() -> Database:
    """
    Return the Database instance. Raises RuntimeError if DB name is not available.
    """
    if _db is None:
        connect()
    if _db is None:
        raise RuntimeError("MongoDB database not configured. Set MONGO_DB_NAME or include DB in MONGO_DB_URL.")
    return _db

def get_profiles_collection() -> Collection:
    """
    Return the 'profiles' collection from the configured database.
    """
    db = get_database()
    return db[MONGO_COLLECTION_NAME]

def close() -> None:
    """
    Close the MongoClient and clear cached references.
    """
    global _client, _db
    if _client is not None:
        _client.close()
        _client = None
        _db = None

# Optional small helper to attach to a FastAPI app:
def attach_fastapi_events(app):
    @app.on_event("startup")
    def _startup():
        connect()

    @app.on_event("shutdown")
    def _shutdown():
        close()

    return app