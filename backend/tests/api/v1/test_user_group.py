import json
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings
from app.user_group.models import UserGroup
from app.user_group.schemas import (
    UserGroupBase,
    UserGroupRead,
    UserGroupReadShort,
)
from app.user_group.schemas_extended import UserGroupReadExtended
from tests.utils.user_group import (
    create_random_user_group_patch,
    validate_read_extended_user_group_attrs,
    validate_read_short_user_group_attrs,
    validate_read_user_group_attrs,
)


def test_read_user_groups(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all user_groups."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/",
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

    validate_read_user_group_attrs(
        obj_out=UserGroupRead(**resp_user), db_item=db_user_group2
    )
    validate_read_user_group_attrs(
        obj_out=UserGroupRead(**resp_user2), db_item=db_user_group3
    )


def test_read_user_groups_with_target_params(
    db_user_group: UserGroup, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all user_groups matching specific attributes
    passed as query attributes.
    """
    settings = get_settings()

    for k in UserGroupBase.__fields__.keys():
        response = api_client_read_only.get(
            f"{settings.API_V1_STR}/user_groups/",
            params={k: db_user_group.__getattribute__(k)},
        )
        assert response.status_code == status.HTTP_200_OK
        content = response.json()
        assert len(content) == 1
        validate_read_user_group_attrs(
            obj_out=UserGroupRead(**content[0]), db_item=db_user_group
        )


def test_read_user_groups_with_limit(
    db_user_group2: UserGroup, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all user_groups limiting the number of output
    items.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"limit": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"limit": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_sorted_user_groups(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all sorted user_groups."""
    settings = get_settings()
    sorted_items = sorted([db_user_group2, db_user_group3], key=lambda x: x.uid)

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"sort": "uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"sort": "-uid"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"sort": "uid_asc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[0].uid
    assert content[1]["uid"] == sorted_items[1].uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"sort": "uid_desc"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == sorted_items[1].uid
    assert content[1]["uid"] == sorted_items[0].uid


def test_read_user_groups_with_skip(
    db_user_group2: UserGroup, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read all user_groups, skipping the first N entries."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"skip": 0}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"skip": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"skip": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"skip": 3}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_user_groups_with_pagination(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all user_groups.

    Paginate returned list.
    """
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"size": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    if content[0]["uid"] == db_user_group2.uid:
        next_page_uid = db_user_group3.uid
    else:
        next_page_uid = db_user_group2.uid

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"size": 1, "page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == next_page_uid

    # Page greater than 0 but size equals None, does nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"page": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2

    # Page index greater than maximum number of pages. Return nothing
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"size": 1, "page": 2}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_user_groups_with_conn(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all user_groups with their relationships."""
    settings = get_settings()

    response = api_client_read_only.get(
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

    validate_read_extended_user_group_attrs(
        obj_out=UserGroupReadExtended(**resp_user), db_item=db_user_group2
    )
    validate_read_extended_user_group_attrs(
        obj_out=UserGroupReadExtended(**resp_user2), db_item=db_user_group3
    )


def test_read_user_groups_short(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    api_client_read_only: TestClient,
) -> None:
    """Execute GET operations to read all user_groups with their shrunk version."""
    settings = get_settings()

    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/", params={"short": True}
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

    validate_read_short_user_group_attrs(
        obj_out=UserGroupReadShort(**resp_user), db_item=db_user_group2
    )
    validate_read_short_user_group_attrs(
        obj_out=UserGroupReadShort(**resp_user2), db_item=db_user_group3
    )


def test_read_user_group_with_name_and_idp(
    db_user_group2: UserGroup, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a specific user group.

    Specify user group name and identity provider endpoint."""
    settings = get_settings()

    db_idp = db_user_group2.identity_provider.single()
    response = api_client_read_only.get(
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
    validate_read_extended_user_group_attrs(
        obj_out=UserGroupReadExtended(**content[0]),
        db_item=db_user_group2,
    )


def test_read_user_group(
    db_user_group: UserGroup, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a user_group."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/{db_user_group.uid}"
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_user_group_attrs(
        obj_out=UserGroupRead(**content), db_item=db_user_group
    )


def test_read_user_group_with_conn(
    db_user_group: UserGroup, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read a user_group with its relationships."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/{db_user_group.uid}",
        params={"with_conn": True},
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_extended_user_group_attrs(
        obj_out=UserGroupReadExtended(**content), db_item=db_user_group
    )


def test_read_user_group_short(
    db_user_group: UserGroup, api_client_read_only: TestClient
) -> None:
    """Execute GET operations to read the shrunk version of a user_group."""
    settings = get_settings()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/{db_user_group.uid}", params={"short": True}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    validate_read_short_user_group_attrs(
        obj_out=UserGroupReadShort(**content), db_item=db_user_group
    )


def test_read_not_existing_user_group(api_client_read_only: TestClient) -> None:
    """Execute GET operations to try to read a not existing user_group."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_only.get(
        f"{settings.API_V1_STR}/user_groups/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"User Group '{item_uuid}' not found"


def test_patch_user_group(
    db_user_group: UserGroup, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a user_group."""
    settings = get_settings()
    data = create_random_user_group_patch()

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/user_groups/{db_user_group.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


def test_patch_user_group_no_edit(
    db_user_group: UserGroup, api_client_read_write: TestClient
) -> None:
    """Execute PATCH operations to update a user_group.

    Nothing changes.
    """
    settings = get_settings()
    data = create_random_user_group_patch(default=True)

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/user_groups/{db_user_group.uid}",
        json=json.loads(data.json(exclude_unset=True)),
    )
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_patch_not_existing_user_group(api_client_read_write: TestClient) -> None:
    """Execute PATCH operations to try to update a not existing user_group."""
    settings = get_settings()
    item_uuid = uuid4()
    data = create_random_user_group_patch()

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/user_groups/{item_uuid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"User Group '{item_uuid}' not found"


def test_patch_user_group_with_duplicated_name_same_idp(
    db_user_group2: UserGroup,
    db_user_group3: UserGroup,
    api_client_read_write: TestClient,
) -> None:
    """Execute PATCH operations to try to assign an already existing name to a
    user_group.
    """
    settings = get_settings()
    data = create_random_user_group_patch()
    data.name = db_user_group2.name

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/user_groups/{db_user_group3.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    content = response.json()
    assert content["detail"] == f"User Group with name '{data.name}' already registered"


def test_patch_user_group_with_duplicated_name_diff_idp(
    db_user_group: UserGroup,
    db_user_group3: UserGroup,
    api_client_read_write: TestClient,
) -> None:
    """Execute PATCH operations to try to assign an already existing name to a
    user_group.
    """
    settings = get_settings()
    data = create_random_user_group_patch()
    data.name = db_user_group.name

    response = api_client_read_write.patch(
        f"{settings.API_V1_STR}/user_groups/{db_user_group3.uid}",
        json=json.loads(data.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    for k, v in data.dict().items():
        assert content[k] == v


# TODO Add tests raising 422


def test_delete_user_group(
    db_user_group: UserGroup, api_client_read_write: TestClient
) -> None:
    """Execute DELETE to remove a public user_group."""
    settings = get_settings()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/user_groups/{db_user_group.uid}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_existing_user_group(api_client_read_write: TestClient) -> None:
    """Execute DELETE operations to try to delete a not existing user_group."""
    settings = get_settings()
    item_uuid = uuid4()
    response = api_client_read_write.delete(
        f"{settings.API_V1_STR}/user_groups/{item_uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"User Group '{item_uuid}' not found"
