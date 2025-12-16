from datetime import datetime
from typing import Any, List, Literal, Optional
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
        populate_by_name = True

        
class Company(BaseModel):
    name: str
    url: Optional[str] = None

class TechStack(BaseModel):
    languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    libraries: List[str] = Field(default_factory=list)
    platforms: List[str] = Field(default_factory=list)


class Timeline(BaseModel):
    started_at: datetime
    ended_at: Optional[datetime] = None


class ProjectBase(BaseModel):
    name: str
    description: str
    company: Optional[Company] = None
    timeline: Timeline
    tech_stack: TechStack

    class Config:
        populate_by_name = True