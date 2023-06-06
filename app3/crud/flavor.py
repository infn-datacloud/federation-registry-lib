from typing import List, Optional
from .. import schemas, models


def create_flavor(item: schemas.FlavorCreate) -> schemas.Flavor:
    return models.Flavor(**item.dict()).save()


def get_flavors(**kwargs) -> List[schemas.Flavor]:
    if kwargs:
        return models.Flavor.nodes.filter(**kwargs).all()
    return models.Flavor.nodes.all()


def get_flavor(**kwargs) -> Optional[schemas.Flavor]:
    return models.Flavor.nodes.get_or_none(**kwargs)


def remove_flavor(item: models.Flavor) -> bool:
    return item.delete()


def connect_flavor_to_project(
    project: models.Project, flavor: models.Flavor
) -> bool:
    return flavor.project.connect(project)
