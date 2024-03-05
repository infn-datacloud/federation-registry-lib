from typing import Any, List, Literal, Optional, Tuple, Union
from unittest.mock import MagicMock

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.location.schemas import LocationCreate, LocationRead, LocationReadPublic
from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.provider.schemas import ProviderRead, ProviderReadPublic
from fed_reg.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
    ComputeServiceCreateExtended,
    NetworkServiceCreateExtended,
    RegionCreateExtended,
)
from fed_reg.region.models import Region
from fed_reg.region.schemas import (
    RegionBase,
    RegionBasePublic,
    RegionCreate,
    RegionQuery,
    RegionRead,
    RegionReadPublic,
    RegionUpdate,
)
from fed_reg.region.schemas_extended import RegionReadExtended, RegionReadExtendedPublic
from fed_reg.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    IdentityServiceCreate,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
)
from tests.create_dict import (
    region_schema_dict,
)
from tests.create_model import (
    block_storage_service_neomodel_query,
    compute_service_neomodel_query,
    identity_service_neomodel_query,
    location_neomodel_query,
    network_service_neomodel_query,
    provider_neomodel_query,
)
from tests.utils import random_lower_string, random_url


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["create_extended"])
    @parametrize(
        type=[
            "block_storage_services",
            "compute_services",
            "identity_services",
            "network_services",
        ]
    )
    @parametrize(len=[0, 1, 2])
    def case_services(
        self,
        block_storage_service_create_ext_schema: BlockStorageServiceCreateExtended,
        compute_service_create_ext_schema: ComputeServiceCreateExtended,
        identity_service_create_schema: IdentityServiceCreate,
        network_service_create_ext_schema: NetworkServiceCreateExtended,
        type: str,
        len: int,
    ) -> Tuple[
        str,
        Union[
            List[BlockStorageServiceCreateExtended],
            List[ComputeServiceCreateExtended],
            List[IdentityServiceCreate],
            List[NetworkServiceCreateExtended],
        ],
    ]:
        if len > 0:
            if type == "block_storage_services":
                service = block_storage_service_create_ext_schema
            elif type == "compute_services":
                service = compute_service_create_ext_schema
            elif type == "identity_services":
                service = identity_service_create_schema
            elif type == "network_services":
                service = network_service_create_ext_schema

            if len == 1:
                return type, [service]
            elif len == 2:
                service2 = service.copy()
                service2.endpoint = random_url()
                return type, [service, service2]
        else:
            return type, []

    @case(tags=["create_extended"])
    @parametrize(with_loc=[True, False])
    def case_location(
        self, location_create_schema: LocationCreate, with_loc: bool
    ) -> Tuple[Literal["location"], Optional[LocationCreate]]:
        if with_loc:
            return "location", location_create_schema
        else:
            return "location", None


class CaseInvalidAttr:
    @case(tags=["base_public", "base", "update"])
    def case_attr(self) -> Tuple[Literal["name"], None]:
        return "name", None

    @case(tags=["create_extended"])
    @parametrize(
        type=[
            "block_storage_services",
            "compute_services",
            "identity_services",
            "network_services",
        ]
    )
    def case_services(
        self,
        block_storage_service_create_ext_schema: BlockStorageServiceCreateExtended,
        compute_service_create_ext_schema: ComputeServiceCreateExtended,
        identity_service_create_schema: IdentityServiceCreate,
        network_service_create_ext_schema: NetworkServiceCreateExtended,
        type: str,
    ) -> Tuple[
        str,
        Union[
            List[BlockStorageServiceCreateExtended],
            List[ComputeServiceCreateExtended],
            List[IdentityServiceCreate],
            List[NetworkServiceCreateExtended],
        ],
        str,
    ]:
        if type == "block_storage_services":
            service = block_storage_service_create_ext_schema
        elif type == "compute_services":
            service = compute_service_create_ext_schema
        elif type == "identity_services":
            service = identity_service_create_schema
        elif type == "network_services":
            service = network_service_create_ext_schema

        return (
            type,
            [service, service],
            "There are multiple items with identical endpoint",
        )


