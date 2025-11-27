from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.pg_models import User
from utils.auth import create_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str) -> User | None:
    """Fetch a user by username."""
    return db.query(User).filter(User.username == username).first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_user_session(user_id: int, db: Session) -> str:
    """Create and return a session token for a user."""
    return create_session(user_id, db)
