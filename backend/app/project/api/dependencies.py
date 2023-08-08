from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.project.crud import project
from app.project.models import Project
from app.project.schemas import ProjectUpdate
from app.provider.api.dependencies import valid_provider_id
from app.provider.models import Provider


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


def is_unique_project(
    *,
    item: ProjectUpdate,
    attr: str,
    provider: Provider = Depends(valid_provider_id),
) -> None:
    """
    Check there are no other projects, belonging to the same
    provider, with the same name or uuid.

    Args:
        item (ProjectUpdate): new data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with identical name or uuid,
            belonging to the same provider, already exists.
    """

    kwargs = {attr: item.__getattribute__(attr)}
    db_item = provider.projects.get_or_none(**kwargs)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with {attr} '{kwargs[attr]}' already registered",
        )


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
        is_unique_project(
            item=update_data, provider=item.provider.single(), attr="name"
        )
    if str(update_data.uuid) != item.uuid:
        is_unique_project(
            item=update_data, provider=item.provider.single(), attr="uuid"
        )
