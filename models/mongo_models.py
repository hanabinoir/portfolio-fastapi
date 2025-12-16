from typing import List, Literal
from pydantic import BaseModel, Field


class ProfileIntroBase(BaseModel):
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

        