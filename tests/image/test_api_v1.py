from typing import Any, Dict, Optional
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.image.models import Image
from app.image.schemas import ImageBase, ImageUpdate
from tests.common.client import CLIENTS_READ_WRITE
from tests.common.utils import random_bool, random_lower_string
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.image import random_os_type


class ImageAPI(BaseAPI[Image, ImageBase, ImageBase, ImageUpdate]):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: Image, public: bool = False
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
        self, *, default: bool = False, from_item: Optional[Image] = None
    ) -> ImageUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.name = random_lower_string()
        item.uuid = uuid4().hex
        item.os_type = random_os_type()
        item.os_distro = random_lower_string()
        item.os_version = random_lower_string()
        item.architecture = random_lower_string()
        item.kernel_id = random_lower_string()
        item.cuda_support = random_bool()
        item.gpu_driver = random_bool()
        item.tags = [random_lower_string()]
        return item


@pytest.fixture(scope="class")
def image_api() -> ImageAPI:
    return ImageAPI(
        base_schema=ImageBase,
        base_public_schema=ImageBase,
        update_schema=ImageUpdate,
        endpoint_group="images",
        item_name="Image",
    )


class TestImageTest(TestBaseAPI):
    """Class with the basic API calls to Image endpoints."""

    __test__ = True
    api = "image_api"
    db_item1 = "db_image"
    db_item2 = "db_image2"
    db_item3 = "db_image3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_name_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing image to a different image
        belonging to a different Provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Image = request.getfixturevalue(self.db_item1)
        new_data: ImageUpdate = api.random_patch_item(from_item=db_item)
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

        Assign the name of an already existing image to a different image
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Image = request.getfixturevalue(self.db_item3)
        new_data: ImageUpdate = api.random_patch_item(from_item=db_item)
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
    def test_patch_item_with_duplicated_uuid_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing image to a different image
        belonging to a different Provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Image = request.getfixturevalue(self.db_item1)
        new_data: ImageUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_uuid_same_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing image to a different image
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Image = request.getfixturevalue(self.db_item3)
        new_data: ImageUpdate = api.random_patch_item(from_item=db_item)
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
    def test_patch_item_changing_visibility(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to change the visibility of a image.

        It is not possible to change the visibility of a image using a patch operation.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Image = request.getfixturevalue(self.db_item1)
        new_data: ImageUpdate = api.random_patch_item(from_item=db_item)
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
