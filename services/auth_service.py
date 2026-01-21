from fastapi import HTTPException, status
from repositories.user_repo import (
    get_user_by_username,
    verify_password,
    create_user_session,
    create_user as repo_create_user,
    assign_user_role,
    get_user_count,
    get_roles,
)
from utils.role import RoleName


def login_user(form_data, db):
    # Regular user login
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    # (No change to token creation for DB-based admins; they receive a normal session)
    access_token = create_user_session(user.id, db)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }


def create_user(form_data, db):
    """Create a new user and return CreateUserResponse-like dict.

    `form_data` is expected to have `username` and `password` attributes (OAuth2PasswordRequestForm).
    """
    # Check for existing user
    if get_user_by_username(db, form_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    # Determine if this will be the first user (count existing users before creating)
    is_first_user = get_user_count(db) == 0

    # If first user, ensure admin role already exists
    roles = get_roles(db)
    admin_role = next((role for role in roles if role.name == RoleName.ADMIN), None)
    if is_first_user and not admin_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ADMIN role not created",
        )

    # Create user
    user = repo_create_user(db, form_data.username, form_data.password)

    # Assign role
    user_role = next((role for role in roles if role.name == RoleName.USER), None)
    role_id = user_role.id if not is_first_user else admin_role.id
    assign_user_role(db, user.id, role_id)

    # Create session token
    access_token = create_user_session(user.id, db)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }
