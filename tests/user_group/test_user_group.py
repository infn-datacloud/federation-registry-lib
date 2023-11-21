from typing import Dict, Optional

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.user_group.models import UserGroup
from app.user_group.schemas import UserGroupBase, UserGroupReadPublic
from app.user_group.schemas_extended import UserGroupReadExtendedPublic
from tests.fixtures.client import (
    CLIENTS,
    CLIENTS_AUTHN,
    CLIENTS_NO_AUTHN,
    CLIENTS_NO_WRITE_AUTHZ,
)
from tests.user_group.common import API_PARAMS_SINGLE_ITEM, UserGroupTest
from tests.utils.user_group import (
    validate_read_extended_public_user_group_attrs,
    validate_read_public_user_group_attrs,
)

a = UserGroupTest()


@pytest.mark.parametrize("client", CLIENTS_NO_AUTHN)
@pytest.mark.parametrize("params", API_PARAMS_SINGLE_ITEM)
def test_read_user_group_no_authn(
    request: pytest.FixtureRequest,
    db_user_group: UserGroup,
    client: TestClient,
    params: Optional[Dict[str, str]],
) -> None:
    """Execute GET operations to read a specific User Group.

    Execute this operation using not-authenticated clients.
    For each, repeat the operation passing 'short', 'with_conn' and no params.
    """
    a.read(
        client=request.getfixturevalue(client),
        db_item=db_user_group,
        params=params,
        public=True,
    )


@pytest.mark.parametrize("client", CLIENTS_AUTHN)
@pytest.mark.parametrize("params", API_PARAMS_SINGLE_ITEM)
def test_read_user_group_authn(
    request: pytest.FixtureRequest,
    db_user_group: UserGroup,
    client: TestClient,
    params: Optional[Dict[str, str]],
) -> None:
    """Execute GET operations to read a specific User Group.

    Execute this operation using authenticated clients.
    For each, repeat the operation passing 'short', 'with_conn' and no params.
    """
    a.read(client=request.getfixturevalue(client), db_item=db_user_group, params=params)


@pytest.mark.parametrize("client", CLIENTS)
def test_read_not_existing_user_group(
    request: pytest.FixtureRequest, client: TestClient
) -> None:
    """Execute GET operations to try to read a not existing User Group.

    Execute this operation using both authenticated and not-authenticated clients.
    The endpoint returns a 404 error.
    """
    a.read(client=request.getfixturevalue(client))


@pytest.mark.parametrize("client", CLIENTS_NO_AUTHN)
def test_read_user_groups(
    request: pytest.FixtureRequest,
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    client: TestClient,
) -> None:
    """Execute GET operations to read all User Groups."""
    content = a.read_multi(client=request.getfixturevalue(client))
    assert len(content) == 2

    if content[0]["uid"] == db_user_group2.uid:
        resp_user = content[0]
        resp_user2 = content[1]
    else:
        resp_user = content[1]
        resp_user2 = content[0]

    validate_read_public_user_group_attrs(
        obj_out=UserGroupReadPublic(**resp_user), db_item=db_user_group2
    )
    validate_read_public_user_group_attrs(
        obj_out=UserGroupReadPublic(**resp_user2), db_item=db_user_group3
    )


