from schemas.profile import ProfileUpdate
from repositories.profile_repo import get_profile, update_profile


def get_profile_data():
    """Retrieve the profile."""
    return get_profile()


def update_profile_data(updated_profile: ProfileUpdate):
    """Update the profile."""
    return update_profile(updated_profile)
