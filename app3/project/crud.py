from typing import List, Optional

from . import schemas, models
from ..crud import truncate, update


def create_project(item: schemas.ProjectCreate) -> models.Project:
    return models.Project.get_or_create(item.dict())[0]


def read_projects(
    skip: int = 0,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    **kwargs
) -> List[models.Project]:
    if kwargs:
        items = models.Project.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Project.nodes.order_by(sort).all()
    return truncate(items=items, skip=skip, limit=limit)


def read_project(**kwargs) -> Optional[models.Project]:
    return models.Project.nodes.get_or_none(**kwargs)


def remove_project(item: models.Project) -> bool:
    return item.delete()


def edit_project(
    old_item: models.Project, new_item: schemas.ProjectPatch
) -> Optional[models.Project]:
    return update(old_item=old_item, new_item=new_item)
