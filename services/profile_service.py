from schemas.profile import ProfileIntroRequest
from repositories.profile_repo import get_profile_intro, update_profile_intro


def get_profile():
    """Retrieve the profile intro."""
    return get_profile_intro()


def update_profile(updated_profile: ProfileIntroRequest):
    """Update the profile intro."""
    return update_profile_intro(updated_profile)
