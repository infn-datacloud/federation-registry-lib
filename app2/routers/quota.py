from uuid import UUID
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..database import db
from .. import crud, schemas

router = APIRouter(prefix="/quotas", tags=["quotas"])


@router.get("/{id}", response_model=schemas.Quota)
def read_quota(id: UUID):
    with db.session() as session:
        item = session.execute_read(crud.get_quota, id=id)
        if item is None:
            raise HTTPException(status_code=404, detail="Quota not found")
        return item


@router.get("/", response_model=List[schemas.Quota])
def read_quotas(
    skip: int = 0,
    limit: int = 100,
    quota_id: Optional[int] = None,
):
    with db.session() as session:
        return session.execute_read(crud.get_quotas)


@router.delete("/{id}")
def delete_quotas(id: UUID):
    with db.session() as session:
        return session.execute_write(crud.remove_quota, id=id)
