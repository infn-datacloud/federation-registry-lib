from typing import Any, Dict, Optional

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.identity_provider.models import IdentityProvider
from app.project.models import Project
from app.provider.models import Provider
from app.sla.models import SLA
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupBase, UserGroupUpdate
from tests.fixtures.client import CLIENTS, CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.utils import random_lower_string


class UserGroupAPI(BaseAPI[UserGroup, UserGroupBase, UserGroupBase, UserGroupUpdate]):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: UserGroup, public: bool = False
    ) -> None:
        db_idp = db_item.identity_provider.single()
        assert db_idp
        assert db_idp.uid == obj.pop("identity_provider").get("uid")

        slas = obj.pop("slas")
        assert len(db_item.slas) == len(slas)
        for db_sla, sla_schema in zip(
            sorted(db_item.slas, key=lambda x: x.uid),
            sorted(slas, key=lambda x: x.get("uid")),
        ):
            assert db_sla.uid == sla_schema.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[UserGroup] = None
    ) -> UserGroupUpdate:
        if default:
            return UserGroupUpdate()
        if from_item:
            d = {
                k: from_item.__getattribute__(k)
                for k in UserGroupBase.__fields__.keys()
            }
            return UserGroupUpdate(**d)
        name = random_lower_string()
        description = random_lower_string()
        return UserGroupUpdate(name=name, description=description)


@pytest.fixture(scope="class")
def user_group_api() -> UserGroupAPI:
    return UserGroupAPI(
        base_schema=UserGroupBase,
        base_public_schema=UserGroupBase,
        endpoint_group="user_groups",
        item_name="User Group",
    )


class TestUserGroupTest(TestBaseAPI):
    """Class with the basic API calls to User Group endpoints."""

    __test__ = True
    api = "user_group_api"
    db_item1 = "db_user_group"
    db_item2 = "db_user_group2"
    db_item3 = "db_user_group3"

    @pytest.mark.parametrize("client, public", CLIENTS)
    def test_read_user_group_from_name_and_idp(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute GET operations to read a specific User Group.

        Retrieve the User Group with the given name and belonging to the identity
        provider with the given endpoint."""
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: UserGroup = request.getfixturevalue(self.db_item2)
        db_idp: IdentityProvider = db_item.identity_provider.single()
        api.read_multi(
            client=request.getfixturevalue(client),
            db_items=[db_item],
            params={
                "with_conn": True,
                "name": db_item.name,
                "idp_endpoint": db_idp.endpoint,
            },
            public=public,
        )

    @pytest.mark.parametrize("client, public", CLIENTS)
    def test_read_user_group_from_provider_name(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute GET operations to read a specific User Group.

        Retrieve the User Groups with an SLA on at least one project of the provider
        with the given name."""
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: UserGroup = request.getfixturevalue(self.db_item1)
        db_sla: SLA = db_item.slas.single()
        db_project: Project = db_sla.projects.single()
        db_provider: Provider = db_project.provider.single()
        api.read_multi(
            client=request.getfixturevalue(client),
            db_items=[db_item],
            params={"with_conn": True, "provider_name": db_provider.name},
            public=public,
        )

    @pytest.mark.parametrize("client, public", CLIENTS)
    def test_read_user_group_from_provider_type(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute GET operations to read a specific User Group.

        Retrieve the User Groups with an SLA on at least one project of the provider
        with the given type."""
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: UserGroup = request.getfixturevalue(self.db_item1)
        db_sla: SLA = db_item.slas.single()
        db_project: Project = db_sla.projects.single()
        db_provider: Provider = db_project.provider.single()
        api.read_multi(
            client=request.getfixturevalue(client),
            db_items=[db_item],
            params={"with_conn": True, "provider_type": db_provider.type},
            public=public,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_user_group_with_duplicated_name_diff_idp(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing user group to a different user group
        belonging to a different Identity Provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: UserGroup = request.getfixturevalue(self.db_item1)
        new_data: UserGroupUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_user_group_with_duplicated_name_same_idp(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing user group to a different user group
        belonging to the same Identity Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: UserGroup = request.getfixturevalue(self.db_item3)
        new_data: UserGroupUpdate = api.random_patch_item(from_item=db_item)
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
