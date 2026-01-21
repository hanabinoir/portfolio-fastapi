from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from models.pg_models import User
from services import project_service
from schemas.project import ProjectListItem, ProjectDetail, ProjectUpdate
from schemas.profile import ProfileUpdateResponse
from utils.auth import require_admin

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("", response_model=List[ProjectListItem])
def get_all_projects():
    """Retrieve all projects with summarized details."""
    return project_service.get_all_projects()


@router.get("/{project_id}", response_model=ProjectDetail)
def get_project_details(project_id: str):
    """Retrieve all properties for a single project."""
    project = project_service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProfileUpdateResponse)
def update_project_details(
    project_id: str, project_data: ProjectUpdate,
    admin_user: User = Depends(require_admin)
    ):
    """Update a project's details."""
    modified_count = project_service.update_project(project_id, project_data)
    if modified_count == 0:
        # Check if the document exists to differentiate between not found and no change
        if project_service.get_project_by_id(project_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return {"message": "No changes detected in project data", "modified_count": 0}

    return {"message": "Project updated successfully", "modified_count": modified_count}
