from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from app.identity_provider.models import IdentityProvider
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupBase, UserGroupUpdate
from tests.fixtures.client import CLIENTS
from tests.utils.api import BaseAPI, TestBaseAPI
from tests.utils.utils import random_lower_string


class UserGroupAPI(BaseAPI[UserGroup, UserGroupBase, UserGroupBase]):
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

    def _random_patch_item(self, *, default: bool = False) -> UserGroupUpdate:
        if default:
            return UserGroupUpdate()
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
        """Execute GET operations to read a specific user group.

        Specify user group name and identity provider endpoint."""
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
