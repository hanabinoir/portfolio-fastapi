from typing import Annotated, List, Literal
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class ProfileIntro(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    name_jp: str
    avatar_url: str
    github_url: str
    linkedin_url: str
    headlines: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    type: Literal["INTRO"] = "INTRO"

    class Config:
        validate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "691d7626fb1ba4c98abbf07e",
                "name": "Vincent Shum",
                "name_jp": "シミズ　ヒロシ",
                "avatar_url": "https://res.cloudinary.com/hanabinoir/image/upload/v1763521930/portfolio/profile_avatar_cyber_punk_jgox1y.png",
                "headlines": ["Mobile Developer", "Web Developer"],
                "skills": ["Kotlin", "Swift", "JavaScript", "Jetpack Compose", "SwiftUI"],
                "type": "INTRO",
            }
        }

        