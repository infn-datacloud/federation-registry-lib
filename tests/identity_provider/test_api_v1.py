from typing import Any, Dict, Optional

import pytest
from fastapi.testclient import TestClient

from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import IdentityProviderBase, IdentityProviderUpdate
from tests.common.utils import random_lower_string, random_url
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI


class IdentityProviderAPI(
    BaseAPI[
        IdentityProvider,
        IdentityProviderBase,
        IdentityProviderBase,
        IdentityProviderUpdate,
    ]
):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: IdentityProvider, public: bool = False
    ) -> None:
        providers = obj.pop("providers")
        assert len(db_item.providers) == len(providers)
        for db_prov, prov_dict in zip(
            sorted(db_item.providers, key=lambda x: x.uid),
            sorted(providers, key=lambda x: x.get("uid")),
        ):
            assert db_prov.uid == prov_dict.get("uid")

        user_groups = obj.pop("user_groups")
        assert len(db_item.user_groups) == len(user_groups)
        for db_user, user_dict in zip(
            sorted(db_item.user_groups, key=lambda x: x.uid),
            sorted(user_groups, key=lambda x: x.get("uid")),
        ):
            assert db_user.uid == user_dict.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[IdentityProvider] = None
    ) -> IdentityProviderUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.endpoint = random_url()
        item.group_claim = random_lower_string()
        return item


@pytest.fixture(scope="class")
def identity_provider_api() -> IdentityProviderAPI:
    return IdentityProviderAPI(
        base_schema=IdentityProviderBase,
        base_public_schema=IdentityProviderBase,
        update_schema=IdentityProviderUpdate,
        endpoint_group="identity_providers",
        item_name="Identity Provider",
    )


class TestIdentityProviderTest(TestBaseAPI):
    """Class with the basic API calls to IdentityProvider endpoints."""

    __test__ = True
    api = "identity_provider_api"
    db_item1 = "db_idp_with_single_user_group"
    db_item2 = "db_idp_with_multiple_user_groups"
    db_item3 = "db_idp_with_multiple_providers"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_endpoint(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the endpoint of an already existing identity provider to a different
        identity provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: IdentityProvider = request.getfixturevalue(self.db_item1)
        new_data: IdentityProviderUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )
