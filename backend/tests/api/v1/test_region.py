import json
from typing import Dict
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.region.models import Region
from app.region.schemas import RegionBase, RegionRead, RegionReadShort
from app.region.schemas_extended import RegionReadExtended
from tests.utils.region import (
    create_random_region_patch,
    validate_read_extended_region_attrs,
    validate_read_region_attrs,
    validate_read_short_region_attrs,
)


def test_read_regions(
    db_region2: Region,
    db_region3: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all regions."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/regions/", headers=read_header)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_region2.uid:
        resp_reg = content[0]
        resp_reg2 = content[1]
    else:
        resp_reg = content[1]
        resp_reg2 = content[0]

    validate_read_region_attrs(obj_out=RegionRead(**resp_reg), db_item=db_region2)
    validate_read_region_attrs(obj_out=RegionRead(**resp_reg2), db_item=db_region3)


def test_read_regions_with_target_params(
    db_region: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all regions matching specific attributes passed as
    query attributes.
    """
    settings = get_settings()

    for k in RegionBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/regions/",
            params={k: db_region.__getattribute__(k)},
            headers=read_header,
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_region_attrs(obj_out=RegionRead(**content[0]), db_item=db_region)


def test_read_regions_with_limit(
    db_region2: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all regions limiting the number of output
    items.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"limit": 0},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"limit": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_regions(
    db_region2: Region,
    db_region3: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all sorted regions."""
    settings = get_settings()
    sorted_items = sorted([db_region2, db_region3], key=lambda x: x.uid)

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"sort": "uid"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"sort": "-uid"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"sort": "uid_asc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"sort": "uid_desc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_regions_with_skip(
    db_region3: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all regions, skipping the first N entries."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"skip": 0},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"skip": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"skip": 2},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"skip": 3},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_regions_with_pagination(
    db_region2: Region,
    db_region3: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all regions.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"size": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_region2.uid:
        next_page_uid = db_region3.uid
    else:
        next_page_uid = db_region2.uid

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"size": 1, "page": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"page": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"size": 1, "page": 2},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_regions_with_conn(
    db_region2: Region,
    db_region3: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all regions with their relationships."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_region2.uid:
        resp_reg = content[0]
        resp_reg2 = content[1]
    else:
        resp_reg = content[1]
        resp_reg2 = content[0]

    validate_read_extended_region_attrs(
        obj_out=RegionReadExtended(**resp_reg), db_item=db_region2
    )
    validate_read_extended_region_attrs(
        obj_out=RegionReadExtended(**resp_reg2), db_item=db_region3
    )


def test_read_regions_short(
    db_region2: Region,
    db_region3: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all regions with their shrunk version."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/regions/",
        params={"short": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_region2.uid:
        resp_reg = content[0]
        resp_reg2 = content[1]
    else:
        resp_reg = content[1]
        resp_reg2 = content[0]

    validate_read_short_region_attrs(
        obj_out=RegionReadShort(**resp_reg), db_item=db_region2
    )
    validate_read_short_region_attrs(
        obj_out=RegionReadShort(**resp_reg2), db_item=db_region3
    )


def test_read_region(
    db_region: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a region."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/regions/{db_region.uid}",
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_region_attrs(obj_out=RegionRead(**content), db_item=db_region)


def test_read_region_with_conn(
    db_region: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a region with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/regions/{db_region.uid}",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_region_attrs(
        obj_out=RegionReadExtended(**content), db_item=db_region
    )


def test_read_region_short(
    db_region: Region,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read the shrunk version of a region."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/regions/{db_region.uid}",
        params={"short": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_region_attrs(
        obj_out=RegionReadShort(**content), db_item=db_region
    )


def test_read_not_existing_region(
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to try to read a not existing region."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/regions/{item_uuid}", headers=read_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Region '{item_uuid}' not found"


def test_patch_region(
    db_region: Region,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to update a region."""
    settings = get_settings()
    data = create_random_region_patch()

    response = client.patch(
        f"{settings.API_V1_STR}/regions/{db_region.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_region_no_edit(
    db_region: Region, client: TestClient, write_header: Dict
) -> None:
    """Execute PATCH operations to update a region.

    Nothing changes.
    """
    settings = get_settings()
    data = create_random_region_patch(default=True)

    response = client.patch(
        f"{settings.API_V1_STR}/regions/{db_region.uid}",
        json=json.loads(data.json(exclude_unset=True)),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_patch_not_existing_region(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to update a not existing region."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_region_patch()

    response = client.patch(
        f"{settings.API_V1_STR}/regions/{item_uuid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Region '{item_uuid}' not found"


def test_patch_region_with_duplicated_name_same_provider(
    db_region2: Region,
    db_region3: Region,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to assign an already existing name to a region
    belonging to the same provider.
    """
    settings = get_settings()
    data = create_random_region_patch()
    data.name = db_region2.name

    response = client.patch(
        f"{settings.API_V1_STR}/regions/{db_region3.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == f"Region with name '{data.name}' already registered"


def test_patch_region_with_duplicated_name_diff_provider(
    db_region: Region,
    db_region3: Region,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to assign an already existing name to a region
    belonging to a different provider.
    """
    settings = get_settings()
    data = create_random_region_patch()
    data.name = db_region.name

    response = client.patch(
        f"{settings.API_V1_STR}/regions/{db_region3.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


# TODO Add tests raising 422


def test_delete_region(
    db_region3: Region,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE to remove a region from a provider with multiple regions."""
    settings = get_settings()
    response = client.delete(
        f"{settings.API_V1_STR}/regions/{db_region3.uid}",
        headers=write_header,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_failed_delete_region(
    db_region: Region,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE to remove a region from a provider with only one region.

    Fail deletion, since a provider must have at least one region.
    """
    settings = get_settings()
    response = client.delete(
        f"{settings.API_V1_STR}/regions/{db_region.uid}",
        headers=write_header,
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    content = response.json()
    assert content["detail"] == "Failed to delete item"


def test_delete_not_existing_region(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE operations to try to delete a not existing region."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.delete(
        f"{settings.API_V1_STR}/regions/{item_uuid}", headers=write_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Region '{item_uuid}' not found"
