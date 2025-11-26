from fastapi import HTTPException
from db.mongodb import get_profiles_collection
from schemas.profile import ProfileIntroRequest


def get_profile_intro():
    """Fetch the profile intro document from MongoDB."""
    coll = get_profiles_collection()
    doc = coll.find_one({"type": "INTRO"})
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc


def update_profile_intro(updated_profile: ProfileIntroRequest):
    """Update the profile intro document in MongoDB."""
    coll = get_profiles_collection()
    data = updated_profile.model_dump(by_alias=True, exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = coll.update_one({"type": "INTRO"}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile updated successfully", "modified_count": result.modified_count}
