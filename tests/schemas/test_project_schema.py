from typing import Any

from pytest_cases import parametrize_with_cases

from fed_reg.project.models import Project
from fed_reg.project.schemas import (
    ProjectBase,
    ProjectBasePublic,
    ProjectRead,
    ProjectReadPublic,
    ProjectUpdate,
)
from tests.create_dict import project_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = project_schema_dict()
    if key:
        d[key] = value
    item = ProjectBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = project_schema_dict()
    if key:
        d[key] = value
    item = ProjectBase(**d)
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid").hex


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(project_model: Project, key: str, value: str) -> None:
    if key:
        project_model.__setattr__(key, value)
    item = ProjectReadPublic.from_orm(project_model)

    assert item.uid
    assert item.uid == project_model.uid
    assert item.description == project_model.description
    assert item.name == project_model.name
    assert item.uuid == project_model.uuid


@parametrize_with_cases("key, value", has_tag="base")
def test_read(project_model: Project, key: str, value: Any) -> None:
    if key:
        project_model.__setattr__(key, value)
    item = ProjectRead.from_orm(project_model)

    assert item.uid
    assert item.uid == project_model.uid
    assert item.description == project_model.description
    assert item.name == project_model.name
    assert item.uuid == project_model.uuid


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = project_schema_dict()
    if key:
        d[key] = value
    item = ProjectUpdate(**d)
    assert item.name == d.get("name")
    assert item.uuid == (d.get("uuid").hex if d.get("uuid") else None)


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