class CaseDBInstance:
    @parametrize(tot_loc=[0, 1])
    def case_location(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        region_model: Region,
        tot_loc: int,
    ) -> Region:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "provider_r1" in query:
                return provider_neomodel_query(1, db_core)
            if "location_r1" in query:
                return location_neomodel_query(tot_loc, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return region_model

    @parametrize(tot_bsto_srv=[0, 1, 2])
    def case_block_storage_services(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        region_model: Region,
        tot_bsto_srv: int,
    ) -> Region:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "provider_r1" in query:
                return provider_neomodel_query(1, db_core)
            if "block_storage_services_r1" in query:
                return block_storage_service_neomodel_query(tot_bsto_srv, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return region_model

    @parametrize(tot_comp_srv=[0, 1, 2])
    def case_compute_services(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        region_model: Region,
        tot_comp_srv: int,
    ) -> Region:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "provider_r1" in query:
                return provider_neomodel_query(1, db_core)
            if "compute_services_r1" in query:
                return compute_service_neomodel_query(tot_comp_srv, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return region_model

    @parametrize(tot_id_srv=[0, 1, 2])
    def case_identity_services(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        region_model: Region,
        tot_id_srv: int,
    ) -> Region:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "provider_r1" in query:
                return provider_neomodel_query(1, db_core)
            if "identity_services_r1" in query:
                return identity_service_neomodel_query(tot_id_srv, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return region_model

    @parametrize(tot_net_srv=[0, 1, 2])
    def case_network_services(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        region_model: Region,
        tot_net_srv: int,
    ) -> Region:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "provider_r1" in query:
                return provider_neomodel_query(1, db_core)
            if "network_services_r1" in query:
                return network_service_neomodel_query(tot_net_srv, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return region_model

    def case_mixed_srv(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        region_model: Region,
    ) -> Region:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "provider_r1" in query:
                return provider_neomodel_query(1, db_core)
            if "block_storage_services_r1" in query:
                return block_storage_service_neomodel_query(1, db_core)
            if "compute_services_r1" in query:
                return compute_service_neomodel_query(1, db_core)
            if "identity_services_r1" in query:
                return identity_service_neomodel_query(1, db_core)
            if "network_services_r1" in query:
                return network_service_neomodel_query(1, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return region_model


class CasePublic:
    @parametrize(is_public=[True, False])
    def case_public(self, is_public: bool):
        return is_public


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(RegionBasePublic, BaseNode)
    d = region_schema_dict()
    if key:
        d[key] = value
    item = RegionBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = region_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        RegionBasePublic(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_base(key: str, value: Any) -> None:
    assert issubclass(RegionBase, RegionBasePublic)
    d = region_schema_dict()
    if key:
        d[key] = value
    item = RegionBase(**d)
    assert item.name == d.get("name")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_base(key: str, value: Any) -> None:
    d = region_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        RegionBase(**d)


def test_create() -> None:
    assert issubclass(RegionCreate, BaseNodeCreate)
    assert issubclass(RegionCreate, RegionBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(RegionUpdate, BaseNodeCreate)
    assert issubclass(RegionUpdate, RegionBase)
    d = region_schema_dict()
    if key:
        d[key] = value
    item = RegionUpdate(**d)
    assert item.name == d.get("name")


def test_query() -> None:
    assert issubclass(RegionQuery, BaseNodeQuery)


@parametrize_with_cases("attr, values", cases=CaseAttr, has_tag=["create_extended"])
def test_create_extended(
    attr: str,
    values: Optional[
        Union[
            LocationCreate,
            List[BlockStorageServiceCreateExtended],
            List[ComputeServiceCreateExtended],
            List[IdentityServiceCreate],
            List[NetworkServiceCreateExtended],
        ]
    ],
) -> None:
    assert issubclass(RegionCreateExtended, RegionCreate)
    d = region_schema_dict()
    d[attr] = values
    item = RegionCreateExtended(**d)
    assert item.__getattribute__(attr) == values


@parametrize_with_cases(
    "attr, values, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
)
def test_invalid_create_extended(
    attr: str,
    values: Union[
        List[BlockStorageServiceCreateExtended],
        List[ComputeServiceCreateExtended],
        List[IdentityServiceCreate],
        List[NetworkServiceCreateExtended],
    ],
    msg: str,
) -> None:
    d = region_schema_dict()
    d[attr] = values
    with pytest.raises(ValueError, match=msg):
        RegionCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(region_model: Region, key: str, value: str) -> None:
    assert issubclass(RegionReadPublic, RegionBasePublic)
    assert issubclass(RegionReadPublic, BaseNodeRead)
    assert RegionReadPublic.__config__.orm_mode

    if key:
        region_model.__setattr__(key, value)
    item = RegionReadPublic.from_orm(region_model)

    assert item.uid
    assert item.uid == region_model.uid
    assert item.description == region_model.description
    assert item.name == region_model.name


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_read_public(region_model: Region, key: str, value: str) -> None:
    region_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        RegionReadPublic.from_orm(region_model)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_read(region_model: Region, key: str, value: Any) -> None:
    assert issubclass(RegionRead, RegionBase)
    assert issubclass(RegionRead, BaseNodeRead)
    assert RegionRead.__config__.orm_mode

    if key:
        region_model.__setattr__(key, value)
    item = RegionRead.from_orm(region_model)

    assert item.uid
    assert item.uid == region_model.uid
    assert item.description == region_model.description
    assert item.name == region_model.name


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_read(region_model: Region, key: str, value: str) -> None:
    region_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        RegionRead.from_orm(region_model)


@parametrize_with_cases("model", cases=CaseDBInstance)
@parametrize_with_cases("public", cases=CasePublic)
def test_read_extended(model: Region, public: bool) -> None:
    if public:
        cls = RegionReadPublic
        cls_ext = RegionReadExtendedPublic
        prov_cls = ProviderReadPublic
        loc_cls = LocationReadPublic
        bsto_srv_cls = BlockStorageServiceReadPublic
        comp_srv_cls = ComputeServiceReadPublic
        id_srv_cls = IdentityServiceReadPublic
        net_srv_cls = NetworkServiceReadPublic
    else:
        cls = RegionRead
        cls_ext = RegionReadExtended
        prov_cls = ProviderRead
        loc_cls = LocationRead
        bsto_srv_cls = BlockStorageServiceRead
        comp_srv_cls = ComputeServiceRead
        id_srv_cls = IdentityServiceRead
        net_srv_cls = NetworkServiceRead

    assert issubclass(cls_ext, cls)
    assert cls_ext.__config__.orm_mode

    item = cls_ext.from_orm(model)

    if not item.location:
        assert not len(model.location.all())
        assert not model.location.single()
    else:
        assert len(model.location.all()) == 1
        assert model.location.single()
    assert len(model.provider.all()) == 1
    assert model.provider.single()
    assert len(item.services) == len(model.services.all())

    if item.location:
        assert isinstance(item.location, loc_cls)
    assert isinstance(item.provider, prov_cls)
    assert all(
        [
            isinstance(i, (bsto_srv_cls, comp_srv_cls, id_srv_cls, net_srv_cls))
            for i in item.services
        ]
    )
