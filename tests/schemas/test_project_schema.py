from typing import Any, Literal

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.project.models import Project
from fed_reg.project.schemas import (
    ProjectBase,
    ProjectBasePublic,
    ProjectCreate,
    ProjectQuery,
    ProjectRead,
    ProjectReadPublic,
    ProjectUpdate,
)
from fed_reg.project.schemas_extended import (
    FlavorRead,
    FlavorReadPublic,
    ImageRead,
    ImageReadPublic,
    NetworkRead,
    NetworkReadPublic,
    ProjectReadExtended,
    ProjectReadExtendedPublic,
    ProviderRead,
    ProviderReadPublic,
    SLAReadExtended,
    SLAReadExtendedPublic,
)
from tests.create_dict import project_schema_dict
from tests.schemas.cases_db_instances import CaseDBInstance, CasePublic
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(ProjectBasePublic, BaseNode)
    d = project_schema_dict()
    if key:
        d[key] = value
    item = ProjectBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = project_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProjectBasePublic(**d)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(ProjectBase, ProjectBasePublic)
    d = project_schema_dict()
    if key:
        d[key] = value
    item = ProjectBase(**d)
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = project_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProjectBase(**d)


def test_create() -> None:
    assert issubclass(ProjectCreate, BaseNodeCreate)
    assert issubclass(ProjectCreate, ProjectBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(ProjectUpdate, BaseNodeCreate)
    assert issubclass(ProjectUpdate, ProjectBase)
    d = project_schema_dict()
    if key:
        d[key] = value
    item = ProjectUpdate(**d)
    assert item.name == d.get("name")
    assert item.uuid == (d.get("uuid").hex if d.get("uuid") else None)


def test_query() -> None:
    assert issubclass(ProjectQuery, BaseNodeQuery)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(project_model: Project, key: str, value: str) -> None:
    assert issubclass(ProjectReadPublic, ProjectBasePublic)
    assert issubclass(ProjectReadPublic, BaseNodeRead)
    assert ProjectReadPublic.__config__.orm_mode

    if key:
        project_model.__setattr__(key, value)
    item = ProjectReadPublic.from_orm(project_model)

    assert item.uid
    assert item.uid == project_model.uid
    assert item.description == project_model.description
    assert item.name == project_model.name
    assert item.uuid == project_model.uuid


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_read_public(project_model: Project, key: str, value: str) -> None:
    project_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProjectReadPublic.from_orm(project_model)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_read(project_model: Project, key: str, value: Any) -> None:
    assert issubclass(ProjectRead, ProjectBase)
    assert issubclass(ProjectRead, BaseNodeRead)
    assert ProjectRead.__config__.orm_mode

    if key:
        project_model.__setattr__(key, value)
    item = ProjectRead.from_orm(project_model)

    assert item.uid
    assert item.uid == project_model.uid
    assert item.description == project_model.description
    assert item.name == project_model.name
    assert item.uuid == project_model.uuid


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_read(project_model: Project, key: str, value: str) -> None:
    project_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProjectRead.from_orm(project_model)


# @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="project")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended(model: Project, public: bool) -> None:
#     if public:
#         cls = ProjectReadPublic
#         cls_ext = ProjectReadExtendedPublic
#         prov_cls = ProviderReadPublic
#         flv_cls = FlavorReadPublic
#         img_cls = ImageReadPublic
#         net_cls = NetworkReadPublic
#         sla_cls = SLAReadExtendedPublic
#     else:
#         cls = ProjectRead
#         cls_ext = ProjectReadExtended
#         prov_cls = ProviderRead
#         flv_cls = FlavorRead
#         img_cls = ImageRead
#         net_cls = NetworkRead
#         sla_cls = SLAReadExtended

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = cls_ext.from_orm(model)

#     assert len(model.provider.all()) == 1
#     assert model.provider.single()
#     assert item.provider

#     assert len(item.flavors) == len(model.private_flavors.all()) + len(
#         model.public_flavors()
#     )
#     assert len(item.images) == len(model.private_images.all()) + len(
#         model.public_images()
#     )
#     assert len(item.networks) == len(model.private_networks.all()) + len(
#         model.public_networks()
#     )
#     if item.sla is not None:
#         assert len(model.sla.all()) == 1
#         assert model.sla.single()
#     else:
#         assert len(model.sla.all()) == 0
#         assert not model.sla.single()

#     assert isinstance(item.provider, prov_cls)
#     assert all([isinstance(i, flv_cls) for i in item.flavors])
#     assert all([isinstance(i, img_cls) for i in item.images])
#     assert all([isinstance(i, net_cls) for i in item.networks])
#     if item.sla is not None:
#         assert isinstance(item.sla, sla_cls)
