from bson import ObjectId
from typing import List, Optional
from db.mongodb import get_projects_collection
from models.mongo_models import ProjectBase


def find_all_projects() -> List[dict]:
    """
    Retrieves all project documents from the collection.
    """
    collection = get_projects_collection()
    pipeline = [
        {
            "$sort": {
                "timeline.started_at": -1,
                "timeline.ended_at": -1
            }
        }
    ]
    # In a descending sort, nulls are last. The pipeline above handles this correctly.
    return list(collection.aggregate(pipeline))


def find_project_by_id(project_id: str) -> Optional[dict]:
    """
    Finds a single project document by its ID.
    """
    if not ObjectId.is_valid(project_id):
        return None
    collection = get_projects_collection()
    return collection.find_one({"_id": ObjectId(project_id)})


def update_project_by_id(project_id: str, project_data: ProjectBase) -> int:
    """
    Updates a project document by its ID.

    Returns:
        The number of documents modified.
    """
    if not ObjectId.is_valid(project_id):
        return 0
    collection = get_projects_collection()
    update_data = project_data.model_dump(by_alias=True, exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(project_id)}, {"$set": update_data})
    return result.modified_count
