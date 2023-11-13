import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderBase,
    IdentityProviderReadPublic,
)
from app.identity_provider.schemas_extended import (
    IdentityProviderReadExtendedPublic,
)
from tests.utils.identity_provider import (
    create_random_identity_provider_patch,
    validate_read_extended_public_identity_provider_attrs,
    validate_read_public_identity_provider_attrs,
)


def test_read_identity_providers(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_providers."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
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

    validate_read_public_identity_provider_attrs(
        obj_out=IdentityProviderReadPublic(**resp_idp),
        db_item=db_idp_with_single_user_group,
    )
    validate_read_public_identity_provider_attrs(
        obj_out=IdentityProviderReadPublic(**resp_idp2),
        db_item=db_idp_with_multiple_user_groups,
    )


def test_read_identity_providers_with_target_params(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_providers matching specific
    attributes passed as query attributes.
    """
    settings = get_settings()

    for k in IdentityProviderBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/identity_providers/",
            params={k: db_idp_with_single_user_group.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_public_identity_provider_attrs(
            obj_out=IdentityProviderReadPublic(**content[0]),
            db_item=db_idp_with_single_user_group,
        )


def test_read_identity_providers_with_limit(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_providers limiting the number of
    output items.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"limit": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"limit": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_identity_providers(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read all sorted identity_providers."""
    settings = get_settings()
    sorted_items = sorted(
        [db_idp_with_single_user_group, db_idp_with_multiple_user_groups],
        key=lambda x: x.uid,
    )

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"sort": "uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"sort": "-uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"sort": "uid_asc"},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"sort": "uid_desc"},
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
) -> None:
    """Execute GET operations to read all identity_providers, skipping the first N
    entries.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"skip": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"skip": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"skip": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"skip": 3}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_identity_providers_with_pagination(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_providers.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"size": 1}
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
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"size": 1, "page": 2},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_identity_providers_with_conn(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_providers with their
    relationships.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/",
        params={"with_conn": True},
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

    validate_read_extended_public_identity_provider_attrs(
        obj_out=IdentityProviderReadExtendedPublic(**resp_idp),
        db_item=db_idp_with_single_user_group,
    )
    validate_read_extended_public_identity_provider_attrs(
        obj_out=IdentityProviderReadExtendedPublic(**resp_idp2),
        db_item=db_idp_with_multiple_user_groups,
    )


def test_read_identity_providers_short(
    db_idp_with_single_user_group: IdentityProvider,
    db_idp_with_multiple_user_groups: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read all identity_providers with their shrunk
    version.
    """
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/", params={"short": True}
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

    # TODO
    # with pytest.raises(ValidationError):
    #     q = IdentityProviderReadShort(**resp_idp)
    # with pytest.raises(ValidationError):
    #     q = IdentityProviderReadShort(**resp_idp2)

    validate_read_public_identity_provider_attrs(
        obj_out=IdentityProviderReadPublic(**resp_idp),
        db_item=db_idp_with_single_user_group,
    )
    validate_read_public_identity_provider_attrs(
        obj_out=IdentityProviderReadPublic(**resp_idp2),
        db_item=db_idp_with_multiple_user_groups,
    )


def test_read_identity_provider(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read a identity_provider."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_public_identity_provider_attrs(
        obj_out=IdentityProviderReadPublic(**content),
        db_item=db_idp_with_single_user_group,
    )


def test_read_identity_provider_with_conn(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read a identity_provider with its relationships."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_public_identity_provider_attrs(
        obj_out=IdentityProviderReadExtendedPublic(**content),
        db_item=db_idp_with_single_user_group,
    )


def test_read_identity_provider_short(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute GET operations to read the shrunk version of a identity_provider."""
    settings = get_settings()
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
        params={"short": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()

    # TODO
    # with pytest.raises(ValidationError):
    #     q = IdentityProviderReadShort(**content)

    validate_read_public_identity_provider_attrs(
        obj_out=IdentityProviderReadPublic(**content),
        db_item=db_idp_with_single_user_group,
    )


def test_read_not_existing_identity_provider(
    client: TestClient,
) -> None:
    """Execute GET operations to try to read a not existing identity_provider."""
    settings = get_settings()
    item_uuid = uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/identity_providers/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"Identity Provider '{item_uuid}' not found"


def test_patch_identity_provider(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a identity_provider.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_identity_provider_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_patch_not_existing_identity_provider(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing identity_provider.

    No access rights. Permission denied
    """
    settings = get_settings()
    data = create_random_identity_provider_patch()
    response = client.patch(
        f"{settings.API_V1_STR}/identity_providers/{uuid4()}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_identity_provider(
    db_idp_with_single_user_group: IdentityProvider,
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a identity_provider.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(
        f"{settings.API_V1_STR}/identity_providers/{db_idp_with_single_user_group.uid}"
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_delete_not_existing_identity_provider(
    client: TestClient,
) -> None:
    """Execute PATCH operations to update a not existing identity_provider.

    No access rights. Permission denied
    """
    settings = get_settings()
    response = client.delete(f"{settings.API_V1_STR}/identity_providers/{uuid4()}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    content = response.json()
    assert content["detail"] == "Not authenticated"
