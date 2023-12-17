from typing import Any, Dict, Optional

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pycountry import countries

from app.location.models import Location
from app.location.schemas import LocationBase, LocationUpdate
from tests.common.client import CLIENTS_READ_WRITE
from tests.common.utils import random_lower_string
from tests.location.utils import random_country, random_latitude, random_longitude
from tests.utils.api_v1 import BaseAPI, TestBaseAPI


class LocationAPI(BaseAPI[Location, LocationBase, LocationBase, LocationUpdate]):
    def _validate_read_attrs(
        self,
        *,
        obj: Dict[str, Any],
        db_item: Location,
        public: bool = False,
        extended: bool = False,
    ) -> None:
        matches = countries.search_fuzzy(db_item.country)
        if len(matches) > 0:
            assert matches[0].alpha_3 == obj.pop("country_code")
        return super()._validate_read_attrs(
            obj=obj, db_item=db_item, public=public, extended=extended
        )

    def _validate_relationships(
        self, *, obj: Dict[str, Any], db_item: Location, public: bool = False
    ) -> None:
        regions = obj.pop("regions")
        assert len(db_item.regions) == len(regions)
        for db_reg, reg_dict in zip(
            sorted(db_item.regions, key=lambda x: x.uid),
            sorted(regions, key=lambda x: x.get("uid")),
        ):
            assert db_reg.uid == reg_dict.get("uid")

        return super()._validate_relationships(obj=obj, db_item=db_item, public=public)

    def random_patch_item(
        self, *, default: bool = False, from_item: Optional[Location] = None
    ) -> LocationUpdate:
        item = super().random_patch_item(default=default, from_item=from_item)
        item.site = random_lower_string()
        item.country = random_country()
        item.latitude = random_latitude()
        item.longitude = random_longitude()
        return item


@pytest.fixture(scope="class")
def location_api() -> LocationAPI:
    return LocationAPI(
        base_schema=LocationBase,
        base_public_schema=LocationBase,
        update_schema=LocationUpdate,
        endpoint_group="locations",
        item_name="Location",
    )


class TestLocationTest(TestBaseAPI):
    """Class with the basic API calls to Location endpoints."""

    __test__ = True
    api = "location_api"
    db_item1 = "db_location"
    db_item2 = "db_location2"
    db_item3 = "db_location3"

    @pytest.mark.parametrize("client, public", CLIENTS_READ_WRITE)
    def test_patch_item_with_duplicated_site(
        self, request: pytest.FixtureRequest, client: TestClient, public: bool
    ) -> None:
        """Execute PATCH operations to try to update a specific item.

        Assign the name of an already existing location to a different location
        belonging to the same Provider. This is not possible.
        The endpoints returns a 400 error.
        """
        api: BaseAPI = request.getfixturevalue(self.api)
        db_item: Location = request.getfixturevalue(self.db_item3)
        new_data: LocationUpdate = api.random_patch_item(from_item=db_item)
        response: Response = api.patch(
            client=request.getfixturevalue(client),
            db_item=request.getfixturevalue(self.db_item2),
            target_status_code=status.HTTP_400_BAD_REQUEST,
            new_data=new_data,
        )
        assert (
            response.json()["detail"]
            == f"{api.item_name} with site '{new_data.site}' already registered"
        )
