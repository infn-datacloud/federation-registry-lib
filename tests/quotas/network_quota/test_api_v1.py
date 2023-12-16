from typing import Any, Dict, Optional

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.project.models import Project
from app.quota.models import NetworkQuota
from app.quota.schemas import NetworkQuotaBase, NetworkQuotaUpdate
from app.service.models import NetworkService
from tests.common.utils import random_non_negative_int
from tests.fixtures.client import CLIENTS, CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI


class NetworkQuotaAPI(
    BaseAPI[
        NetworkQuota,
        NetworkQuotaBase,
        NetworkQuotaBase,
        NetworkQuotaUpdate,
    ]
):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: NetworkQuota, public: bool = False
    ) -> None:
        db_project: Project = db_item.project.single()
        assert db_project
        assert db_project.uid == obj.pop("project").get("uid")

        db_service: NetworkService = db_item.service.single()
        assert db_service
        assert db_service.uid == obj.pop("service").get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[NetworkQuota] = None
    ) -> NetworkQuotaUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.public_ips = random_non_negative_int()
        item.networks = random_non_negative_int()
        item.ports = random_non_negative_int()
        item.security_groups = random_non_negative_int()
        item.security_group_rules = random_non_negative_int()
        return item


@pytest.fixture(scope="class")
def network_quota_api() -> NetworkQuotaAPI:
    return NetworkQuotaAPI(
        base_schema=NetworkQuotaBase,
        base_public_schema=NetworkQuotaBase,
        update_schema=NetworkQuotaUpdate,
        endpoint_group="network_quotas",
        item_name="Network Quota",
    )


class TestNetworkQuotaTest(TestBaseAPI):
    """Class with the basic API calls to NetworkQuota endpoints."""

    __test__ = True
    api = "network_quota_api"
    db_item1 = "db_network_quota"
    db_item2 = "db_network_quota2"
    db_item3 = "db_network_quota3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_changing_per_user(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to change the per_user flag of a network quota.

        In this case the project has only the quota which will be modified.
        The operation succeeds.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: NetworkQuota = request.getfixturevalue(self.db_item1)
        new_data: NetworkQuotaUpdate = api.random_patch_item(from_item=db_item)
        new_data.per_user = not db_item.per_user
        api.patch(
            client=request.getfixturevalue(client), db_item=db_item, new_data=new_data
        )

    @pytest.mark.parametrize("client, public", CLIENTS)
    def test_patch_item_with_duplicated_per_user(
        self,
        request: pytest.FixtureRequest,
        client: TestClient,
        public: bool,
        db_network_quota_per_user: NetworkQuota,
    ) -> None:
        """Execute PATCH operations to try to change the per_user flag of a network
        quota.

        In this case the project already has a quota of the same type, pointing to the
        same service and with the same per_user flag.
        The endpoint returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: NetworkQuota = db_network_quota_per_user
        new_data: NetworkQuotaUpdate = api.random_patch_item(from_item=db_item)
        new_data.per_user = not new_data.per_user
        response: Response = api.patch(
            client=request.getfixturevalue(client),
            db_item=db_item,
            new_data=new_data,
            target_status_code=status.HTTP_400_BAD_REQUEST,
        )
        db_project: Project = db_item.project.single()
        db_service: NetworkService = db_item.service.single()
        msg = "Duplicated Network Quota, to not apply to each user, on "
        msg += f"Project '{db_project.uid}' and Service {db_service.uid}"
        assert response.json()["detail"] == msg
