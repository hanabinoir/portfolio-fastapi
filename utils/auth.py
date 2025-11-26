import secrets
import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone, timedelta
import pytz

from models.pg_models import Session, User
from db import pg_db
from config import settings

SESSION_DAYS = 14

def create_session(user_id: int, db):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS)
    session = Session(
        id=str(uuid.uuid4()),
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return token



security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(pg_db.get_db)
):
    token = credentials.credentials

    session = db.query(Session).filter_by(
        token=token,
        revoked=False
    ).first()

    if not session or pytz.utc.localize(session.expires_at) < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    ## Admin user handling
    user_id = session.user_id
    admin_id = getattr(settings, "ADMIN_ID", 0)
    if user_id == admin_id:
        return User(id=admin_id, username="admin", hashed_password="")

    ## Normal user handling
    user = session.user
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")

    return user

def require_admin(user: User = Depends(get_current_user)):
    ## Admin user check
    if user.username == "admin":
        return user

    ## Normal user check
    role_names = {role.name.lower() for role in user.roles}

    if "admin" not in role_names:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    return user
