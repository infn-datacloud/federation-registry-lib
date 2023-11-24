from typing import Any, Dict, Optional
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.flavor.models import Flavor
from app.flavor.schemas import FlavorBase, FlavorUpdate
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)


class FlavorAPI(BaseAPI[Flavor, FlavorBase, FlavorBase, FlavorUpdate]):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: Flavor, public: bool = False
    ) -> None:
        projects = obj.pop("projects")
        assert len(db_item.projects) == len(projects)
        for db_proj, proj_dict in zip(
            sorted(db_item.projects, key=lambda x: x.uid),
            sorted(projects, key=lambda x: x.get("uid")),
        ):
            assert db_proj.uid == proj_dict.get("uid")

        services = obj.pop("services")
        assert len(db_item.services) == len(services)
        for db_serv, serv_dict in zip(
            sorted(db_item.services, key=lambda x: x.uid),
            sorted(services, key=lambda x: x.get("uid")),
        ):
            assert db_serv.uid == serv_dict.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[Flavor] = None
    ) -> FlavorUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.name = random_lower_string()
        item.uuid = uuid4().hex
        item.disk = random_non_negative_int()
        item.ram = random_non_negative_int()
        item.vcpus = random_non_negative_int()
        item.swap = random_non_negative_int()
        item.ephemeral = random_non_negative_int()
        item.infiniband = random_bool()
        item.gpus = random_positive_int()
        item.gpu_model = random_lower_string()
        item.gpu_vendor = random_lower_string()
        item.local_storage = random_lower_string()
        return item


@pytest.fixture(scope="class")
def flavor_api() -> FlavorAPI:
    return FlavorAPI(
        base_schema=FlavorBase,
        base_public_schema=FlavorBase,
        update_schema=FlavorUpdate,
        endpoint_group="flavors",
        item_name="Flavor",
    )


class TestFlavorTest(TestBaseAPI):
    """Class with the basic API calls to Flavor endpoints."""

    __test__ = True
    api = "flavor_api"
    db_item1 = "db_flavor"
    db_item2 = "db_flavor2"
    db_item3 = "db_flavor3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_flavor_with_duplicated_name_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing flavor to a different flavor
        belonging to a different Provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Flavor = request.getfixturevalue(self.db_item1)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_flavor_with_duplicated_name_same_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing flavor to a different flavor
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Flavor = request.getfixturevalue(self.db_item3)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
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
    def test_patch_flavor_with_duplicated_uuid_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing flavor to a different flavor
        belonging to a different Provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Flavor = request.getfixturevalue(self.db_item1)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_flavor_with_duplicated_uuid_same_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing flavor to a different flavor
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Flavor = request.getfixturevalue(self.db_item3)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
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
    def test_patch_flavor_changing_visibility(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to change the visibility of a flavor.

        It is not possible to change the visibility of a flavor using a patch operation.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Flavor = request.getfixturevalue(self.db_item1)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
        new_data.is_public = not new_data.is_public
        response: Response = api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            target_status_code=status.HTTP_400_BAD_REQUEST,
            new_data=new_data,
        )
        assert (
            response.json()["detail"] == f"{api.item_name} visibility can't be changed"
        )
