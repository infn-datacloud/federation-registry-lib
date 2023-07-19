from fastapi import HTTPException, status
from pydantic import UUID4

from app.sla.crud import sla
from app.sla.models import SLA
from app.sla.schemas import SLACreate


def valid_sla_id(sla_uid: UUID4) -> SLA:
    item = sla.get(uid=str(sla_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SLA '{sla_uid}' not found",
        )
    return item


def valid_document(item: SLACreate) -> SLACreate:
    db_item = sla.get(document_uuid=item.document_uuid)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Document '{item.document_uuid}' already used by another SLA",
        )
    return item
