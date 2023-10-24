from random import choice
from typing import List, Union
from uuid import uuid4

from app.image.enum import ImageOS
from app.image.models import Image
from app.image.schemas import ImageBase, ImageRead, ImageReadShort, ImageUpdate
from app.image.schemas_extended import ImageReadExtended
from app.provider.schemas_extended import ImageCreateExtended
from app.tests.utils.utils import random_bool, random_lower_string


def create_random_image(
    *, default: bool = False, projects: List[str] = []
) -> ImageCreateExtended:
    name = random_lower_string()
    uuid = uuid4()
    kwargs = {}
    if not default:
        kwargs = {
            "description": random_lower_string(),
            "os_type": random_os_type(),
            "os_distro": random_lower_string(),
            "os_version": random_lower_string(),
            "architecture": random_lower_string(),
            "is_public": len(projects) == 0,
            "kernel_id": random_lower_string(),
            "cuda_support": random_bool(),
            "gpu_driver": random_bool(),
            "tags": [random_lower_string()],
        }
        if len(projects) > 0:
            kwargs["projects"] = projects
    return ImageCreateExtended(name=name, uuid=uuid, **kwargs)


def create_random_image_patch(default: bool = False) -> ImageUpdate:
    if default:
        return ImageUpdate()
    description = random_lower_string()
    name = random_lower_string()
    uuid = uuid4()
    os_type = random_os_type()
    os_distro = random_lower_string()
    os_version = random_lower_string()
    architecture = random_lower_string()
    is_public = random_bool()
    kernel_id = random_lower_string()
    cuda_support = random_bool()
    gpu_driver = random_bool()
    tags = [random_lower_string()]
    return ImageUpdate(
        description=description,
        name=name,
        uuid=uuid,
        os_type=os_type,
        os_distro=os_distro,
        os_version=os_version,
        architecture=architecture,
        is_public=is_public,
        kernel_id=kernel_id,
        cuda_support=cuda_support,
        gpu_driver=gpu_driver,
        tags=tags,
    )


def random_os_type() -> str:
    return choice([i.value for i in ImageOS])


def validate_image_attrs(*, obj_in: ImageBase, db_item: Image) -> None:
    assert db_item.description == obj_in.description
    assert db_item.name == obj_in.name
    assert db_item.uuid == obj_in.uuid
    assert db_item.is_public == obj_in.is_public
    assert db_item.os_type == obj_in.os_type
    assert db_item.os_distro == obj_in.os_distro
    assert db_item.os_version == obj_in.os_version
    assert db_item.architecture == obj_in.architecture
    assert db_item.kernel_id == obj_in.kernel_id
    assert db_item.cuda_support == obj_in.cuda_support
    assert db_item.gpu_driver == obj_in.gpu_driver
    assert db_item.tags == obj_in.tags


def validate_create_image_attrs(*, obj_in: ImageCreateExtended, db_item: Image) -> None:
    validate_image_attrs(obj_in=obj_in, db_item=db_item)
    assert len(db_item.projects) == len(obj_in.projects)
    for db_proj, proj_in in zip(db_item.projects, obj_in.projects):
        assert db_proj.uuid == proj_in


def validate_read_image_attrs(
    *, obj_out: Union[ImageRead, ImageReadShort, ImageReadExtended], db_item: Image
) -> None:
    assert db_item.uid == obj_out.uid
    validate_image_attrs(obj_in=obj_out, db_item=db_item)

    if isinstance(obj_out, ImageReadExtended):
        assert len(db_item.projects) == len(obj_out.projects)
        for db_proj, proj_out in zip(db_item.projects, obj_out.projects):
            assert db_proj.uid == proj_out.uid
        assert len(db_item.services) == len(obj_out.services)
        for db_serv, serv_out in zip(db_item.services, obj_out.services):
            assert db_serv.uid == serv_out.uid
