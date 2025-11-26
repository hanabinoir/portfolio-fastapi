from fastapi import APIRouter, Depends
from models.mongo_models import ProfileIntro
from models.pg_models import User

from utils.auth import require_admin
from services.profile_service import get_profile, update_profile

router = APIRouter()


@router.get("/profile", response_model=ProfileIntro)
def read_profile():
    return get_profile()


@router.post("/profile/edit")
def edit_profile(updated_profile: ProfileIntro, admin_user: User = Depends(require_admin)):
    return update_profile(updated_profile)
