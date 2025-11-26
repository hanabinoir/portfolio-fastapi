from fastapi import HTTPException, status
from db.mongodb import get_profiles_collection
from models.mongo_models import ProfileIntro


def get_profile():
    coll = get_profiles_collection()
    doc = coll.find_one({"type": "INTRO"})
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc


def update_profile(updated_profile: ProfileIntro):
    coll = get_profiles_collection()
    data = updated_profile.model_dump(by_alias=True, exclude_unset=True)
    data.pop("_id", None)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = coll.update_one({"type": "INTRO"}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile updated successfully", "modified_count": result.modified_count}
