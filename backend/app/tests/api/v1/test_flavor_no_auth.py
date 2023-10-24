from uuid import uuid4

from app.config import get_settings
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorReadPublic, FlavorReadShort
from app.flavor.schemas_extended import FlavorReadExtendedPublic
from app.tests.utils.flavor import (
    create_random_flavor_patch,
    validate_read_flavor_attrs,
)
from fastapi import status
from fastapi.testclient import TestClient


def test_read_flavors(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read all flavors."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/flavors/",
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

    validate_read_flavor_attrs(
        obj_out=FlavorReadPublic(**resp_public_flavor), db_item=db_public_flavor
    )
    validate_read_flavor_attrs(
        obj_out=FlavorReadPublic(**resp_private_flavor), db_item=db_private_flavor
    )


def test_read_flavors_with_target_params(
    db_public_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read all flavors matching specific attributes
    passed as query attributes."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"uid": db_public_flavor.uid}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    validate_read_flavor_attrs(
        obj_out=FlavorReadPublic(**content[0]), db_item=db_public_flavor
    )


def test_read_flavors_with_limit(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read all flavors limiting the number of output
    items."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"limit": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"limit": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_flavors(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read all sorted flavors."""
    settings = get_settings()
    sorted_items = list(
        sorted([db_public_flavor, db_private_flavor], key=lambda x: x.uid)
    )

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"sort": "uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"sort": "-uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"sort": "uid_asc"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/flavors/",
        params={"sort": "uid_desc"},
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
) -> None:
    """Execute GET operations to read all flavors, skipping the first N
    entries."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"skip": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"skip": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"skip": 2})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"skip": 3})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_flavors_with_pagination(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read all flavors.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"size": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_public_flavor.uid:
        next_page_uid = db_private_flavor.uid
    else:
        next_page_uid = db_public_flavor.uid

    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"page": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/flavors/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_flavors_with_conn(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read all flavors with their relationships."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"with_conn": True})
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
        obj_out=FlavorReadExtendedPublic(**resp_public_flavor), db_item=db_public_flavor
    )
    validate_read_flavor_attrs(
        obj_out=FlavorReadExtendedPublic(**resp_private_flavor),
        db_item=db_private_flavor,
    )


def test_read_flavors_short(
    db_public_flavor: Flavor,
    db_private_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read all flavors with their shrunk version."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/flavors/", params={"short": True})
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
        obj_out=FlavorReadShort(**resp_public_flavor), db_item=db_public_flavor
    )
    validate_read_flavor_attrs(
        obj_out=FlavorReadShort(**resp_private_flavor), db_item=db_private_flavor
    )


def test_read_public_flavor(
    db_public_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read a public flavor."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_flavor_attrs(
        obj_out=FlavorReadPublic(**content), db_item=db_public_flavor
    )


def test_read_public_flavor_with_conn(
    db_public_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read a public flavor with its
    relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_flavor_attrs(
        obj_out=FlavorReadExtendedPublic(**content), db_item=db_public_flavor
    )


def test_read_public_flavor_short(
    db_public_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read the shrunk version of a public flavor."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_flavor_attrs(
        obj_out=FlavorReadShort(**content), db_item=db_public_flavor
    )


def test_read_private_flavor(
    db_private_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read a private flavor."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_private_flavor.uid}",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["uid"] == db_private_flavor.uid
    validate_read_flavor_attrs(
        obj_out=FlavorReadPublic(**content), db_item=db_private_flavor
    )


def test_read_private_flavor_with_conn(
    db_private_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read a private flavor with its
    relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_private_flavor.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_flavor_attrs(
        obj_out=FlavorReadExtendedPublic(**content), db_item=db_private_flavor
    )


def test_read_private_flavor_short(
    db_private_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute GET operations to read the shrunk version of a public flavor."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{db_private_flavor.uid}", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_flavor_attrs(
        obj_out=FlavorReadShort(**content), db_item=db_private_flavor
    )


def test_read_not_existing_flavor(
    client: TestClient,
) -> None:
    """Execute GET operations to try to read a not existing flavor."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/flavors/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Flavor '{item_uuid}' not found"


def test_patch_flavor(
    db_public_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a flavor.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_flavor_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}",
        json=data.json(),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_patch_not_existing_flavor(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing flavor.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_flavor_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/flavors/{uuid4()}",
        json=data.json(),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_flavor(
    db_public_flavor: Flavor,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a flavor.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/flavors/{db_public_flavor.uid}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_not_existing_flavor(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing flavor.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/flavors/{uuid4()}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"
