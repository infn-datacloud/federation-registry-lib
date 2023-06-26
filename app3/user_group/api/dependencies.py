from fastapi import HTTPException, status
from pydantic import UUID4

from ..crud import read_user_group
from ..models import UserGroup
from ..schemas import UserGroupCreate


def valid_user_group_id(user_group_uid: UUID4) -> UserGroup:
    item = read_user_group(uid=str(user_group_uid).replace("-", ""))
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User Group {user_group_uid} not found",
        )
    return item

def is_unique_user_group(item: UserGroupCreate) -> UserGroupCreate:
    db_item = read_user_group(name=item.name)
    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User Group with name '{item.name}' already registered",
        )
    return item
