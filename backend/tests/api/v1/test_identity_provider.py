import json
from typing import Dict
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderBase,
    IdentityProviderRead,
    IdentityProviderReadShort,
)
from app.identity_provider.schemas_extended import IdentityProviderReadExtended
from tests.utils.identity_provider import (
    create_random_identity_provider_patch,
    validate_read_extended_identity_provider_attrs,
    validate_read_identity_provider_attrs,
    validate_read_short_identity_provider_attrs,
)


def test_read_identity_providers(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all identity_providers."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", headers=read_header
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_idp_with_single_user_group.uid:
        resp_idp = content[0]
        resp_idp2 = content[1]
    else:
        resp_idp = content[1]
        resp_idp2 = content[0]

    validate_read_identity_provider_attrs(
        obj_out=IdentityProviderRead(**resp_idp),
        db_item=db_idp_with_single_user_group,
    )
    validate_read_identity_provider_attrs(
        obj_out=IdentityProviderRead(**resp_idp2),
        db_item=db_idp_with_multiple_user_groups,
    )


def test_read_identity_providers_with_target_params(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all identity_providers matching specific
    attributes passed as query attributes.
    """
    settings = get_settings()

    for k in IdentityProviderBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/identity_providers/",
            params={k: db_idp_with_single_user_group.__getattribute__(k)},
            headers=read_header,
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_identity_provider_attrs(
            obj_out=IdentityProviderRead(**content[0]),
            db_item=db_idp_with_single_user_group,
        )


def test_read_identity_providers_with_limit(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all identity_providers limiting the number of
    output items.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"limit": 0},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"limit": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_identity_providers(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all sorted identity_providers."""
    settings = get_settings()
    sorted_items = sorted(
        [db_idp_with_single_user_group, db_idp_with_multiple_user_groups],
        key=lambda x: x.uid,
    )

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"sort": "uid"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"sort": "-uid"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"sort": "uid_asc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"sort": "uid_desc"},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_identity_providers_with_skip(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all identity_providers, skipping the first N
    entries.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"skip": 0},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"skip": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"skip": 2},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"skip": 3},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_identity_providers_with_pagination(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all identity_providers.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"size": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_idp_with_single_user_group.uid:
        next_page_uid = db_idp_with_multiple_user_groups.uid
    else:
        next_page_uid = db_idp_with_single_user_group.uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"size": 1, "page": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"page": 1},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"size": 1, "page": 2},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_identity_providers_with_conn(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all identity_providers with their
    relationships.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_idp_with_single_user_group.uid:
        resp_idp = content[0]
        resp_idp2 = content[1]
    else:
        resp_idp = content[1]
        resp_idp2 = content[0]

    validate_read_extended_identity_provider_attrs(
        obj_out=IdentityProviderReadExtended(**resp_idp),
        db_item=db_idp_with_single_user_group,
    )
    validate_read_extended_identity_provider_attrs(
        obj_out=IdentityProviderReadExtended(**resp_idp2),
        db_item=db_idp_with_multiple_user_groups,
    )


def test_read_identity_providers_short(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read all identity_providers with their shrunk
    version.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"short": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_idp_with_single_user_group.uid:
        resp_idp = content[0]
        resp_idp2 = content[1]
    else:
        resp_idp = content[1]
        resp_idp2 = content[0]

    validate_read_short_identity_provider_attrs(
        obj_out=IdentityProviderReadShort(**resp_idp),
        db_item=db_idp_with_single_user_group,
    )
    validate_read_short_identity_provider_attrs(
        obj_out=IdentityProviderReadShort(**resp_idp2),
        db_item=db_idp_with_multiple_user_groups,
    )


def test_read_identity_provider(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a identity_provider."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_identity_provider_attrs(
        obj_out=IdentityProviderRead(**content),
        db_item=db_idp_with_single_user_group,
    )


def test_read_identity_provider_with_conn(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read a identity_provider with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
        params={"with_conn": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_identity_provider_attrs(
        obj_out=IdentityProviderReadExtended(**content),
        db_item=db_idp_with_single_user_group,
    )


def test_read_identity_provider_short(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to read the shrunk version of a identity_provider."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
        params={"short": True},
        headers=read_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_identity_provider_attrs(
        obj_out=IdentityProviderReadShort(**content),
        db_item=db_idp_with_single_user_group,
    )


def test_read_not_existing_identity_provider(
    client: TestClient,
    read_header: Dict,
) -> None:
    """Execute GET operations to try to read a not existing identity_provider."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/{item_uuid}",
        headers=read_header,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Identity Provider '{item_uuid}' not found"


def test_patch_identity_provider(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to update a identity_provider."""
    settings = get_settings()
    data = create_random_identity_provider_patch()

    response = client.patch(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_identity_provider_no_edit(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to update a identity_provider.

    Nothing changes.
    """
    settings = get_settings()
    data = create_random_identity_provider_patch(default=True)

    response = client.patch(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
        json=json.loads(data.json(exclude_unset=True)),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_patch_not_existing_identity_provider(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to update a not existing identity_provider."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_identity_provider_patch()

    response = client.patch(
        f"{settings.API_V1_STR}/identity_providers/{item_uuid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Identity Provider '{item_uuid}' not found"


def test_patch_identity_provider_with_duplicated_endpoint(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute PATCH operations to try to assign an already existing endpoint to a
    identity_provider.
    """
    settings = get_settings()
    data = create_random_identity_provider_patch()
    data.endpoint = db_idp_with_single_user_group.endpoint

    uid = db_idp_with_multiple_user_groups.uid
    response = client.patch(
        f"{settings.API_V1_STR}/identity_providers/{uid}",
        json=json.loads(data.json()),
        headers=write_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert (
        content["detail"]
        == f"Identity Provider with endpoint '{data.endpoint}' already registered"
    )


# TODO Add tests raising 422


def test_delete_identity_provider(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE to remove a public identity_provider."""
    settings = get_settings()
    response = client.delete(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
        headers=write_header,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_existing_identity_provider(
    client: TestClient,
    write_header: Dict,
) -> None:
    """Execute DELETE operations to try to delete a not existing identity_provider."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.delete(
        f"{settings.API_V1_STR}/identity_providers/{item_uuid}",
        headers=write_header,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Identity Provider '{item_uuid}' not found"
