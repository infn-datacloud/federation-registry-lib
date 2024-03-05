from typing import List, Tuple
from unittest.mock import MagicMock

from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fed_reg.location.schemas import LocationRead, LocationReadPublic
from fed_reg.provider.models import Provider
from fed_reg.provider.schemas_extended import (
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
    RegionReadExtended,
    RegionReadExtendedPublic,
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)
from fed_reg.region.models import Region
from fed_reg.region.schemas import RegionRead, RegionReadPublic
from fed_reg.service.schemas import IdentityServiceRead, IdentityServiceReadPublic
from tests.create_model import (
    block_storage_service_neomodel_query,
    compute_service_neomodel_query,
    connect_provider_and_idp_neomodel,
    identity_provider_neomodel_query,
    identity_service_neomodel_query,
    location_neomodel_query,
    network_service_neomodel_query,
    project_neomodel_query,
    region_neomodel_query,
    user_group_neomodel_query,
)


class CaseDBInstance:
    @case(tags=["provider"])
    @parametrize(tot_proj=[0, 1, 2])
    @parametrize(tot_reg=[0, 1, 2])
    @parametrize(tot_idp=[0, 1, 2])
    def case_provider(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        provider_model: Provider,
        tot_proj: int,
        tot_reg: int,
        tot_idp: int,
    ) -> Provider:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "identity_providers_r1" in query:
                items, rels = identity_provider_neomodel_query(tot_idp, db_core)
                for item in items:
                    connect_provider_and_idp_neomodel(
                        db_core, provider=provider_model, identity_provider=item[0]
                    )
                return items, rels
            if "projects_r1" in query:
                return project_neomodel_query(tot_proj, db_core)
            if "regions_r1" in query:
                return region_neomodel_query(tot_reg, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return provider_model

    @case(tags=["region"])
    @parametrize(tot_loc=[0, 1])
    @parametrize(tot_bsto_srv=[0, 1, 2])
    @parametrize(tot_comp_srv=[0, 1, 2])
    @parametrize(tot_id_srv=[0, 1, 2])
    @parametrize(tot_net_srv=[0, 1, 2])
    def case_region(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        region_model: Region,
        tot_loc: int,
        tot_bsto_srv: int,
        tot_comp_srv: int,
        tot_id_srv: int,
        tot_net_srv: int,
    ) -> Provider:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "location_r1" in query:
                return location_neomodel_query(tot_loc, db_core)
            if "block_storage_services_r1" in query:
                return block_storage_service_neomodel_query(tot_bsto_srv, db_core)
            if "compute_services_r1" in query:
                return compute_service_neomodel_query(tot_comp_srv, db_core)
            if "identity_services_r1" in query:
                return identity_service_neomodel_query(tot_id_srv, db_core)
            if "network_services_r1" in query:
                return network_service_neomodel_query(tot_net_srv, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return region_model

    @case(tags=["identity_provider"])
    @parametrize(tot_group=[0, 1, 2])
    def case_identity_provider(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        provider_model: Provider,
        tot_group: int,
    ) -> Provider:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "identity_providers_r1" in query:
                items, rels = identity_provider_neomodel_query(1, db_core)
                for item in items:
                    connect_provider_and_idp_neomodel(
                        db_core, provider=provider_model, identity_provider=item[0]
                    )
                return items, rels
            if "user_groups_r1" in query:
                return user_group_neomodel_query(tot_group, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return provider_model


class CasePublic:
    @parametrize(is_public=[True, False])
    def case_public(self, is_public: bool):
        return is_public


@parametrize_with_cases("model", cases=CaseDBInstance, has_tag="region")
@parametrize_with_cases("public", cases=CasePublic)
def test_read_extended_subclass_region(model: Region, public: bool) -> None:
    if public:
        cls = RegionReadPublic
        cls_ext = RegionReadExtendedPublic
        loc_cls = LocationReadPublic
        bsto_srv_cls = BlockStorageServiceReadExtendedPublic
        comp_srv_cls = ComputeServiceReadExtendedPublic
        id_srv_cls = IdentityServiceReadPublic
        net_srv_cls = NetworkServiceReadExtendedPublic
    else:
        cls = RegionRead
        cls_ext = RegionReadExtended
        loc_cls = LocationRead
        bsto_srv_cls = BlockStorageServiceReadExtended
        comp_srv_cls = ComputeServiceReadExtended
        id_srv_cls = IdentityServiceRead
        net_srv_cls = NetworkServiceReadExtended

    assert issubclass(cls_ext, cls)
    assert cls_ext.__config__.orm_mode

    item = cls_ext.from_orm(model)

    if not item.location:
        assert not len(model.location.all())
        assert not model.location.single()
    else:
        assert len(model.location.all()) == 1
        assert model.location.single()
    assert len(item.services) == len(model.services.all())

    if item.location:
        assert isinstance(item.location, loc_cls)
    assert all(
        [
            isinstance(i, (bsto_srv_cls, comp_srv_cls, id_srv_cls, net_srv_cls))
            for i in item.services
        ]
    )


@parametrize_with_cases("model", cases=CaseDBInstance, has_tag="identity_provider")
@parametrize_with_cases("public", cases=CasePublic)
def test_read_extended_subclass_identity_provider(
    model: Provider, public: bool
) -> None:
    if public:
        prov_cls = ProviderReadExtendedPublic
        cls = IdentityProviderReadPublic
        cls_ext = IdentityProviderReadExtendedPublic
        group_cls = UserGroupReadExtendedPublic
    else:
        prov_cls = ProviderReadExtended
        cls = IdentityProviderRead
        cls_ext = IdentityProviderReadExtended
        group_cls = UserGroupReadExtended

    assert issubclass(cls_ext, cls)
    assert cls_ext.__config__.orm_mode

    item = prov_cls.from_orm(model)

    model = model.identity_providers.all()[0]
    item = item.identity_providers[0]
    assert len(item.user_groups) == len(model.user_groups.all())
    assert len(item.user_groups) == len(model.user_groups.all())

    assert all([isinstance(i, group_cls) for i in item.user_groups])
