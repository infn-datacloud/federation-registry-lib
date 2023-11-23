from typing import Any, Dict, Optional

import pytest
from fastapi.testclient import TestClient

from app.region.models import Region
from app.service.models import ComputeService
from app.service.schemas import ComputeServiceBase, ComputeServiceUpdate
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.compute_service import random_compute_service_name
from tests.utils.utils import random_url


class ComputeServiceAPI(
    BaseAPI[
        ComputeService,
        ComputeServiceBase,
        ComputeServiceBase,
        ComputeServiceUpdate,
    ]
):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: ComputeService, public: bool = False
    ) -> None:
        db_region: Region = db_item.region.single()
        assert db_region
        assert db_region.uid == obj.pop("region").get("uid")

        flavors = obj.pop("flavors")
        assert len(db_item.flavors) == len(flavors)
        for db_flav, flav_dict in zip(
            sorted(db_item.flavors, key=lambda x: x.uid),
            sorted(flavors, key=lambda x: x.get("uid")),
        ):
            assert db_flav.uid == flav_dict.get("uid")

        images = obj.pop("images")
        assert len(db_item.images) == len(images)
        for db_img, img_dict in zip(
            sorted(db_item.images, key=lambda x: x.uid),
            sorted(images, key=lambda x: x.get("uid")),
        ):
            assert db_img.uid == img_dict.get("uid")

        quotas = obj.pop("quotas")
        assert len(db_item.quotas) == len(quotas)
        for db_quota, quota_dict in zip(
            sorted(db_item.quotas, key=lambda x: x.uid),
            sorted(quotas, key=lambda x: x.get("uid")),
        ):
            assert db_quota.uid == quota_dict.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[ComputeService] = None
    ) -> ComputeServiceUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.endpoint = random_url()
        item.name = random_compute_service_name()
        return item


@pytest.fixture(scope="class")
def compute_service_api() -> ComputeServiceAPI:
    return ComputeServiceAPI(
        base_schema=ComputeServiceBase,
        base_public_schema=ComputeServiceBase,
        update_schema=ComputeServiceUpdate,
        endpoint_group="compute_services",
        item_name="Compute Service",
    )


class TestComputeServiceTest(TestBaseAPI):
    """Class with the basic API calls to ComputeService endpoints."""

    __test__ = True
    api = "compute_service_api"
    db_item1 = "db_compute_serv"
    db_item2 = "db_compute_serv2"
    db_item3 = "db_compute_serv3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_compute_service_with_duplicated_endpoint(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the endpoint of an already existing identity provider to a different
        identity provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: ComputeService = request.getfixturevalue(self.db_item1)
        new_data: ComputeServiceUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )
