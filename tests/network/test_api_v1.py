from typing import Any, Dict, Optional
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.network.models import Network
from app.network.schemas import NetworkBase, NetworkUpdate
from app.project.models import Project
from app.service.models import NetworkService
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.utils import random_bool, random_lower_string, random_non_negative_int


class NetworkAPI(BaseAPI[Network, NetworkBase, NetworkBase, NetworkUpdate]):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: Network, public: bool = False
    ) -> None:
        db_project: Project = db_item.project.single()
        if db_project:
            assert db_project.uid == obj.pop("project").get("uid")
        else:
            assert not obj.pop("project")

        db_service: NetworkService = db_item.service.single()
        assert db_service
        assert db_service.uid == obj.pop("service").get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[Network] = None
    ) -> NetworkUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.name = random_lower_string()
        item.uuid = uuid4().hex
        item.is_router_external = random_bool()
        item.is_default = random_bool()
        item.mtu = random_non_negative_int()
        item.proxy_ip = random_lower_string()
        item.proxy_user = random_non_negative_int()
        item.tags = [random_lower_string()]
        return item


@pytest.fixture(scope="class")
def network_api() -> NetworkAPI:
    return NetworkAPI(
        base_schema=NetworkBase,
        base_public_schema=NetworkBase,
        update_schema=NetworkUpdate,
        endpoint_group="networks",
        item_name="Network",
    )


class TestNetworkTest(TestBaseAPI):
    """Class with the basic API calls to Network endpoints."""

    __test__ = True
    api = "network_api"
    db_item1 = "db_network"
    db_item2 = "db_network2"
    db_item3 = "db_network3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_uuid_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing network to a different network
        belonging to a different Provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Network = request.getfixturevalue(self.db_item1)
        new_data: NetworkUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_uuid_same_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing network to a different network
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Network = request.getfixturevalue(self.db_item3)
        new_data: NetworkUpdate = api.random_patch_item(from_item=db_item)
        response: Response = api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            target_status_code=status.HTTP_400_BAD_REQUEST,
            new_data=new_data,
        )
        assert (
            response.json()["detail"]
            == f"{api.item_name} with uuid '{new_data.uuid}' already registered"
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_changing_visibility(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to change the visibility of a network.

        It is not possible to change the visibility of a network using a patch
        operation. The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Network = request.getfixturevalue(self.db_item1)
        new_data: NetworkUpdate = api.random_patch_item(from_item=db_item)
        new_data.is_shared = not new_data.is_shared
        response: Response = api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            target_status_code=status.HTTP_400_BAD_REQUEST,
            new_data=new_data,
        )
        assert (
            response.json()["detail"] == f"{api.item_name} visibility can't be changed"
        )
