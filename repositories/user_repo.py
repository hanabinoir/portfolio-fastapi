from sqlalchemy.orm import Session
import bcrypt
from models.pg_models import User
from utils.auth import create_session


def get_user_by_username(db: Session, username: str) -> User | None:
    """Fetch a user by username."""
    return db.query(User).filter(User.username == username).first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


def create_user_session(user_id: int, db: Session) -> str:
    """Create and return a session token for a user."""
    return create_session(user_id, db)


def create_user(db: Session, username: str, password: str) -> User:
    """Create a new user with `username` and plain `password` (hashed).

    Returns the newly created User model.
    """
    password_bytes = password.encode('utf-8')[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    user = User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_count(db: Session) -> int:
    """Return the total number of users in the database."""
    return db.query(User).count()


def get_roles(db: Session):
    """Return a Role by its name, or None if not found."""
    from models.pg_models import Role

    return db.query(Role).all()


def assign_user_role(db: Session, user_id: int, role_id: int) -> None:
    """Associate an existing role (by id) to a user. Raises if role does not exist."""
    from models.pg_models import Role, UserRole

    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        # Caller should validate existence; raise to avoid creating a phantom association
        raise ValueError("role not found")

    # Create association if not exists
    exists = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role.id,
    ).first()
    if not exists:
        user_role = UserRole(user_id=user_id, role_id=role.id)
        db.add(user_role)
        db.commit()
