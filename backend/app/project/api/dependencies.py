from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.project.crud import project
from app.project.models import Project
from app.project.schemas import ProjectUpdate
from app.utils import find_duplicates


def valid_project_id(project_uid: UUID4) -> Project:
    """
    Check given uid corresponds to an entity in the DB.

    Args:
        project_uid (UUID4): uid of the target DB entity.

    Returns:
        Project: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = project.get(uid=str(project_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_uid}' not found",
        )
    return item


def project_has_no_sla(
    project: Project = Depends(valid_project_id),
) -> Project:
    """
    Check target project is not already involved into a SLA.

    Args:
        update_data (ProejctRead): new data.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity already has an associated SLA.
    """
    
    if project.sla.single():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project '{project.name}' already has an associated SLA",
        )
    return project


def validate_new_project_values(
    update_data: ProjectUpdate, item: Project = Depends(valid_project_id)
) -> None:
    """
    Check given data are valid ones. Check there are no other projects,
    belonging to the same provider, with the same uuid and name.

    Args:
        update_data (ProjectUpdate): new data.
        item (Project): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with identical name or uuid, 
            belonging to the same provider, already exists.
    """

    if update_data.name != item.name:
        find_duplicates(item.provider.single().projects.all(), "name")
    if str(update_data.uuid) != item.uuid:
        find_duplicates(item.provider.single().projects.all(), "uuid")
