from typing import List, Optional
from .. import schemas, models


def create_project(item: schemas.ProjectCreate) -> models.Project:
    return models.Project(**item.dict()).save()


def get_projects(
    skip: int = 0, limit: Optional[int] = None, sort: Optional[str] = None, **kwargs
) -> List[models.Project]:
    if kwargs:
        items = models.Project.nodes.filter(**kwargs).order_by(sort).all()
    else:
        items = models.Project.nodes.order_by(sort).all()
    if limit is None:
        return items[skip:]
    return items[skip : skip + limit]


def get_project(**kwargs) -> Optional[models.Project]:
    return models.Project.nodes.get_or_none(**kwargs)


def remove_project(item: models.Project) -> bool:
    return item.delete()


def update_project(
    old_item: models.Project, new_item: schemas.ProjectUpdate
) -> Optional[models.Project]:
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
