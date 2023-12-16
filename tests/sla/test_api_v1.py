from typing import Any, Dict, Optional
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response

from app.sla.models import SLA
from app.sla.schemas import SLABase, SLAUpdate
from app.user_group.models import UserGroup
from tests.common.utils import random_date
from tests.fixtures.client import CLIENTS_READ_WRITE
from tests.utils.api_v1 import BaseAPI, TestBaseAPI


class SLAAPI(BaseAPI[SLA, SLABase, SLABase, SLAUpdate]):
    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: SLA, public: bool = False
    ) -> None:
        db_user_group: UserGroup = db_item.user_group.single()
        assert db_user_group
        assert db_user_group.uid == obj.pop("user_group").get("uid")

        projects = obj.pop("projects")
        assert len(db_item.projects) == len(projects)
        for db_proj, sla_dict in zip(
            sorted(db_item.projects, key=lambda x: x.uid),
            sorted(projects, key=lambda x: x.get("uid")),
        ):
            assert db_proj.uid == sla_dict.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[SLA] = None
    ) -> SLAUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.doc_uuid = uuid4().hex
        d1 = random_date()
        d2 = random_date()
        if d1 < d2:
            item.start_date = d1
            item.end_date = d2
        else:
            item.start_date = d2
            item.end_date = d1
        return item


@pytest.fixture(scope="class")
def sla_api() -> SLAAPI:
    return SLAAPI(
        base_schema=SLABase,
        base_public_schema=SLABase,
        update_schema=SLAUpdate,
        endpoint_group="slas",
        item_name="SLA",
    )


class TestSLATest(TestBaseAPI):
    """Class with the basic API calls to SLA endpoints."""

    __test__ = True
    api = "sla_api"
    db_item1 = "db_sla"
    db_item2 = "db_sla2"
    db_item3 = "db_sla3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_doc_uuid(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the document uuid of an already existing SLA to a different SLA.
        This is not possible. The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: SLA = request.getfixturevalue(self.db_item3)
        new_data: SLAUpdate = api.random_patch_item(from_item=db_item)
        response: Response = api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            target_status_code=status.HTTP_400_BAD_REQUEST,
            new_data=new_data,
        )
        assert (
            response.json()["detail"]
            == f"Document '{new_data.doc_uuid}' already used by another {api.item_name}"
        )
