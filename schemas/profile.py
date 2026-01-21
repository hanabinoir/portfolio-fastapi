from typing import Annotated
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from models.mongo_models import ProfileIntroBase

PyObjectId = Annotated[str, BeforeValidator(str)]


class ProfileIntroUpdate(ProfileIntroBase):
    """Profile intro update request schema (excludes _id)."""

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Lorem Ipsum",
                "name_jp": "イロハニホヘト",
                "avatar_url": "https://example.com/avatar.png",
                "github_url": "https://github.com/user",
                "linkedin_url": "https://linkedin.com/in/user",
                "headlines": ["Position 1", "Position 2"],
                "skills": ["Skill 1", "Skill 2", "Skill 3"],
                "type": "INTRO",
            }
        }


class ProfileIntro(ProfileIntroBase):
    """Profile intro response schema."""
    id: PyObjectId = Field(alias="_id")

    class Config:
        json_schema_extra = {
            "example": {
                "_id": "691d7626fb1ba4c98abbf07e",
                "name": "Lorem Ipsum",
                "name_jp": "イロハニホヘト",
                "avatar_url": "https://example.com/avatar.png",
                "github_url": "https://github.com/user",
                "linkedin_url": "https://linkedin.com/in/user",
                "headlines": ["Assassin", "Wizard"],
                "skills": ["Skill 1", "Skill 2", "Skill 3"],
                "type": "INTRO",
            }
        }


class ProfileUpdateResponse(BaseModel):
    """Profile update response schema."""
    message: str
    modified_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Profile updated successfully",
                "modified_count": 1,
            }
        }
