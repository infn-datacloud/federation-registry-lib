from typing import Any, Dict, Optional
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.project.models import Project
from app.project.schemas import ProjectBase, ProjectUpdate
from app.provider.models import Provider
from app.sla.models import SLA
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI
from tests.utils.utils import random_lower_string


class ProjectAPI(BaseAPI[Project, ProjectBase, ProjectBase, ProjectUpdate]):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: Project, public: bool = False
    ) -> None:
        db_provider: Provider = db_item.provider.single()
        assert db_provider
        assert db_provider.uid == obj.pop("provider").get("uid")

        db_sla: SLA = db_item.sla.single()
        if db_sla:
            assert db_sla.uid == obj.pop("sla").get("uid")
        else:
            assert not obj.pop("sla")

        flavors = obj.pop("flavors")
        out_obj_private_flavors = list(filter(lambda x: not x.is_public, flavors))
        assert len(db_item.private_flavors) == len(out_obj_private_flavors)
        for i, j in zip(
            sorted(db_item.private_flavors, key=lambda x: x.uid),
            sorted(out_obj_private_flavors, key=lambda x: x.get("uid")),
        ):
            assert i.uid == j.get("uid")
        out_obj_public_flavors = list(filter(lambda x: x.is_public, flavors))
        assert len(db_item.public_flavors()) == len(out_obj_public_flavors)
        for i, j in zip(
            sorted(db_item.public_flavors(), key=lambda x: x.uid),
            sorted(out_obj_public_flavors, key=lambda x: x.get("uid")),
        ):
            assert i.uid == j.get("uid")

        images = obj.pop("images")
        out_obj_private_images = list(filter(lambda x: not x.is_public, images))
        assert len(db_item.private_images) == len(out_obj_private_images)
        for i, j in zip(
            sorted(db_item.private_images, key=lambda x: x.uid),
            sorted(out_obj_private_images, key=lambda x: x.get("uid")),
        ):
            assert i.uid == j.get("uid")
        out_obj_public_images = list(filter(lambda x: x.is_public, images))
        assert len(db_item.public_images()) == len(out_obj_public_images)
        for i, j in zip(
            sorted(db_item.public_images(), key=lambda x: x.uid),
            sorted(out_obj_public_images, key=lambda x: x.get("uid")),
        ):
            assert i.uid == j.get("uid")

        networks = obj.pop("networks")
        out_obj_private_networks = list(filter(lambda x: not x.is_shared, networks))
        assert len(db_item.private_networks) == len(out_obj_private_networks)
        for i, j in zip(
            sorted(db_item.private_networks, key=lambda x: x.uid),
            sorted(out_obj_private_networks, key=lambda x: x.get("uid")),
        ):
            assert i.uid == j.get("uid")
        out_obj_public_networks = list(filter(lambda x: x.is_shared, networks))
        assert len(db_item.public_networks()) == len(out_obj_public_networks)
        for i, j in zip(
            sorted(db_item.public_networks(), key=lambda x: x.uid),
            sorted(out_obj_public_networks, key=lambda x: x.get("uid")),
        ):
            assert i.uid == j.get("uid")

        quotas = obj.pop("quotas")
        assert len(db_item.quotas) == len(quotas)
        for i, j in zip(
            sorted(db_item.quotas, key=lambda x: x.uid),
            sorted(quotas, key=lambda x: x.get("uid")),
        ):
            assert i.uid == j.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[Project] = None
    ) -> ProjectUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.name = random_lower_string()
        item.uuid = uuid4().hex
        return item


@pytest.fixture(scope="class")
def project_api() -> ProjectAPI:
    return ProjectAPI(
        base_schema=ProjectBase,
        base_public_schema=ProjectBase,
        update_schema=ProjectUpdate,
        endpoint_group="projects",
        item_name="Project",
    )


class TestProjectTest(TestBaseAPI):
    """Class with the basic API calls to Project endpoints."""

    __test__ = True
    api = "project_api"
    db_item1 = "db_project"
    db_item2 = "db_project2"
    db_item3 = "db_project3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_project_with_duplicated_name_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing project to a different project
        belonging to a different Provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Project = request.getfixturevalue(self.db_item1)
        new_data: ProjectUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_project_with_duplicated_name_same_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing project to a different project
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Project = request.getfixturevalue(self.db_item3)
        new_data: ProjectUpdate = api.random_patch_item(from_item=db_item)
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
    def test_patch_project_with_duplicated_uuid_diff_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing project to a different project
        belonging to a different Provider. This is possible.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Project = request.getfixturevalue(self.db_item1)
        new_data: ProjectUpdate = api.random_patch_item(from_item=db_item)
        api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            new_data=new_data,
        )

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_project_with_duplicated_uuid_same_provider(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the uuid of an already existing project to a different project
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Project = request.getfixturevalue(self.db_item3)
        new_data: ProjectUpdate = api.random_patch_item(from_item=db_item)
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
