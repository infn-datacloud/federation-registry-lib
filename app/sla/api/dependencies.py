from typing import Union
from fastapi import Depends, HTTPException, status
from pydantic import UUID4

from app.sla.crud import sla
from app.sla.models import SLA
from app.sla.schemas import SLACreate, SLAUpdate


def valid_sla_id(sla_uid: UUID4) -> SLA:
    item = sla.get(uid=str(sla_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SLA '{sla_uid}' not found",
        )
    return item


def is_unique_sla(item: Union[SLACreate, SLAUpdate]) -> None:
    db_item = sla.get(document_uuid=item.document_uuid)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document '{item.document_uuid}' already used by another SLA",
        )


def validate_new_sla_values(
    update_data: SLAUpdate, item: SLA = Depends(valid_sla_id)
) -> None:
    if update_data.document_uuid != item.document_uuid:
        is_unique_sla(update_data)
