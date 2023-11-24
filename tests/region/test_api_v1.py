from typing import Any, Dict, Optional

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.location.models import Location
from app.provider.models import Provider
from app.region.models import Region
from app.region.schemas import RegionBase, RegionUpdate
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.utils import random_lower_string


class RegionAPI(BaseAPI[Region, RegionBase, RegionBase, RegionUpdate]):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: Region, public: bool = False
    ) -> None:
        db_provider: Provider = db_item.provider.single()
        assert db_provider
        assert db_provider.uid == obj.pop("provider").get("uid")

        db_location: Location = db_item.location.single()
        if db_location:
            assert db_location.uid == obj.pop("location").get("uid")
        else:
            assert not obj.pop("location")

        services = obj.pop("services")
        assert len(db_item.services) == len(services)
        for db_serv, serv_schema in zip(
            sorted(db_item.services, key=lambda x: x.uid),
            sorted(services, key=lambda x: x.get("uid")),
        ):
            assert db_serv.uid == serv_schema.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[Region] = None
    ) -> RegionUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.name = random_lower_string()
        return item


@pytest.fixture(scope="class")
def region_api() -> RegionAPI:
    return RegionAPI(
        base_schema=RegionBase,
        base_public_schema=RegionBase,
        update_schema=RegionUpdate,
        endpoint_group="regions",
        item_name="Region",
    )


class TestRegionTest(TestBaseAPI):
    """Class with the basic API calls to Region endpoints."""

    __test__ = True
    api = "region_api"
    db_item1 = "db_region"
    db_item2 = "db_region2"
    db_item3 = "db_region3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_name_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing region to a different region
        belonging to a different Provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Region = request.getfixturevalue(self.db_item1)
        new_data: RegionUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_name_same_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing region to a different region
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Region = request.getfixturevalue(self.db_item3)
        new_data: RegionUpdate = api.random_patch_item(from_item=db_item)
        response: Response = api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            target_status_code=status.HTTP_400_BAD_REQUEST,
            new_data=new_data,
        )
        assert (
            response.json()["detail"]
            == f"{api.item_name} with name '{new_data.name}' already registered"
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_failed_delete_item(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute DELETE to remove a region from a provider with only one region.

        Fail deletion, since a provider must have at least one region.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        api.delete(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item1),
            target_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
