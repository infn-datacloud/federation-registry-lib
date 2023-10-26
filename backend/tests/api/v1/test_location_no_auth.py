import json
from uuid import uuid4

from app.config import get_settings
from app.location.models import Location
from app.location.schemas import LocationBase, LocationReadPublic
from app.location.schemas_extended import LocationReadExtendedPublic
from fastapi import status
from fastapi.testclient import TestClient
from tests.utils.location import (
    create_random_location_patch,
    validate_read_extended_public_location_attrs,
    validate_read_public_location_attrs,
)


def test_read_locations(
    db_location: Location,
    db_location2: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read all locations."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/locations/",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_location.uid:
        resp_loc1 = content[0]
        resp_loc2 = content[1]
    else:
        resp_loc1 = content[1]
        resp_loc2 = content[0]

    validate_read_public_location_attrs(
        obj_out=LocationReadPublic(**resp_loc1), db_item=db_location
    )
    validate_read_public_location_attrs(
        obj_out=LocationReadPublic(**resp_loc2), db_item=db_location2
    )


def test_read_locations_with_target_params(
    db_location: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read all locations matching specific
    attributes passed as query attributes."""
    settings = get_settings()

    for k in LocationBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/locations/",
            params={k: db_location.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_public_location_attrs(
            obj_out=LocationReadPublic(**content[0]), db_item=db_location
        )


def test_read_locations_with_limit(
    db_location: Location,
    db_location2: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read all locations limiting the number of
    output items."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"limit": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"limit": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_locations(
    db_location: Location,
    db_location2: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read all sorted locations."""
    settings = get_settings()
    sorted_items = list(sorted([db_location, db_location2], key=lambda x: x.uid))

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"sort": "uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"sort": "-uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/locations/", params={"sort": "uid_asc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/locations/",
        params={"sort": "uid_desc"},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_locations_with_skip(
    db_location: Location,
    db_location2: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read all locations, skipping the first N
    entries."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"skip": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"skip": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"skip": 2})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"skip": 3})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_locations_with_pagination(
    db_location: Location,
    db_location2: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read all locations.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"size": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_location.uid:
        next_page_uid = db_location2.uid
    else:
        next_page_uid = db_location.uid

    response = client.get(
        f"{settings.API_V1_STR}/locations/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(f"{settings.API_V1_STR}/locations/", params={"page": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/locations/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_locations_with_conn(
    db_location: Location,
    db_location2: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read all locations with their
    relationships."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/locations/", params={"with_conn": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_location.uid:
        resp_loc1 = content[0]
        resp_loc2 = content[1]
    else:
        resp_loc1 = content[1]
        resp_loc2 = content[0]

    validate_read_extended_public_location_attrs(
        obj_out=LocationReadExtendedPublic(**resp_loc1), db_item=db_location
    )
    validate_read_extended_public_location_attrs(
        obj_out=LocationReadExtendedPublic(**resp_loc2),
        db_item=db_location2,
    )


def test_read_locations_short(
    db_location: Location,
    db_location2: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read all locations with their shrunk
    version."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/locations/", params={"short": True})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_location.uid:
        resp_loc1 = content[0]
        resp_loc2 = content[1]
    else:
        resp_loc1 = content[1]
        resp_loc2 = content[0]

    # TODO
    # with pytest.raises(ValidationError):
    #     q = LocationReadShort(**resp_loc1)
    # with pytest.raises(ValidationError):
    #     q = LocationReadShort(**resp_loc2)

    validate_read_public_location_attrs(
        obj_out=LocationReadPublic(**resp_loc1), db_item=db_location
    )
    validate_read_public_location_attrs(
        obj_out=LocationReadPublic(**resp_loc2), db_item=db_location2
    )


def test_read_location(
    db_location: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read a location."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/locations/{db_location.uid}",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_public_location_attrs(
        obj_out=LocationReadPublic(**content), db_item=db_location
    )


def test_read_location_with_conn(
    db_location: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read a location with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/locations/{db_location.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_public_location_attrs(
        obj_out=LocationReadExtendedPublic(**content), db_item=db_location
    )


def test_read_location_short(
    db_location: Location,
    client: TestClient,
) -> None:
    """Execute GET operations to read the shrunk version of a location."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/locations/{db_location.uid}", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()

    # TODO
    # with pytest.raises(ValidationError):
    #     q = LocationReadShort(**content)

    validate_read_public_location_attrs(
        obj_out=LocationReadPublic(**content), db_item=db_location
    )


def test_read_not_existing_location(
    client: TestClient,
) -> None:
    """Execute GET operations to try to read a not existing location."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/locations/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Location '{item_uuid}' not found"


def test_patch_location(
    db_location: Location,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a location.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_location_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/locations/{db_location.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_patch_not_existing_location(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing location.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_location_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/locations/{uuid4()}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_location(
    db_location: Location,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a location.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/locations/{db_location.uid}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_not_existing_location(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing location.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/locations/{uuid4()}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"
