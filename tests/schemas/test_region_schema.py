from typing import Any, Optional

from pytest_cases import parametrize_with_cases

from fed_reg.location.schemas import LocationCreate
from fed_reg.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
    ComputeServiceCreateExtended,
    NetworkServiceCreateExtended,
    ObjectStoreServiceCreateExtended,
    RegionCreateExtended,
)
from fed_reg.region.models import Region
from fed_reg.region.schemas import (
    RegionBase,
    RegionBasePublic,
    RegionRead,
    RegionReadPublic,
    RegionUpdate,
)
from fed_reg.service.schemas import IdentityServiceCreate
from tests.create_dict import region_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = region_schema_dict()
    if key:
        d[key] = value
    item = RegionBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = region_schema_dict()
    if key:
        d[key] = value
    item = RegionBase(**d)
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(region_model: Region, key: str, value: str) -> None:
    if key:
        region_model.__setattr__(key, value)
    item = RegionReadPublic.from_orm(region_model)

    assert item.uid
    assert item.uid == region_model.uid
    assert item.description == region_model.description
    assert item.name == region_model.name


@parametrize_with_cases("key, value", has_tag="base")
def test_read(region_model: Region, key: str, value: Any) -> None:
    if key:
        region_model.__setattr__(key, value)
    item = RegionRead.from_orm(region_model)

    assert item.uid
    assert item.uid == region_model.uid
    assert item.description == region_model.description
    assert item.name == region_model.name


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = region_schema_dict()
    if key:
        d[key] = value
    item = RegionUpdate(**d)
    assert item.name == d.get("name")


@parametrize_with_cases("attr, values", has_tag="create_extended")
def test_create_extended(
    attr: str,
    values: Optional[
        LocationCreate
        | list[BlockStorageServiceCreateExtended]
        | list[ComputeServiceCreateExtended]
        | list[IdentityServiceCreate]
        | list[NetworkServiceCreateExtended]
        | list[ObjectStoreServiceCreateExtended]
    ],
) -> None:
    d = region_schema_dict()
    d[attr] = values
    item = RegionCreateExtended(**d)
    assert item.__getattribute__(attr) == values


# @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="region")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended(model: Region, public: bool) -> None:
#     if public:
#         cls = RegionReadPublic
#         cls_ext = RegionReadExtendedPublic
#         prov_cls = ProviderReadPublic
#         loc_cls = LocationReadPublic
#         bsto_srv_cls = BlockStorageServiceReadPublic
#         comp_srv_cls = ComputeServiceReadPublic
#         id_srv_cls = IdentityServiceReadPublic
#         net_srv_cls = NetworkServiceReadPublic
#     else:
#         cls = RegionRead
#         cls_ext = RegionReadExtended
#         prov_cls = ProviderRead
#         loc_cls = LocationRead
#         bsto_srv_cls = BlockStorageServiceRead
#         comp_srv_cls = ComputeServiceRead
#         id_srv_cls = IdentityServiceRead
#         net_srv_cls = NetworkServiceRead

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = cls_ext.from_orm(model)

#     if not item.location:
#         assert not len(model.location.all())
#         assert not model.location.single()
#     else:
#         assert len(model.location.all()) == 1
#         assert model.location.single()
#         assert item.location
#     assert len(model.provider.all()) == 1
#     assert model.provider.single()
#     assert item.provider
#     assert len(item.services) == len(model.services.all())

#     if item.location:
#         assert isinstance(item.location, loc_cls)
#     assert isinstance(item.provider, prov_cls)
#     assert all(
#         [
#             isinstance(i, (bsto_srv_cls, comp_srv_cls, id_srv_cls, net_srv_cls))
#             for i in item.services
#         ]
#     )