def test_read_user_groups_with_target_params(
    db_user_group: UserGroup,
    client: TestClient,
) -> None:
    """Execute GET operations to read all user_groups matching specific attributes
    passed as query attributes.
    """
    settings = get_settings()

    for k in UserGroupBase.__fields__.keys():
        response = client.get(
            f"{settings.API_V1_STR}/user_groups/",
            params={k: db_user_group.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_public_user_group_attrs(
            obj_out=UserGroupReadPublic(**content[0]), db_item=db_user_group
        )


def test_read_user_groups_with_limit(
    db_user_group2: UserGroup,
    client: TestClient,
) -> None:
    """Execute GET operations to read all user_groups limiting the number of output
    items.
    """
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"limit": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"limit": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_user_groups(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    client: TestClient,
) -> None:
    """Execute GET operations to read all sorted user_groups."""
    settings = get_settings()
    sorted_items = sorted([db_user_group2, db_user_group3], key=lambda x: x.uid)

    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"sort": "uid"})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/user_groups/", params={"sort": "-uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = client.get(
        f"{settings.API_V1_STR}/user_groups/", params={"sort": "uid_asc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = client.get(
        f"{settings.API_V1_STR}/user_groups/",
        params={"sort": "uid_desc"},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_user_groups_with_skip(
    db_user_group2: UserGroup,
    client: TestClient,
) -> None:
    """Execute GET operations to read all user_groups, skipping the first N entries."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"skip": 0})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"skip": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"skip": 2})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"skip": 3})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_user_groups_with_pagination(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    client: TestClient,
) -> None:
    """Execute GET operations to read all user_groups.

    Paginate returned list.
    """
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"size": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_user_group2.uid:
        next_page_uid = db_user_group3.uid
    else:
        next_page_uid = db_user_group2.uid

    response = client.get(
        f"{settings.API_V1_STR}/user_groups/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"page": 1})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_user_groups_with_conn(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    client: TestClient,
) -> None:
    """Execute GET operations to read all user_groups with their relationships."""
    settings = get_settings()

    response = client.get(
        f"{settings.API_V1_STR}/user_groups/", params={"with_conn": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_user_group2.uid:
        resp_user = content[0]
        resp_user2 = content[1]
    else:
        resp_user = content[1]
        resp_user2 = content[0]

    validate_read_extended_public_user_group_attrs(
        obj_out=UserGroupReadExtendedPublic(**resp_user),
        db_item=db_user_group2,
    )
    validate_read_extended_public_user_group_attrs(
        obj_out=UserGroupReadExtendedPublic(**resp_user2),
        db_item=db_user_group3,
    )


def test_read_user_groups_short(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    client: TestClient,
) -> None:
    """Execute GET operations to read all user_groups with their shrunk version."""
    settings = get_settings()

    response = client.get(f"{settings.API_V1_STR}/user_groups/", params={"short": True})
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    if content[0]["uid"] == db_user_group2.uid:
        resp_user = content[0]
        resp_user2 = content[1]
    else:
        resp_user = content[1]
        resp_user2 = content[0]

    # TODO
    # with pytest.raises(ValidationError):
    #     q = UserGroupReadShort(**resp_user)
    # with pytest.raises(ValidationError):
    #     q = UserGroupReadShort(**resp_user2)

    validate_read_public_user_group_attrs(
        obj_out=UserGroupReadPublic(**resp_user), db_item=db_user_group2
    )
    validate_read_public_user_group_attrs(
        obj_out=UserGroupReadPublic(**resp_user2), db_item=db_user_group3
    )


def test_read_user_group_with_name_and_idp(
    db_user_group2: UserGroup, client: TestClient
) -> None:
    """Execute GET operations to read a specific user group.

    Specify user group name and identity provider endpoint."""
    settings = get_settings()

    db_idp = db_user_group2.identity_provider.single()
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/",
        params={
            "with_conn": True,
            "name": db_user_group2.name,
            "idp_endpoint": db_idp.endpoint,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    validate_read_extended_public_user_group_attrs(
        obj_out=UserGroupReadExtendedPublic(**content[0]),
        db_item=db_user_group2,
    )


@pytest.mark.parametrize("client", ["api_client_no_token"])
def test_patch_user_group_no_authn(
    request: pytest.FixtureRequest, db_user_group: UserGroup, client: TestClient
) -> None:
    """Execute PATCH operations to update a specific User Group.

    Client not authenticated. The endpoints raises a 403 error.
    """
    a.patch(
        client=request.getfixturevalue(client),
        db_item=db_user_group,
        target_status_code=status.HTTP_403_FORBIDDEN,
    )


@pytest.mark.parametrize("client", CLIENTS_NO_WRITE_AUTHZ)
def test_patch_user_group_no_authz(
    request: pytest.FixtureRequest, db_user_group: UserGroup, client: TestClient
) -> None:
    """Execute PATCH operations to update a specific User Group.

    Client with no write access. The endpoints raises a 401 error.
    """
    a.patch(
        client=request.getfixturevalue(client),
        db_item=db_user_group,
        target_status_code=status.HTTP_401_UNAUTHORIZED,
    )


@pytest.mark.parametrize("client", ["api_client_read_write_authz"])
def test_patch_user_group_authz(
    request: pytest.FixtureRequest, db_user_group: UserGroup, client: TestClient
) -> None:
    """Execute PATCH operations to update a specific User Group.

    Update the User Group attributes in the database.
    """
    a.patch(client=request.getfixturevalue(client), db_item=db_user_group)


@pytest.mark.parametrize("client", CLIENTS)
def test_patch_not_existing_user_group(
    request: pytest.FixtureRequest, client: TestClient
) -> None:
    """Execute PATCH operations to try to update a not existing User Group.

    Execute this operation using both authenticated and not-authenticated clients.
    The endpoint returns a 404 error.
    """
    a.patch(client=request.getfixturevalue(client))


@pytest.mark.parametrize("client", ["api_client_no_token"])
def test_delete_user_group_no_authn(
    request: pytest.FixtureRequest, db_user_group: UserGroup, client: TestClient
) -> None:
    """Execute DELETE operations to delete a specific User Group.

    Client not authenticated. The endpoints raises a 403 error.
    """
    a.delete(
        client=request.getfixturevalue(client),
        db_item=db_user_group,
        target_status_code=status.HTTP_403_FORBIDDEN,
    )


@pytest.mark.parametrize("client", CLIENTS_NO_WRITE_AUTHZ)
def test_delete_user_group_no_authz(
    request: pytest.FixtureRequest, db_user_group: UserGroup, client: TestClient
) -> None:
    """Execute DELETE operations to delete a specific User Group.

    Client with no write access. The endpoints raises a 401 error.
    """
    a.delete(
        client=request.getfixturevalue(client),
        db_item=db_user_group,
        target_status_code=status.HTTP_401_UNAUTHORIZED,
    )


@pytest.mark.parametrize("client", ["api_client_read_write_authz"])
def test_delete_user_group_authz(
    request: pytest.FixtureRequest, db_user_group: UserGroup, client: TestClient
) -> None:
    """Execute DELETE operations to delete a specific User Group.

    Delete the User Group from the database.
    """
    a.delete(client=request.getfixturevalue(client), db_item=db_user_group)


@pytest.mark.parametrize("client", CLIENTS)
def test_delete_not_existing_user_group(
    request: pytest.FixtureRequest, client: TestClient
) -> None:
    """Execute DELETE operations to try to delete a not existing User Group.

    Execute this operation using both authenticated and not-authenticated clients.
    The endpoint returns a 404 error.
    """
    a.delete(client=request.getfixturevalue(client))
