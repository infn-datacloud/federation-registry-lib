import uuid
from fastapi import status
from fastapi.testclient import TestClient

from ...utils.user_group import (
    create_random_update_user_group_data,
    create_random_user_group,
)
from ...utils.utils import random_lower_string
from ....user_group.schemas import UserGroup
from ....config import settings

# STANDARD OPERATIONS


def test_create_user_group(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/user_groups/",
        json=data,
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert "uid" in content
    assert content["description"] == data["description"]
    assert content["name"] == data["name"]


def test_read_user_group(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    item = UserGroup.from_orm(create_random_user_group())
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/{item.uid}",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["uid"] == str(item.uid)
    assert content["description"] == item.description
    assert content["name"] == item.name


def test_read_user_groups(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    create_random_user_group()
    create_random_user_group()
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2


def test_update_user_group(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    item = UserGroup.from_orm(create_random_user_group())
    data = create_random_update_user_group_data()
    response = client.put(
        f"{settings.API_V1_STR}/user_groups/{item.uid}",
        json=data.dict(),
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["uid"] == str(item.uid)
    assert content["description"] == data.description
    assert content["name"] == data.name


def test_delete_user_group(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    item = UserGroup.from_orm(create_random_user_group())
    response = client.delete(
        f"{settings.API_V1_STR}/user_groups/{item.uid}",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


# STANDARD CUSTOMIZATIONS


def test_read_user_groups_with_limit(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    create_random_user_group()
    create_random_user_group()
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?limit=1",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1


def test_read_user_groups_with_params(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    create_random_user_group()
    item = UserGroup.from_orm(create_random_user_group())
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?description={item.description}",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == str(item.uid)
    assert content[0]["description"] == item.description
    assert content[0]["name"] == item.name


def test_read_user_groups_with_sort(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    items = []
    items.append(UserGroup.from_orm(create_random_user_group()))
    items.append(UserGroup.from_orm(create_random_user_group()))
    sorted_items = list(sorted(items, key=lambda x: x.uid))
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?sort=uid",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == str(sorted_items[0].uid)
    assert content[1]["uid"] == str(sorted_items[1].uid)

    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?sort=uid_asc",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == str(sorted_items[0].uid)
    assert content[1]["uid"] == str(sorted_items[1].uid)

    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?sort=uid_desc",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == str(sorted_items[1].uid)
    assert content[1]["uid"] == str(sorted_items[0].uid)


def test_read_user_groups_with_skip(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    items = []
    items.append(UserGroup.from_orm(create_random_user_group()))
    items.append(UserGroup.from_orm(create_random_user_group()))
    sorted_items = list(sorted(items, key=lambda x: x.uid))
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?sort=uid&skip=1",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["uid"] == str(sorted_items[1].uid)


def test_read_user_groups_with_skip_greater_than_list_len(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    items = []
    items.append(UserGroup.from_orm(create_random_user_group()))
    items.append(UserGroup.from_orm(create_random_user_group()))
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?sort=uid&skip=2",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_user_groups_with_pagination(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    items = []
    items.append(UserGroup.from_orm(create_random_user_group()))
    items.append(UserGroup.from_orm(create_random_user_group()))
    items.append(UserGroup.from_orm(create_random_user_group()))
    items.append(UserGroup.from_orm(create_random_user_group()))
    sorted_items = list(sorted(items, key=lambda x: x.uid))
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?sort=uid&size=2",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == str(sorted_items[0].uid)
    assert content[1]["uid"] == str(sorted_items[1].uid)

    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?sort=uid&size=2&page=1",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == str(sorted_items[2].uid)
    assert content[1]["uid"] == str(sorted_items[3].uid)


def test_read_user_groups_with_size_none_page_greater_than_zero(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    items = []
    items.append(UserGroup.from_orm(create_random_user_group()))
    items.append(UserGroup.from_orm(create_random_user_group()))
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?sort=uid&page=1",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2


def test_read_user_groups_with_page_value_greater_than_list_len(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    items = []
    items.append(UserGroup.from_orm(create_random_user_group()))
    items.append(UserGroup.from_orm(create_random_user_group()))
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/?sort=uid&size=2&page=1",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 0


def test_read_user_group_not_existing(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    item_uuid = uuid.uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/{item_uuid}",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"User Group {item_uuid} not found"


def test_update_user_group_not_existing(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    item_uuid = uuid.uuid4()
    data = create_random_update_user_group_data()
    response = client.put(
        f"{settings.API_V1_STR}/user_groups/{item_uuid}",
        json=data.dict(),
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"User Group {item_uuid} not found"


def test_delete_user_group_not_existing(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    item_uuid = uuid.uuid4()
    response = client.delete(
        f"{settings.API_V1_STR}/user_groups/{item_uuid}",
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"User Group {item_uuid} not found"


# SPECIFIC CUSTOM OPERATIONS


def test_create_user_group_with_existing_name(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    item = UserGroup.from_orm(create_random_user_group())
    data = {"name": item.name}
    response = client.post(
        f"{settings.API_V1_STR}/user_groups/",
        json=data,
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
    content = response.json()
    assert (
        content["detail"]
        == f"User Group with name '{data['name']}' already registered"
    )


def test_update_user_group_with_existing_name(
    client: TestClient,
    # superuser_token_headers: dict,
) -> None:
    item = UserGroup.from_orm(create_random_user_group())
    item2 = UserGroup.from_orm(create_random_user_group())
    data = {"name": item.name}
    response = client.put(
        f"{settings.API_V1_STR}/user_groups/{item2.uid}",
        json=data,
        # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
    content = response.json()
    assert (
        content["detail"]
        == f"User Group with name '{data['name']}' already registered"
    )
