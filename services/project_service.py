from typing import List, Optional
from repositories import project_repo
from schemas.project import ProjectListItem, ProjectDetail, ProjectUpdate


def get_all_projects() -> List[ProjectListItem]:
    """
    Service to get all projects for the list view.
    """
    projects_data = project_repo.find_all_projects()
    return [ProjectListItem.model_validate(p) for p in projects_data]


def get_project_by_id(project_id: str) -> Optional[ProjectDetail]:
    """
    Service to get a single project by its ID.
    """
    project_data = project_repo.find_project_by_id(project_id)
    if project_data:
        return ProjectDetail.model_validate(project_data)
    return None


def update_project(project_id: str, project_update: ProjectUpdate) -> int:
    """
    Service to update a project.

    Returns:
        The number of modified documents.
    """
    return project_repo.update_project_by_id(project_id, project_update)
