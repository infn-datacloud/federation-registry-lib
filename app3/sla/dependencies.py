from typing import List
from fastapi import Body, Depends, HTTPException, status
from pydantic import UUID4

from .crud import read_sla
from .models import SLA
from .schemas import SLACreate
from ..project.dependencies import valid_project_id
from ..provider.schemas import Provider
from ..quota.schemas import Quota
from ..user_group.dependencies import valid_user_group_id


def valid_sla_id(sla_uid: UUID4) -> SLA:
    item = read_sla(uid=str(sla_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User Group {sla_uid} not found",
        )
    return item


# def is_unique_sla(item: SLACreate) -> SLACreate:
#    db_item = read_sla(name=item.name)
#    if db_item is not None:
#        raise HTTPException(
#            status_code=status.HTTP_400_BAD_REQUEST,
#            detail=f"SLA with name '{item.name}' already registered",
#        )
#    return item


def valid_quota_list(quotas: List[Quota], provider: Provider):
    for quota in quotas:
        service = quota.service.single()
        
    return item


def validate_sla_entities(item: SLACreate) -> SLACreate:
    project = valid_project_id(item.project_uid)
    user_group = valid_user_group_id(item.user_group_uid)
    if project.sla.single():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project {item.project_uid} already has an associated SLA",
        )
    provider = project.provider.single()
    quotas = valid_quota_list(quotas=item.quotas, provider=provider)
    return item
