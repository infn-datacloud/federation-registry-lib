from fastapi import HTTPException, status
from pydantic import UUID4

from app.user_group.crud import user_group
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupCreate


def valid_user_group_id(user_group_uid: UUID4) -> UserGroup:
    item = user_group.get(uid=str(user_group_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User Group '{user_group_uid}' not found",
        )
    return item


def is_unique_user_group(item: UserGroupCreate) -> None:
    db_item = user_group.get(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User Group with name '{item.name}' already registered",
        )
