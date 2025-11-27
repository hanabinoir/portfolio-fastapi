from typing import Generator, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings

PG_DATABASE_URL = getattr(settings, "PG_DATABASE_URL")

_engine: Optional[object] = None
_SessionLocal: Optional[sessionmaker] = None


def connect():
    """Create SQLAlchemy engine and sessionmaker if not already created."""
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(PG_DATABASE_URL, pool_pre_ping=True)
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    return _engine


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a SQLAlchemy Session.

    Usage in routes: `db: Session = Depends(pg_db.get_db)`
    """
    global _SessionLocal
    if _SessionLocal is None:
        connect()
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def close() -> None:
    """Dispose the SQLAlchemy engine and clear sessionmaker."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
        _engine = None
        _SessionLocal = None
