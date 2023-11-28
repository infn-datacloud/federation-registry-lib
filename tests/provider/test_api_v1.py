from typing import Any, Dict, Optional

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from app.provider.models import Provider
from app.provider.schemas import ProviderBase, ProviderUpdate
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.provider import random_status, random_type
from tests.utils.utils import random_bool, random_email, random_lower_string


class ProviderAPI(BaseAPI[Provider, ProviderBase, ProviderBase, ProviderUpdate]):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: Provider, public: bool = False
    ) -> None:
        projects = obj.pop("projects")
        assert len(db_item.projects) == len(projects)
        for db_proj, proj_dict in zip(
            sorted(db_item.projects, key=lambda x: x.uid),
            sorted(projects, key=lambda x: x.get("uid")),
        ):
            assert db_proj.uid == proj_dict.get("uid")

        identity_providers = obj.pop("identity_providers")
        assert len(db_item.identity_providers) == len(identity_providers)
        for db_idp, idp_dict in zip(
            sorted(db_item.identity_providers, key=lambda x: x.uid),
            sorted(identity_providers, key=lambda x: x.get("uid")),
        ):
            assert db_idp.uid == idp_dict.get("uid")

        regions = obj.pop("regions")
        assert len(db_item.regions) == len(regions)
        for db_reg, reg_dict in zip(
            sorted(db_item.regions, key=lambda x: x.uid),
            sorted(regions, key=lambda x: x.get("uid")),
        ):
            assert db_reg.uid == reg_dict.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[Provider] = None
    ) -> ProviderUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.name = random_lower_string()
        item.type = random_type()
        item.is_public = random_bool()
        item.support_emails = [random_email()]
        item.status = random_status()
        return item


@pytest.fixture(scope="class")
def provider_api() -> ProviderAPI:
    return ProviderAPI(
        base_schema=ProviderBase,
        base_public_schema=ProviderBase,
        update_schema=ProviderUpdate,
        endpoint_group="providers",
        item_name="Provider",
    )


class TestProviderTest(TestBaseAPI):
    """Class with the basic API calls to Provider endpoints."""

    __test__ = True
    api = "provider_api"
    db_item1 = "db_provider"
    db_item2 = "db_provider2"
    db_item3 = "db_provider3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_name_and_type(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name and type of an already existing provider to a different
        provider. This is not possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Provider = request.getfixturevalue(self.db_item1)
        new_data: ProviderUpdate = api.random_patch_item(from_item=db_item)
        response: Response = api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )
        assert (
            response.json()["detail"]
            == f"{api.item_name} with name '{new_data.name}' and "
            f"type '{new_data.type}' already registered"
        )
