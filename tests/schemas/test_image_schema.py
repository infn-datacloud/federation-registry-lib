from typing import Any
from uuid import UUID

from pytest_cases import parametrize_with_cases

from fed_reg.image.enum import ImageOS
from fed_reg.image.models import Image
from fed_reg.image.schemas import (
    ImageBase,
    ImageBasePublic,
    ImageRead,
    ImageReadPublic,
    ImageUpdate,
)
from fed_reg.provider.schemas_extended import ImageCreateExtended
from tests.create_dict import image_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = image_schema_dict()
    if key:
        d[key] = value
    item = ImageBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = image_schema_dict()
    if key:
        d[key] = value
    item = ImageBase(**d)
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex
    assert item.os_type == (d.get("os_type").value if d.get("os_type") else None)
    assert item.os_distro == d.get("os_distro")
    assert item.os_version == d.get("os_version")
    assert item.architecture == d.get("architecture")
    assert item.kernel_id == d.get("kernel_id")
    assert item.cuda_support == d.get("cuda_support", False)
    assert item.is_public == d.get("is_public", True)
    assert item.gpu_driver == d.get("gpu_driver", False)
    assert item.tags == d.get("tags", [])


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = image_schema_dict()
    if key:
        d[key] = value
    item = ImageUpdate(**d)
    assert item.name == d.get("name")
    assert item.uuid == (d.get("uuid").hex if d.get("uuid") else None)


@parametrize_with_cases("projects", has_tag="create_extended")
def test_create_extended(projects: list[UUID]) -> None:
    d = image_schema_dict()
    d["is_public"] = len(projects) == 0
    d["projects"] = projects
    item = ImageCreateExtended(**d)
    assert item.projects == [i.hex for i in projects]


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(image_model: Image, key: str, value: str) -> None:
    if key:
        image_model.__setattr__(key, value)
    item = ImageReadPublic.from_orm(image_model)

    assert item.uid
    assert item.uid == image_model.uid
    assert item.description == image_model.description
    assert item.name == image_model.name
    assert item.uuid == image_model.uuid


@parametrize_with_cases("key, value", has_tag="base")
def test_read(image_model: Image, key: str, value: Any) -> None:
    if key:
        if isinstance(value, ImageOS):
            value = value.value
        image_model.__setattr__(key, value)
    item = ImageRead.from_orm(image_model)

    assert item.uid
    assert item.uid == image_model.uid
    assert item.description == image_model.description
    assert item.name == image_model.name
    assert item.uuid == image_model.uuid
    assert item.os_type == image_model.os_type
    assert item.os_distro == image_model.os_distro
    assert item.os_version == image_model.os_version
    assert item.architecture == image_model.architecture
    assert item.kernel_id == image_model.kernel_id
    assert item.cuda_support == image_model.cuda_support
    assert item.is_public == image_model.is_public
    assert item.gpu_driver == image_model.gpu_driver
    assert item.tags == image_model.tags


# TODO Test read extended classes
