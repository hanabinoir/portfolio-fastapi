from pydantic import BaseModel, Field
from typing import Optional

from models.mongo_models import ProjectBase, Company, Timeline
from .profile import PyObjectId


class ProjectListItem(ProjectBase):
    """
    Schema for items in the project list response.
    Endpoint: /projects
    """
    id: PyObjectId = Field(alias="_id")

    class Config:
        from_attributes = True
        populate_by_name = True


class ProjectDetail(ProjectBase):
    """
    Schema for the detailed project response.
    Endpoint: /projects/{id}
    """
    id: PyObjectId = Field(alias="_id")

    class Config:
        from_attributes = True
        populate_by_name = True


class ProjectUpdate(ProjectBase):
    """
    Schema for updating a project.
    Endpoint: PUT /projects/{id}
    """
    pass
