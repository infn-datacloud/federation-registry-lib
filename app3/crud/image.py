from typing import List, Optional
from .. import schemas, models


def create_image(item: schemas.ImageCreate) -> schemas.Image:
    return models.Image(**item.dict()).save()


def get_images(**kwargs) -> List[schemas.Image]:
    if kwargs:
        return models.Image.nodes.filter(**kwargs).all()
    return models.Image.nodes.all()


def get_image(**kwargs) -> Optional[schemas.Image]:
    return models.Image.nodes.get_or_none(**kwargs)


def remove_image(item: models.Image) -> bool:
    return item.delete()


def connect_image_to_project(
    project: models.Project, image: models.Image
) -> bool:
    return image.project.connect(project)
