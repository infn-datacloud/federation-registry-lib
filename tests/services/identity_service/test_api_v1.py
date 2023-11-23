from typing import Any, Dict, Optional

import pytest
from fastapi.testclient import TestClient

from app.region.models import Region
from app.service.models import IdentityService
from app.service.schemas import IdentityServiceBase, IdentityServiceUpdate
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.identity_service import random_identity_service_name
from tests.utils.utils import random_url


class IdentityServiceAPI(
    BaseAPI[
        IdentityService,
        IdentityServiceBase,
        IdentityServiceBase,
        IdentityServiceUpdate,
    ]
):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: IdentityService, public: bool = False
    ) -> None:
        db_region: Region = db_item.region.single()
        assert db_region
        assert db_region.uid == obj.pop("region").get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[IdentityService] = None
    ) -> IdentityServiceUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.endpoint = random_url()
        item.name = random_identity_service_name()
        return item


@pytest.fixture(scope="class")
def identity_service_api() -> IdentityServiceAPI:
    return IdentityServiceAPI(
        base_schema=IdentityServiceBase,
        base_public_schema=IdentityServiceBase,
        update_schema=IdentityServiceUpdate,
        endpoint_group="identity_services",
        item_name="Identity Service",
    )


class TestIdentityServiceTest(TestBaseAPI):
    """Class with the basic API calls to IdentityService endpoints."""

    __test__ = True
    api = "identity_service_api"
    db_item1 = "db_identity_serv"
    db_item2 = "db_identity_serv2"
    db_item3 = "db_identity_serv3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_identity_service_with_duplicated_endpoint(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the endpoint of an already existing identity provider to a different
        identity provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: IdentityService = request.getfixturevalue(self.db_item1)
        new_data: IdentityServiceUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )
