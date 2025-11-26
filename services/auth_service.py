from fastapi import HTTPException, status
from config import settings
from repositories.user_repo import (
    get_user_by_username,
    verify_password,
    create_user_session,
)


def login_user(form_data, db):
    """Handle user login: check admin or query DB and verify password."""
    admin_emails = getattr(settings, "ADMIN_EMAILS", [])
    admin_id = getattr(settings, "ADMIN_ID", 0)
    
    # Check if admin login
    if form_data.username in admin_emails:
        access_token = create_user_session(admin_id, db)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": admin_id,
            "username": form_data.username,
        }

    # Regular user login
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    access_token = create_user_session(user.id, db)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }
