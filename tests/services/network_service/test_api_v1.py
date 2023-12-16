from typing import Any, Dict, Optional

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.region.models import Region
from app.service.enum import ServiceType
from app.service.models import NetworkService
from app.service.schemas import NetworkServiceBase, NetworkServiceUpdate
from tests.common.utils import random_url
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.network_service import random_network_service_name


class NetworkServiceAPI(
    BaseAPI[
        NetworkService,
        NetworkServiceBase,
        NetworkServiceBase,
        NetworkServiceUpdate,
    ]
):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: NetworkService, public: bool = False
    ) -> None:
        db_region: Region = db_item.region.single()
        assert db_region
        assert db_region.uid == obj.pop("region").get("uid")

        networks = obj.pop("networks")
        assert len(db_item.networks) == len(networks)
        for db_net, net_dict in zip(
            sorted(db_item.networks, key=lambda x: x.uid),
            sorted(networks, key=lambda x: x.get("uid")),
        ):
            assert db_net.uid == net_dict.get("uid")

        quotas = obj.pop("quotas")
        assert len(db_item.quotas) == len(quotas)
        for db_quota, quota_dict in zip(
            sorted(db_item.quotas, key=lambda x: x.uid),
            sorted(quotas, key=lambda x: x.get("uid")),
        ):
            assert db_quota.uid == quota_dict.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[NetworkService] = None
    ) -> NetworkServiceUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.endpoint = random_url()
        item.name = random_network_service_name()
        return item


@pytest.fixture(scope="class")
def network_service_api() -> NetworkServiceAPI:
    return NetworkServiceAPI(
        base_schema=NetworkServiceBase,
        base_public_schema=NetworkServiceBase,
        update_schema=NetworkServiceUpdate,
        endpoint_group="network_services",
        item_name="Network Service",
    )


class TestNetworkServiceTest(TestBaseAPI):
    """Class with the basic API calls to NetworkService endpoints."""

    __test__ = True
    api = "network_service_api"
    db_item1 = "db_network_serv"
    db_item2 = "db_network_serv2"
    db_item3 = "db_network_serv3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_endpoint(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the endpoint of an already existing identity provider to a different
        identity provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: NetworkService = request.getfixturevalue(self.db_item1)
        new_data: NetworkServiceUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_changing_type(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to change the type of a network service.

        At first this should not be allowed by schema construction. In any case, if a
        request arrives, it is discarded since the payload is not a network
        service object.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: NetworkService = request.getfixturevalue(self.db_item1)
        new_data: NetworkServiceUpdate = api.random_patch_item(from_item=db_item)
        for t in [i.value for i in ServiceType]:
            if t != ServiceType.NETWORK.value:
                d = new_data.dict(exclude_unset=True)
                d["type"] = t
                api.patch(
                    client=request.getfixturevalue(client),
                    db_item=request.getfixturevalue(self.db_item2),
                    new_data=d,
                    target_status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
