from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from ..crud import project
from ..models import Project as ProjectModel
from ..schemas import Project


def valid_project_id(project_uid: UUID4) -> ProjectModel:
    item = project.get(uid=str(project_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_uid} not found",
        )
    return item


def project_has_no_sla(
    project: Project = Depends(valid_project_id),
) -> ProjectModel:
    if project.sla.single():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project {project.uid} already has an associated SLA",
        )
    return project
