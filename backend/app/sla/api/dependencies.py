from typing import Union

from app.sla.crud import sla
from app.sla.models import SLA
from app.sla.schemas import SLACreate, SLAUpdate
from fastapi import Depends, HTTPException, status
from pydantic import UUID4


def valid_sla_id(sla_uid: UUID4) -> SLA:
    """
    Check given uid corresponds to an entity in the DB.

    Args:
        sla_uid (UUID4): uid of the target DB entity.

    Returns:
        SLA: DB entity with given uid.

    Raises:
        NotFoundError: DB entity with given uid not found.
    """

    item = sla.get(uid=str(sla_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SLA '{sla_uid}' not found",
        )
    return item


def is_unique_sla(item: Union[SLACreate, SLAUpdate]) -> None:
    """
    Check there are no other SLAs with the same document uuid.

    Args:
        item (SLACreate | SLAUpdate): new data.

    Returns:
        None

    Raises:
        BadRequestError: DB entity with given document uuid already exists.
    """

    db_item = sla.get(document_uuid=item.document_uuid)
    if db_item is not None:
        msg = f"Document '{item.document_uuid}' already used "
        msg += "by another SLA"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


def validate_new_sla_values(
    update_data: SLAUpdate, item: SLA = Depends(valid_sla_id)
) -> None:
    """
    Check given data are valid ones. Check there are no other
    SLAs with the same document uuid.

    Args:
        update_data (FlavorUpdate): new data.
        item (Flavor): DB entity to update.

    Returns:
        None

    Raises:
        NotFoundError: DB entity with given uid not found.
        BadRequestError: DB entity with given document uuid already exists.
    """

    if (
        update_data.document_uuid is not None
        and str(update_data.document_uuid) != item.document_uuid
    ):
        is_unique_sla(update_data)
