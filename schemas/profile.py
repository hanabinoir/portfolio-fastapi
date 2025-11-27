from typing import List, Optional, Literal, Annotated
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class ProfileIntroRequest(BaseModel):
    """Profile intro update request schema (excludes _id)."""
    name: Optional[str] = None
    name_jp: Optional[str] = None
    avatar_url: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    headlines: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Vincent Shum",
                "name_jp": "シミズ　ヒロシ",
                "avatar_url": "https://example.com/avatar.png",
                "github_url": "https://github.com/user",
                "linkedin_url": "https://linkedin.com/in/user",
                "headlines": ["Mobile Developer", "Web Developer"],
                "skills": ["Kotlin", "Swift", "JavaScript"],
            }
        }


class ProfileIntroResponse(BaseModel):
    """Profile intro response schema."""
    id: PyObjectId = Field(alias="_id")
    name: str
    name_jp: str
    avatar_url: str
    github_url: str
    linkedin_url: str
    headlines: List[str]
    skills: List[str]
    type: Literal["INTRO"] = "INTRO"

    class Config:
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "691d7626fb1ba4c98abbf07e",
                "name": "Vincent Shum",
                "name_jp": "シミズ　ヒロシ",
                "avatar_url": "https://res.cloudinary.com/hanabinoir/image/upload/v1763521930/portfolio/profile_avatar_cyber_punk_jgox1y.png",
                "github_url": "https://github.com/hanabinoir",
                "linkedin_url": "https://linkedin.com/in/vincent",
                "headlines": ["Mobile Developer", "Web Developer"],
                "skills": ["Kotlin", "Swift", "JavaScript", "Jetpack Compose", "SwiftUI"],
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
