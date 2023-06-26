from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import read_project
from ..models import Project


def valid_project_id(project_uid: UUID4) -> Project:
    item = read_project(uid=str(project_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_uid} not found",
        )
    return item