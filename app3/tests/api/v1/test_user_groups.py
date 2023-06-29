import uuid
from fastapi import status
from fastapi.testclient import TestClient

from ....config import settings
from ...utils.user_group import create_random_user_group
from ...utils.utils import random_lower_string


def test_create_user_group(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
    }
    response = client.post(
        f"{settings.API_V1_STR}/user_groups/",
        json=data,  # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert "uid" in content
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]


def test_read_user_group(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    item = create_random_user_group()
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/{item.uid}",  # headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["uid"] == str(item.uid)
    assert content["name"] == item.name
    assert content["description"] == item.description


def test_read_user_groups(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    item = create_random_user_group()
    item2 = create_random_user_group()
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/",  # headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2
    assert content[0]["uid"] == str(item.uid)
    assert content[0]["name"] == item.name
    assert content[0]["description"] == item.description
    assert content[1]["uid"] == str(item2.uid)
    assert content[1]["name"] == item2.name
    assert content[1]["description"] == item2.description


def test_update_user_group(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    item = create_random_user_group()
    data = {"name": random_lower_string()}
    response = client.put(
        f"{settings.API_V1_STR}/user_groups/{item.uid}",
        json=data,  # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["uid"] == str(item.uid)
    assert content["name"] == data["name"]
    assert content["description"] == item.description

    data2 = {"description": random_lower_string()}
    response = client.put(
        f"{settings.API_V1_STR}/user_groups/{item.uid}",
        json=data2,  # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["uid"] == str(item.uid)
    assert content["name"] == data["name"]
    assert content["description"] == data2["description"]


def test_delete_user_group(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    item = create_random_user_group()
    response = client.delete(
        f"{settings.API_V1_STR}/user_groups/{item.uid}",  # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_create_user_group_with_existing_name(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    item = create_random_user_group()
    data = {"name": item.name}
    response = client.post(
        f"{settings.API_V1_STR}/user_groups/",
        json=data,  # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
    content = response.json()
    assert (
        content["detail"]
        == f"User Group with name '{data['name']}' already registered"
    )


def test_update_user_group_with_existing_name(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    item = create_random_user_group()
    item2 = create_random_user_group()
    data = {"name": item.name}
    response = client.put(
        f"{settings.API_V1_STR}/user_groups/{item2.uid}",
        json=data,  # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text
    content = response.json()
    assert (
        content["detail"]
        == f"User Group with name '{data['name']}' already registered"
    )


def test_read_user_group_not_existing(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    item_uuid = uuid.uuid4()
    response = client.get(
        f"{settings.API_V1_STR}/user_groups/{item_uuid}",  # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"User Group {item_uuid} not found"


def test_update_user_group_not_existing(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    item_uuid = uuid.uuid4()
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
    }
    response = client.put(
        f"{settings.API_V1_STR}/user_groups/{item_uuid}",
        json=data,  # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"User Group {item_uuid} not found"


def test_delete_user_group_not_existing(
    client: TestClient,  # superuser_token_headers: dict,
) -> None:
    item_uuid = uuid.uuid4()
    response = client.delete(
        f"{settings.API_V1_STR}/user_groups/{item_uuid}",  # headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    content = response.json()
    assert content["detail"] == f"User Group {item_uuid} not found"
