from typing import List, Optional
from .. import schemas, models


def create_project(item: schemas.ProjectCreate) -> schemas.Project:
    return models.Project(**item.dict()).save()


def get_projects(**kwargs) -> List[schemas.Project]:
    if kwargs:
        return models.Project.nodes.filter(**kwargs).all()
    return models.Project.nodes.all()


def get_project(**kwargs) -> Optional[schemas.Project]:
    return models.Project.nodes.get_or_none(**kwargs)


def remove_project(item: models.Project) -> bool:
    return item.delete()


def connect_project_to_user_group(
    user_group: models.UserGroup, project: models.Project
) -> bool:
    return project.user_group.connect(user_group)
