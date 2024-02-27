from typing import Any, List, Literal, Optional, Tuple
from uuid import UUID, uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.image.enum import ImageOS
from fed_reg.image.schemas import (
    ImageBase,
    ImageBasePublic,
    ImageCreate,
    ImageQuery,
    ImageUpdate,
)
from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from fed_reg.provider.schemas_extended import ImageCreateExtended
from tests.create_dict import image_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(value=[True, False])
    @parametrize(attr=["is_public", "cuda_support", "gpu_driver"])
    def case_boolean(self, attr: str, value: bool) -> Tuple[str, bool]:
        return attr, value

    @parametrize(attr=["os_distro", "os_version", "architecture", "kernel_id"])
    def case_string(self, attr: str) -> Tuple[str, str]:
        return attr, random_lower_string()

    @parametrize(value=[i for i in ImageOS])
    def case_os_type(self, value: str) -> Tuple[Literal["os_type"], ImageOS]:
        return "os_type", value

    @parametrize(len=[0, 1, 2])
    def case_tag_list(self, len: int) -> Tuple[Literal["tags"], Optional[List[str]]]:
        attr = "tags"
        if len == 0:
            return attr, []
        elif len == 1:
            return attr, [random_lower_string()]
        else:
            return attr, [random_lower_string() for _ in range(len)]

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_projects(self, len: int) -> List[UUID]:
        if len == 1:
            return [uuid4()]
        elif len == 2:
            return [uuid4(), uuid4()]
        return []


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> Tuple[str, None]:
        return attr, None

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_projects(self, len: int) -> Tuple[List[UUID], str]:
        if len == 1:
            return [uuid4()], "Public images do not have linked projects"
        elif len == 2:
            i = uuid4()
            return [i, i], "There are multiple identical items"
        return [], "Projects are mandatory for private images"


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(ImageBasePublic, BaseNode)
    d = image_schema_dict()
    if key:
        d[key] = value
    item = ImageBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = image_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ImageBasePublic(**d)


@parametrize_with_cases(
    "key, value", cases=CaseAttr, filter=lambda f: not f.has_tag("create_extended")
)
def test_base(key: str, value: Any) -> None:
    assert issubclass(ImageBase, ImageBasePublic)
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


@parametrize_with_cases(
    "key, value",
    cases=CaseInvalidAttr,
    filter=lambda f: not f.has_tag("create_extended"),
)
def test_invalid_base(key: str, value: Any) -> None:
    d = image_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ImageBase(**d)


def test_create() -> None:
    assert issubclass(ImageCreate, BaseNodeCreate)
    assert issubclass(ImageCreate, ImageBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(ImageUpdate, BaseNodeCreate)
    assert issubclass(ImageUpdate, ImageBase)
    d = image_schema_dict()
    if key:
        d[key] = value
    item = ImageUpdate(**d)
    assert item.name == d.get("name")
    assert item.uuid == (d.get("uuid").hex if d.get("uuid") else None)


def test_query() -> None:
    assert issubclass(ImageQuery, BaseNodeQuery)


@parametrize_with_cases("projects", cases=CaseAttr, has_tag=["create_extended"])
def test_create_extended(projects: List[UUID]) -> None:
    assert issubclass(ImageCreateExtended, ImageCreate)
    d = image_schema_dict()
    d["is_public"] = len(projects) == 0
    d["projects"] = projects
    item = ImageCreateExtended(**d)
    assert item.projects == [i.hex for i in projects]


@parametrize_with_cases(
    "projects, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
)
def test_invalid_create_extended(projects: List[UUID], msg: str) -> None:
    assert issubclass(ImageCreateExtended, ImageCreate)
    d = image_schema_dict()
    if len(projects) == 0 or len(projects) == 2:
        d["is_public"] = False
    elif len(projects) == 1:
        d["is_public"] = True
    d["projects"] = projects
    with pytest.raises(ValueError, match=msg):
        ImageCreateExtended(**d)


# TODO Test all read classes
