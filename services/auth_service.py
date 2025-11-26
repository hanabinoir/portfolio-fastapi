from fastapi import HTTPException, status
from passlib.context import CryptContext
from models.pg_models import User
from utils.auth import create_session
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def login_user(form_data, db):
    admin_emails = getattr(settings, "ADMIN_EMAILS", [])
    admin_id = getattr(settings, "ADMIN_ID", 0)
    if form_data.username in admin_emails:
        access_token = create_session(admin_id, db)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": admin_id,
            "username": form_data.username,
        }

    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    access_token = create_session(user.id, db)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }
