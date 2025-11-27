from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session as DBSession

from db import pg_db
from services.auth_service import login_user
from schemas.auth import LoginResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: DBSession = Depends(pg_db.get_db)
):
    """User login endpoint. Returns access token and user info."""
    return login_user(form_data, db)
