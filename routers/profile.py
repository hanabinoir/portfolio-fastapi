from fastapi import APIRouter, Depends
from models.pg_models import User

from utils.auth import require_admin
from services.profile_service import get_profile_data, update_profile_data
from schemas.profile import Profile, ProfileUpdate, ProfileUpdateResponse

router = APIRouter()


@router.get("/profile", response_model=Profile)
def read_profile():
    """Fetch the profile."""
    return get_profile_data()


@router.post("/profile/edit", response_model=ProfileUpdateResponse)
def edit_profile(
    updated_profile: ProfileUpdate,
    admin_user: User = Depends(require_admin)
):
    """Update the profile. Requires admin privileges."""
    return update_profile_data(updated_profile)
