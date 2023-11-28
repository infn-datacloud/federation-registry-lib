from typing import Any, Dict, Optional

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.project.models import Project
from app.quota.models import BlockStorageQuota
from app.quota.schemas import BlockStorageQuotaBase, BlockStorageQuotaUpdate
from app.service.models import BlockStorageService
from tests.fixtures.client import CLIENTS, CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.utils import random_non_negative_int


class BlockStorageQuotaAPI(
    BaseAPI[
        BlockStorageQuota,
        BlockStorageQuotaBase,
        BlockStorageQuotaBase,
        BlockStorageQuotaUpdate,
    ]
):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: BlockStorageQuota, public: bool = False
    ) -> None:
        db_project: Project = db_item.project.single()
        assert db_project
        assert db_project.uid == obj.pop("project").get("uid")

        db_service: BlockStorageService = db_item.service.single()
        assert db_service
        assert db_service.uid == obj.pop("service").get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[BlockStorageQuota] = None
    ) -> BlockStorageQuotaUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.gigabytes = random_non_negative_int()
        item.per_volume_gigabytes = random_non_negative_int()
        item.volumes = random_non_negative_int()
        return item


@pytest.fixture(scope="class")
def block_storage_quota_api() -> BlockStorageQuotaAPI:
    return BlockStorageQuotaAPI(
        base_schema=BlockStorageQuotaBase,
        base_public_schema=BlockStorageQuotaBase,
        update_schema=BlockStorageQuotaUpdate,
        endpoint_group="block_storage_quotas",
        item_name="Block Storage Quota",
    )


class TestBlockStorageQuotaTest(TestBaseAPI):
    """Class with the basic API calls to BlockStorageQuota endpoints."""

    __test__ = True
    api = "block_storage_quota_api"
    db_item1 = "db_block_storage_quota"
    db_item2 = "db_block_storage_quota2"
    db_item3 = "db_block_storage_quota3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_changing_per_user(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to change the per_user flag of a block storage
        quota.

        In this case the project has only the quota which will be modified.
        The operation succeeds.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: BlockStorageQuota = request.getfixturevalue(self.db_item1)
        new_data: BlockStorageQuotaUpdate = api.random_patch_item(from_item=db_item)
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
        db_block_storage_quota_per_user: BlockStorageQuota,
    ) -> None:
        """Execute PATCH operations to try to change the per_user flag of a block
        storage quota.

        In this case the project already has a quota of the same type, pointing to the
        same service and with the same per_user flag.
        The endpoint returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: BlockStorageQuota = db_block_storage_quota_per_user
        new_data: BlockStorageQuotaUpdate = api.random_patch_item(from_item=db_item)
        new_data.per_user = not new_data.per_user
        response: Response = api.patch(
            client=request.getfixturevalue(client),
            db_item=db_item,
            new_data=new_data,
            target_status_code=status.HTTP_400_BAD_REQUEST,
        )
        db_project: Project = db_item.project.single()
        db_service: BlockStorageService = db_item.service.single()
        msg = "Duplicated Block Storage Quota, to not apply to each user, on "
        msg += f"Project '{db_project.uid}' and Service {db_service.uid}"
        assert response.json()["detail"] == msg
