import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.flavor.models import Flavor
from app.flavor.schemas import FlavorUpdate
from tests.common.client import CLIENTS_READ_WRITE
from tests.flavor.controller import FlavorController
from tests.utils.api_v1 import TestBaseAPI


class TestFlavorAPI(TestBaseAPI):
    """Class with the basic API calls to Flavor endpoints."""

    __test__ = True
    controller = "flavor_controller"
    db_item1 = "db_flavor"
    db_item2 = "db_flavor2"
    db_item3 = "db_flavor3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_name_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing flavor to a different flavor
        belonging to a different Provider. This is possible.
        """
        api: FlavorController = request.getfixturevalue(self.controller)
        db_item: Flavor = request.getfixturevalue(self.db_item1)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
        api.api_patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_name_same_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing flavor to a different flavor
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: FlavorController = request.getfixturevalue(self.controller)
        db_item: Flavor = request.getfixturevalue(self.db_item3)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
        response: Response = api.api_patch(
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
    def test_patch_item_with_duplicated_uuid_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing flavor to a different flavor
        belonging to a different Provider. This is possible.
        """
        api: FlavorController = request.getfixturevalue(self.controller)
        db_item: Flavor = request.getfixturevalue(self.db_item1)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
        api.api_patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_uuid_same_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing flavor to a different flavor
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: FlavorController = request.getfixturevalue(self.controller)
        db_item: Flavor = request.getfixturevalue(self.db_item3)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
        response: Response = api.api_patch(
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
        """Execute PATCH operations to try to change the visibility of a flavor.

        It is not possible to change the visibility of a flavor using a patch operation.
        The endpoints returns a 400 error.
        """
        api: FlavorController = request.getfixturevalue(self.controller)
        db_item: Flavor = request.getfixturevalue(self.db_item1)
        new_data: FlavorUpdate = api.random_patch_item(from_item=db_item)
        new_data.is_public = not new_data.is_public
        response: Response = api.api_patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            target_status_code=status.HTTP_400_BAD_REQUEST,
            new_data=new_data,
        )
        assert (
            response.json()["detail"] == f"{api.item_name} visibility can't be changed"
        )
