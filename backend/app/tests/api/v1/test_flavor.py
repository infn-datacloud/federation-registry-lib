from typing import Dict
from uuid import uuid4

from app.config import get_settings
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorRead, FlavorReadShort
from app.flavor.schemas_extended import FlavorReadExtended
from app.tests.utils.flavor import (
    create_random_flavor_patch,
    validate_read_extended_flavor_attrs,
    validate_read_flavor_attrs,
    validate_read_short_flavor_attrs,
)
from fastapi import status
from fastapi.testclient import TestClient


def test_read_flavors(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all flavors."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/flavors/", headers=read_header)
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_flavor.uid:
        resp_public_flavor = content[0]
        resp_private_flavor = content[1]
    else:
        resp_public_flavor = content[1]
        resp_private_flavor = content[0]

    validate_read_flavor_attrs(
        obj_out=FlavorRead(**resp_public_flavor), db_item=db_public_flavor
    )
    validate_read_flavor_attrs(
        obj_out=FlavorRead(**resp_private_flavor), db_item=db_private_flavor
    )


def test_read_flavors_with_target_params(
    db_public_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all flavors matching specific attributes
    passed as query attributes."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/flavors/",
        params={"uid": db_public_flavor.uid},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    validate_read_flavor_attrs(
        obj_out=FlavorRead(**content[0]), db_item=db_public_flavor
    )


def test_read_flavors_with_limit(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all flavors limiting the number of output
    items."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"limit": 0}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"limit": 1}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_flavors(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all sorted flavors."""
    settings = get_settings()
    sorted_items = list(
        sorted([db_public_flavor, db_private_flavor], key=lambda x: x.uid)
    )

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"sort": "uid"}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"sort": "-uid"}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/flavors/",
        params={"sort": "uid_asc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/flavors/",
        params={"sort": "uid_desc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_flavors_with_skip(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all flavors, skipping the first N
    entries."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"skip": 0}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"skip": 1}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"skip": 2}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"skip": 3}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_flavors_with_pagination(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all flavors.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"size": 1}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_public_flavor.uid:
        next_page_uid = db_private_flavor.uid
    else:
        next_page_uid = db_public_flavor.uid

    response = client.get(
        f"{settings.API_V1_STR}/flavors/",
        params={"size": 1, "page": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"page": 1}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/flavors/",
        params={"size": 1, "page": 2},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_flavors_with_conn(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all flavors with their relationships."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/flavors/",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_flavor.uid:
        resp_public_flavor = content[0]
        resp_private_flavor = content[1]
    else:
        resp_public_flavor = content[1]
        resp_private_flavor = content[0]

    validate_read_extended_flavor_attrs(
        obj_out=FlavorReadExtended(**resp_public_flavor), db_item=db_public_flavor
    )
    validate_read_extended_flavor_attrs(
        obj_out=FlavorReadExtended(**resp_private_flavor), db_item=db_private_flavor
    )


def test_read_flavors_short(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all flavors with their shrunk version."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"short": True}, headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_public_flavor.uid:
        resp_public_flavor = content[0]
        resp_private_flavor = content[1]
    else:
        resp_public_flavor = content[1]
        resp_private_flavor = content[0]

    validate_read_short_flavor_attrs(
        obj_out=FlavorReadShort(**resp_public_flavor), db_item=db_public_flavor
    )
    validate_read_short_flavor_attrs(
        obj_out=FlavorReadShort(**resp_private_flavor), db_item=db_private_flavor
    )


def test_read_flavor(
    db_public_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a flavor."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}", headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_flavor_attrs(obj_out=FlavorRead(**content), db_item=db_public_flavor)


def test_read_flavor_with_conn(
    db_public_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a public flavor with its
    relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_flavor_attrs(
        obj_out=FlavorReadExtended(**content), db_item=db_public_flavor
    )


def test_read_private_flavor_with_conn(
    db_private_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a private flavor with its
    relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_private_flavor.uid}",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_flavor_attrs(
        obj_out=FlavorReadExtended(**content), db_item=db_private_flavor
    )


def test_read_flavor_short(
    db_public_flavor: Flavor,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read the shrunk version of a flavor."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}",
        params={"short": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_flavor_attrs(
        obj_out=FlavorReadShort(**content), db_item=db_public_flavor
    )


def test_read_not_existing_flavor(
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to try to read a not existing flavor."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{item_uuid}", headers=read_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Flavor '{item_uuid}' not found"


def test_patch_public_flavor(
    db_public_flavor: Flavor,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to update a public flavor."""
    settings = get_settings()
    data = create_random_flavor_patch()
    data.is_public = db_public_flavor.is_public

    response = client.patch(
        f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}",
        json=data.dict(),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_private_flavor(
    db_private_flavor: Flavor,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to update a private flavor."""
    settings = get_settings()
    data = create_random_flavor_patch()
    data.is_public = db_private_flavor.is_public

    response = client.patch(
        f"{settings.API_V1_STR}/flavors/{db_private_flavor.uid}",
        json=data.dict(),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_not_existing_flavor(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to update a not existing flavor."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_flavor_patch()

    response = client.patch(
        f"{settings.API_V1_STR}/flavors/{item_uuid}",
        json=data.dict(),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Flavor '{item_uuid}' not found"


def test_patch_flavor_changing_visibility(
    db_private_flavor: Flavor,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to change the visibility of a flavor."""
    settings = get_settings()
    data = create_random_flavor_patch()
    data.is_public = not db_private_flavor.is_public

    response = client.patch(
        f"{settings.API_V1_STR}/flavors/{db_private_flavor.uid}",
        json=data.dict(),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == "Flavor visibility can't be changed"


def test_patch_flavor_with_duplicated_uuid(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to assign an already existing UUID to a
    flavor."""
    settings = get_settings()
    data = create_random_flavor_patch()
    data.is_public = db_private_flavor.is_public
    data.uuid = db_public_flavor.uuid

    response = client.patch(
        f"{settings.API_V1_STR}/flavors/{db_private_flavor.uid}",
        json=data.dict(),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == f"Flavor with uuid '{data.uuid}' already registered"


def test_patch_flavor_with_duplicated_name(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to assign a name already in use to a
    flavor."""
    settings = get_settings()
    data = create_random_flavor_patch()
    data.is_public = db_private_flavor.is_public
    data.name = db_public_flavor.name

    response = client.patch(
        f"{settings.API_V1_STR}/flavors/{db_private_flavor.uid}",
        json=data.dict(),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == f"Flavor with name '{data.name}' already registered"


# TODO Add tests raising 422


def test_delete_public_flavor(
    db_public_flavor: Flavor,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE to remove a public flavor."""
    settings = get_settings()
    response = client.delete(
        f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}", headers=write_header
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_private_flavor(
    db_private_flavor: Flavor,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE to remove a private flavor."""
    settings = get_settings()
    response = client.delete(
        f"{settings.API_V1_STR}/flavors/{db_private_flavor.uid}", headers=write_header
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_existing_flavor(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE operations to try to delete a not existing flavor."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.delete(
        f"{settings.API_V1_STR}/flavors/{item_uuid}", headers=write_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Flavor '{item_uuid}' not found"
