from fastapi import APIRouter, Depends
from models.pg_models import User

from utils.auth import require_admin
from services.profile_service import get_profile, update_profile
from schemas.profile import ProfileIntroResponse, ProfileIntroRequest, ProfileUpdateResponse

router = APIRouter()


@router.get("/profile", response_model=ProfileIntroResponse)
def read_profile():
    """Fetch the profile intro."""
    return get_profile()


@router.post("/profile/edit", response_model=ProfileUpdateResponse)
def edit_profile(
    updated_profile: ProfileIntroRequest,
    admin_user: User = Depends(require_admin)
):
    """Update the profile intro. Requires admin privileges."""
    return update_profile(updated_profile)
