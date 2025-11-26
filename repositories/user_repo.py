from sqlalchemy.orm import Session
from models.pg_models import User


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()
