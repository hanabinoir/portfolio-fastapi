from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from config import settings

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
        _client.admin.command("ping")
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
    coll = db[MONGO_COLLECTION_NAME]
    return coll

def close() -> None:
    """
    Close the MongoClient and clear cached references.
    """
    global _client, _db
    if _client is not None:
        _client.close()
        _client = None
        _db = None
